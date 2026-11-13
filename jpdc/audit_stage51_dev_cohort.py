#!/usr/bin/env python3
"""Stage51 all-or-nothing DEV-only descriptive cohort audit. No p-value claims."""
import argparse
import json
from pathlib import Path

SEEDS=(101,102)
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
POLICIES=("PRED_GREEDY","CASPER_FULL","QUEUE_PRESSURE_05","QUEUE_PRESSURE_E2E_05")
TASKS=12000

def summarize(sources):
    assert set(sources)==set(SEEDS),("missing or duplicated scientific seeds",set(sources))
    data={}
    for seed in SEEDS:
        src=sources[seed]
        assert src["status"]=="PASS" and src["seed_index"]==seed
        assert src["source_task_observations"]==TASKS*len(SCENARIOS)*len(POLICIES)
        assert src["methods_not_authors_original_DFAQ_LB"] is True
        rows=src["rows"]
        assert len(rows)==len(SCENARIOS)*len(POLICIES)
        for r in rows:
            assert r["seed"]==seed and r["scenario"] in SCENARIOS and r["policy"] in POLICIES
            key=(seed,r["scenario"],r["policy"])
            assert key not in data
            assert 0<=r["post_mission_deadline_misses"]<=r["post_mission_n"]
            data[key]=r
    assert len(data)==len(SEEDS)*len(SCENARIOS)*len(POLICIES)
    cohort=[]
    for scenario in SCENARIOS:
        for policy in POLICIES:
            rows=[data[(seed,scenario,policy)] for seed in SEEDS]
            counts=[x["post_mission_deadline_misses"] for x in rows]
            denominators=[x["post_mission_n"] for x in rows]
            assert denominators==[data[(seed,scenario,"PRED_GREEDY")]["post_mission_n"] for seed in SEEDS]
            by_seed=[dict(seed=seed,post_mission_n=denominators[i],
                          deadline_misses=counts[i],
                          delta_vs_casper_full=counts[i]-data[(seed,scenario,"CASPER_FULL")]["post_mission_deadline_misses"],
                          delta_vs_pred_greedy=counts[i]-data[(seed,scenario,"PRED_GREEDY")]["post_mission_deadline_misses"],
                          changed_dispatches=(rows[i]["baseline"] or {}).get("switches_vs_pred_greedy"))
                     for i,seed in enumerate(SEEDS)]
            cohort.append(dict(scenario=scenario,policy=policy,
                               pooled_descriptive_misses=sum(counts),
                               pooled_descriptive_tasks=sum(denominators),
                               per_source_seed=by_seed))
    return dict(status="PASS",study="Stage51 DEV, not heldout",
                scientific_independent_source_seed_n=2,
                dependent_task_policy_observations=TASKS*len(SEEDS)*len(SCENARIOS)*len(POLICIES),
                no_significance_claim=True,
                author_original_DFAQ_LB_reproduced=False,
                original_java_cloudsim_queue_parity="STILL FAILED",
                rows=cohort)

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--seed101",required=True)
    ap.add_argument("--seed102",required=True)
    ap.add_argument("--out",required=True)
    a=ap.parse_args()
    result=summarize({101:json.loads(Path(a.seed101).read_text()),
                      102:json.loads(Path(a.seed102).read_text())})
    p=Path(a.out)
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+"\n")
    for row in result["rows"]:
        print("JPDC_STAGE51_DEV_DESCRIPTIVE_SUMMARY",json.dumps(row,sort_keys=True))
    print("JPDC_STAGE51_DEV_ALL_OR_NOTHING_AUDIT_PASS")
