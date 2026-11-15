#!/usr/bin/env python3
"""Stage66 original posthoc source task-discordance cohort audit; zero new seeds."""
import argparse,json
from pathlib import Path

SEEDS=(1811,1815,1816,1818)
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
EXPECTED_POST={
(1811,SCENARIOS[0]):(0,0),(1811,SCENARIOS[1]):(1,1),
(1815,SCENARIOS[0]):(1,2),(1815,SCENARIOS[1]):(4,1),
(1816,SCENARIOS[0]):(1,2),(1816,SCENARIOS[1]):(1,1),
(1818,SCENARIOS[0]):(0,0),(1818,SCENARIOS[1]):(0,0)}
EXPECTED_ALL={
(1811,SCENARIOS[0]):(2,3),(1811,SCENARIOS[1]):(3,4),
(1815,SCENARIOS[0]):(10,10),(1815,SCENARIOS[1]):(13,9),
(1816,SCENARIOS[0]):(5,7),(1816,SCENARIOS[1]):(5,6),
(1818,SCENARIOS[0]):(0,1),(1818,SCENARIOS[1]):(0,1)}

def audit(data):
    assert set(data)==set(SEEDS)
    cells=[]
    for seed in SEEDS:
        obj=data[seed]
        assert obj["status"]=="PASS" and obj["seed"]==seed
        assert obj["selected_after_known_stage65_failure"]
        assert obj["independent_new_holdout_source_n"]==0
        assert obj["original_stage65_safety_gate"]=="FAIL"
        assert len(obj["results"])==2
        for r in obj["results"]:
            sc=r["scenario"]
            assert sc in SCENARIOS and r["seed"]==seed
            assert r["original_stage65_source_aggregate_parity"]
            assert r["task_level_causal_effect_not_identifiable"]
            phases=r["phases"]
            for phase in ("PRE","POST","ALL"):
                v=phases[phase]
                assert v["mission_count"]==v["both_miss"]+v["neither_miss"]+v["full_only_miss"]+v["new_only_miss"]
                assert v["full_misses"]==v["both_miss"]+v["full_only_miss"]
                assert v["partial_misses"]==v["both_miss"]+v["new_only_miss"]
                assert v["partial_minus_full"]==v["new_only_miss"]-v["full_only_miss"]
                assert len(v["discordant_task_details"])==v["new_only_miss"]+v["full_only_miss"]
                assert len({x["task_index"] for x in v["discordant_task_details"]})==len(v["discordant_task_details"])
                for x in v["discordant_task_details"]:
                    f=x["original_full"];n=x["frozen_partial"]
                    assert f["task_index"]==n["task_index"]==x["task_index"]
                    assert f["actual_deadline_miss"]!=n["actual_deadline_miss"]
                    assert (x["label"]=="NEW_ONLY_MISS")==bool(n["actual_deadline_miss"])
                    assert x["changed_own_selected_node"]==(f["chosen_node"]!=n["chosen_node"])
                    assert x["task_index"]>=10000 if phase=="POST" else True
                    assert x["task_index"]<10000 if phase=="PRE" else True
            assert (phases["POST"]["full_misses"],phases["POST"]["partial_misses"])==EXPECTED_POST[(seed,sc)]
            assert (phases["ALL"]["full_misses"],phases["ALL"]["partial_misses"])==EXPECTED_ALL[(seed,sc)]
            assert phases["PRE"]["mission_count"]+phases["POST"]["mission_count"]==phases["ALL"]["mission_count"]
            assert phases["PRE"]["new_only_miss"]+phases["POST"]["new_only_miss"]==phases["ALL"]["new_only_miss"]
            assert phases["PRE"]["full_only_miss"]+phases["POST"]["full_only_miss"]==phases["ALL"]["full_only_miss"]
            phases_short={}
            for phase in ("PRE","POST","ALL"):
                v=phases[phase]
                phases_short[phase]={k:v[k] for k in (
                    "mission_count","full_misses","partial_misses","partial_minus_full",
                    "new_only_miss","full_only_miss","both_miss","neither_miss")}
                differences=v["discordant_task_details"]
                phases_short[phase]["discordant_own_node_changes"]=sum(
                    x["changed_own_selected_node"] for x in differences)
                phases_short[phase]["new_only_task_ids"]=[x["task_index"] for x in differences if x["label"]=="NEW_ONLY_MISS"]
                phases_short[phase]["full_only_task_ids"]=[x["task_index"] for x in differences if x["label"]=="FULL_ONLY_MISS"]
            cells.append(dict(seed=seed,scenario=sc,phases=phases_short))
    assert len(cells)==8
    return dict(status="PASS",technical="PASS",
        scientific_scope="POSTHOC spent four source seeds, no confirmatory inference",
        original_stage65_all_eight_source_holdout_safety="FAIL",
        independent_new_source_seeds=0,
        source_seed_subset_selected_after_outcomes=list(SEEDS),
        task_trajectory_outcome_difference_not_causal_effect=True,
        cells=cells)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--source-dir",required=True)
    p.add_argument("--out",required=True)
    a=p.parse_args()
    original={}
    for seed in SEEDS:
        path=Path(a.source_dir)/f"jpdc-stage66-posthoc-task-forensics-{seed}"
        assert (path/"source.json").read_bytes()==(path/"repeat.json").read_bytes()
        assert (path/"source.log").read_bytes()==(path/"repeat.log").read_bytes()
        original[seed]=json.loads((path/"source.json").read_text())
    result=audit(original)
    out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,sort_keys=True,indent=2,allow_nan=False)+"\n")
    for cell in result["cells"]:
        print("JPDC_STAGE66_POSTHOC_SOURCE_TASK_CONTRAST",json.dumps(cell,sort_keys=True))
    print("JPDC_STAGE66_ORIGINAL_PAIRED_TASK_COHORT_AUDIT_PASS")
