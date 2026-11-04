#!/usr/bin/env python3
"""Fixed single seed80 novel network-risk mechanism pilot. NOT a holdout."""
import argparse,json,math
from pathlib import Path
from independent_physical_calibration_stage3 import calibrate
from independent_network_risk_physical_pilot import simulate,NEW_POLICY
from independent_casper_deployment_stage4 import simulate as original_stage4

SEED=80
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
POLICIES=("PRED_GREEDY","CASPER_FULL",NEW_POLICY)
N=12000

def execute():
    cal=calibrate(SEED,80000,include_reference=True)
    assert cal["postburnin_service_ratio_count"]==70000
    rows=[]
    for scenario in SCENARIOS:
        for policy in POLICIES:
            r=simulate(SEED,scenario,policy,cal,N)
            assert r["deployment_tasks"]==N and r["status"]=="PASS"
            assert sum(r["node_dispatch_counts"])==N
            assert r["network_feedback_events"]==N
            assert r["network_feedback_strictly_delayed"]
            assert sum(r["rank_counts"].values())==r["mission_tasks"]
            assert 0<=r["postshock_positive_network_feedback"]<=r["network_positive_excess_feedback"]
            assert 0<=r["risk_changed_node_selections"]<=N
            assert 0<=r["risk_positive_penalty_arrivals"]<=N
            if policy==NEW_POLICY:
                assert r["post_cert_rate"]==0
                assert r["adaptive_feedback_events"]==r["health_alarm_transitions"]==0
            else:
                # The new feedback events must not change either comparator's
                # original native strict-FCFS physical outcomes/decisions.
                original=original_stage4(SEED,scenario,policy,cal,N)
                fields=("mission_deadline_misses","post_deadline_miss_rate",
                        "node_dispatch_counts","rank_counts",
                        "post_cert_rate","post_abstention_rate",
                        "post_false_cert_rate","adaptive_feedback_events",
                        "eta_gt_one_dispatches","health_alarm_transitions",
                        "mean_latency_ms","mean_wait_ms")
                for field in fields:
                    v=r[field];expected=original[field]
                    if isinstance(v,float) and isinstance(expected,float):
                        assert math.isclose(v,expected,abs_tol=1e-8,rel_tol=0),(scenario,policy,field,v,expected)
                    else:assert v==expected,(scenario,policy,field,v,expected)
                print("JPDC_NEW_POLICY_ORIGINAL_COMPARATOR_PHYSICAL_REGRESSION_PASS",scenario,policy)
            rows.append(r)
            print("NEW_RISK_PILOT_RESULT",scenario,policy,
                  "MISSION_misses",r["mission_deadline_misses"],
                  "post_miss_rate",r["post_deadline_miss_rate"],
                  "network_excess_obs",r["network_positive_excess_feedback"],
                  "risk_activated_arrivals",r["risk_positive_penalty_arrivals"],
                  "risk_reselected",r["risk_changed_node_selections"],
                  "damaged_postshock_dispatches",r["postshock_affected_dispatches"])
    if len(rows)!=6 or sum(x["deployment_tasks"] for x in rows)!=72000:
        raise AssertionError("incomplete fixed mechanism pilot")
    return {"status":"PASS","scope":"seed80 exploratory development mechanism pilot, NOT confirmatory",
            "policy_design":"completion-delayed per-node 32-sample 90percentile network excess",
            "seed_index":SEED,"scenarios":list(SCENARIOS),
            "policies":list(POLICIES),"deployment_task_policy_observations":72000,
            "calibration":{k:v for k,v in cal.items() if k!="reference_scores"},
            "rows":rows}
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--out",required=True);a=p.parse_args()
    out=execute();f=Path(a.out);f.parent.mkdir(parents=True,exist_ok=True)
    f.write_text(json.dumps(out,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print("JPDC_NEW_NETWORK_RESIDUAL_PHYSICAL_PILOT_PASS")
