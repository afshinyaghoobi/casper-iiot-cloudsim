#!/usr/bin/env python3
"""Stage52 preregistered untouched 8-seed source holdout: frozen Stage51 comparators."""
import argparse, json
from pathlib import Path
from independent_physical_calibration_stage3 import calibrate
from independent_physical_queue_baseline_stage51 import simulate
from independent_network_probe_stage6 import simulate as frozen_stage6

HOLDOUT_SEEDS=tuple(range(1101,1109))
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
POLICIES=("PRED_GREEDY","CASPER_FULL","QUEUE_PRESSURE_05","QUEUE_PRESSURE_E2E_05")
TASK_COUNT=12000

def run(seed):
    if seed not in HOLDOUT_SEEDS:
        raise ValueError("not a preregistered Stage52 independent holdout seed")
    cal=calibrate(seed,80000,include_reference=True)
    assert cal["status"]=="PASS" and cal["postburnin_service_ratio_count"]==70000
    rows=[]
    for sc in SCENARIOS:
        for policy in POLICIES:
            result=simulate(seed,sc,policy,cal,TASK_COUNT)
            assert result["status"]=="PASS" and result["deployment_tasks"]==TASK_COUNT
            assert result["cpu_finish_events"]==TASK_COUNT
            assert result["e2e_feedback_events"]==result["network_feedback_events"]==TASK_COUNT
            if policy in POLICIES[:2]:
                old=dict(result)
                old.pop("shadow_network_epoch")
                assert old==frozen_stage6(seed,sc,policy,cal,TASK_COUNT),("Stage6 parity",seed,sc,policy)
            diag=result.get("stage51_comparator")
            if policy in POLICIES[2:]:
                assert diag is not None and diag["label"]==policy
                assert diag["decisions"]==TASK_COUNT
                assert diag["selected_queue_pressure_sum_ms"]>=0
                assert diag["selected_delivered_e2e_penalty_sum_ms"]>=0
                if policy=="QUEUE_PRESSURE_05":
                    assert diag["selected_delivered_e2e_penalty_sum_ms"]==0
                miss=diag["post_mission_deadline_misses"]
            else:
                assert diag is None
                miss=round(result["post_deadline_miss_rate"]*result["post_mission_tasks"])
            assert 0<=miss<=result["post_mission_tasks"]
            assert abs(miss/result["post_mission_tasks"]-result["post_deadline_miss_rate"])<1e-10
            row=dict(seed=seed,scenario=sc,policy=policy,
                     post_mission_n=result["post_mission_tasks"],
                     post_mission_deadline_misses=miss,
                     all_mission_deadline_misses=result["mission_deadline_misses"],
                     mean_latency_ms=result["mean_latency_ms"],
                     mean_wait_ms=result["mean_wait_ms"],
                     baseline=diag)
            rows.append(row)
            print("JPDC_STAGE52_HOLDOUT_SOURCE_ROW",json.dumps(row,sort_keys=True),flush=True)
    assert len(rows)==8
    for sc in SCENARIOS:
        same={r["post_mission_n"] for r in rows if r["scenario"]==sc}
        assert len(same)==1,(seed,sc,same)
    return dict(status="PASS",seed_index=seed,scientific_unit="original_source_seed",
                source_task_observations=TASK_COUNT*len(rows),
                note="Stage52 independent source holdout seed; aggregate n8 required",
                methods_not_authors_original_DFAQ_LB=True,rows=rows)

if __name__=="__main__":
    a=argparse.ArgumentParser()
    a.add_argument("--seed",type=int,required=True)
    a.add_argument("--out",required=True)
    args=a.parse_args()
    data=run(args.seed)
    dest=Path(args.out)
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(data,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print("JPDC_STAGE52_HOLDOUT_SOURCE_COMPLETE_PASS",args.seed,flush=True)
