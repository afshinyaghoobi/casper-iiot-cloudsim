#!/usr/bin/env python3
"""Stage16 frozen prospective source-level paired validation, sharded by seed."""
import argparse,json,math
from pathlib import Path
from independent_physical_calibration_stage3 import calibrate
from independent_physical_guarded_freshness_stage15 import simulate as simulate
from independent_network_probe_stage6 import simulate as frozen_original

SEEDS=tuple(range(301,309))
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
POLICIES=("CASPER_FULL","PRED_GREEDY","NEW_FRESHNESS_GUARDED")
TASKS=12000

def run(seed):
    if seed not in SEEDS:raise ValueError("unregistered seed")
    cal=calibrate(seed,80000,include_reference=True)
    assert cal["postburnin_service_ratio_count"]==70000
    rows=[]
    for scenario in SCENARIOS:
        group={}
        for policy in POLICIES:
            r=simulate(seed,scenario,policy,cal,TASKS)
            if policy!="NEW_FRESHNESS_GUARDED":
                legacy=dict(r)
                legacy.pop("shadow_network_epoch")
                assert legacy==frozen_original(seed,scenario,policy,cal,TASKS),(
                    "legacy policy parity fail",seed,scenario,policy)
                print("STAGE16_ORIGINAL_STAGE6_PARITY_PASS",seed,scenario,policy,flush=True)
            else:
                a=r["stage14_active"]
                assert a["causal_e2e_delivered"]==TASKS
                assert a["normal_arrivals"]//100==a["probe_opportunities"]
                assert a["probe_attempts"]+a["probe_skipped"]==a["probe_opportunities"]
                assert a["probe_attempts"]<=a["normal_arrivals"]//100
                assert a["mission_unverified_decisions"]<=r["mission_tasks"]
                print("STAGE16_GUARDED_CAUSAL_BUDGET_PASS",seed,scenario,flush=True)
            assert r["deployment_tasks"]==r["cpu_finish_events"]==r["e2e_feedback_events"]==TASKS
            assert r["network_feedback_events"]==TASKS
            post=round(r["post_deadline_miss_rate"]*r["post_mission_tasks"])
            assert math.isclose(post/r["post_mission_tasks"],r["post_deadline_miss_rate"],abs_tol=1e-12)
            item=dict(seed=seed,scenario=scenario,policy=policy,
                      mission_tasks=r["mission_tasks"],post_mission_tasks=r["post_mission_tasks"],
                      total_misses=r["mission_deadline_misses"],
                      pre_misses=r["mission_deadline_misses"]-post,
                      post_misses=post,mean_latency_ms=r["mean_latency_ms"],
                      mean_wait_ms=r["mean_wait_ms"],
                      affected_postshock_dispatches=r["postshock_affected_dispatches"],
                      probes=r.get("stage14_active",{}).get("probe_attempts"),
                      changed_routes=r.get("stage14_active",{}).get("arrivals_changed_from_nominal_greedy"))
            rows.append(item)
            group[policy]=item
            print("STAGE16_RESULT",json.dumps(item,sort_keys=True),flush=True)
        assert len({group[p]["mission_tasks"] for p in POLICIES})==1
        assert len({group[p]["post_mission_tasks"] for p in POLICIES})==1
    assert len(rows)==6
    return dict(status="PASS",scientific_seed_index=seed,protocol="STAGE16_PAIRED_EIGHT_SEED_PROTOCOL_PREREG_2026-11-06",
                rows=rows,task_policy_observations=72000)

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--seed",type=int,required=True);p.add_argument("--out",required=True)
    args=p.parse_args()
    result=run(args.seed)
    dest=Path(args.out);dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(result,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print("JPDC_STAGE16_PER_SEED_PHYSICAL_PAIRING_PASS",args.seed,flush=True)
