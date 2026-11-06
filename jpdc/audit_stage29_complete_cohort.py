#!/usr/bin/env python3
"""Archive-only Stage29 complete independent scientific seed cohort gate.

Require *all* four preregistered seed results; do not select positive seeds.
"""
import argparse,json,statistics
from pathlib import Path
SEEDS=(501,502,503,504)
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
POLICIES=("PRED_GREEDY","CASPER_FULL")

p=argparse.ArgumentParser()
p.add_argument("--directory",required=True)
p.add_argument("--out",required=True)
args=p.parse_args()
files=list(Path(args.directory).rglob("seed_*.json"))
byseed={}
for file in files:
    x=json.loads(file.read_text())
    seed=x["scientific_seed"]
    assert seed in SEEDS and seed not in byseed,("unexpected/duplicate scientific seed",seed)
    assert x["status"]=="PASS" and x["task_policy_records"]==48000
    assert x["scientific_units"]==1 and x["original_stage6_parity_all_arms"]
    assert len(x["rows"])==4
    entries={(r["scenario"],r["policy"]):r for r in x["rows"]}
    assert len(entries)==4
    assert set(entries)=={(s,q) for s in SCENARIOS for q in POLICIES}
    for r in x["rows"]:
        assert r["seed"]==seed and r["stage6_exact_policy_json_parity"]
    byseed[seed]=entries
assert tuple(sorted(byseed))==SEEDS,("cannot report incomplete preregistered cohort",sorted(byseed))
rows=[]
for scenario in SCENARIOS:
    for policy in POLICIES:
        items=[byseed[s][(scenario,policy)] for s in SEEDS]
        summary=dict(scenario=scenario,policy=policy,scientific_seeds=list(SEEDS),
                     scientific_replicates=4)
        for group in ("all","pre","post","post_high","post_mission","post_normal"):
            vals=[r[group]["empirical_inclusion"] for r in items]
            assert all(x is not None for x in vals)
            summary[group]=dict(seed_level_mean=statistics.mean(vals),
                seed_level_min=min(vals),seed_level_max=max(vals),
                seed_level_values=[dict(seed=s,rate=v) for s,v in zip(SEEDS,vals)],
                total_eligible=sum(r[group]["eligible"] for r in items),
                total_missed=sum(r[group]["high"]+r[group]["low"] for r in items),
                total_abstained=sum(r[group]["abstained"] for r in items))
        if scenario==SCENARIOS[0] and policy=="PRED_GREEDY":
            summary["S2_greedy_post_operational_target_pass_counts"]={
                name:sum(byseed[s][(scenario,policy)]
                         ["preregistered_S2_greedy_post_90pct_criteria"][name] for s in SEEDS)
                for name in ("all","HIGH","MISSION")}
        print("JPDC_STAGE29_FULL_COHORT_RESULT",json.dumps(summary,sort_keys=True),flush=True)
        rows.append(summary)
result=dict(status="PASS",complete_frozen_cohort=True,source_seeds=list(SEEDS),
            independent_scientific_replicates=4,dependent_task_policy_observations=192000,
            claim="frozen Stage28 q estimate empirical coverage only; not valid deterministic bound or new scheduler efficacy",
            original_e42_unchanged=True,original_stage6_all_policy_parity=True,
            output_rows=rows)
dest=Path(args.out)
dest.parent.mkdir(parents=True,exist_ok=True)
dest.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
print("JPDC_STAGE29_ALL_FOUR_SEEDS_COMPLETE_COHORT_AUDIT_PASS",flush=True)
