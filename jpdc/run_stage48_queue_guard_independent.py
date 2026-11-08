#!/usr/bin/env python3
"""Stage48 preregistered fixed 8-SEED independent science, unchanged Stage47 policy."""
import argparse,json
from pathlib import Path
from independent_physical_calibration_stage3 import calibrate
from independent_physical_queue_guard_stage47 import simulate
from independent_network_probe_stage6 import simulate as source_stage6
from independent_physical_regime_gated_stage42 import simulate as stage42
from independent_physical_node_local_regime_stage44 import simulate as stage44

SEEDS=tuple(range(1001,1009))
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
POLICIES=("PRED_GREEDY","CASPER_FULL","NEW_REGIME_GATED_MISSION_COMBINED",
          "NEW_NODE_REGIME_MISSION_COMBINED",
          "NEW_QUEUE_GUARDED_NODE_E2E","NEW_QUEUE_GUARDED_NODE_COMBINED")
N=12000

def run(seed):
    if seed not in SEEDS:raise ValueError("seed outside prospectively frozen DEV set")
    cal=calibrate(seed,80000,include_reference=True)
    assert cal["postburnin_service_ratio_count"]==70000
    rows=[]
    for sc in SCENARIOS:
        for policy in POLICIES:
            result=simulate(seed,sc,policy,cal,N)
            assert result["status"]=="PASS" and result["deployment_tasks"]==N
            assert result["cpu_finish_events"]==result["e2e_feedback_events"]==result["network_feedback_events"]==N
            if policy in ("PRED_GREEDY","CASPER_FULL"):
                original=dict(result);original.pop("shadow_network_epoch")
                assert original==source_stage6(seed,sc,policy,cal,N),("original source parity",seed,sc,policy)
            if policy=="NEW_REGIME_GATED_MISSION_COMBINED":
                assert result==stage42(seed,sc,policy,cal,N),("frozen Stage42 drift",seed,sc)
            if policy=="NEW_NODE_REGIME_MISSION_COMBINED":
                assert result==stage44(seed,sc,policy,cal,N),("frozen Stage44 drift",seed,sc)
            diag=result.get("stage47_queue_gate")
            if diag is not None:
                assert diag["calls"]==diag["mission_network_mode_issues"]
                assert diag["switched"]<=diag["calls"]
                assert sum(diag["denial_reasons"].values())==diag["calls"]
                assert diag["causal_queue_backlog_is_not_a_safety_bound"]
                assert result["stage44_node_regime"]["cpu_finish_observations"]==N
                assert result["stage44_node_regime"]["network_e2e_deliveries"]==N
                miss=diag["post_mission_deadline_misses"]
            elif policy in ("NEW_REGIME_GATED_MISSION_COMBINED","NEW_NODE_REGIME_MISSION_COMBINED"):
                miss=(result.get("stage44_node_regime") or result["stage42_regime"])["post_mission_deadline_misses"]
            else:
                miss=round(result["post_deadline_miss_rate"]*result["post_mission_tasks"])
            assert 0<=miss<=result["post_mission_tasks"]
            assert abs(miss/result["post_mission_tasks"]-result["post_deadline_miss_rate"])<1e-10
            row=dict(seed=seed,scenario=sc,policy=policy,post_mission_n=result["post_mission_tasks"],
                post_mission_deadline_misses=miss,
                all_mission_deadline_misses=result["mission_deadline_misses"],
                mean_latency_ms=result["mean_latency_ms"],mean_wait_ms=result["mean_wait_ms"],
                guard=diag,original_prior_source_exact_parity=(policy in POLICIES[:4]))
            rows.append(row)
            print("JPDC_STAGE48_INDEPENDENT_SOURCE_RESULT",json.dumps(row,sort_keys=True),flush=True)
    assert len(rows)==12
    for sc in SCENARIOS:
        assert len({x["post_mission_n"] for x in rows if x["scenario"]==sc})==1
    return dict(status="PASS",scientific_seed=seed,independent_scientific_unit=True,
        dependent_task_policy_observations=N*len(rows),
        original_java_e42_not_modified=True,no_statistical_claim=True,
        rows=rows)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--seed",type=int,required=True)
    p.add_argument("--out",required=True)
    args=p.parse_args()
    val=run(args.seed)
    f=Path(args.out);f.parent.mkdir(parents=True,exist_ok=True)
    f.write_text(json.dumps(val,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print("JPDC_STAGE48_FROZEN_INDEPENDENT_SOURCE_SEED_COMPLETE_PASS",args.seed,flush=True)
