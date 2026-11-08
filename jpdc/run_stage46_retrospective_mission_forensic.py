#!/usr/bin/env python3
"""Stage46 POSTHOC forensic on already inspected Stage45 seeds, not new evidence."""
import argparse,json,math
from pathlib import Path
from independent_physical_calibration_stage3 import calibrate
from independent_physical_node_local_regime_stage44 import simulate
from independent_network_probe_stage6 import simulate as original_stage6
from independent_physical_mission_only_feedback_stage38 import simulate as frozen_stage38
from independent_physical_regime_gated_stage42 import simulate as frozen_stage42

SEEDS=(901,903)
SCENARIO="S3_HIDDEN_NETWORK_50LOSS"
COUNT=12000
POST=10000
POLICIES=("PRED_GREEDY","CASPER_FULL","NEW_REGIME_GATED_MISSION_COMBINED",
          "NEW_MISSION_ONLY_CPU_E2E_FEEDBACK",
          "NEW_NODE_REGIME_MISSION_E2E","NEW_NODE_REGIME_MISSION_COMBINED")
EXPECTED={901:{"CASPER_FULL":7,"NEW_NODE_REGIME_MISSION_COMBINED":3,
               "NEW_NODE_REGIME_MISSION_E2E":3},
          903:{"CASPER_FULL":15,"NEW_NODE_REGIME_MISSION_COMBINED":18,
               "NEW_NODE_REGIME_MISSION_E2E":18}}

def source(seed,policy,cal):
    rows=[]
    state=simulate(seed,SCENARIO,policy,cal,COUNT,mission_audit_hook=rows.append)
    assert state["status"]=="PASS"
    assert state["cpu_finish_events"]==state["e2e_feedback_events"]==COUNT
    assert len(rows)==state["mission_tasks"]
    index={r["task_index"]:r for r in rows}
    assert len(index)==len(rows) and all(r["task_class"]=="MISSION" for r in rows)
    assert sum(int(r["actual_deadline_miss"]) for r in rows)==state["mission_deadline_misses"]
    n=sum(i>=POST for i in index)
    assert n==state["post_mission_tasks"]
    miss=sum(int(r["actual_deadline_miss"]) for i,r in index.items() if i>=POST)
    assert abs(miss/n-state["post_deadline_miss_rate"])<1e-10
    if policy in EXPECTED[seed]:
        assert miss==EXPECTED[seed][policy],("unchanged Stage45 source outcome",seed,policy,miss)
    for i,r in index.items():
        assert i==r["task_index"] and r["cpu_finished_ms"]>=r["arrival_ms"]
        assert r["actual_cpu_ms"]>0 and r["actual_network_ms"]>0 and r["actual_wait_ms"]>=0
        assert math.isclose(r["actual_total_latency_ms"],
            r["actual_cpu_ms"]+r["actual_wait_ms"]+r["actual_network_ms"],
            rel_tol=0,abs_tol=1e-8)
        assert r["actual_deadline_miss"]==(r["actual_total_latency_ms"]>r["deadline_ms"])
    if policy in ("PRED_GREEDY","CASPER_FULL"):
        copy=dict(state);copy.pop("shadow_network_epoch")
        assert copy==original_stage6(seed,SCENARIO,policy,cal,COUNT)
    elif policy=="NEW_REGIME_GATED_MISSION_COMBINED":
        assert state==frozen_stage42(seed,SCENARIO,policy,cal,COUNT)
    elif policy=="NEW_MISSION_ONLY_CPU_E2E_FEEDBACK":
        assert state==frozen_stage38(seed,SCENARIO,policy,cal,COUNT)
    return state,index,miss,n

def forensic(baseline,candidate):
    assert baseline.keys()==candidate.keys()
    post=[i for i in sorted(baseline) if i>=POST]
    improved=[i for i in post if baseline[i]["actual_deadline_miss"] and
                                  not candidate[i]["actual_deadline_miss"]]
    harmed=[i for i in post if not baseline[i]["actual_deadline_miss"] and
                                candidate[i]["actual_deadline_miss"]]
    changed=[i for i in post if baseline[i]["chosen_node"]!=candidate[i]["chosen_node"]]
    same_node_different_wait=[i for i in post
        if baseline[i]["chosen_node"]==candidate[i]["chosen_node"] and
           abs(baseline[i]["actual_wait_ms"]-candidate[i]["actual_wait_ms"])>1e-8]
    def detail(i):
        b=baseline[i];c=candidate[i]
        return dict(task_index=i,baseline_node=b["chosen_node"],candidate_node=c["chosen_node"],
            baseline_greedy_node=b["original_greedy_node"],
            candidate_greedy_node=c["original_greedy_node"],
            baseline_deadline_ms=b["deadline_ms"],candidate_deadline_ms=c["deadline_ms"],
            baseline_miss=b["actual_deadline_miss"],candidate_miss=c["actual_deadline_miss"],
            baseline_latency_ms=b["actual_total_latency_ms"],
            candidate_latency_ms=c["actual_total_latency_ms"],
            baseline_wait_ms=b["actual_wait_ms"],candidate_wait_ms=c["actual_wait_ms"],
            baseline_cpu_ms=b["actual_cpu_ms"],candidate_cpu_ms=c["actual_cpu_ms"],
            baseline_network_ms=b["actual_network_ms"],candidate_network_ms=c["actual_network_ms"],
            baseline_nominal_ms=b["nominal_chosen_latency_ms"],
            candidate_nominal_ms=c["nominal_chosen_latency_ms"])
    assert len(harmed)-len(improved)==(
        sum(candidate[i]["actual_deadline_miss"] for i in post)-
        sum(baseline[i]["actual_deadline_miss"] for i in post))
    return dict(post_mission_count=len(post),post_route_different_nodes=len(changed),
        same_selected_node_but_different_wait=len(same_node_different_wait),
        new_missed_task_ids=harmed,avoided_missed_task_ids=improved,
        net_new_misses=len(harmed)-len(improved),
        changed_task_details=[detail(i) for i in changed],
        discordant_miss_details=[detail(i) for i in sorted(set(harmed+improved))],
        same_node_wait_different_task_ids=same_node_different_wait)

def run(seed):
    assert seed in SEEDS
    cal=calibrate(seed,80000,include_reference=True)
    assert cal["postburnin_service_ratio_count"]==70000
    raw={}
    for policy in POLICIES:
        state,task_index,miss,n=source(seed,policy,cal)
        raw[policy]=(state,task_index,miss,n)
        print("JPDC_STAGE46_SOURCE_POLICY_EXACT_PARITY",
              json.dumps(dict(seed=seed,policy=policy,
                post_mission_misses=miss,post_mission_n=n),sort_keys=True),flush=True)
    base=raw["CASPER_FULL"][1]
    pairs={}
    for policy in POLICIES:
        item=forensic(base,raw[policy][1])
        assert item["post_mission_count"]==raw[policy][3]
        if policy=="NEW_NODE_REGIME_MISSION_COMBINED":
            assert item["net_new_misses"]==(-4 if seed==901 else 3)
        pairs[policy]=item
        print("JPDC_STAGE46_POSTHOC_PAIRED_MISSION_SUMMARY",
              json.dumps(dict(seed=seed,policy=policy,
                  changed_nodes=item["post_route_different_nodes"],
                  changed_wait_on_same_node=item["same_selected_node_but_different_wait"],
                  new_misses=len(item["new_missed_task_ids"]),
                  avoided_misses=len(item["avoided_missed_task_ids"]),
                  net_new_misses=item["net_new_misses"],
                  new_ids=item["new_missed_task_ids"],
                  avoided_ids=item["avoided_missed_task_ids"]),sort_keys=True),flush=True)
    assert len({n for _,_,_,n in raw.values()})==1
    return dict(status="PASS",seed=seed,scenario=SCENARIO,
                already_examined_stage45_source_seed=True,
                independent_efficacy_replicates=0,
                dependent_task_policy_observations=COUNT*len(POLICIES),
                frozen_original_policy_parity=True,
                full_source_mission_count=len(base),
                post_mission_n=raw["CASPER_FULL"][3],
                post_mission_misses_by_policy={p:v[2] for p,v in raw.items()},
                task_paired_forensic=pairs,
                caution="Retrospective, policy-level queue interference; per-task differences are not iid or isolated causal effects.")

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--seed",type=int,required=True)
    p.add_argument("--out",required=True);a=p.parse_args()
    obj=run(a.seed)
    f=Path(a.out);f.parent.mkdir(parents=True,exist_ok=True)
    f.write_text(json.dumps(obj,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print("JPDC_STAGE46_RETROSPECTIVE_TASK_PAIRED_FORENSIC_PASS",a.seed,flush=True)
