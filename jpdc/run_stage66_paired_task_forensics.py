#!/usr/bin/env python3
"""Stage66 retrospective paired per-task discordance on ORIGINAL spent holdout.

No new policy, no retuning; reproduce frozen Stage65 source aggregate first.
"""
import argparse
import json
import math
from collections import Counter
from pathlib import Path
from independent_physical_calibration_stage3 import calibrate
from independent_physical_partial_live_stage64 import simulate,PARTIAL_POLICY

SELECTED=(1811,1815,1816,1818)
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
POLICIES=("CASPER_FULL",PARTIAL_POLICY)
N=12000

def same(a,b):
    return math.isclose(a,b,rel_tol=1e-11,abs_tol=1e-8)

def run(seed,original_file):
    if seed not in SELECTED:raise ValueError("posthoc seed not in prereg")
    original=json.loads(Path(original_file).read_text())
    assert original["status"]=="PASS" and original["source_seed"]==seed
    assert original["source_task_observations"]==72000 and len(original["rows"])==6
    old={(r["scenario"],r["policy"]):r for r in original["rows"]}
    cal=calibrate(seed,80000,include_reference=True)
    assert cal["status"]=="PASS" and cal["postburnin_service_ratio_count"]==70000
    output=[]
    for sc in SCENARIOS:
        paired={}
        for policy in POLICIES:
            traces=[]
            result=simulate(seed,sc,policy,cal,N,mission_audit_hook=traces.append)
            assert result["status"]=="PASS"
            assert result["deployment_tasks"]==N
            assert result["cpu_finish_events"]==result["e2e_feedback_events"]==N
            expected=old[(sc,policy)]
            assert expected["post_mission_n"]==result["post_mission_tasks"]
            miss=sum(int(t["actual_deadline_miss"]) for t in traces)
            postmiss=sum(int(t["actual_deadline_miss"]) for t in traces if t["task_index"]>=10000)
            assert miss==expected["all_mission_deadline_misses"]==result["mission_deadline_misses"]
            assert postmiss==expected["post_mission_deadline_misses"]
            assert same(expected["mean_latency_ms"],result["mean_latency_ms"])
            assert same(expected["mean_wait_ms"],result["mean_wait_ms"])
            assert len(traces)==result["mission_tasks"]
            assert len({t["task_index"] for t in traces})==len(traces)
            if policy==PARTIAL_POLICY:
                assert result["stage64_live_partial"]==expected["candidate"]
            else:assert expected["candidate"] is None
            paired[policy]={x["task_index"]:x for x in traces}
        full=paired["CASPER_FULL"]
        new=paired[PARTIAL_POLICY]
        assert set(full)==set(new)
        phases={}
        for phase,filter_fn in (("PRE",lambda i:i<10000),
                                ("POST",lambda i:i>=10000),
                                ("ALL",lambda i:True)):
            ids=sorted(i for i in full if filter_fn(i))
            labels=Counter()
            mismatches=[]
            for i in ids:
                f,n=full[i],new[i]
                assert f["task_index"]==n["task_index"]==i
                assert f["task_class"]==n["task_class"]=="MISSION"
                assert same(f["arrival_ms"],n["arrival_ms"])
                assert same(f["deadline_ms"],n["deadline_ms"])
                fm=bool(f["actual_deadline_miss"])
                nm=bool(n["actual_deadline_miss"])
                label=("BOTH_MISS" if fm and nm else "FULL_ONLY_MISS" if fm else
                       "NEW_ONLY_MISS" if nm else "NEITHER_MISS")
                labels[label]+=1
                if fm!=nm:
                    keys=("task_index","chosen_node","original_greedy_node",
                          "deadline_ms","nominal_chosen_latency_ms","actual_cpu_ms",
                          "actual_wait_ms","actual_network_ms","actual_total_latency_ms",
                          "actual_deadline_miss","arrival_ms")
                    mismatches.append(dict(task_index=i,label=label,
                        changed_own_selected_node=f["chosen_node"]!=n["chosen_node"],
                        original_full={k:f[k] for k in keys},
                        frozen_partial={k:n[k] for k in keys}))
            assert sum(labels.values())==len(ids)
            assert sum(int(full[i]["actual_deadline_miss"]) for i in ids)==(
                labels["BOTH_MISS"]+labels["FULL_ONLY_MISS"])
            assert sum(int(new[i]["actual_deadline_miss"]) for i in ids)==(
                labels["BOTH_MISS"]+labels["NEW_ONLY_MISS"])
            assert len(mismatches)==labels["NEW_ONLY_MISS"]+labels["FULL_ONLY_MISS"]
            phases[phase]=dict(mission_count=len(ids),
                both_miss=labels["BOTH_MISS"],neither_miss=labels["NEITHER_MISS"],
                full_only_miss=labels["FULL_ONLY_MISS"],
                new_only_miss=labels["NEW_ONLY_MISS"],
                full_misses=labels["BOTH_MISS"]+labels["FULL_ONLY_MISS"],
                partial_misses=labels["BOTH_MISS"]+labels["NEW_ONLY_MISS"],
                partial_minus_full=labels["NEW_ONLY_MISS"]-labels["FULL_ONLY_MISS"],
                discordant_task_details=mismatches)
        assert phases["PRE"]["mission_count"]+phases["POST"]["mission_count"]==phases["ALL"]["mission_count"]
        for name in ("full_misses","partial_misses","new_only_miss","full_only_miss"):
            assert phases["PRE"][name]+phases["POST"][name]==phases["ALL"][name]
        assert phases["POST"]["full_misses"]==old[(sc,"CASPER_FULL")]["post_mission_deadline_misses"]
        assert phases["POST"]["partial_misses"]==old[(sc,PARTIAL_POLICY)]["post_mission_deadline_misses"]
        assert phases["ALL"]["full_misses"]==old[(sc,"CASPER_FULL")]["all_mission_deadline_misses"]
        assert phases["ALL"]["partial_misses"]==old[(sc,PARTIAL_POLICY)]["all_mission_deadline_misses"]
        result=dict(seed=seed,scenario=sc,posthoc_selected=True,phases=phases,
                    original_stage65_source_aggregate_parity=True,
                    original_method_unchanged=True,
                    task_level_causal_effect_not_identifiable=True)
        output.append(result)
        print("JPDC_STAGE66_ORIGINAL_PAIRED_FORENSICS",json.dumps(result,sort_keys=True),flush=True)
    return dict(status="PASS",seed=seed,selected_after_known_stage65_failure=True,
                independent_new_holdout_source_n=0,original_stage65_safety_gate="FAIL",
                observed_alternate_policy_trajectory_not_single_task_counterfactual=True,
                results=output)

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--seed",type=int,required=True)
    ap.add_argument("--original-file",required=True)
    ap.add_argument("--out",required=True)
    a=ap.parse_args()
    obj=run(a.seed,a.original_file)
    p=Path(a.out);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print("JPDC_STAGE66_ORIGINAL_TASK_FORENSIC_PARITY_PASS",a.seed,flush=True)
