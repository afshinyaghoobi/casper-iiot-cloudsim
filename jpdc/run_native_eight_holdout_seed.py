#!/usr/bin/env python3
"""Frozen native independent holdout: run one unseen seed, all eight modes.

No Java outcomes, calibration quantiles or original physical traces imported.
Read the preregistration before interpreting paired effects.
"""
import argparse,json,math
from pathlib import Path
from independent_physical_calibration_stage3 import calibrate
from independent_casper_deployment_stage4 import simulate,POLICIES,POLICY_FLAGS

SEEDS=tuple(range(60,70))
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
TASKS=30000
CAL_TASKS=80000
def run_one(seed):
    if seed not in SEEDS:raise ValueError("seed is outside frozen holdout")
    calibration=calibrate(seed,CAL_TASKS,include_reference=True)
    assert calibration["status"]=="PASS"
    assert calibration["postburnin_service_ratio_count"]==70000
    assert calibration["mission_score_count"]==sum(calibration["rank_counts"])
    assert len(calibration["reference_scores"])==calibration["mission_score_count"]
    assert all(math.isfinite(x) and x>0 for x in
               [*calibration["q_rank"],calibration["q_global"],*calibration["tier_thresholds"]])
    rows=[]
    for scenario in SCENARIOS:
        denominator=None
        for policy in POLICIES:
            r=simulate(seed,scenario,policy,calibration,TASKS)
            assert r["status"]=="PASS" and r["deployment_tasks"]==TASKS
            assert r["policy_flags"]==POLICY_FLAGS[policy]
            assert r["scientific_seed"]==4202202600+seed
            assert sum(r["node_dispatch_counts"])==TASKS
            assert sum(r["rank_counts"].values())==r["mission_tasks"]
            assert r["mission_tasks"]>0 and r["post_mission_tasks"]>0
            assert 0<=r["mission_deadline_misses"]<=r["mission_tasks"]
            assert 0<=r["post_deadline_miss_rate"]<=1
            if denominator is None:
                denominator=(r["mission_tasks"],r["post_mission_tasks"])
            assert denominator==(r["mission_tasks"],r["post_mission_tasks"]),(
                "MISSION original workload cohort differs across policies",seed,scenario)
            flags=POLICY_FLAGS[policy]
            if flags["adaptive"]:
                assert r["adaptive_feedback_events"]==r["mission_tasks"]
            else:
                assert r["adaptive_feedback_events"]==r["eta_gt_one_dispatches"]==0
            if not flags["health"]:
                assert r["health_alarm_transitions"]==r["health_alarmed_nodes"]==r["probes"]==0
            if not flags["cp"]:
                assert r["post_cert_rate"]==0 and r["post_false_cert_rate"] is None
                assert r["post_abstention_rate"] is None and r["post_family_covered_rate"] is None
            else:
                assert r["post_cert_rate"] is not None
                assert r["post_false_cert_rate"]<=r["post_cert_rate"]
                assert math.isclose(r["post_cert_rate"]+r["post_abstention_rate"],1.0,
                                    abs_tol=1e-12,rel_tol=0)
            rows.append(r)
            print("HOLDOUT_NATIVE_ROW",seed,scenario,policy,
                  "post_mission",r["post_mission_tasks"],
                  "post_miss_rate",r["post_deadline_miss_rate"],
                  "rank_counts",r["rank_counts"],"health_alarms",r["health_alarm_transitions"],
                  "adaptive_dispatches",r["eta_gt_one_dispatches"])
    assert len(rows)==16 and sum(r["deployment_tasks"] for r in rows)==480000
    return {
        "status":"PASS","seed_index":seed,"scientific_seed":4202202600+seed,
        "scope":"native Python strict FCFS original-model seed holdout, NOT YAFS/CloudSim-equivalent",
        "calibration":{key:value for key,value in calibration.items() if key!="reference_scores"},
        "policy_modes":list(POLICIES),"scenarios":list(SCENARIOS),
        "deployment_tasks_per_run":TASKS,
        "total_task_policy_observations":480000,
        "rows":rows}
def main():
    p=argparse.ArgumentParser();p.add_argument("--seed",type=int,required=True)
    p.add_argument("--out",required=True);a=p.parse_args()
    result=run_one(a.seed)
    dest=Path(a.out);dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+"\n",encoding="utf-8")
    print("JPDC_NATIVE_EIGHT_SEED_HOLDOUT_COHORT_PASS",a.seed)
if __name__=="__main__":main()
