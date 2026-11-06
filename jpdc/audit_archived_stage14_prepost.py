#!/usr/bin/env python3
"""Read-only Stage14 frozen artifact audit; no simulations or parameter tuning."""
import json,sys,math
from pathlib import Path
x=json.loads(Path(sys.argv[1]).read_text())
assert x["status"]=="PASS" and x["seed_index"]==84 and len(x["rows"])==8
out=[]
for row in x["rows"]:
    npost=row["post_mission_tasks"]
    rate=row["post_deadline_miss_rate"]
    assert npost>0 and rate is not None
    post=round(npost*rate)
    assert math.isclose(post/npost,rate,rel_tol=0,abs_tol=1e-12)
    total=row["mission_deadline_misses"]
    assert 0<=post<=total
    pre=total-post
    pre_denom=row["mission_tasks"]-npost
    assert pre_denom>0
    a=row.get("stage14_active")
    row_out=dict(scenario=row["scenario"],policy=row["policy"],
        mission_total=total,mission_pre=pre,mission_post=post,
        pre_mission_tasks=pre_denom,post_mission_tasks=npost,
        pre_miss_rate=pre/pre_denom,post_miss_rate=rate,
        mean_latency_ms=row["mean_latency_ms"],
        mean_wait_ms=row["mean_wait_ms"],
        affected_postshock_dispatches=row["postshock_affected_dispatches"],
        probe_attempts=a["probe_attempts"] if a else None,
        probe_changed_choices=a["probe_changed_choices"] if a else None,
        mission_unverified=a["mission_unverified_decisions"] if a else None,
        probe_normal_deadline_misses=a["probe_normal_deadline_misses"] if a else None,
        probe_actual_latency_sum_ms=a["probe_actual_latency_sum_ms"] if a else None,
        active_route_changed_from_greedy=a["arrivals_changed_from_nominal_greedy"] if a else None)
    out.append(row_out)
    print("STAGE14_FROZEN_MISS_DECOMPOSITION",json.dumps(row_out,sort_keys=True))
assert len(out)==8
for scenario in x["scenario_names"]:
    original=[r for r in out if r["scenario"]==scenario and r["policy"]=="CASPER_FULL"][0]
    new=[r for r in out if r["scenario"]==scenario and r["policy"]=="NEW_FRESHNESS_ACTIVE"][0]
    print("STAGE14_FROZEN_VS_CASPER_FULL",scenario,
          "delta_total_misses",new["mission_total"]-original["mission_total"],
          "delta_pre_misses",new["mission_pre"]-original["mission_pre"],
          "delta_post_misses",new["mission_post"]-original["mission_post"],
          "delta_mean_latency_ms",round(new["mean_latency_ms"]-original["mean_latency_ms"],6))
print("JPDC_STAGE14_FROZEN_PREPOST_MISS_ACCOUNTING_PASS")
