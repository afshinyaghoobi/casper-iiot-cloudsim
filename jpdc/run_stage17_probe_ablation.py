#!/usr/bin/env python3
"""Prespecified Stage17 native causal probing ablation; developmental seeds86/87."""
import argparse,json,math
from pathlib import Path
from independent_physical_calibration_stage3 import calibrate
from independent_physical_probe_ablation_stage17 import simulate as stage17
from independent_physical_guarded_freshness_stage15 import simulate as stage15
from independent_network_probe_stage6 import simulate as legacy

SEEDS=(86,87)
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
POLICIES=("PRED_GREEDY","CASPER_FULL","NEW_FRESHNESS_GUARDED","NEW_FRESHNESS_NO_ACTIVE_PROBE")
COUNT=12000
EXTRA=("stage17_selected_node_counts","stage17_mission_nominal_detour_sum_ms","stage17_mission_nominal_detour_max_ms")

def run(seed):
    if seed not in SEEDS:raise ValueError("unregistered exploratory seed")
    cal=calibrate(seed,80000,include_reference=True)
    assert cal["postburnin_service_ratio_count"]==70000
    rows=[]
    for scenario in SCENARIOS:
        for policy in POLICIES:
            r=stage17(seed,scenario,policy,cal,COUNT)
            if policy in POLICIES[:2]:
                prior=dict(r);prior.pop("shadow_network_epoch")
                assert prior==legacy(seed,scenario,policy,cal,COUNT),(seed,scenario,policy,"legacy output changed")
            else:
                data=r["stage14_active"]
                assert sum(data["stage17_selected_node_counts"])==COUNT
                assert data["stage17_mission_nominal_detour_max_ms"]<=2.+1e-9
                assert data["causal_e2e_delivered"]==COUNT
                assert data["probe_attempts"]<=data["normal_arrivals"]//100
                if policy=="NEW_FRESHNESS_GUARDED":
                    original=stage15(seed,scenario,policy,cal,COUNT)
                    updated=json.loads(json.dumps(r))
                    for k in EXTRA:updated["stage14_active"].pop(k)
                    assert updated==original,(seed,scenario,"original Stage15 policy changed")
                else:
                    assert data["probe_attempts"]==data["probe_changed_choices"]==0
                    assert data["probe_skipped"]==data["probe_opportunities"]
            assert r["cpu_finish_events"]==r["e2e_feedback_events"]==r["deployment_tasks"]==COUNT
            post=round(r["post_deadline_miss_rate"]*r["post_mission_tasks"])
            assert math.isclose(post/r["post_mission_tasks"],r["post_deadline_miss_rate"],abs_tol=1e-12)
            out=dict(seed=seed,scenario=scenario,policy=policy,
                     mission_tasks=r["mission_tasks"],post_mission_tasks=r["post_mission_tasks"],
                     total_misses=r["mission_deadline_misses"],pre_misses=r["mission_deadline_misses"]-post,
                     post_misses=post,mean_latency_ms=r["mean_latency_ms"],mean_wait_ms=r["mean_wait_ms"],
                     stage17_stats=r.get("stage14_active"))
            rows.append(out)
            print("STAGE17_ABLATION",json.dumps(out,sort_keys=True),flush=True)
    assert len(rows)==8
    return dict(status="PASS",seed_index=seed,scope="Stage17 exploratory only, not Stage16 confirmation",
                task_policy_observations=96000,rows=rows)

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--seed",required=True,type=int);p.add_argument("--out",required=True)
    a=p.parse_args();result=run(a.seed)
    dest=Path(a.out);dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(result,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print("JPDC_STAGE17_EXPLORATORY_PROBING_ABLATION_PASS",a.seed,flush=True)
