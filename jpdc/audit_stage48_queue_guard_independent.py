#!/usr/bin/env python3
"""Strict Stage48 eight-of-eight source paired MISSION deadline result auditor."""
import argparse,json,math,statistics
from pathlib import Path
SEEDS=tuple(range(1001,1009))
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
POLICIES=("PRED_GREEDY","CASPER_FULL","NEW_REGIME_GATED_MISSION_COMBINED",
          "NEW_NODE_REGIME_MISSION_COMBINED",
          "NEW_QUEUE_GUARDED_NODE_E2E","NEW_QUEUE_GUARDED_NODE_COMBINED")
CANDIDATES=POLICIES[-2:]

def sign_p(diff):
    nz=[z for z in diff if z!=0]
    if not nz:return None
    n=len(nz)
    side=min(sum(z>0 for z in nz),sum(z<0 for z in nz))
    return min(1.,2.*sum(math.comb(n,i) for i in range(side+1))/2**n)

def audit(folder):
    sources={}
    for p in Path(folder).rglob("seed_*.json"):
        d=json.loads(p.read_text())
        seed=d["scientific_seed"]
        assert seed in SEEDS and seed not in sources,("duplicated/unregistered seed",seed)
        assert d["status"]=="PASS" and d["independent_scientific_unit"] is True
        assert d["dependent_task_policy_observations"]==144000
        rows={(x["scenario"],x["policy"]):x for x in d["rows"]}
        assert len(rows)==12 and set(rows)=={(sc,policy) for sc in SCENARIOS for policy in POLICIES}
        assert sum(x["original_prior_source_exact_parity"] for x in rows.values())==8
        for x in rows.values():
            assert x["seed"]==seed and x["post_mission_n"]>0
            if x["guard"] is not None:
                g=x["guard"]
                assert g["calls"]==g["mission_network_mode_issues"]
                assert 0<=g["switched"]<=g["calls"]
                assert sum(g["denial_reasons"].values())==g["calls"]
                assert g["causal_queue_backlog_is_not_a_safety_bound"]
        sources[seed]=rows
    assert tuple(sorted(sources))==SEEDS,("complete preregistered eight source seeds mandatory",sorted(sources))
    result=[]
    for sc in SCENARIOS:
        for policy in POLICIES:
            each=[]
            for seed in SEEDS:
                row=sources[seed][(sc,policy)]
                base=sources[seed][(sc,"CASPER_FULL")]
                node=sources[seed][(sc,"NEW_NODE_REGIME_MISSION_COMBINED")]
                assert row["post_mission_n"]==base["post_mission_n"]==node["post_mission_n"]
                gate=row["guard"]
                each.append(dict(seed=seed,post_mission_n=row["post_mission_n"],
                    post_mission_misses=row["post_mission_deadline_misses"],
                    baseline_full_misses=base["post_mission_deadline_misses"],
                    old_node_misses=node["post_mission_deadline_misses"],
                    diff_vs_full=row["post_mission_deadline_misses"]-base["post_mission_deadline_misses"],
                    diff_vs_prior_node=row["post_mission_deadline_misses"]-node["post_mission_deadline_misses"],
                    latency_ms=row["mean_latency_ms"],wait_ms=row["mean_wait_ms"],
                    gate_calls=gate["calls"] if gate else None,
                    gate_switches=gate["switched"] if gate else None,
                    guard_reasons=gate["denial_reasons"] if gate else None))
            diff=[r["diff_vs_full"] for r in each]
            node_diff=[r["diff_vs_prior_node"] for r in each]
            item=dict(scenario=sc,policy=policy,independent_source_n=8,
                source_rows=each,mission_denominator_pooled_descriptive_only=sum(x["post_mission_n"] for x in each),
                mission_misses_pooled_descriptive_only=sum(x["post_mission_misses"] for x in each),
                paired_mean_vs_full=statistics.mean(diff),
                paired_mean_vs_frozen_node=statistics.mean(node_diff),
                improved_seeds=sum(d<0 for d in diff),harmed_seeds=sum(d>0 for d in diff),
                tied_seeds=sum(d==0 for d in diff),
                sign_two_sided_exact_p=sign_p(diff),
                seed_mean_latency_ms=statistics.mean(x["latency_ms"] for x in each),
                seed_mean_wait_ms=statistics.mean(x["wait_ms"] for x in each))
            result.append(item)
            print("JPDC_STAGE48_ALL_EIGHT_SOURCE_PAIRED_DEADLINE_RESULT",
                  json.dumps({k:v for k,v in item.items() if k!="source_rows"},sort_keys=True),flush=True)
    gates={}
    for p in CANDIDATES:
        s2=next(r for r in result if r["scenario"]==SCENARIOS[0] and r["policy"]==p)
        s3=next(r for r in result if r["scenario"]==SCENARIOS[1] and r["policy"]==p)
        gates[p]=dict(
            S2_mean_no_harm_vs_FULL=s2["paired_mean_vs_full"]<=0,
            S2_harmed_seeds_at_most_two=s2["harmed_seeds"]<=2,
            S3_mean_strict_benefit_vs_FULL=s3["paired_mean_vs_full"]<0,
            S3_harmed_seeds_at_most_two=s3["harmed_seeds"]<=2,
            S3_mean_no_harm_vs_previous_node=s3["paired_mean_vs_frozen_node"]<=0,
            S3_no_more_than_two_harmed_vs_prior_node=sum(x["diff_vs_prior_node"]>0 for x in s3["source_rows"])<=2,
            S3_route_switches_at_least_one_in_six_seeds=sum(x["gate_switches"]>0 for x in s3["source_rows"])>=6,
            S2_queue_gate_mode_below_one_percent_each_seed=all(x["gate_calls"]<=120 for x in s2["source_rows"]),
            S2_sign_p_below05=s2["sign_two_sided_exact_p"] is not None and s2["sign_two_sided_exact_p"]<.05,
            S3_sign_p_below05=s3["sign_two_sided_exact_p"] is not None and s3["sign_two_sided_exact_p"]<.05)
    print("JPDC_STAGE48_PREDECLARED_HOLDOUT_SELECTION_GATES",json.dumps(gates,sort_keys=True),flush=True)
    return dict(status="PASS",all_eight_preregistered_source_seeds=list(SEEDS),
        independent_source_n=8,dependent_task_policy_observations=1152000,
        original_e42_source_frozen=True,statistical_unit_is_source_seed=True,
        no_queue_safety_bound_or_java_equivalence=True,selection_gates=gates,rows=result)

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--input",required=True);parser.add_argument("--out",required=True)
    a=parser.parse_args()
    obj=audit(a.input)
    f=Path(a.out);f.parent.mkdir(parents=True,exist_ok=True)
    f.write_text(json.dumps(obj,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print("JPDC_STAGE48_COMPLETE_EIGHT_SEED_ORIGINAL_SOURCE_DEADLINE_AUDIT_PASS")
