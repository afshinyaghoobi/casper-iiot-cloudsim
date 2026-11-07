#!/usr/bin/env python3
"""Stage41 exact complete eight-seed paired actual-MISSION deadline audit."""
import argparse,json,math,statistics
from pathlib import Path

SEEDS=tuple(range(701,709))
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
POLICIES=("PRED_GREEDY","CASPER_FULL","NEW_MISSION_ONLY_CPU_E2E_FEEDBACK",
          "NEW_FULL_ANCHORED_E2E","NEW_FULL_ANCHORED_CPU_E2E")
CANDIDATES=("NEW_FULL_ANCHORED_E2E","NEW_FULL_ANCHORED_CPU_E2E")

def sign_p(ds):
    nz=[d for d in ds if d]
    n=len(nz)
    if n==0:return None
    k=min(sum(v>0 for v in nz),sum(v<0 for v in nz))
    return min(1.,2.*sum(math.comb(n,i) for i in range(k+1))/2**n)

def cohort(folder):
    data={}
    for f in Path(folder).rglob("seed_*.json"):
        r=json.loads(f.read_text())
        seed=r["source_seed"]
        assert seed in SEEDS and seed not in data,("unexpected/duplicate",seed)
        assert r["status"]=="PASS" and r["independent_source_cohort"] and r["task_policy_observations"]==120000
        rows={(z["scenario"],z["policy"]):z for z in r["rows"]}
        assert len(rows)==10 and set(rows)=={(a,b) for a in SCENARIOS for b in POLICIES}
        assert sum(bool(z["exact_frozen_prior_policy_parity"]) for z in rows.values())==6
        for z in rows.values():
            assert z["seed"]==seed and z["post_mission_n"]>0
            if z["mission_anchored_reranker"] is not None:
                x=z["mission_anchored_reranker"]
                assert x["decisions"]==x["causal_cpu_finishes"]==x["causal_e2e_network_deliveries"]==12000
                assert x["mission_switches"]<=x["mission_decisions"]
        data[seed]=rows
    assert tuple(sorted(data))==SEEDS,("incomplete cohort",sorted(data))
    table=[]
    for sc in SCENARIOS:
        for policy in POLICIES:
            vals=[]
            for seed in SEEDS:
                p=data[seed][(sc,policy)]
                b=data[seed][(sc,"CASPER_FULL")]
                g=data[seed][(sc,"PRED_GREEDY")]
                assert p["post_mission_n"]==b["post_mission_n"]==g["post_mission_n"]
                diag=p["mission_anchored_reranker"]
                vals.append(dict(seed=seed,n=p["post_mission_n"],miss=p["post_mission_deadline_misses"],
                    vs_FULL=p["post_mission_deadline_misses"]-b["post_mission_deadline_misses"],
                    vs_GREEDY=p["post_mission_deadline_misses"]-g["post_mission_deadline_misses"],
                    latency_ms=p["mean_latency_ms"],wait_ms=p["mean_wait_ms"],
                    mission_switches=diag["mission_switches"] if diag else None))
            diff=[v["vs_FULL"] for v in vals]
            record=dict(scenario=sc,policy=policy,scientific_n=8,
                seed_rows=vals,post_mission_total=sum(x["n"] for x in vals),
                pooled_misses_descriptive_only=sum(x["miss"] for x in vals),
                paired_mean_miss_difference_vs_FULL=statistics.mean(diff),
                paired_min=min(diff),paired_max=max(diff),
                improved_seed_count=sum(v<0 for v in diff),
                harmed_seed_count=sum(v>0 for v in diff),
                tied_seed_count=sum(v==0 for v in diff),
                two_sided_exact_sign_p=sign_p(diff),
                seed_mean_latency_ms=statistics.mean(v["latency_ms"] for v in vals),
                seed_mean_wait_ms=statistics.mean(v["wait_ms"] for v in vals))
            table.append(record)
            print("JPDC_STAGE41_FULL_ANCHORED_PAIRED_COHORT_RESULT",
                  json.dumps({k:v for k,v in record.items() if k!="seed_rows"},sort_keys=True),flush=True)
    gates={}
    for p in CANDIDATES:
        s2=next(r for r in table if r["scenario"]==SCENARIOS[0] and r["policy"]==p)
        s3=next(r for r in table if r["scenario"]==SCENARIOS[1] and r["policy"]==p)
        gates[p]=dict(
            S2_no_mean_harm_vs_FULL=s2["paired_mean_miss_difference_vs_FULL"]<=0,
            S2_at_most_two_harmed_seeds=s2["harmed_seed_count"]<=2,
            S3_strict_mean_improvement_vs_FULL=s3["paired_mean_miss_difference_vs_FULL"]<0,
            S3_at_most_two_harmed_seeds=s3["harmed_seed_count"]<=2,
            S2_sign_p_below_05=s2["two_sided_exact_sign_p"] is not None and s2["two_sided_exact_sign_p"]<.05,
            S3_sign_p_below_05=s3["two_sided_exact_sign_p"] is not None and s3["two_sided_exact_sign_p"]<.05)
    print("JPDC_STAGE41_PREDECLARED_INDEPENDENT_SCHEDULING_GATES",json.dumps(gates,sort_keys=True),flush=True)
    return dict(status="PASS",all_eight_source_seeds_complete=True,seeds=list(SEEDS),
        scientific_independent_replicates=8,dependent_task_policy_observations=960000,
        no_statistical_claim_from_dependent_tasks=True,
        no_cloudsim_parity_or_coverage_guarantee=True,
        frozen_retention_gates=gates,rows=table)

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--input",required=True);p.add_argument("--out",required=True)
    a=p.parse_args()
    result=cohort(a.input)
    o=Path(a.out);o.parent.mkdir(parents=True,exist_ok=True)
    o.write_text(json.dumps(result,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print("JPDC_STAGE41_COMPLETE_EIGHT_SEED_FULL_ANCHORED_PAIRED_AUDIT_PASS",flush=True)
