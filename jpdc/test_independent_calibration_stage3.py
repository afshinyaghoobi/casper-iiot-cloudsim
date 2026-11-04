#!/usr/bin/env python3
"""Native calibration falsification tests: physical conservation and input guards."""
from independent_physical_calibration_stage3 import calibrate, BURN_IN
from independent_workload_generator import calibration_mission_ranks,conformal_qhat
import math

seed=4202202650
expected=calibration_mission_ranks(seed,12000,BURN_IN)
r=calibrate(50,12000)
assert r["calibration_tasks"]==12000
assert r["postburnin_service_ratio_count"]==2000
assert r["mission_score_count"]==len(expected)
assert r["rank_counts"]==[sum(v==rank for v in expected.values()) for rank in (1,2,3)]
assert sum(r["tier_counts"])==2000
assert r["probe_budget_consumed"]>0
assert r["actual_probes"]>=0
assert r["telemetry_resets"]>0
assert math.isfinite(r["mean_physical_wait_ms"])
print("PASS independent post-burnin conservation and randomized rank assignments")
print("PASS real native original-model sparse probe opportunities:",r["probe_budget_consumed"])

for invalid in (0,BURN_IN-1,BURN_IN):
    try:calibrate(50,invalid)
    except ValueError:pass
    else:raise AssertionError("calibration sample count guard failed")
for invalid in ([],[float("nan")],[float("inf")]):
    try:
        result=conformal_qhat(invalid,.01)
        if invalid:raise AssertionError("invalid score accepted")
        assert math.isinf(result)
    except ValueError:
        assert bool(invalid)
print("PASS invalid sample counts and nonfinite calibration scores rejected")
print("JPDC_NATIVE_CALIBRATION_STAGE3_UNIT_PASS")
