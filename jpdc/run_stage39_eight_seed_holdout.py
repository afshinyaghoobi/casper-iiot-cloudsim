#!/usr/bin/env python3
"""Stage39 fixed 8-seed independent original-source scheduling policy evaluation."""
import argparse,json
from pathlib import Path
from independent_physical_calibration_stage3 import calibrate
from independent_physical_mission_only_feedback_stage38 import simulate
from independent_network_probe_stage6 import simulate as original_stage6

SEEDS=tuple(range(601,609))
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
POLICIES=("PRED_GREEDY","CASPER_FULL",
 "NEW_CPU_FEEDBACK_ONLY","NEW_E2E_FEEDBACK_ONLY","NEW_CPU_E2E_FEEDBACK",
 "NEW_MISSION_ONLY_CPU_FEEDBACK","NEW_MISSION_ONLY_CPU_E2E_FEEDBACK")
N=12000

def run(seed):
    if seed not in SEEDS:raise ValueError("source seed outside preregistered cohort")
    calibration=calibrate(seed,80000,include_reference=True)
    assert calibration["postburnin_service_ratio_count"]==70000
    rows=[]
    for scenario in SCENARIOS:
        for policy in POLICIES:
            v=simulate(seed,scenario,policy,calibration,N)
            assert v["status"]=="PASS" and v["deployment_tasks"]==N
            assert v["cpu_finish_events"]==v["e2e_feedback_events"]==v["network_feedback_events"]==N
            assert v["not_cloudsim_queue_equivalent"] is True
            if policy in ("PRED_GREEDY","CASPER_FULL"):
                original=dict(v);original.pop("shadow_network_epoch")
                assert original==original_stage6(seed,scenario,policy,calibration,N),(
                    seed,scenario,policy,"frozen original Stage6 policy JSON drift")
                post_misses=round(v["post_deadline_miss_rate"]*v["post_mission_tasks"])
            else:
                a=v["stage37_feedback"]
                assert a["decisions"]==a["causal_cpu_finishes"]==a["delayed_network_observations"]==N
                assert a["budget_violations"]==0 and a["risk_certificate"] is False
                if policy.startswith("NEW_MISSION_ONLY"):
                    assert a["background_changes_from_greedy"]==0
                    assert a["changed_from_greedy"]==a["mission_changed_from_greedy"]
                    assert a["mission_only_feedback"] is True
                post_misses=a["post_mission_deadline_misses"]
            assert 0<=post_misses<=v["post_mission_tasks"]
            assert abs(post_misses/v["post_mission_tasks"]-v["post_deadline_miss_rate"])<1e-10
            a=v.get("stage37_feedback")
            row=dict(seed=seed,scenario=scenario,policy=policy,
                post_mission_n=v["post_mission_tasks"],
                post_mission_deadline_misses=post_misses,
                full_mission_deadline_misses=v["mission_deadline_misses"],
                mean_latency_ms=v["mean_latency_ms"],
                mean_wait_ms=v["mean_wait_ms"],
                routing_changed_from_greedy=a["changed_from_greedy"] if a else None,
                mission_routing_changed_from_greedy=a["mission_changed_from_greedy"] if a else None,
                background_changed_from_greedy=a["background_changes_from_greedy"] if a else None,
                exact_frozen_stage6_parity=(policy in ("PRED_GREEDY","CASPER_FULL")),
                no_deadline_certificate=True)
            rows.append(row)
            print("JPDC_STAGE39_SOURCE_SEED_RESULT",json.dumps(row,sort_keys=True),flush=True)
    assert len(rows)==14
    for sc in SCENARIOS:
        subgroup=[r for r in rows if r["scenario"]==sc]
        assert len({r["post_mission_n"] for r in subgroup})==1
    return dict(status="PASS",scientific_seed=seed,scientific_replicates=1,
        dependent_task_policy_observations=14*N,original_e42_unchanged=True,
        original_stage6_exact_parity_all_four=True,
        uncertainty_guaranteed=False,rows=rows)

if __name__=="__main__":
    a=argparse.ArgumentParser();a.add_argument("--seed",type=int,required=True)
    a.add_argument("--out",required=True);args=a.parse_args()
    obj=run(args.seed)
    out=Path(args.out);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(obj,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print("JPDC_STAGE39_ONE_PREREG_SOURCE_SEED_COMPLETE_PASS",args.seed,flush=True)
