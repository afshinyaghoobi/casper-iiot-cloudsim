#!/usr/bin/env python3
"""Stage45 fixed eight independent source seeds901–908, frozen node-local detector."""
import argparse,json
from pathlib import Path
from independent_physical_calibration_stage3 import calibrate
from independent_physical_node_local_regime_stage44 import simulate
from independent_network_probe_stage6 import simulate as frozen_stage6
from independent_physical_mission_only_feedback_stage38 import simulate as frozen_stage38
from independent_physical_regime_gated_stage42 import simulate as frozen_stage42

SEEDS=tuple(range(901,909))
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
POLICIES=("PRED_GREEDY","CASPER_FULL","NEW_REGIME_GATED_MISSION_COMBINED",
          "NEW_MISSION_ONLY_CPU_E2E_FEEDBACK",
          "NEW_NODE_REGIME_MISSION_E2E","NEW_NODE_REGIME_MISSION_COMBINED")
N=12000

def run(seed):
    if seed not in SEEDS:raise ValueError("unregistered development seed")
    cal=calibrate(seed,80000,include_reference=True)
    assert cal["postburnin_service_ratio_count"]==70000
    rows=[]
    for scenario in SCENARIOS:
        for policy in POLICIES:
            z=simulate(seed,scenario,policy,cal,N)
            assert z["status"]=="PASS" and z["deployment_tasks"]==N
            assert z["cpu_finish_events"]==z["e2e_feedback_events"]==z["network_feedback_events"]==N
            assert z["not_cloudsim_queue_equivalent"] is True
            if policy in ("PRED_GREEDY","CASPER_FULL"):
                baseline=dict(z);baseline.pop("shadow_network_epoch")
                assert baseline==frozen_stage6(seed,scenario,policy,cal,N),(
                    "original Stage6 policy exact parity",seed,scenario,policy)
            elif policy=="NEW_MISSION_ONLY_CPU_E2E_FEEDBACK":
                assert z==frozen_stage38(seed,scenario,policy,cal,N),(
                    "old Stage38 policy exact parity",seed,scenario,policy)
            elif policy=="NEW_REGIME_GATED_MISSION_COMBINED":
                assert z==frozen_stage42(seed,scenario,policy,cal,N),(
                    "old Stage42 policy exact parity",seed,scenario,policy)
            state=z.get("stage44_node_regime")
            if state is not None:
                assert state["decisions"]==state["cpu_finish_observations"]==state["network_e2e_deliveries"]==N
                assert state["mission_network_regime_dispatches"]+state["mission_full_regime_dispatches"]==z["mission_tasks"]
                assert sum(state["network_node_evidence_counts"])==N
                assert sum(state["cpu_node_evidence_counts"])==N
                assert state["hidden_scenario_or_true_fault_mask_used_at_dispatch"] is False
                assert state["no_hard_deadline_or_conformal_certificate"] is True
                post_misses=state["post_mission_deadline_misses"]
            elif policy=="NEW_REGIME_GATED_MISSION_COMBINED":
                post_misses=z["stage42_regime"]["post_mission_deadline_misses"]
            elif policy=="NEW_MISSION_ONLY_CPU_E2E_FEEDBACK":
                post_misses=z["stage37_feedback"]["post_mission_deadline_misses"]
            else:
                post_misses=round(z["post_deadline_miss_rate"]*z["post_mission_tasks"])
            assert abs(post_misses/z["post_mission_tasks"]-z["post_deadline_miss_rate"])<1e-10
            row=dict(seed=seed,scenario=scenario,policy=policy,
                     post_mission_n=z["post_mission_tasks"],
                     post_mission_deadline_misses=post_misses,
                     full_mission_deadline_misses=z["mission_deadline_misses"],
                     mean_latency_ms=z["mean_latency_ms"],
                     mean_wait_ms=z["mean_wait_ms"],
                     node_regime=state,
                     original_source_parity=(policy in POLICIES[:4]))
            rows.append(row)
            print("JPDC_STAGE45_NODE_LOCAL_INDEPENDENT_SEED_RESULT",json.dumps(row,sort_keys=True),flush=True)
    assert len(rows)==12
    for sc in SCENARIOS:
        assert len({r["post_mission_n"] for r in rows if r["scenario"]==sc})==1
    return dict(status="PASS",scientific_seed=seed,
                independent_source_scientific_unit=1,complete_cohort_required=True,
                dependent_task_policy_observations=144000,
                no_cross_engine_or_safety_guarantee=True,rows=rows)

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--seed",type=int,required=True)
    p.add_argument("--out",required=True);a=p.parse_args()
    d=run(a.seed)
    f=Path(a.out);f.parent.mkdir(parents=True,exist_ok=True)
    f.write_text(json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print("JPDC_STAGE45_NODE_LOCAL_ONE_INDEPENDENT_SEED_COMPLETE_PASS",a.seed,flush=True)
