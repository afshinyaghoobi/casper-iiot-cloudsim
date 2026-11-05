#!/usr/bin/env python3
"""Frozen seed81 matched feedback-timing development check, no efficacy inference."""
import argparse,json,math
from pathlib import Path
from independent_physical_calibration_stage3 import calibrate
from independent_harmonized_e2e_feedback_stage5 import simulate,NEW_POLICY
from independent_casper_deployment_stage4 import simulate as original_stage4

SEED=81
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
POLICIES=("PRED_GREEDY","CASPER_FULL",NEW_POLICY)
N=12000

def execute():
    calibration=calibrate(SEED,80000,include_reference=True)
    assert calibration["postburnin_service_ratio_count"]==70000
    rows=[]
    old_full_comparisons=[]
    for scenario in SCENARIOS:
        for policy in POLICIES:
            result=simulate(SEED,scenario,policy,calibration,N)
            assert result["status"]=="PASS" and result["deployment_tasks"]==N
            assert result["cpu_finish_events"]==result["e2e_feedback_events"]==result["network_feedback_events"]==N
            assert result["network_feedback_strictly_delayed"] and result["e17_feedback_strictly_delayed"]
            assert sum(result["node_dispatch_counts"])==N
            assert sum(result["rank_counts"].values())==result["mission_tasks"]
            assert result["adaptive_feedback_events"]==result["e17_observed_at_e2e"]
            assert (result["adaptive_feedback_events"]==result["mission_tasks"])==(policy=="CASPER_FULL")
            if policy=="PRED_GREEDY":
                prior=original_stage4(SEED,scenario,policy,calibration,N)
                for k in ("node_dispatch_counts","mission_deadline_misses","rank_counts",
                          "post_deadline_miss_rate","mean_latency_ms","mean_wait_ms"):
                    a=result[k];b=prior[k]
                    if isinstance(a,float):
                        assert math.isclose(a,b,rel_tol=0,abs_tol=1e-8),(scenario,k,a,b)
                    else:assert a==b,(scenario,k,a,b)
                print("JPDC_STAGE5_UNCHANGED_GREEDY_ORIGINAL_PHYSICAL_PARITY_PASS",scenario)
            elif policy=="CASPER_FULL":
                old=original_stage4(SEED,scenario,policy,calibration,N)
                old_full_comparisons.append({
                    "scenario":scenario,
                    "old_mission_deadline_misses":old["mission_deadline_misses"],
                    "harmonized_mission_deadline_misses":result["mission_deadline_misses"],
                    "old_post_mission_miss_rate":old["post_deadline_miss_rate"],
                    "harmonized_post_mission_miss_rate":result["post_deadline_miss_rate"],
                    "old_eta_gt_one_dispatches":old["eta_gt_one_dispatches"],
                    "harmonized_eta_gt_one_dispatches":result["eta_gt_one_dispatches"],
                    "old_node_dispatch_counts":old["node_dispatch_counts"],
                    "harmonized_node_dispatch_counts":result["node_dispatch_counts"]})
            rows.append(result)
            print("STAGE5_HARMONIZED_RESULT",scenario,policy,
                  "mission_misses",result["mission_deadline_misses"],
                  "post_miss_rate",result["post_deadline_miss_rate"],
                  "network_positive_feedback",result["network_positive_excess_feedback"],
                  "risk_reroutes",result["risk_changed_node_selections"],
                  "affected_postshock_dispatches",result["postshock_affected_dispatches"],
                  "e17_feedback_at_e2e",result["e17_observed_at_e2e"])
    assert len(rows)==6 and sum(x["deployment_tasks"] for x in rows)==72000
    assert len(old_full_comparisons)==2
    return {
      "status":"PASS","seed_index":SEED,"scope":"known-development harmonized E2E feedback pilot, NO confirmatory inference",
      "original_E42_untouched":True,
      "policies":list(POLICIES),"scenarios":list(SCENARIOS),
      "total_task_policy_observations":72000,
      "calibration":{k:v for k,v in calibration.items() if k!="reference_scores"},
      "old_full_vs_harmonized_full":old_full_comparisons,"rows":rows}

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--out",required=True);a=p.parse_args()
    out=execute();dest=Path(a.out);dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(out,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print("JPDC_STAGE5_HARMONIZED_E2E_COMPLETE_PHYSICAL_PILOT_PASS")
