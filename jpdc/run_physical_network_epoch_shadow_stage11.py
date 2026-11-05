#!/usr/bin/env python3
"""Original-model physical 21-node E2E network shadow observability, DEV seed83.

No confirmed performance comparison and no routing changes from prior Stage6.
"""
import argparse,json,math
from pathlib import Path
from independent_physical_calibration_stage3 import calibrate
from independent_physical_network_epoch_shadow_stage11 import simulate as shadow_sim
from independent_network_probe_stage6 import simulate as original_sim

SEED=83
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
POLICIES=("PRED_GREEDY","CASPER_FULL","NEW_NETWORK_RESIDUAL","NEW_NETWORK_RESIDUAL_PROBE")
TASKS=12000

def run():
    cal=calibrate(SEED,80000,include_reference=True)
    assert cal["postburnin_service_ratio_count"]==70000
    rows=[]
    for scenario in SCENARIOS:
        for policy in POLICIES:
            r=shadow_sim(SEED,scenario,policy,cal,TASKS)
            prior=original_sim(SEED,scenario,policy,cal,TASKS)
            expected=dict(prior)
            actual=dict(r)
            shadow=actual.pop("shadow_network_epoch")
            assert actual==expected,(scenario,policy,
                [(k,actual.get(k),expected.get(k)) for k in actual if actual.get(k)!=expected.get(k)][:5])
            assert shadow["feedback_events"]==TASKS
            assert shadow["shadow_only_no_routing_control"]
            assert shadow["affected_postshock_dispatches"]==r["postshock_affected_dispatches"]
            assert shadow["affected_postshock_feedback"]==shadow["affected_postshock_dispatches"]
            assert sum(shadow["alarms_by_node"])==shadow["alarm_count"]
            assert 0<=shadow["affected_nodes_observed_postshock"]<=6
            assert 0<=shadow["affected_nodes_alarmed"]<=shadow["affected_nodes_observed_postshock"]
            assert shadow["distinct_affected_unobserved_nodes"]+shadow["affected_nodes_observed_postshock"]==6
            assert 0<=shadow["false_alarms"]<=shadow["alarm_count"]
            assert r["cpu_finish_events"]==r["e2e_feedback_events"]==TASKS
            if shadow["first_observed_affected_alarm_e2e_ms"] is not None:
                assert shadow["first_exposed_task_arrival_ms"]<=shadow["first_observed_affected_alarm_e2e_ms"]
                assert shadow["first_exposed_task_e2e_delivery_ms"]<=shadow["first_observed_affected_alarm_e2e_ms"]
                assert shadow["detector_delay_from_first_affected_feedback_ms"]>=0
            if scenario=="S2_HIDDEN_COMPUTE_40LOSS":
                assert shadow["alarm_count"]==0
                assert shadow["false_alarms"]==0
            print("STAGE11_SHADOW_RESULT",scenario,policy,
                  "MISSION_misses",r["mission_deadline_misses"],
                  "post_miss_rate",r["post_deadline_miss_rate"],
                  "damaged_dispatches",shadow["affected_postshock_dispatches"],
                  "damaged_nodes_seen",shadow["affected_nodes_observed_postshock"],
                  "damaged_nodes_alarmed",shadow["affected_nodes_alarmed"],
                  "alarms",shadow["alarm_count"],
                  "false_alarms",shadow["false_alarms"],
                  "late_quarantine",sum(shadow["quarantined_reports_by_node"]),
                  "first_alarm_delay_ms",shadow["detector_delay_from_first_affected_feedback_ms"])
            print("JPDC_STAGE11_SOURCE_POLICY_EXACT_REGRESSION_PASS",scenario,policy)
            rows.append(r)
    assert len(rows)==8 and sum(r["deployment_tasks"] for r in rows)==96000
    return dict(status="PASS",scope="one previously unused DEVELOPMENT seed83; shadow-only no efficacy inference",
                scientific_seed_index=SEED,scenarios=list(SCENARIOS),policies=list(POLICIES),
                task_policy_observations=96000,
                calibration={k:v for k,v in cal.items() if k!="reference_scores"},
                rows=rows)

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    args=p.parse_args();output=run()
    dest=Path(args.out);dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(output,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print("JPDC_STAGE11_NATIVE_SHADOW_E2E_DIAGNOSTIC_PASS")
