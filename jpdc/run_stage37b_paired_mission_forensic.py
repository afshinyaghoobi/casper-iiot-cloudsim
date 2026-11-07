#!/usr/bin/env python3
"""Stage37b retrospective paired source task-level MISSION routing forensic.

One already examined DEVELOPMENT seed91, dependent jobs not statistical reps.
PASSIVE hooks only. Do not change schedule/routing and claim confirmation.
"""
import argparse,json,math
from pathlib import Path
from independent_physical_calibration_stage3 import calibrate
from independent_physical_feedback_deadline_stage37 import simulate
from independent_network_probe_stage6 import simulate as original_stage6

SEED=91
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
POLICIES=("PRED_GREEDY","CASPER_FULL","NEW_CPU_FEEDBACK_ONLY",
          "NEW_E2E_FEEDBACK_ONLY","NEW_CPU_E2E_FEEDBACK")
N=12000
def case(seed,scenario,policy,cal):
    trace=[]
    source=simulate(seed,scenario,policy,cal,N,mission_audit_hook=trace.append)
    assert source["status"]=="PASS" and len(trace)==source["mission_tasks"]
    assert len({r["task_index"] for r in trace})==len(trace)
    assert sum(int(r["actual_deadline_miss"]) for r in trace)==source["mission_deadline_misses"]
    assert (sum(int(r["actual_deadline_miss"]) for r in trace if r["task_index"]>=10000)
            ==round(source["post_deadline_miss_rate"]*source["post_mission_tasks"]))
    for r in trace:
        assert r["task_class"]=="MISSION"
        assert (r["arrival_ms"]<=r["cpu_finished_ms"] and
            abs(r["actual_total_latency_ms"]-
                (r["actual_wait_ms"]+r["actual_cpu_ms"]+r["actual_network_ms"]))<1e-8)
        assert r["actual_deadline_miss"]==(r["actual_total_latency_ms"]>r["deadline_ms"])
        assert r["differs_from_nominal_greedy"]==(r["chosen_node"]!=r["original_greedy_node"])
    if policy in ("PRED_GREEDY","CASPER_FULL"):
        parity=dict(source);parity.pop("shadow_network_epoch")
        assert parity==original_stage6(seed,scenario,policy,cal,N)
    return source,{r["task_index"]:r for r in trace}

def diff(ref,other):
    assert ref.keys()==other.keys()
    post=[i for i in sorted(ref) if i>=10000]
    improved=[i for i in post if ref[i]["actual_deadline_miss"] and not other[i]["actual_deadline_miss"]]
    harmed=[i for i in post if not ref[i]["actual_deadline_miss"] and other[i]["actual_deadline_miss"]]
    same=[i for i in post if ref[i]["actual_deadline_miss"]==other[i]["actual_deadline_miss"]]
    changed=[i for i in post if ref[i]["chosen_node"]!=other[i]["chosen_node"]]
    return dict(total_post_mission_tasks=len(post),
                routing_changed_in_post=len(changed),
                improved_miss_task_ids=improved,
                newly_missed_task_ids=harmed,
                unchanged_miss_outcome_count=len(same),
                net_post_mission_deadline_miss_difference=len(harmed)-len(improved),
                changed_routes_by_task=[dict(task=i,baseline_node=ref[i]["chosen_node"],
                                             candidate_node=other[i]["chosen_node"],
                                             baseline_miss=ref[i]["actual_deadline_miss"],
                                             candidate_miss=other[i]["actual_deadline_miss"])
                                         for i in changed])
def run():
    cal=calibrate(SEED,80000,include_reference=True)
    assert cal["postburnin_service_ratio_count"]==70000
    out=[]
    for scenario in SCENARIOS:
        cases={}
        for policy in POLICIES:
            source,trace=case(SEED,scenario,policy,cal)
            cases[policy]=(source,trace)
        allids={p:set(t) for p,(_,t) in cases.items()}
        assert len({tuple(sorted(ids)) for ids in allids.values()})==1
        for policy in POLICIES:
            aggregate,trace=cases[policy]
            comparisons={base:diff(cases[base][1],trace)
                         for base in ("PRED_GREEDY","CASPER_FULL")}
            post=[r for r in trace.values() if r["task_index"]>=10000]
            outcome=dict(scenario=scenario,policy=policy,
                 post_mission_count=len(post),
                 post_mission_misses=sum(r["actual_deadline_miss"] for r in post),
                 post_mission_policy_reroutes_vs_own_greedy=sum(r["differs_from_nominal_greedy"] for r in post),
                 post_mission_missed_task_details=[
                     dict(task_index=r["task_index"],
                          node=r["chosen_node"],
                          nominal_greedy_node=r["original_greedy_node"],
                          actual_latency_ms=r["actual_total_latency_ms"],
                          actual_cpu_ms=r["actual_cpu_ms"],
                          actual_network_ms=r["actual_network_ms"],
                          actual_wait_ms=r["actual_wait_ms"],
                          deadline_ms=r["deadline_ms"])
                     for r in sorted(post,key=lambda z:z["task_index"])
                     if r["actual_deadline_miss"]],
                 compared_to=comparisons,
                 original_stage6_exact_parity=policy in ("PRED_GREEDY","CASPER_FULL"))
            out.append(outcome)
            print("STAGE37B_PAIRED_MISSION_FORENSIC",
                  json.dumps({k:v for k,v in outcome.items() if k!="post_mission_missed_task_details"
                    and k!="compared_to"}|{"changes_vs_greedy":comparisons["PRED_GREEDY"]["routing_changed_in_post"],
                            "new_misses_vs_greedy":len(comparisons["PRED_GREEDY"]["newly_missed_task_ids"]),
                            "saved_misses_vs_greedy":len(comparisons["PRED_GREEDY"]["improved_miss_task_ids"]),
                            "new_misses_vs_full":len(comparisons["CASPER_FULL"]["newly_missed_task_ids"]),
                            "saved_misses_vs_full":len(comparisons["CASPER_FULL"]["improved_miss_task_ids"])},
                  sort_keys=True),flush=True)
    assert len(out)==10
    return dict(status="PASS",source_seed=SEED,scientific_units=1,
                task_policy_observations=N*len(out),
                retrospective_after_stage37_outcomes=True,
                source_scheduler_physics_unchanged=True,
                results=out)
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    args=p.parse_args()
    result=run()
    dest=Path(args.out);dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(result,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print("JPDC_STAGE37B_PAIRED_MISSION_ROUTING_FORENSIC_COMPLETE_PASS")
