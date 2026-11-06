#!/usr/bin/env python3
"""Stage23 fixed DEV seed88: compare robust interval dominance vs originals."""
import argparse,json,math
from pathlib import Path
from independent_physical_calibration_stage3 import calibrate
from independent_physical_robust_dominance_stage23 import simulate as prototype
from independent_physical_guarded_freshness_stage15 import simulate as frozen_guard
from independent_network_probe_stage6 import simulate as frozen_stage6

SEED=88
N=12000
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
POLICIES=("PRED_GREEDY","CASPER_FULL","NEW_FRESHNESS_GUARDED","NEW_ROBUST_INTERVAL_DOMINANCE")
def run():
    cal=calibrate(SEED,80000,include_reference=True)
    assert cal["postburnin_service_ratio_count"]==70000
    rows=[]
    for scenario in SCENARIOS:
        for policy in POLICIES:
            r=prototype(SEED,scenario,policy,cal,N)
            if policy in ("PRED_GREEDY","CASPER_FULL"):
                original=dict(r);original.pop("shadow_network_epoch")
                assert original==frozen_stage6(SEED,scenario,policy,cal,N),(scenario,policy,"frozen Stage6 drift")
                print("STAGE23_FROZEN_STAGE6_EXACT_PARITY_PASS",scenario,policy,flush=True)
            elif policy=="NEW_FRESHNESS_GUARDED":
                assert r==frozen_guard(SEED,scenario,policy,cal,N),(scenario,"frozen Stage15 drift")
                print("STAGE23_FROZEN_STAGE15_EXACT_PARITY_PASS",scenario,flush=True)
            else:
                a=r["stage23_robust"]
                assert a["causal_e2e_delivered"]==a["decisions"]==N
                assert a["probe_attempts"]==r["probes"]==0
                assert 0<=a["mission_switches"]<=a["switches"]<=N
                assert a["mission_changed_from_greedy"]==a["mission_switches"]
                assert a["arrivals_changed_from_greedy"]==a["switches"]
                print("STAGE23_CAUSAL_ROBUST_SOURCE_INTEGRITY_PASS",scenario,flush=True)
            assert r["deployment_tasks"]==r["cpu_finish_events"]==r["e2e_feedback_events"]==N
            assert r["network_feedback_events"]==N
            post=round(r["post_deadline_miss_rate"]*r["post_mission_tasks"])
            assert math.isclose(post/r["post_mission_tasks"],r["post_deadline_miss_rate"],abs_tol=1e-12)
            row=dict(seed=SEED,scenario=scenario,policy=policy,
                     total_mission=r["mission_tasks"],post_mission=r["post_mission_tasks"],
                     total_mission_misses=r["mission_deadline_misses"],
                     pre_misses=r["mission_deadline_misses"]-post,
                     post_misses=post,mean_latency_ms=r["mean_latency_ms"],
                     mean_wait_ms=r["mean_wait_ms"],
                     postshock_affected_dispatches=r["postshock_affected_dispatches"],
                     source_stage23_robust=r.get("stage23_robust"))
            rows.append(row)
            print("STAGE23_PHYSICAL_RESULT",json.dumps(row,sort_keys=True),flush=True)
    assert len(rows)==8
    return dict(status="PASS",scientific_scope="ONE development seed88; no significance inference",
                seed_index=SEED,task_policy_observations=96000,
                frozen_scenarios=list(SCENARIOS),frozen_policies=list(POLICIES),rows=rows)
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    a=p.parse_args();out=run()
    dest=Path(a.out);dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(out,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print("JPDC_STAGE23_ROBUST_SOURCE_PHYSICAL_DEVELOPMENT_MATRIX_PASS",flush=True)
