#!/usr/bin/env python3
"""Stage61 prespecified DEV-only shadow feasibility, no routing modification."""
import argparse
import json
from pathlib import Path
from independent_physical_calibration_stage3 import calibrate
from independent_physical_shadow_stage61 import simulate
from independent_network_probe_stage6 import simulate as frozen_stage6

SEEDS=(1411,1412)
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
POLICIES=("PRED_GREEDY","CASPER_FULL")
TASK_COUNT=12000

def run(seed):
    if seed not in SEEDS:
        raise ValueError("Stage61 source seed not preregistered")
    cal=calibrate(seed,80000,include_reference=True)
    assert cal["status"]=="PASS" and cal["postburnin_service_ratio_count"]==70000
    rows=[]
    for sc in SCENARIOS:
        for policy in POLICIES:
            actual=simulate(seed,sc,policy,cal,TASK_COUNT)
            assert actual["status"]=="PASS" and actual["deployment_tasks"]==TASK_COUNT
            extra=actual.pop("stage61_shadow_feasibility")
            observed=dict(actual)
            observed.pop("shadow_network_epoch")
            assert observed==frozen_stage6(seed,sc,policy,cal,TASK_COUNT),(
                "routing and physics original source parity",seed,sc,policy)
            assert extra["mission_arrivals"]==actual["mission_tasks"]
            assert extra["post_mission_arrivals"]==actual["post_mission_tasks"]
            assert extra["CPU_completion_deliveries"]==TASK_COUNT
            assert extra["E2E_delivered_feedback"]==TASK_COUNT
            assert extra["coverage_empirically_calibrated"] is False
            rows.append(dict(seed=seed,scenario=sc,policy=policy,shadow=extra,
                original_policy_mission_misses=actual["mission_deadline_misses"],
                original_policy_post_mission_miss_rate=actual["post_deadline_miss_rate"]))
            print("JPDC_STAGE61_SOURCE_SHADOW_FEASIBILITY",
                  json.dumps(rows[-1],sort_keys=True),flush=True)
    assert len(rows)==4
    return dict(status="PASS",source_seed=seed,model="strict-FCFS Python original-source shadow mode",
        no_route_changes=True,original_source_parity=True,
        scientific_source_seed_n_for_this_result=1,source_task_observations=TASK_COUNT*4,
        coverage_calibrated=False,original_Java_SpaceShared_parity_still_failed=True,
        rows=rows)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--seed",type=int,required=True)
    p.add_argument("--out",required=True)
    a=p.parse_args()
    d=run(a.seed)
    dest=Path(a.out)
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print("JPDC_STAGE61_SOURCE_SHADOW_AND_STAGE6_PARITY_PASS",a.seed)
