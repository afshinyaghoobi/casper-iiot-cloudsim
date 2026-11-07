#!/usr/bin/env python3
"""Stage37 preregistered DEVELOPMENT seed91, actual 3-arm scheduling comparison.

Dependent task-policy observations: scientific unit=ONE source seed.
"""
import argparse,json
from pathlib import Path
from independent_physical_calibration_stage3 import calibrate
from independent_physical_feedback_deadline_stage37 import simulate
from independent_network_probe_stage6 import simulate as frozen_stage6

SEED=91
COUNT=12000
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
POLICIES=("PRED_GREEDY","CASPER_FULL",
          "NEW_CPU_FEEDBACK_ONLY","NEW_E2E_FEEDBACK_ONLY","NEW_CPU_E2E_FEEDBACK")

def run():
    cal=calibrate(SEED,80000,include_reference=True)
    assert cal["postburnin_service_ratio_count"]==70000
    outputs=[]
    for scenario in SCENARIOS:
        for policy in POLICIES:
            result=simulate(SEED,scenario,policy,cal,COUNT)
            assert result["status"]=="PASS" and result["deployment_tasks"]==COUNT
            assert result["cpu_finish_events"]==COUNT
            assert result["e2e_feedback_events"]==COUNT
            assert result["network_feedback_events"]==COUNT
            post=result["post_mission_tasks"]
            assert post>0
            if policy in ("PRED_GREEDY","CASPER_FULL"):
                copy=dict(result);copy.pop("shadow_network_epoch")
                assert copy==frozen_stage6(SEED,scenario,policy,cal,COUNT),(scenario,policy,"ORIGINAL_STAGE6_JSON_PARITY")
                assert "stage37_feedback" not in result
                miss=round(result["post_deadline_miss_rate"]*post)
                print("STAGE37_FROZEN_STAGE6_EXACT_POLICY_PARITY_PASS",scenario,policy,flush=True)
            else:
                detail=result["stage37_feedback"]
                assert detail["decisions"]==COUNT
                assert detail["causal_cpu_finishes"]==COUNT
                assert detail["delayed_network_observations"]==COUNT
                assert detail["budget_violations"]==0
                assert detail["risk_certificate"] is False
                miss=detail["post_mission_deadline_misses"]
                assert abs(result["post_deadline_miss_rate"]-miss/post)<1e-10
            summary=dict(seed=SEED,scenario=scenario,policy=policy,post_mission_n=post,
                         post_mission_deadline_misses=miss,
                         post_mission_miss_rate=miss/post,
                         full_mission_deadline_misses=result["mission_deadline_misses"],
                         mean_e2e_ms=result["mean_latency_ms"],
                         mean_wait_ms=result["mean_wait_ms"],
                         post_exposed_affected_dispatches=result["postshock_affected_dispatches"],
                         source_stage6_exact_policy_json_parity=(policy in ("PRED_GREEDY","CASPER_FULL")),
                         scheduling_feedback=result.get("stage37_feedback"))
            outputs.append(summary)
            print("STAGE37_DEV_SOURCE_POLICY_RESULT",json.dumps(summary,sort_keys=True),flush=True)
    assert len(outputs)==len(SCENARIOS)*len(POLICIES)
    for sc in SCENARIOS:
        policies={x["policy"]:x for x in outputs if x["scenario"]==sc}
        assert set(policies)==set(POLICIES)
        for name in POLICIES:
            assert policies[name]["post_mission_n"]==policies["PRED_GREEDY"]["post_mission_n"]
    return dict(status="PASS",research_stage=37,scientific_seed=SEED,
                independent_scientific_replicates=1,
                dependent_task_policy_observations=COUNT*len(outputs),
                original_physics="native_Python_stochastic_strict_FCFS",
                no_java_cross_engine_parity_claim=True,
                output_rows=outputs,
                caveat="Development-only n=1. No strong novelty or statistical superiority; no certified deadlines.")
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    a=p.parse_args()
    data=run()
    f=Path(a.out);f.parent.mkdir(parents=True,exist_ok=True)
    f.write_text(json.dumps(data,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print("JPDC_STAGE37_SOURCE_SCHEDULING_DEVELOPMENT_COMPLETE_PASS",flush=True)
