#!/usr/bin/env python3
"""Stage40 fixed source DEV seed93/94, CASPER_FULL anchored MISSION reranking."""
import argparse,json
from pathlib import Path
from independent_physical_calibration_stage3 import calibrate
from independent_physical_full_anchored_stage40 import simulate
from independent_network_probe_stage6 import simulate as frozen_stage6
from independent_physical_mission_only_feedback_stage38 import simulate as frozen_stage38

SEEDS=(93,94)
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
POLICIES=("PRED_GREEDY","CASPER_FULL","NEW_MISSION_ONLY_CPU_E2E_FEEDBACK",
          "NEW_FULL_ANCHORED_E2E","NEW_FULL_ANCHORED_CPU_E2E")
N=12000

def run(seed):
    assert seed in SEEDS
    calibration=calibrate(seed,80000,include_reference=True)
    assert calibration["postburnin_service_ratio_count"]==70000
    results=[]
    for scenario in SCENARIOS:
        for policy in POLICIES:
            x=simulate(seed,scenario,policy,calibration,N)
            assert x["status"]=="PASS" and x["deployment_tasks"]==N
            assert x["cpu_finish_events"]==x["e2e_feedback_events"]==x["network_feedback_events"]==N
            if policy in ("CASPER_FULL","PRED_GREEDY"):
                old=dict(x);old.pop("shadow_network_epoch")
                assert old==frozen_stage6(seed,scenario,policy,calibration,N),("exact Stage6 baseline drift",seed,scenario,policy)
            elif policy=="NEW_MISSION_ONLY_CPU_E2E_FEEDBACK":
                assert x==frozen_stage38(seed,scenario,policy,calibration,N),("frozen Stage38 policy drift",seed,scenario)
            f=x.get("stage40_full_anchored")
            if f is not None:
                assert f["source_CASPER_FULL_flags_preserved"] and f["mission_only_reranking"]
                assert f["decisions"]==f["causal_cpu_finishes"]==f["causal_e2e_network_deliveries"]==N
                assert sum(f["fallback_reasons"].values())==N
                assert f["mission_switches"]<=f["mission_decisions"]
                post_miss=f["post_mission_deadline_misses"]
            elif policy=="NEW_MISSION_ONLY_CPU_E2E_FEEDBACK":
                post_miss=x["stage37_feedback"]["post_mission_deadline_misses"]
            else:
                post_miss=round(x["post_deadline_miss_rate"]*x["post_mission_tasks"])
            assert 0<=post_miss<=x["post_mission_tasks"]
            assert abs(post_miss/x["post_mission_tasks"]-x["post_deadline_miss_rate"])<1e-10
            row=dict(seed=seed,scenario=scenario,policy=policy,
                post_mission_n=x["post_mission_tasks"],
                post_mission_deadline_misses=post_miss,
                full_mission_deadline_misses=x["mission_deadline_misses"],
                mean_latency_ms=x["mean_latency_ms"],
                mean_wait_ms=x["mean_wait_ms"],
                mission_anchored_reranker=f,
                exact_frozen_prior_policy_parity=policy in ("PRED_GREEDY","CASPER_FULL","NEW_MISSION_ONLY_CPU_E2E_FEEDBACK"))
            results.append(row)
            print("JPDC_STAGE40_CASPER_FULL_ANCHORED_DEV",json.dumps(row,sort_keys=True),flush=True)
    assert len(results)==10
    for sc in SCENARIOS:
        z=[r for r in results if r["scenario"]==sc]
        assert len({r["post_mission_n"] for r in z})==1
    return dict(status="PASS",source_seed=seed,development_only=True,
        original_source_unchanged=True,scientific_replicates=1,
        task_policy_observations=N*len(results),rows=results)

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--seed",type=int,required=True)
    parser.add_argument("--out",required=True)
    args=parser.parse_args()
    result=run(args.seed)
    f=Path(args.out);f.parent.mkdir(parents=True,exist_ok=True)
    f.write_text(json.dumps(result,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print("JPDC_STAGE40_ONE_FROZEN_FULL_ANCHORED_DEVELOPMENT_SOURCE_COMPLETE_PASS",args.seed)
