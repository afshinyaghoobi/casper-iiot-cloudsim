#!/usr/bin/env python3
"""Stage45 audit mandatory eight source seeds and actual MISSION paired outcomes."""
import argparse,json,math,statistics
from pathlib import Path
SEEDS=tuple(range(901,909))
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
POLICIES=("PRED_GREEDY","CASPER_FULL","NEW_REGIME_GATED_MISSION_COMBINED",
          "NEW_MISSION_ONLY_CPU_E2E_FEEDBACK",
          "NEW_NODE_REGIME_MISSION_E2E","NEW_NODE_REGIME_MISSION_COMBINED")
NEW=("NEW_NODE_REGIME_MISSION_COMBINED","NEW_NODE_REGIME_MISSION_E2E")

def sign_p(diff):
    valid=[d for d in diff if d!=0]
    if not valid:return None
    n=len(valid)
    k=min(sum(d<0 for d in valid),sum(d>0 for d in valid))
    return min(1.,2*sum(math.comb(n,i) for i in range(k+1))/2**n)

def audit(folder):
    rows={}
    for f in Path(folder).rglob("seed_*.json"):
        d=json.loads(f.read_text())
        seed=d["scientific_seed"]
        assert seed in SEEDS and seed not in rows,("duplicate/unregistered source",seed)
        assert d["status"]=="PASS" and d["independent_source_scientific_unit"]==1
        assert d["task_policy_dependent_observations"]==144000
        r={(z["scenario"],z["policy"]):z for z in d["rows"]}
        assert len(r)==12 and set(r)=={(sc,p) for sc in SCENARIOS for p in POLICIES}
        for x in r.values():
            assert x["seed"]==seed and x["post_mission_n"]>0
            if x["node_regime"] is not None:
                v=x["node_regime"]
                assert v["decisions"]==v["cpu_finish_observations"]==v["network_e2e_deliveries"]==12000
                assert v["no_hard_deadline_or_conformal_certificate"] is True
                assert v["hidden_scenario_or_true_fault_mask_used_at_dispatch"] is False
                assert sum(v["network_node_evidence_counts"])==12000
                assert sum(v["cpu_node_evidence_counts"])==12000
        rows[seed]=r
    assert tuple(sorted(rows))==SEEDS,("MANDATORY complete science cohort",sorted(rows))
    out=[]
    for sc in SCENARIOS:
        for policy in POLICIES:
            each=[]
            for seed in SEEDS:
                r=rows[seed][(sc,policy)]
                full=rows[seed][(sc,"CASPER_FULL")]
                global_mode=rows[seed][(sc,"NEW_REGIME_GATED_MISSION_COMBINED")]
                ungated=rows[seed][(sc,"NEW_MISSION_ONLY_CPU_E2E_FEEDBACK")]
                assert r["post_mission_n"]==full["post_mission_n"]==global_mode["post_mission_n"]==ungated["post_mission_n"]
                reg=r["node_regime"]
                g=global_mode["node_regime"] # global policy has no stage44 diagnostic
                assert g is None
                each.append(dict(seed=seed,n=r["post_mission_n"],miss=r["post_mission_deadline_misses"],
                  full_miss=full["post_mission_deadline_misses"],
                  vs_full=r["post_mission_deadline_misses"]-full["post_mission_deadline_misses"],
                  vs_global=r["post_mission_deadline_misses"]-global_mode["post_mission_deadline_misses"],
                  vs_ungated=r["post_mission_deadline_misses"]-ungated["post_mission_deadline_misses"],
                  mean_latency_ms=r["mean_latency_ms"],mean_wait_ms=r["mean_wait_ms"],
                  node_network_dispatches=reg["network_regime_dispatches"] if reg else None,
                  node_mission_network_dispatches=reg["mission_network_regime_dispatches"] if reg else None,
                  first_network_mode_ms=reg["first_network_regime_dispatch_ms"] if reg else None))
            df=[x["vs_full"] for x in each]
            rec=dict(scenario=sc,policy=policy,scientific_source_seed_n=8,
                     seed_rows=each,pooled_mission_denominator_descriptive_only=sum(x["n"] for x in each),
                     pooled_mission_misses_descriptive_only=sum(x["miss"] for x in each),
                     paired_mean_misses_vs_full=statistics.mean(df),
                     paired_min=min(df),paired_max=max(df),
                     improved_seeds=sum(d<0 for d in df),harmed_seeds=sum(d>0 for d in df),
                     tied_seeds=sum(d==0 for d in df),two_sided_exact_sign_p=sign_p(df),
                     paired_mean_vs_global=statistics.mean(x["vs_global"] for x in each),
                     paired_mean_vs_ungated=statistics.mean(x["vs_ungated"] for x in each),
                     seed_mean_latency_ms=statistics.mean(x["mean_latency_ms"] for x in each),
                     seed_mean_wait_ms=statistics.mean(x["mean_wait_ms"] for x in each))
            out.append(rec)
            print("JPDC_STAGE45_EIGHT_SEED_NODE_LOCAL_PAIRED_RESULT",
                  json.dumps({k:v for k,v in rec.items() if k!="seed_rows"},sort_keys=True),flush=True)
    gates={}
    for p in NEW:
        s2=next(r for r in out if r["scenario"]==SCENARIOS[0] and r["policy"]==p)
        s3=next(r for r in out if r["scenario"]==SCENARIOS[1] and r["policy"]==p)
        gates[p]=dict(S2_no_mean_harm_vs_FULL=s2["paired_mean_misses_vs_full"]<=0,
            S2_at_most2_harmed_seeds=s2["harmed_seeds"]<=2,
            S3_strict_mean_gain_vs_FULL=s3["paired_mean_misses_vs_full"]<0,
            S3_at_most2_harmed_seeds=s3["harmed_seeds"]<=2,
            S2_network_false_mode_le1percent_each_seed=all(x["node_network_dispatches"]<=120 for x in s2["seed_rows"]),
            S3_network_mode_ge5percent_in6of8=sum(x["node_network_dispatches"]>=600 for x in s3["seed_rows"])>=6,
            S2_sign_p_below05=(s2["two_sided_exact_sign_p"] is not None and s2["two_sided_exact_sign_p"]<.05),
            S3_sign_p_below05=(s3["two_sided_exact_sign_p"] is not None and s3["two_sided_exact_sign_p"]<.05))
    print("JPDC_STAGE45_PREDECLARED_COMPLETE_NODE_LOCAL_HOLDOUT_GATES",json.dumps(gates,sort_keys=True),flush=True)
    return dict(status="PASS",complete_mandatory_source_seeds=list(SEEDS),
                independent_scientific_source_n=8,
                dependent_task_policy_observations=1152000,
                no_engine_equivalence_claim=True,no_certified_deadline_guarantee=True,
                predeclared_gates=gates,rows=out)

if __name__=="__main__":
    parser=argparse.ArgumentParser();parser.add_argument("--input",required=True)
    parser.add_argument("--out",required=True);args=parser.parse_args()
    r=audit(args.input)
    o=Path(args.out);o.parent.mkdir(parents=True,exist_ok=True)
    o.write_text(json.dumps(r,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print("JPDC_STAGE45_COMPLETE_ALL_EIGHT_INDEPENDENT_NODE_LOCAL_MISSION_COHORT_PASS",flush=True)
