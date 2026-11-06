#!/usr/bin/env python3
"""Stage29 preregistered four independent source seed validation of frozen Stage28.

NO estimator tuning, physical policy modifications, or target-coverage guarantee.
"""
import argparse,json,math
from pathlib import Path
from independent_physical_calibration_stage3 import calibrate
from independent_physical_cpu_nonnetwork_trace_stage27 import simulate
from independent_network_probe_stage6 import simulate as original_stage6
from replay_stage28_archived_full_q import replay

SEEDS=(501,502,503,504)
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
POLICIES=("PRED_GREEDY","CASPER_FULL")
TASKS=12000

def selection(items,key):
    matching=[x for x in items if x["group"]==key]
    if len(matching)!=1:raise AssertionError(("missing fixed subgroup",key))
    return matching[0]

def evaluate(seed):
    if seed not in SEEDS:raise ValueError("unregistered scientific seed")
    cal=calibrate(seed,80000,include_reference=True)
    assert cal["postburnin_service_ratio_count"]==70000
    rows=[]
    for scenario in SCENARIOS:
        for policy in POLICIES:
            labels=[]
            result=simulate(seed,scenario,policy,cal,TASKS,queue_trace_hook=labels.append)
            frozen=dict(result)
            frozen.pop("shadow_network_epoch")
            assert frozen==original_stage6(seed,scenario,policy,cal,TASKS),(seed,scenario,policy,"original Stage6 parity")
            assert len(labels)==TASKS and sorted(r["task_index"] for r in labels)==list(range(TASKS))
            for t in labels:
                assert t["arrival_ms"]<=t["actual_start_ms"]<=t["delivered_cpu_finish_ms"]
                assert abs(t["signed_nonnetwork_residual_ms"]-
                    (t["signed_wait_residual_ms"]+t["signed_cpu_residual_ms"]))<1e-8
                assert t["queue_model_context"]=="native_python_strict_fcfs_vq_telemetry50ms"
            groups=replay(labels)
            overall=selection(groups,["all","all"])
            pre=selection(groups,["phase","pre"])
            post=selection(groups,["phase","post"])
            high=selection(groups,["phase_class","post","HIGH"])
            mission=selection(groups,["phase_class","post","MISSION"])
            normal=selection(groups,["phase_class","post","NORMAL"])
            assert overall["n"]==TASKS and pre["n"]==10000 and post["n"]==2000
            assert high["n"]+mission["n"]+normal["n"]==post["n"]
            assert overall["eligible"]==pre["eligible"]+post["eligible"]
            assert all(g["eligible"]==g["covered"]+g["low"]+g["high"]
                       for g in (overall,pre,post,high,mission,normal))
            assert all(g["eligible"]>0 for g in (pre,post,high,mission,normal))
            row=dict(seed=seed,scenario=scenario,policy=policy,
                     all=overall,pre=pre,post=post,post_high=high,
                     post_mission=mission,post_normal=normal,
                     stage6_exact_policy_json_parity=True,
                     scientific_scope="strict Python FCFS source only, frozen descriptive Stage28 intervals")
            if scenario==SCENARIOS[0] and policy=="PRED_GREEDY":
                row["preregistered_S2_greedy_post_90pct_criteria"]={
                    "all":post["empirical_inclusion"]>=.90,
                    "HIGH":high["empirical_inclusion"]>=.90,
                    "MISSION":mission["empirical_inclusion"]>=.90}
            rows.append(row)
            print("JPDC_STAGE29_INDEPENDENT_SEED_ROW",json.dumps(row,sort_keys=True),flush=True)
    assert len(rows)==4
    return dict(status="PASS",scientific_seed=seed,scientific_units=1,
                original_stage6_parity_all_arms=True,task_policy_records=48000,
                calibration_source="Stage3 native seed-specific 80k; original full-q Stage28 fixed",
                uncertainty_guarantee=False,rows=rows)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--seed",required=True,type=int)
    p.add_argument("--out",required=True)
    a=p.parse_args()
    out=evaluate(a.seed)
    dest=Path(a.out);dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(out,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print("JPDC_STAGE29_FROZEN_INDEPENDENT_SOURCE_SEED_PASS",a.seed,flush=True)
