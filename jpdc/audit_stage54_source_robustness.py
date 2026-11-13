#!/usr/bin/env python3
"""Stage54 posthoc seed-level multiplicity, LOO and bootstrap robustness.

No new physical experiment, no independent holdout, no CASPER policy changes.
"""
import argparse
import json
import math
import random
from pathlib import Path

SEEDS = tuple(range(1101, 1109))
SCENARIOS = ("S2_HIDDEN_COMPUTE_40LOSS", "S3_HIDDEN_NETWORK_50LOSS")
METHODS = ("QUEUE_PRESSURE_05", "QUEUE_PRESSURE_E2E_05")
REFERENCE = "CASPER_FULL"
BOOTSTRAPS = 20000
RNG_SEED = 20261113

def exact_two_sided_sign(d):
    v=[x for x in d if x]
    if not v:
        return 1.0
    n=len(v)
    npos=sum(x>0 for x in v)
    lo=min(npos,n-npos)
    return min(1.0, 2.0*sum(math.comb(n,i) for i in range(lo+1))/2**n)

def holm_adjust(pvalues):
    n=len(pvalues)
    ordered=sorted(range(n),key=lambda i:(pvalues[i],i))
    out=[None]*n
    prior=0.0
    for rank,i in enumerate(ordered):
        prior=max(prior,min(1.0,(n-rank)*pvalues[i]))
        out[i]=prior
    return out

def percentile_nearest_rank(data,frac):
    if not data or not 0 < frac <= 1:
        raise ValueError("bad quantile")
    ordered=sorted(data)
    return ordered[math.ceil(frac*len(ordered))-1]

def analyze(source):
    assert source["status"]=="PASS", "Stage52 original audit must have passed"
    assert source["scientific_independent_source_seed_n"]==8
    assert tuple(source["source_seeds"])==SEEDS
    assert source["dependent_task_policy_observations"]==768000
    summaries={(s["scenario"],s["policy"]):s for s in source["source_summaries"]}
    assert len(summaries)==8, "original four policies in both scenarios"
    for sc in SCENARIOS:
        per_refs=summaries[(sc,REFERENCE)]["per_source"]
        assert [v["seed"] for v in per_refs]==list(SEEDS)
        assert sum(v["post_n"] for v in per_refs)==739
        for method in METHODS:
            a=summaries[(sc,method)]
            assert [v["seed"] for v in a["per_source"]]==list(SEEDS)
            assert [v["post_n"] for v in a["per_source"]]==[v["post_n"] for v in per_refs]
            assert a["misses"]==sum(v["post_misses"] for v in a["per_source"])
            assert a["post_mission_n"]==739
            delta=[v["post_misses"]-ref["post_misses"]
                   for v,ref in zip(a["per_source"],per_refs)]
            assert a["paired_delta_vs_full"]==delta
            assert math.isclose(exact_two_sided_sign(delta),
                                a["exact_sign_vs_full"]["p_two_sided"],abs_tol=1e-12)
    rng=random.Random(RNG_SEED)
    comparisons=[]
    # Exact protocol order; no posthoc favorable sorting or selection.
    for sc in SCENARIOS:
        for method in METHODS:
            s=summaries[(sc,method)]
            delta=s["paired_delta_vs_full"]
            mean=sum(delta)/len(delta)
            loo=[dict(omitted_seed=seed,mean_delta=sum(delta[:i]+delta[i+1:])/7)
                 for i,seed in enumerate(SEEDS)]
            samples=[]
            for _ in range(BOOTSTRAPS):
                samples.append(sum(delta[rng.randrange(8)] for _ in range(8))/8)
            comparison=dict(scenario=sc,method=method,reference=REFERENCE,
                            per_seed_delta_misses=delta,
                            source_n=8,pooled_dependent_tasks=s["post_mission_n"],
                            mean_delta_misses_per_seed=mean,
                            pooled_delta_misses=sum(delta),
                            sign_p_unadjusted=exact_two_sided_sign(delta),
                            leave_one_source_out=loo,
                            loo_min_mean_delta=min(v["mean_delta"] for v in loo),
                            loo_max_mean_delta=max(v["mean_delta"] for v in loo),
                            loo_effect_direction_reversal_count=sum(
                                (v["mean_delta"]*mean < 0) for v in loo),
                            bootstrap_B=BOOTSTRAPS,
                            bootstrap_2_5_pct_mean_delta=percentile_nearest_rank(samples,.025),
                            bootstrap_97_5_pct_mean_delta=percentile_nearest_rank(samples,.975))
            comparisons.append(comparison)
    adj=holm_adjust([x["sign_p_unadjusted"] for x in comparisons])
    for x,p in zip(comparisons,adj):
        x["holm_four_contrast_posthoc_adjusted_p"]=p
        x["holm_exploratory_below_0_05"]=p<.05
    return dict(status="PASS",study="Stage54 posthoc existing Stage52-only statistical sensitivity",
                scientific_seed_n=8,new_scientific_seeds=0,
                reused_heldout_seeds=list(SEEDS),
                no_new_physical_reruns=True,confirmatory_inference=False,
                authors_original_DFAQ_LB_reproduced=False,
                original_30k_Java_Python_parity_still_failed=True,
                bootstrap_random_seed=RNG_SEED,comparisons=comparisons)

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",required=True)
    ap.add_argument("--out",required=True)
    args=ap.parse_args()
    obj=analyze(json.loads(Path(args.input).read_text()))
    dest=Path(args.out)
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(obj,sort_keys=True,indent=2,allow_nan=False)+"\n")
    for x in obj["comparisons"]:
        print("JPDC_STAGE54_SOURCE_ROBUSTNESS",json.dumps({k:v for k,v in x.items()
              if k!="leave_one_source_out"},sort_keys=True))
    print("JPDC_STAGE54_POSTHOC_SOURCE_ROBUSTNESS_AUDIT_PASS")
