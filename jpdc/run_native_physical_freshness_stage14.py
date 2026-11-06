#!/usr/bin/env python3
"""Preregistered Stage14 DEV-only physical scheduling matrix, single seed84."""
import argparse,json
from pathlib import Path
from independent_physical_calibration_stage3 import calibrate
from independent_physical_freshness_stage14 import simulate as fresh_sim
from independent_network_probe_stage6 import simulate as frozen_stage6

SEED=84
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
POLICIES=("PRED_GREEDY","CASPER_FULL","NEW_NETWORK_RESIDUAL_PROBE","NEW_FRESHNESS_ACTIVE")
TASKS=12000

def run():
    cal=calibrate(SEED,80000,include_reference=True)
    assert cal["postburnin_service_ratio_count"]==70000
    rows=[]
    for scenario in SCENARIOS:
        for policy in POLICIES:
            r=fresh_sim(SEED,scenario,policy,cal,TASKS)
            active=r.get("stage14_active")
            if policy!="NEW_FRESHNESS_ACTIVE":
                original=frozen_stage6(SEED,scenario,policy,cal,TASKS)
                legacy=dict(r)
                legacy.pop("shadow_network_epoch")
                assert legacy==original,(scenario,policy,"frozen baseline regression changed")
                print("JPDC_STAGE14_FROZEN_STAGE6_POLICY_EXACT_PARITY_PASS",scenario,policy)
            else:
                assert active and active["causal_e2e_delivered"]==TASKS
                assert active["probe_attempts"]<=active["normal_arrivals"]//100
                assert active["probe_opportunities"]==active["normal_arrivals"]//100
                assert active["probe_attempts"]+active["probe_skipped"]==active["probe_opportunities"]
                assert r["cpu_finish_events"]==r["e2e_feedback_events"]==TASKS
                assert active["mission_unverified_decisions"]<=r["mission_tasks"]
                print("JPDC_STAGE14_CAUSAL_ACTIVE_POLICY_INTEGRITY_PASS",scenario)
            assert r["deployment_tasks"]==TASKS
            assert r["network_feedback_events"]==TASKS
            assert r["shadow_network_epoch"]["feedback_events"]==TASKS
            assert r["cpu_finish_events"]==r["e2e_feedback_events"]==TASKS
            print("STAGE14_RESULT",scenario,policy,
                  "mission_misses",r["mission_deadline_misses"],
                  "post_miss_rate",r["post_deadline_miss_rate"],
                  "latency_mean_ms",r["mean_latency_ms"],
                  "affected_dispatches",r["postshock_affected_dispatches"],
                  "new_probe_attempts",active["probe_attempts"] if active else None,
                  "unverified_mission",active["mission_unverified_decisions"] if active else None)
            rows.append(r)
    assert len(rows)==8
    return dict(status="PASS",scope="single seed84 DEVELOPMENT, no inferential comparison",
                seed_index=SEED,task_policy_observations=TASKS*len(rows),
                scenario_names=list(SCENARIOS),policies=list(POLICIES),
                calibration={k:v for k,v in cal.items() if k!="reference_scores"},rows=rows)

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",required=True)
    args=parser.parse_args()
    x=run()
    p=Path(args.out)
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(x,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print("JPDC_STAGE14_NATIVE_PHYSICAL_EIGHT_ARM_DEV_MATRIX_PASS")
