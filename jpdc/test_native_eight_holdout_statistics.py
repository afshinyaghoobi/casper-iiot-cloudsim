#!/usr/bin/env python3
"""Synthetic fail-closed primary statistics tests: NEVER scientific holdout observations."""
from pathlib import Path
from tempfile import TemporaryDirectory
import json, math
from analyze_native_eight_holdout import (
    SEEDS,SCENARIOS,POLICIES,analyze,exact_sign_test)
assert exact_sign_test([1.0]*10)["p_two_sided"]==2/1024
assert exact_sign_test([0.0]*10)["p_two_sided"]==1.0
assert exact_sign_test([1]*6+[-1]*2+[0]*2)=={
    "positive":6,"negative":2,"ties":2,"nonzero":8,"p_two_sided":74/256}
print("PASS preregistered exact two-sided sign test + zero-tie accounting")

def build(seed, benefit=0.0):
    rows=[]
    for c in SCENARIOS:
        for p in POLICIES:
            rate=.1 if p!="PRED_GREEDY" else .1+benefit
            rows.append({
                "seed_index":seed,"status":"PASS","policy":p,"scenario":c,
                "deployment_tasks":30000,"node_dispatch_counts":[30000]+[0]*20,
                "rank_counts":{"1":100,"2":0,"3":0},
                "mission_tasks":100,"post_mission_tasks":50,
                "post_deadline_miss_rate":rate,"mission_deadline_misses":20,
                "post_cert_rate":0.1,"post_false_cert_rate":0.0,
                "post_abstention_rate":.9,"post_family_covered_rate":.9,
                "health_alarm_transitions":0,"eta_gt_one_dispatches":0,
                "probes":0,"probe_violations":0,"postshock_affected_dispatches":0})
    return {
        "seed_index":seed,"scientific_seed":4202202600+seed,
        "status":"PASS","deployment_tasks_per_run":30000,
        "total_task_policy_observations":480000,
        "policy_modes":list(POLICIES),"scenarios":list(SCENARIOS),
        "calibration":{"calibration_tasks":80000,"scientific_seed":4202202600+seed,
                       "postburnin_service_ratio_count":70000},
        "rows":rows}

with TemporaryDirectory() as d:
    paths=[]
    for seed in SEEDS:
        path=Path(d)/f"seed{seed}.json"
        path.write_text(json.dumps(build(seed,0.03)))
        paths.append(path)
    a=analyze(paths)
    assert a["complete_arms"]==160 and a["primary_significant"]
    assert a["exact_two_sided_sign_test"]["p_two_sided"]==.001953125
    assert math.isclose(a["mean_benefit"],.03,abs_tol=1e-12)
    assert len(a["native_all_eight_secondary"])==160
    print("PASS synthetic complete frozen ten-seed artifact aggregation")
    for corrupt in (paths[:-1],paths[:-1]+[paths[0]]):
        try:analyze(corrupt)
        except ValueError:pass
        else:raise AssertionError("accepted incomplete/duplicate seed set")
    bad=build(60,0.0)
    bad["rows"][0]["post_mission_tasks"]=49
    original=paths[0].read_text()
    paths[0].write_text(json.dumps(bad))
    try:analyze(paths)
    except ValueError:pass
    else:raise AssertionError("accepted cross-policy cohort drift")
    paths[0].write_text(original)
    print("PASS incomplete, duplicate and cohort-manipulated scientific inputs rejected")
print("JPDC_NATIVE_HOLDOUT_STATS_UNIT_PASS")
