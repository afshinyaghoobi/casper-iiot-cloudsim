#!/usr/bin/env python3
"""Stage43 eight-of-eight independent-source regime-gated MISSION audit.

Source seed—not dependent task—is the scientific paired unit.
"""
import argparse,json,statistics,math
from pathlib import Path

SEEDS=tuple(range(801,809))
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
POLICIES=("PRED_GREEDY","CASPER_FULL","NEW_MISSION_ONLY_CPU_E2E_FEEDBACK",
          "NEW_REGIME_GATED_MISSION_E2E","NEW_REGIME_GATED_MISSION_COMBINED")
CANDIDATES=POLICIES[-2:]

def exact_sign_p(diff):
    nz=[d for d in diff if d]
    n=len(nz)
    if not n:return None
    k=min(sum(d<0 for d in nz),sum(d>0 for d in nz))
    return min(1.,2*sum(math.comb(n,i) for i in range(k+1))/(2**n))

def run(source_dir):
    byseed={}
    for file in Path(source_dir).rglob("seed_*.json"):
        r=json.loads(file.read_text())
        seed=r["scientific_seed"]
        assert seed in SEEDS and seed not in byseed,("duplicate or unregistered seed",seed)
        assert r["status"]=="PASS" and r["independent_science_unit"]==1
        assert r["task_policy_dependent_observations"]==120000
        rows={(z["scenario"],z["policy"]):z for z in r["rows"]}
        assert len(rows)==10 and set(rows)=={(a,b) for a in SCENARIOS for b in POLICIES}
        for row in rows.values():
            assert row["seed"]==seed and row["post_mission_n"]>0
            assert row["source_no_cloudsim_parity_claim"]
        byseed[seed]=rows
    assert tuple(sorted(byseed))==SEEDS,("FULL eight-seed cohort required",sorted(byseed))
    results=[]
    for sc in SCENARIOS:
        for policy in POLICIES:
            items=[]
            for seed in SEEDS:
                row=byseed[seed][(sc,policy)]
                original=byseed[seed][(sc,"CASPER_FULL")]
                greedy=byseed[seed][(sc,"PRED_GREEDY")]
                assert row["post_mission_n"]==original["post_mission_n"]==greedy["post_mission_n"]
                reg=row["regime"]
                if reg is not None:
                    assert reg["regime_decisions"]==reg["network_e2e_deliveries"]==reg["cpu_finish_observations"]==12000
                    assert 0<=reg["network_regime_dispatches"]<=12000
                items.append(dict(seed=seed,mission_n=row["post_mission_n"],
                                  mission_misses=row["post_mission_deadline_misses"],
                                  vs_FULL=row["post_mission_deadline_misses"]-original["post_mission_deadline_misses"],
                                  vs_GREEDY=row["post_mission_deadline_misses"]-greedy["post_mission_deadline_misses"],
                                  mean_latency_ms=row["mean_latency_ms"],
                                  mean_wait_ms=row["mean_wait_ms"],
                                  network_mode_dispatches=reg["network_regime_dispatches"] if reg else None,
                                  network_mode_mission_dispatches=reg["mission_network_regime_dispatches"] if reg else None,
                                  first_network_mode_ms=reg["first_network_regime_dispatch_ms"] if reg else None))
            diffs=[x["vs_FULL"] for x in items]
            rec=dict(scenario=sc,policy=policy,independent_source_n=8,
                     post_mission_total=sum(x["mission_n"] for x in items),
                     mission_misses_pooled_descriptive_only=sum(x["mission_misses"] for x in items),
                     paired_mean_miss_difference_vs_FULL=statistics.mean(diffs),
                     paired_min=min(diffs),paired_max=max(diffs),
                     better_seed_count=sum(x<0 for x in diffs),
                     worse_seed_count=sum(x>0 for x in diffs),
                     tie_seed_count=sum(x==0 for x in diffs),
                     two_sided_exact_sign_p=exact_sign_p(diffs),
                     seed_mean_latency_ms=statistics.mean(x["mean_latency_ms"] for x in items),
                     seed_mean_wait_ms=statistics.mean(x["mean_wait_ms"] for x in items),
                     seed_rows=items)
            results.append(rec)
            print("JPDC_STAGE43_ALL_SEED_REGIME_RESULT",json.dumps({
                k:v for k,v in rec.items() if k!="seed_rows"},sort_keys=True),flush=True)
    gates={}
    for p in CANDIDATES:
        s2=next(x for x in results if x["scenario"]==SCENARIOS[0] and x["policy"]==p)
        s3=next(x for x in results if x["scenario"]==SCENARIOS[1] and x["policy"]==p)
        gates[p]=dict(
            S2_no_mean_harm_vs_FULL=s2["paired_mean_miss_difference_vs_FULL"]<=0,
            S2_at_most_2_harmed_seeds=s2["worse_seed_count"]<=2,
            S3_strict_mean_gain_vs_FULL=s3["paired_mean_miss_difference_vs_FULL"]<0,
            S3_at_most_2_harmed_seeds=s3["worse_seed_count"]<=2,
            S2_network_false_mode_fraction_below_1pct_every_seed=all(
                x["network_mode_dispatches"]<=120 for x in s2["seed_rows"]),
            S3_network_mode_5pct_in_6_of_8=sum(
                x["network_mode_dispatches"]>=600 for x in s3["seed_rows"])>=6,
            S2_sign_p_below_point05=s2["two_sided_exact_sign_p"] is not None and s2["two_sided_exact_sign_p"]<.05,
            S3_sign_p_below_point05=s3["two_sided_exact_sign_p"] is not None and s3["two_sided_exact_sign_p"]<.05)
    print("JPDC_STAGE43_FIXED_REGIME_SCHEDULER_GATES",json.dumps(gates,sort_keys=True),flush=True)
    return dict(status="PASS",all_eight_scientific_seeds=True,source_seeds=list(SEEDS),
                independent_source_scientific_n=8,dependent_task_policy_observations=960000,
                no_theoretical_or_java_queue_guarantee=True,
                frozen_retention_gates=gates,rows=results)

if __name__=="__main__":
    a=argparse.ArgumentParser();a.add_argument("--input",required=True);a.add_argument("--out",required=True)
    args=a.parse_args()
    data=run(args.input)
    f=Path(args.out);f.parent.mkdir(parents=True,exist_ok=True)
    f.write_text(json.dumps(data,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print("JPDC_STAGE43_COMPLETE_EIGHT_SEED_CAUSAL_REGIME_PAIRED_AUDIT_PASS",flush=True)
