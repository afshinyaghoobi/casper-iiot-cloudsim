#!/usr/bin/env python3
"""Stage5 source-level and mechanism invariants, fail closed on early feedback."""
import inspect
from independent_harmonized_e2e_feedback_stage5 import simulate
from independent_physical_calibration_stage3 import calibrate
from network_residual_risk_policy import NetworkResidualRisk

src=inspect.getsource(simulate)
assert src.index("elif kind==0:")<src.index("else:\n            # Only completed")
cpu_branch=src.split("elif kind==0:",1)[1].split("else:\n            # Only completed",1)[0]
e2e_branch=src.split("else:\n            # Only completed",1)[1]
assert ".observe(outcome_score)" not in cpu_branch, "E17 updated on CPU completion"
assert "e17.observe(outcome_score)" in e2e_branch
assert "risk_state.observe_e2e" not in cpu_branch
assert "risk_state.observe_e2e" in e2e_branch
assert "cpu_finish_time+actual_net" in e2e_branch
print("PASS no E17 or network risk outcome ingestion at CPU finish")
print("PASS original E17 and network risk observe in physically later end-to-end event")
# independent complete 10,010-task post-change smoke test, enough to
# exercise real physical scenario fault events without full matrix tuning.
cal=calibrate(81,80000,include_reference=True)
x=simulate(81,"S3_HIDDEN_NETWORK_50LOSS","CASPER_FULL",cal,10010)
assert x["status"]=="PASS"
assert x["cpu_finish_events"]==x["e2e_feedback_events"]==x["network_feedback_events"]==10010
assert x["e17_observed_at_e2e"]==x["mission_tasks"]==x["adaptive_feedback_events"]
assert x["e17_feedback_strictly_delayed"]
print("JPDC_STAGE5_E2E_FEEDBACK_TIMING_UNIT_PASS")
