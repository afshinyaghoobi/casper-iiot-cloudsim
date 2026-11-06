#!/usr/bin/env python3
"""Stage31 frozen detector multi-seed source validation; no new policy decisions."""
import argparse,json
from pathlib import Path
from independent_physical_calibration_stage3 import calibrate
from independent_physical_cpu_nonnetwork_trace_stage27 import simulate
from independent_network_probe_stage6 import simulate as frozen_stage6
from replay_stage30_archived_cpu_alarm import run_one

SEEDS=(505,506,507,508)
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
POLICIES=("PRED_GREEDY","CASPER_FULL")
N=12000

def evaluate(seed):
    if seed not in SEEDS:raise ValueError("scientific seed not preregistered")
    cal=calibrate(seed,80000,include_reference=True)
    assert cal["postburnin_service_ratio_count"]==70000
    data=[]
    for scenario in SCENARIOS:
        for policy in POLICIES:
            trace=[]
            source=simulate(seed,scenario,policy,cal,N,queue_trace_hook=trace.append)
            original=dict(source);original.pop("shadow_network_epoch")
            assert original==frozen_stage6(seed,scenario,policy,cal,N),(seed,scenario,policy,"Stage6 original parity failed")
            assert len(trace)==N and sorted(x["task_index"] for x in trace)==list(range(N))
            detail=run_one(trace)
            alarm=detail["alarm"]
            post=detail["groups"]["phase/post"]
            mission=detail["groups"]["phase_class/post/MISSION"]
            high=detail["groups"]["phase_class/post/HIGH"]
            assert post["n"]==2000 and high["n"]+mission["n"]<=post["n"]
            assert alarm["issued"]+alarm["abstention_sparse"]+alarm["abstention_revoked"]==N
            s2=(scenario==SCENARIOS[0])
            checks={
                "S2_alarm_after_shock_no_pre_alarm":bool(
                    alarm["alarm_count"]==1 and
                    not alarm["pre_shock_false_alarm"] and
                    alarm["first_alarm_delivery_lag_vs_postshock_arrival_ms"]>=0) if s2 else None,
                "S2_at_most_50pct_post_MISSION_revocation":(
                    mission["revoked"]/mission["n"]<=.5) if s2 else None,
                "S3_no_CPU_false_alarm":alarm["alarm_count"]==0 if not s2 else None,
                "S3_at_least_90pct_post_MISSION_issued":(
                    mission["issued"]/mission["n"]>=.90) if not s2 else None
            }
            row=dict(seed=seed,scenario=scenario,policy=policy,
                     original_stage6_exact_policy_parity=True,
                     alarm=alarm,post=post,post_mission=mission,post_high=high,
                     frozen_operational_gate_results=checks)
            print("JPDC_STAGE31_SOURCE_ALARM_RESULT",json.dumps(row,sort_keys=True),flush=True)
            data.append(row)
    assert len(data)==4
    return dict(status="PASS",seed=seed,source_scientific_units=1,
                task_policy_evaluations=48000,original_stage6_parity_all_four=True,
                detector_code_frozen_from_stage30=True,
                detector_is_not_a_scheduling_intervention=True,
                cpu_error_guarantee=False,rows=data)
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--seed",required=True,type=int);p.add_argument("--out",required=True)
    a=p.parse_args()
    result=evaluate(a.seed)
    dest=Path(a.out);dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(result,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print("JPDC_STAGE31_FROZEN_INDEPENDENT_CPU_ALARM_SEED_PASS",a.seed,flush=True)
