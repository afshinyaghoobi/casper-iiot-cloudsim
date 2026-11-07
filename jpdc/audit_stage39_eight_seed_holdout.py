#!/usr/bin/env python3
"""Stage39 all-8-seed fixed-cohort paired MISSION deadline statistical audit.

One scientific unit per source seed. No task-iid p-values, no cherry-picking.
"""
import argparse,json,math,statistics
from pathlib import Path
SEEDS=tuple(range(601,609))
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
POLICIES=("PRED_GREEDY","CASPER_FULL",
 "NEW_CPU_FEEDBACK_ONLY","NEW_E2E_FEEDBACK_ONLY","NEW_CPU_E2E_FEEDBACK",
 "NEW_MISSION_ONLY_CPU_FEEDBACK","NEW_MISSION_ONLY_CPU_E2E_FEEDBACK")
TARGET="NEW_MISSION_ONLY_CPU_E2E_FEEDBACK"

def sign_p(two_sided_diffs):
    nonzero=[d for d in two_sided_diffs if d!=0]
    n=len(nonzero)
    if not n:return None
    improve=sum(d<0 for d in nonzero)
    harm=sum(d>0 for d in nonzero)
    tail=sum(math.comb(n,k) for k in range(min(improve,harm)+1))
    return min(1.,2.*tail/(2**n))

def analyze(input_dir):
    found={}
    for path in Path(input_dir).rglob("seed_*.json"):
        x=json.loads(path.read_text())
        s=x["scientific_seed"]
        assert s in SEEDS and s not in found,("unknown or duplicate seed",s)
        assert x["status"]=="PASS" and x["scientific_replicates"]==1
        assert x["dependent_task_policy_observations"]==168000
        assert x["original_stage6_exact_parity_all_four"]
        policy_map={(r["scenario"],r["policy"]):r for r in x["rows"]}
        assert len(policy_map)==14
        assert set(policy_map)=={(sc,p) for sc in SCENARIOS for p in POLICIES}
        for v in policy_map.values():
            assert v["seed"]==s and v["post_mission_n"]>0
            assert v["no_deadline_certificate"]
        found[s]=policy_map
    assert tuple(sorted(found))==SEEDS,("missing full prereg cohort",sorted(found))
    output=[]
    for sc in SCENARIOS:
        each=[]
        for policy in POLICIES:
            details=[]
            for s in SEEDS:
                x=found[s][(sc,policy)]
                b=found[s][(sc,"CASPER_FULL")]
                g=found[s][(sc,"PRED_GREEDY")]
                assert x["post_mission_n"]==b["post_mission_n"]==g["post_mission_n"]
                details.append(dict(seed=s,post_mission_n=x["post_mission_n"],
                    miss=x["post_mission_deadline_misses"],
                    baseline_full_miss=b["post_mission_deadline_misses"],
                    baseline_greedy_miss=g["post_mission_deadline_misses"],
                    diff_vs_full=x["post_mission_deadline_misses"]-b["post_mission_deadline_misses"],
                    diff_vs_greedy=x["post_mission_deadline_misses"]-g["post_mission_deadline_misses"],
                    mean_latency_ms=x["mean_latency_ms"],
                    mean_wait_ms=x["mean_wait_ms"],
                    mission_switches=x["mission_routing_changed_from_greedy"],
                    background_switches=x["background_changed_from_greedy"]))
            vs_full=[r["diff_vs_full"] for r in details]
            vs_greedy=[r["diff_vs_greedy"] for r in details]
            item=dict(scenario=sc,policy=policy,scientific_seed_n=8,
                post_mission_misses_by_seed=[dict(seed=r["seed"],n=r["post_mission_n"],miss=r["miss"]) for r in details],
                vs_full=dict(paired_differences=vs_full,seed_level_mean=statistics.mean(vs_full),
                    min=min(vs_full),max=max(vs_full),better=sum(z<0 for z in vs_full),
                    worse=sum(z>0 for z in vs_full),ties=sum(z==0 for z in vs_full),
                    two_sided_exact_sign_p=sign_p(vs_full)),
                vs_greedy=dict(paired_differences=vs_greedy,seed_level_mean=statistics.mean(vs_greedy),
                    min=min(vs_greedy),max=max(vs_greedy),better=sum(z<0 for z in vs_greedy),
                    worse=sum(z>0 for z in vs_greedy),ties=sum(z==0 for z in vs_greedy),
                    two_sided_exact_sign_p=sign_p(vs_greedy)),
                mean_latency_ms=statistics.mean(r["mean_latency_ms"] for r in details),
                mean_wait_ms=statistics.mean(r["mean_wait_ms"] for r in details),
                all_seed_rows=details)
            each.append(item)
            print("JPDC_STAGE39_COMPLETE_SEED_PAIRED_RESULT",json.dumps({
                k:v for k,v in item.items() if k not in ("all_seed_rows",)},sort_keys=True),flush=True)
        output.extend(each)
    chosen={r["scenario"]:r for r in output if r["policy"]==TARGET}
    s2=chosen[SCENARIOS[0]]["vs_full"]
    s3=chosen[SCENARIOS[1]]["vs_full"]
    gates=dict(
        S2_no_mean_mission_deadline_harm_vs_FULL=s2["seed_level_mean"]<=0,
        S3_strict_mean_mission_deadline_improvement_vs_FULL=s3["seed_level_mean"]<0,
        S2_at_most_2_of_8_seeds_worse_vs_FULL=s2["worse"]<=2,
        S3_at_most_2_of_8_seeds_worse_vs_FULL=s3["worse"]<=2,
        S2_exact_sign_p_lt_point05=(s2["two_sided_exact_sign_p"] is not None and s2["two_sided_exact_sign_p"]<.05),
        S3_exact_sign_p_lt_point05=(s3["two_sided_exact_sign_p"] is not None and s3["two_sided_exact_sign_p"]<.05))
    print("JPDC_STAGE39_PREDECLARED_HOLDOUT_GATES",json.dumps(gates,sort_keys=True),flush=True)
    return dict(status="PASS",complete_fixed_eight_seed_cohort=True,
        source_seeds=list(SEEDS),scientific_independent_replicates=8,
        dependent_task_policy_observations=1344000,
        actual_deadline_outcomes_only=True,
        no_java_cross_engine_parity_claim=True,
        no_reported_theoretical_guarantee=True,
        candidate_retention_gates=gates,rows=output)

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--input",required=True);p.add_argument("--out",required=True)
    a=p.parse_args()
    obj=analyze(a.input)
    dst=Path(a.out);dst.parent.mkdir(parents=True,exist_ok=True)
    dst.write_text(json.dumps(obj,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print("JPDC_STAGE39_ALL_EIGHT_PREREG_SOURCE_SEEDS_PAIRED_AUDIT_COMPLETE_PASS",flush=True)
