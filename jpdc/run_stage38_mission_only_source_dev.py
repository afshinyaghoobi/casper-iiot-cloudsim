#!/usr/bin/env python3
"""Stage38 predeclared new development seed92 actual deadline paired ablation."""
import argparse,json
from pathlib import Path
from independent_physical_calibration_stage3 import calibrate
from independent_physical_mission_only_feedback_stage38 import simulate
from independent_network_probe_stage6 import simulate as frozen_stage6
from independent_physical_feedback_deadline_stage37 import simulate as original_stage37

SEED=92
N=12000
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
POLICIES=("PRED_GREEDY","CASPER_FULL","NEW_CPU_FEEDBACK_ONLY",
          "NEW_CPU_E2E_FEEDBACK","NEW_MISSION_ONLY_CPU_FEEDBACK",
          "NEW_MISSION_ONLY_CPU_E2E_FEEDBACK")
def run():
    cal=calibrate(SEED,80000,include_reference=True)
    assert cal["postburnin_service_ratio_count"]==70000
    outcomes=[]
    for sc in SCENARIOS:
        for p in POLICIES:
            result=simulate(SEED,sc,p,cal,N)
            assert result["status"]=="PASS" and result["deployment_tasks"]==N
            assert result["cpu_finish_events"]==result["e2e_feedback_events"]==N
            original=dict(result);original.pop("shadow_network_epoch")
            if p in ("PRED_GREEDY","CASPER_FULL"):
                assert original==frozen_stage6(SEED,sc,p,cal,N),(sc,p,"Stage6 exact parity")
            if p in ("NEW_CPU_FEEDBACK_ONLY","NEW_CPU_E2E_FEEDBACK"):
                assert result==original_stage37(SEED,sc,p,cal,N),(sc,p,"Stage37 exact old policy drift")
            feedback=result.get("stage37_feedback")
            if feedback is not None:
                assert feedback["decisions"]==feedback["causal_cpu_finishes"]==N
                assert feedback["budget_violations"]==0
                if p.startswith("NEW_MISSION_ONLY"):
                    assert feedback["mission_only_feedback"]
                    assert feedback["background_changes_from_greedy"]==0
                    assert feedback["changed_from_greedy"]==feedback["mission_changed_from_greedy"]
                else:
                    assert feedback["mission_only_feedback"] is False
                miss=feedback["post_mission_deadline_misses"]
                class_misses=feedback["deadline_misses_by_class"]
            else:
                miss=round(result["post_deadline_miss_rate"]*result["post_mission_tasks"])
                class_misses={}
            assert abs(miss/result["post_mission_tasks"]-result["post_deadline_miss_rate"])<1e-10
            o=dict(scenario=sc,policy=p,seed=SEED,
                   post_mission_n=result["post_mission_tasks"],
                   post_mission_deadline_misses=miss,
                   mission_deadline_misses_overall=result["mission_deadline_misses"],
                   mean_latency_ms=result["mean_latency_ms"],
                   mean_wait_ms=result["mean_wait_ms"],
                   changes_from_greedy=feedback["changed_from_greedy"] if feedback else None,
                   mission_changes_from_greedy=feedback["mission_changed_from_greedy"] if feedback else None,
                   background_changes_from_greedy=feedback["background_changes_from_greedy"] if feedback else None,
                   deadline_misses_by_class=class_misses,
                   frozen_prior_policy_exact_parity=(p in ("PRED_GREEDY","CASPER_FULL","NEW_CPU_FEEDBACK_ONLY","NEW_CPU_E2E_FEEDBACK")),
                   false_deadline_certification=False)
            outcomes.append(o)
            print("STAGE38_SOURCE_SEED92_MISSION_ONLY_RESULT",json.dumps(o,sort_keys=True),flush=True)
    assert len(outcomes)==12
    return dict(status="PASS",scientific_seed=SEED,scientific_units=1,
                dependent_task_policy_observations=N*len(outcomes),
                stage37_rule_frozen=True,
                original_physics_unmodified=True,
                no_statistical_superiority_claim=True,
                task_policy_outcomes=outcomes)
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    args=p.parse_args()
    data=run()
    f=Path(args.out);f.parent.mkdir(parents=True,exist_ok=True)
    f.write_text(json.dumps(data,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print("JPDC_STAGE38_MISSION_ONLY_FEEDBACK_SOURCE_DEVELOPMENT_COMPLETE_PASS")
