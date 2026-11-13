#!/usr/bin/env python3
"""Stage58 original DEV source-cohort descriptive audit, no inferential claims."""
import argparse
import json
from pathlib import Path

SEEDS=(1311,1312)
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
METHODS=("PRED_GREEDY","CASPER_FULL","LEAST_INFLIGHT","CAPACITY_WEIGHTED_LEAST_INFLIGHT")

def audit(src):
    assert set(src)==set(SEEDS)
    lookup={}
    for seed in SEEDS:
        obj=src[seed]
        assert obj["status"]=="PASS" and obj["seed_index"]==seed
        assert obj["source_task_observations"]==96000
        assert obj["methods_not_authors_original_DFAQ_LB"] is True
        assert len(obj["rows"])==8
        for r in obj["rows"]:
            key=(seed,r["scenario"],r["policy"])
            assert r["seed"]==seed and r["scenario"] in SCENARIOS and r["policy"] in METHODS
            assert key not in lookup
            assert 0<=r["post_mission_deadline_misses"]<=r["post_mission_n"]
            if r["policy"] in METHODS[2:]:
                assert r["baseline"] is not None and r["baseline"]["policy"]==r["policy"]
                assert r["baseline"]["authors_original_DFAQ_LB_reproduced"] is False
                assert r["baseline"]["decisions"]==12000
            else:
                assert r["baseline"] is None
            lookup[key]=r
    assert len(lookup)==16
    rows=[]
    for sc in SCENARIOS:
        for seed in SEEDS:
            assert len({lookup[(seed,sc,p)]["post_mission_n"] for p in METHODS})==1
        for p in METHODS:
            data=[lookup[(seed,sc,p)] for seed in SEEDS]
            full=[lookup[(seed,sc,"CASPER_FULL")] for seed in SEEDS]
            greedy=[lookup[(seed,sc,"PRED_GREEDY")] for seed in SEEDS]
            rows.append(dict(scenario=sc,policy=p,
                post_mission_n=sum(x["post_mission_n"] for x in data),
                post_mission_misses=sum(x["post_mission_deadline_misses"] for x in data),
                per_seed=[dict(seed=seed,post_n=data[i]["post_mission_n"],
                    misses=data[i]["post_mission_deadline_misses"],
                    delta_vs_full=data[i]["post_mission_deadline_misses"]-full[i]["post_mission_deadline_misses"],
                    delta_vs_greedy=data[i]["post_mission_deadline_misses"]-greedy[i]["post_mission_deadline_misses"],
                    switches=(data[i]["baseline"] or {}).get("switches_vs_same_state_greedy"),
                    all_mission_misses=data[i]["all_mission_deadline_misses"],
                    mean_latency_ms=data[i]["mean_latency_ms"],
                    mean_wait_ms=data[i]["mean_wait_ms"]) for i,seed in enumerate(SEEDS)]))
    return dict(status="PASS",study="DEV ONLY, no separate untouched validation",
         scientific_independent_source_seed_n=2,
         independent_holdout_n=0,
         dependent_policy_task_observations=192000,
         original_DFAQ_LB_reproduced=False,
         Stage57_MCT_alias_reused_as_independent=False,
         Java_Python_queue_parity_still_failed=True,
         no_significance_claim=True,rows=rows)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--source-dir",required=True)
    p.add_argument("--out",required=True)
    a=p.parse_args()
    d=Path(a.source_dir)
    source={}
    for seed in SEEDS:
        folder=d/f"jpdc-stage58-classic-load-seed-{seed}"
        f=folder/"source.json"
        assert f.is_file(),f
        assert f.read_bytes()==(folder/"repeat.json").read_bytes()
        assert (folder/"source.log").read_bytes()==(folder/"repeat.log").read_bytes()
        source[seed]=json.loads(f.read_text())
    out=audit(source)
    p=Path(a.out)
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(out,sort_keys=True,indent=2,allow_nan=False)+"\n")
    for r in out["rows"]:
        print("JPDC_STAGE58_DEV_COHORT",json.dumps(r,sort_keys=True))
    print("JPDC_STAGE58_DEV_COHORT_AUDIT_PASS")
