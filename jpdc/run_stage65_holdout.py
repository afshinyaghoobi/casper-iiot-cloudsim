#!/usr/bin/env python3
"""Stage65 frozen first actual route experiment: FULL fallback, new HOLDOUT n=2."""
import argparse,json
from pathlib import Path
from independent_physical_calibration_stage3 import calibrate
from independent_physical_partial_live_stage64 import simulate,PARTIAL_POLICY
from independent_network_probe_stage6 import simulate as original_stage6

SEEDS=(1811,1812,1813,1814,1815,1816,1817,1818)
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
POLICIES=("PRED_GREEDY","CASPER_FULL",PARTIAL_POLICY)
COUNT=12000

def run(seed):
    if seed not in SEEDS:raise ValueError("seed outside preregistered new HOLDOUT source")
    cal=calibrate(seed,80000,include_reference=True)
    assert cal["status"]=="PASS" and cal["postburnin_service_ratio_count"]==70000
    rows=[]
    for sc in SCENARIOS:
        for policy in POLICIES:
            result=simulate(seed,sc,policy,cal,COUNT)
            assert result["status"]=="PASS" and result["deployment_tasks"]==COUNT
            assert result["cpu_finish_events"]==result["e2e_feedback_events"]==COUNT
            assert result["network_feedback_events"]==COUNT
            assert result["stage62_shadow_feasibility"]["shadow_only_no_routing_effect"]
            assert result["stage62_shadow_feasibility"]["CPU_completion_deliveries"]==COUNT
            assert result["stage62_shadow_feasibility"]["E2E_delivered_feedback"]==COUNT
            if policy in POLICIES[:2]:
                control=dict(result)
                control.pop("shadow_network_epoch")
                control.pop("stage62_shadow_feasibility")
                assert control==original_stage6(seed,sc,policy,cal,COUNT),(
                    "original full JSON source parity",seed,sc,policy)
            diag=result.get("stage64_live_partial")
            if policy==PARTIAL_POLICY:
                assert diag is not None and diag["policy"]==policy
                assert diag["source_causal_feedback_only"] and diag["full_original_fallback"]
                assert not diag["historical_sample_max_calibrated"]
                assert diag["mission_attempts"]==result["mission_tasks"]
                assert diag["mission_ready"]+diag["mission_fallback"]==result["mission_tasks"]
                assert 0<=diag["actual_mission_switches_vs_instantaneous_full"]<=diag["mission_ready"]
                assert diag["postshock_actual_switches_vs_instantaneous_full"]<=diag["actual_mission_switches_vs_instantaneous_full"]
                miss=diag["postshock_mission_misses"]
            else:
                assert diag is None
                miss=round(result["post_deadline_miss_rate"]*result["post_mission_tasks"])
            n=result["post_mission_tasks"]
            assert 0<=miss<=n
            assert abs(miss/n-result["post_deadline_miss_rate"])<=1e-10
            row=dict(seed=seed,scenario=sc,policy=policy,
                post_mission_n=n,post_mission_deadline_misses=miss,
                all_mission_deadline_misses=result["mission_deadline_misses"],
                mean_latency_ms=result["mean_latency_ms"],
                mean_wait_ms=result["mean_wait_ms"],candidate=diag)
            rows.append(row)
            print("JPDC_STAGE65_DEV_SOURCE_ROW",json.dumps(row,sort_keys=True),flush=True)
    assert len(rows)==6
    for sc in SCENARIOS:
        assert len({r["post_mission_n"] for r in rows if r["scenario"]==sc})==1
    return dict(status="PASS",source_seed=seed,source_task_observations=COUNT*len(rows),
        source_seed_statistical_n=1,never_used_source_holdout=True,
        model="strict-FCFS Python synthetic physical backend",
        not_empirically_calibrated=True,original_java_spaceshared_queue_parity_failed=True,
        rows=rows)
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--seed",type=int,required=True)
    p.add_argument("--out",required=True)
    a=p.parse_args()
    obj=run(a.seed)
    dest=Path(a.out);dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(obj,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print("JPDC_STAGE65_DEV_SOURCE_COMPLETE_PASS",a.seed,flush=True)
