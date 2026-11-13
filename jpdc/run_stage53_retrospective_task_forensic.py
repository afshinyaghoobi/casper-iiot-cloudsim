#!/usr/bin/env python3
"""Stage53 posthoc, source task-ID-matched mechanism diagnostic, NOT independent science."""
import argparse,json,math
from pathlib import Path
from independent_physical_calibration_stage3 import calibrate
from independent_physical_queue_baseline_stage51 import simulate

SEED=1107
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
POLICIES=("PRED_GREEDY","CASPER_FULL","QUEUE_PRESSURE_05","QUEUE_PRESSURE_E2E_05")
EXPECTED={"S2_HIDDEN_COMPUTE_40LOSS":(6,1,5,5),
          "S3_HIDDEN_NETWORK_50LOSS":(1,1,0,2)}
N=12000
AFTER=10000
TOL=1e-8

def task_details(rows,task_id):
    x=rows[task_id]
    return dict(task_id=task_id,chosen_node=x["chosen_node"],
                original_greedy_node=x["original_greedy_node"],
                arrival_ms=x["arrival_ms"],deadline_ms=x["deadline_ms"],
                predicted_latency_ms=x["nominal_chosen_latency_ms"],
                cpu_ms=x["actual_cpu_ms"],wait_ms=x["actual_wait_ms"],
                network_ms=x["actual_network_ms"],
                latency_ms=x["actual_total_latency_ms"],
                missed=x["actual_deadline_miss"])

def compare(a,b):
    ids=set(a)
    assert ids==set(b)
    saved=sorted(i for i in ids if a[i]["actual_deadline_miss"] and not b[i]["actual_deadline_miss"])
    newly_late=sorted(i for i in ids if not a[i]["actual_deadline_miss"] and b[i]["actual_deadline_miss"])
    different_nodes=sorted(i for i in ids if a[i]["chosen_node"]!=b[i]["chosen_node"])
    assert sum(b[i]["actual_deadline_miss"] for i in ids)-sum(a[i]["actual_deadline_miss"] for i in ids)==len(newly_late)-len(saved)
    selected_ids=sorted(set(saved+newly_late))
    return dict(saved_count=len(saved),new_count=len(newly_late),
        saved_ids=saved,new_ids=newly_late,
        post_mission_different_node_count=len(different_nodes),
        selected_task_details=[dict(task_id=i,reference=task_details(a,i),
                                    candidate=task_details(b,i)) for i in selected_ids],
        paired_outcome_not_individual_causal_proof=True)

def run(original_source):
    assert original_source["status"]=="PASS" and original_source["seed_index"]==SEED
    assert len(original_source["rows"])==len(SCENARIOS)*len(POLICIES)
    original={(x["scenario"],x["policy"]):x for x in original_source["rows"]}
    assert len(original)==8
    cal=calibrate(SEED,80000,include_reference=True)
    assert cal["status"]=="PASS"
    summaries=[]
    for sc in SCENARIOS:
        histories={}
        totals=[]
        for policy in POLICIES:
            trace=[]
            result=simulate(SEED,sc,policy,cal,N,mission_audit_hook=trace.append)
            assert result["status"]=="PASS" and result["deployment_tasks"]==N
            assert result["cpu_finish_events"]==result["e2e_feedback_events"]==N
            obj=original[(sc,policy)]
            assert abs(result["mean_latency_ms"]-obj["mean_latency_ms"])<=TOL
            assert abs(result["mean_wait_ms"]-obj["mean_wait_ms"])<=TOL
            assert result["mission_deadline_misses"]==obj["all_mission_deadline_misses"]
            assert result["post_mission_tasks"]==obj["post_mission_n"]==96
            post={x["task_index"]:x for x in trace if x["task_index"]>=AFTER}
            assert len(post)==96 and len({x["task_index"] for x in trace})==len(trace)
            assert sum(int(x["actual_deadline_miss"]) for x in post.values())==obj["post_mission_deadline_misses"]
            totals.append(len([x for x in post.values() if x["actual_deadline_miss"]]))
            histories[policy]=post
        assert tuple(totals)==EXPECTED[sc],(sc,totals)
        ids=set(histories["CASPER_FULL"])
        for policy in POLICIES:
            assert set(histories[policy])==ids
            for task_id in ids:
                ref=histories["CASPER_FULL"][task_id]
                x=histories[policy][task_id]
                assert x["task_class"]=="MISSION" and ref["task_class"]=="MISSION"
                assert math.isclose(ref["arrival_ms"],x["arrival_ms"],abs_tol=TOL)
                assert math.isclose(ref["deadline_ms"],x["deadline_ms"],abs_tol=TOL)
                assert abs((x["actual_cpu_ms"]+x["actual_wait_ms"]+x["actual_network_ms"])-
                           x["actual_total_latency_ms"])<=TOL
        results={}
        for policy in POLICIES:
            if policy=="CASPER_FULL":continue
            results[f"{policy}_vs_FULL"]=compare(histories["CASPER_FULL"],histories[policy])
        results["QUEUE_E2E_vs_QUEUE_ONLY"]=compare(histories["QUEUE_PRESSURE_05"],
                                                   histories["QUEUE_PRESSURE_E2E_05"])
        summaries.append(dict(scenario=sc,scientific_seed=SEED,
                              post_mission_n=96,policy_names=POLICIES,
                              policy_post_mission_misses=dict(zip(POLICIES,totals)),
                              comparisons=results))
    return dict(status="PASS",analysis="POSTHOC already spent holdout seed1107",
                independent_scientific_n_added=0,no_new_policy_efficacy_claim=True,
                original_source_stage52_untouched=True,
                simulator="isolated Python strict FCFS; no original Java parity",scenarios=summaries)

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--stage52-original-seed-file",required=True)
    parser.add_argument("--out",required=True)
    a=parser.parse_args()
    src=json.loads(Path(a.stage52_original_seed_file).read_text())
    obj=run(src)
    p=Path(a.out)
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,sort_keys=True,indent=2,allow_nan=False)+"\n")
    for row in obj["scenarios"]:
        for key,value in row["comparisons"].items():
            print("JPDC_STAGE53_POSTHOC_TASK_ID_PAIR",row["scenario"],key,
                  json.dumps({k:v for k,v in value.items() if k!="selected_task_details"},sort_keys=True))
    print("JPDC_STAGE53_RETROSPECTIVE_SOURCE_RECONCILIATION_PASS")
