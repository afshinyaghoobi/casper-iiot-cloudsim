#!/usr/bin/env python3
"""Immutable original Stage23 source-development pilot audit only; no reruns."""
import argparse,json,math
from pathlib import Path
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
POLICIES=("PRED_GREEDY","CASPER_FULL","NEW_FRESHNESS_GUARDED","NEW_ROBUST_INTERVAL_DOMINANCE")
p=argparse.ArgumentParser();p.add_argument("--original",required=True);p.add_argument("--out",required=True)
a=p.parse_args()
raw=json.loads(Path(a.original).read_text())
assert raw["status"]=="PASS" and raw["seed_index"]==88
assert raw["task_policy_observations"]==96000 and len(raw["rows"])==8
rows={(r["scenario"],r["policy"]):r for r in raw["rows"]}
assert len(rows)==8 and set(rows)=={(s,p) for s in SCENARIOS for p in POLICIES}
summary=[]
for scenario in SCENARIOS:
    original={policy:rows[scenario,policy] for policy in POLICIES}
    g=original["PRED_GREEDY"];full=original["CASPER_FULL"]
    guard=original["NEW_FRESHNESS_GUARDED"];robust=original["NEW_ROBUST_INTERVAL_DOMINANCE"]
    for r in original.values():
        assert r["total_mission"]==630 and r["post_mission"]==105
        assert r["total_mission_misses"]==r["pre_misses"]+r["post_misses"]
        assert all(math.isfinite(r[x]) for x in ("mean_latency_ms","mean_wait_ms"))
    a=robust["source_stage23_robust"]
    assert a["decisions"]==a["causal_e2e_delivered"]==12000
    assert a["probe_attempts"]==0
    assert 0<=a["mission_switches"]<=a["switches"]
    assert a["arrivals_changed_from_greedy"]==a["switches"]
    assert a["mission_changed_from_greedy"]==a["mission_switches"]
    for r in (g,full,guard):
        assert r["source_stage23_robust"] is None
    item=dict(
        scenario=scenario,seed=88,mission_jobs_per_arm=630,post_mission_jobs=105,
        full_total_misses=full["total_mission_misses"],
        greedy_total_misses=g["total_mission_misses"],
        guarded_total_misses=guard["total_mission_misses"],
        robust_total_misses=robust["total_mission_misses"],
        robust_minus_full_total_misses=robust["total_mission_misses"]-full["total_mission_misses"],
        robust_minus_guarded_total_misses=robust["total_mission_misses"]-guard["total_mission_misses"],
        robust_pre_misses=robust["pre_misses"],robust_post_misses=robust["post_misses"],
        full_pre_misses=full["pre_misses"],full_post_misses=full["post_misses"],
        robust_switches=a["switches"],robust_mission_switches=a["mission_switches"],
        robust_unverified_decisions=a["unverified_decisions"],
        robust_mean_latency_ms=robust["mean_latency_ms"],
        full_mean_latency_ms=full["mean_latency_ms"],
        robust_mean_wait_ms=robust["mean_wait_ms"],
        full_mean_wait_ms=full["mean_wait_ms"],
        robust_affected_postshock_dispatches=robust["postshock_affected_dispatches"],
        full_affected_postshock_dispatches=full["postshock_affected_dispatches"])
    print("STAGE23_FROZEN_EVIDENCE",json.dumps(item,sort_keys=True))
    summary.append(item)
result=dict(status="PASS",science="ONE development seed, not independent confirmatory efficacy",
            seed=88,comparisons=summary,
            original_stage23_run=42238156427,
            no_new_source_simulation=True,
            original_fcfs_java_fidelity="FAIL, CloudSimPlus and strict Python not equivalent")
out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
print("JPDC_STAGE23_IMMUTABLE_EIGHT_ARM_DEVELOPMENT_AUDIT_PASS")
