#!/usr/bin/env python3
"""Stage43 eight fixed source independent seeds, frozen Stage42 regime selector."""
import argparse,json
from pathlib import Path
from independent_physical_calibration_stage3 import calibrate
from independent_physical_regime_gated_stage42 import simulate
from independent_network_probe_stage6 import simulate as original_stage6
from independent_physical_mission_only_feedback_stage38 import simulate as frozen_stage38

SEEDS=tuple(range(801,809))
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
POLICIES=("PRED_GREEDY","CASPER_FULL","NEW_MISSION_ONLY_CPU_E2E_FEEDBACK",
          "NEW_REGIME_GATED_MISSION_E2E",
          "NEW_REGIME_GATED_MISSION_COMBINED")
N=12000
def run(seed):
    if seed not in SEEDS:raise ValueError("unregistered prospective development seed")
    cal=calibrate(seed,80000,include_reference=True)
    assert cal["postburnin_service_ratio_count"]==70000
    rows=[]
    for sc in SCENARIOS:
        for policy in POLICIES:
            z=simulate(seed,sc,policy,cal,N)
            assert z["status"]=="PASS" and z["deployment_tasks"]==N
            assert z["cpu_finish_events"]==z["e2e_feedback_events"]==z["network_feedback_events"]==N
            if policy in ("PRED_GREEDY","CASPER_FULL"):
                orig=dict(z);orig.pop("shadow_network_epoch")
                assert orig==original_stage6(seed,sc,policy,cal,N),("original Stage6 source changed",seed,sc,policy)
            if policy=="NEW_MISSION_ONLY_CPU_E2E_FEEDBACK":
                assert z==frozen_stage38(seed,sc,policy,cal,N),("Stage38 frozen source drift",seed,sc)
            state=z.get("stage42_regime")
            if state is not None:
                assert state["regime_decisions"]==state["cpu_finish_observations"]==state["network_e2e_deliveries"]==N
                assert state["mission_network_regime_dispatches"]+state["mission_full_regime_dispatches"]==z["mission_tasks"]
                assert not state["conditional_safety_certificate"]
                feedback=z["stage37_feedback"]
                assert feedback["decisions"]==feedback["causal_cpu_finishes"]==N
                assert feedback["budget_violations"]==0
                missed=state["post_mission_deadline_misses"]
            elif policy=="NEW_MISSION_ONLY_CPU_E2E_FEEDBACK":
                missed=z["stage37_feedback"]["post_mission_deadline_misses"]
            else:
                missed=round(z["post_deadline_miss_rate"]*z["post_mission_tasks"])
            assert abs(missed/z["post_mission_tasks"]-z["post_deadline_miss_rate"])<1e-10
            row=dict(seed=seed,scenario=sc,policy=policy,
                post_mission_n=z["post_mission_tasks"],post_mission_deadline_misses=missed,
                all_mission_deadline_misses=z["mission_deadline_misses"],
                mean_latency_ms=z["mean_latency_ms"],mean_wait_ms=z["mean_wait_ms"],
                health_alarms=z["health_alarm_transitions"],
                source_no_cloudsim_parity_claim=z["not_cloudsim_queue_equivalent"],
                regime=state)
            rows.append(row)
            print("JPDC_STAGE43_INDEPENDENT_SOURCE_REGIME_RESULT",json.dumps(row,sort_keys=True),flush=True)
    assert len(rows)==10
    for sc in SCENARIOS:
        assert len({x["post_mission_n"] for x in rows if x["scenario"]==sc})==1
    return dict(status="PASS",scientific_seed=seed,independent_science_unit=1,
                task_policy_dependent_observations=120000,
                original_source_parity=True,regime_is_not_safety_certificate=True,
                rows=rows)

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--seed",type=int,required=True)
    p.add_argument("--out",required=True);a=p.parse_args()
    data=run(a.seed)
    f=Path(a.out);f.parent.mkdir(parents=True,exist_ok=True)
    f.write_text(json.dumps(data,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print("JPDC_STAGE43_ONE_FIXED_INDEPENDENT_SOURCE_SEED_COMPLETE_PASS",a.seed,flush=True)
