#!/usr/bin/env python3
"""Stage16 seed-level paired aggregate; immutable per-seed JSON only, no simulation."""
import argparse,json,math,random,statistics
from collections import defaultdict
from pathlib import Path

SEEDS=tuple(range(301,309))
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
POLICIES=("CASPER_FULL","PRED_GREEDY","NEW_FRESHNESS_GUARDED")

def sign_p(deltas):
    nz=[x for x in deltas if x!=0]
    n=len(nz);pos=sum(x>0 for x in nz);neg=n-pos
    return min(1.0,2*sum(math.comb(n,k) for k in range(min(pos,neg)+1))/(2**n)) if n else 1.

def ci(diffs):
    rng=random.Random(16016)
    av=[]
    for _ in range(10000):
        sample=[diffs[rng.randrange(len(diffs))] for _ in range(len(diffs))]
        av.append(statistics.mean(sample))
    av.sort()
    return [av[249],av[9749]]

def run(root):
    found=list(Path(root).rglob("seed.json"))
    byseed={}
    for f in found:
        obj=json.loads(f.read_text())
        seed=obj["scientific_seed_index"]
        if seed in byseed:raise AssertionError(("duplicate seed",seed))
        if seed not in SEEDS or obj["status"]!="PASS" or len(obj["rows"])!=6:
            raise AssertionError(("invalid seed result",f))
        byseed[seed]=obj
    assert tuple(sorted(byseed))==SEEDS,("missing preregistered seed results",sorted(byseed))
    records={}
    for seed in SEEDS:
        for row in byseed[seed]["rows"]:
            key=(seed,row["scenario"],row["policy"])
            assert key not in records
            assert row["total_misses"]==row["pre_misses"]+row["post_misses"]
            records[key]=row
    assert len(records)==8*2*3
    summary=[]
    for scenario in SCENARIOS:
        for baseline in ("CASPER_FULL","PRED_GREEDY"):
            g=[records[(s,scenario,"NEW_FRESHNESS_GUARDED")]["total_misses"] for s in SEEDS]
            b=[records[(s,scenario,baseline)]["total_misses"] for s in SEEDS]
            delta=[x-y for x,y in zip(g,b)]
            item=dict(scenario=scenario,comparison="GUARDED_minus_"+baseline,
                      seed_indices=list(SEEDS),guarded_misses=g,baseline_misses=b,
                      seed_paired_miss_differences=delta,
                      mean_paired_miss_difference=statistics.mean(delta),
                      sign_test_two_sided=sign_p(delta),
                      nonzero_pairs=sum(d!=0 for d in delta),ties=sum(d==0 for d in delta),
                      paired_seed_bootstrap_percentile_95=ci(delta))
            summary.append(item)
            print("STAGE16_FROZEN_PAIRED_SEED_SUMMARY",json.dumps(item,sort_keys=True))
    return dict(status="PASS",scientific_units=8,scenarios=list(SCENARIOS),
                registered_seeds=list(SEEDS),no_task_level_pseudoreplication=True,
                predeclared_primary="S3 GUARDED minus CASPER_FULL all MISSION misses",
                summary=summary)
if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--root",required=True);parser.add_argument("--out",required=True)
    a=parser.parse_args()
    x=run(a.root)
    dest=Path(a.out);dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(x,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print("JPDC_STAGE16_EIGHT_INDEPENDENT_SEEDS_PAIRED_AGGREGATE_PASS")
