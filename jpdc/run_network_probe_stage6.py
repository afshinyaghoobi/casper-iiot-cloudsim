#!/usr/bin/env python3
"""Stage6 original fixed seed82 development, all outcomes source-generated."""
import argparse,json,math
from pathlib import Path
from independent_physical_calibration_stage3 import calibrate
from independent_network_probe_stage6 import simulate,NEW_POLICY,PROBE_POLICY
from independent_harmonized_e2e_feedback_stage5 import simulate as stage5

SEED=82
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
POLICIES=("PRED_GREEDY","CASPER_FULL",NEW_POLICY,PROBE_POLICY)
TASKS=12000

def execute():
    calibration=calibrate(SEED,80000,include_reference=True)
    assert calibration["postburnin_service_ratio_count"]==70000
    rows=[]
    for scenario in SCENARIOS:
        for policy in POLICIES:
            r=simulate(SEED,scenario,policy,calibration,TASKS)
            assert r["status"]=="PASS" and r["deployment_tasks"]==TASKS
            assert r["cpu_finish_events"]==r["e2e_feedback_events"]==r["network_feedback_events"]==TASKS
            assert r["e17_observed_at_e2e"]==r["adaptive_feedback_events"]
            assert sum(r["node_dispatch_counts"])==TASKS
            assert sum(r["rank_counts"].values())==r["mission_tasks"]
            if policy!=PROBE_POLICY:
                prior=stage5(SEED,scenario,policy,calibration,TASKS)
                fields=("mission_deadline_misses","post_deadline_miss_rate",
                        "node_dispatch_counts","rank_counts","post_cert_rate",
                        "post_abstention_rate","post_false_cert_rate",
                        "adaptive_feedback_events","eta_gt_one_dispatches",
                        "health_alarm_transitions","mean_latency_ms","mean_wait_ms",
                        "risk_changed_node_selections","risk_positive_penalty_arrivals",
                        "postshock_affected_dispatches","network_positive_excess_feedback")
                for field in fields:
                    v=r[field];old=prior[field]
                    if isinstance(v,float) and isinstance(old,float):
                        assert math.isclose(v,old,rel_tol=0,abs_tol=1e-8),(scenario,policy,field,v,old)
                    else:assert v==old,(scenario,policy,field,v,old)
                assert r["network_probe_attempts"]==r["network_probe_changed_choices"]==0
                print("JPDC_STAGE6_UNCHANGED_OLD_POLICY_REGRESSION_PASS",scenario,policy)
            else:
                assert r["adaptive_feedback_events"]==r["health_alarm_transitions"]==0
                assert r["post_cert_rate"]==0
                assert 0<=r["network_probe_attempts"]<=r["network_probe_opportunities"]<=r["normal_arrivals"]//100
                assert r["network_probe_attempts"]+r["network_probe_skipped_empty"]==r["network_probe_opportunities"]
                assert 0<=r["network_probe_changed_choices"]<=r["network_probe_attempts"]
                assert 0<=r["network_probe_positive_feedback"]<=r["network_probe_attempts"]
                assert 0<=r["network_probe_normal_deadline_misses"]<=r["network_probe_attempts"]
                assert r["network_node_feedback_counts"] is not None
                assert sum(r["network_node_feedback_counts"])==TASKS
            rows.append(r)
            print("STAGE6_ROW",scenario,policy,"mission_misses",r["mission_deadline_misses"],
                  "post_mission_rate",r["post_deadline_miss_rate"],
                  "affected_postshock",r["postshock_affected_dispatches"],
                  "positive_network",r["network_positive_excess_feedback"],
                  "risk_reroutes",r["risk_changed_node_selections"],
                  "probe_opportunities",r["network_probe_opportunities"],
                  "probe_attempts",r["network_probe_attempts"],
                  "probe_changed",r["network_probe_changed_choices"],
                  "probe_positive_network",r["network_probe_positive_feedback"],
                  "probe_misses",r["network_probe_normal_deadline_misses"])
    assert len(rows)==8 and sum(r["deployment_tasks"] for r in rows)==96000
    return {
        "status":"PASS","scope":"seed82 source-independent development pilot, NO efficacy inference",
        "scientific_seed_index":SEED,"scenarios":list(SCENARIOS),
        "policies":list(POLICIES),"task_policy_observations":96000,
        "calibration":{k:v for k,v in calibration.items() if k!="reference_scores"},
        "rows":rows,
    }

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    args=p.parse_args();res=execute()
    target=Path(args.out);target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(res,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print("JPDC_STAGE6_NETWORK_PROBING_FIXED_MATRIX_PASS")
