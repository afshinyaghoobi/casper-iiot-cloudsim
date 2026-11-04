#!/usr/bin/env python3
"""Fail-closed preregistered seed-level paired analysis of native holdout.

Importing this file never reads results automatically. Sign-test and bootstrap
rules were declared before the first seed60–69 holdout execution.
"""
from collections import Counter
import argparse,json,math,random
from pathlib import Path

SEEDS=tuple(range(60,70))
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
POLICIES=("CLOUD_ONLY","EDGE_FIRST","PRED_GREEDY","GLOBAL_CP",
          "RANKED_CP_STATIC","CASPER_ADAPT_NO_HEALTH",
          "CASPER_HEALTH_STATIC","CASPER_FULL")
CAL_TASKS=80000
DEPLOY_TASKS=30000

def exact_sign_test(values):
    pos=sum(x>0 for x in values)
    neg=sum(x<0 for x in values)
    ties=sum(x==0 for x in values)
    n=pos+neg
    if not n:return {"positive":pos,"negative":neg,"ties":ties,"nonzero":0,"p_two_sided":1.0}
    k=min(pos,neg)
    numerator=sum(math.comb(n,i) for i in range(k+1))
    return {"positive":pos,"negative":neg,"ties":ties,"nonzero":n,
            "p_two_sided":min(1.0,2*numerator/(2**n))}

def analyze(paths):
    documents={}
    for path in paths:
        data=json.loads(Path(path).read_text(encoding="utf-8"))
        seed=data.get("seed_index")
        if seed not in SEEDS or seed in documents:
            raise ValueError("unknown or duplicated frozen holdout seed")
        if data.get("status")!="PASS" or data.get("scientific_seed")!=4202202600+seed:
            raise ValueError("incorrect seed/science status")
        if data.get("deployment_tasks_per_run")!=DEPLOY_TASKS:
            raise ValueError("incorrect deployment task size")
        if data.get("total_task_policy_observations")!=16*DEPLOY_TASKS:
            raise ValueError("incorrect per-seed task count")
        if data.get("policy_modes")!=list(POLICIES) or data.get("scenarios")!=list(SCENARIOS):
            raise ValueError("changed preregistered arms")
        cal=data.get("calibration",{})
        if cal.get("calibration_tasks")!=CAL_TASKS or cal.get("scientific_seed")!=4202202600+seed:
            raise ValueError("invalid native calibration")
        if cal.get("postburnin_service_ratio_count")!=70000 or "reference_scores" in cal:
            raise ValueError("calibration provenance/completeness failure")
        rows=data.get("rows")
        if not isinstance(rows,list) or len(rows)!=16:raise ValueError("incomplete 16 rows")
        mapped={}
        for row in rows:
            key=(row.get("scenario"),row.get("policy"))
            if key[0] not in SCENARIOS or key[1] not in POLICIES or key in mapped:
                raise ValueError("invalid or duplicate scenario-policy")
            if row.get("seed_index")!=seed or row.get("status")!="PASS":
                raise ValueError("wrong run provenance")
            if row.get("deployment_tasks")!=DEPLOY_TASKS:
                raise ValueError("non-preregistered task count")
            if sum(row.get("node_dispatch_counts",[]))!=DEPLOY_TASKS:
                raise ValueError("incomplete physical dispatch")
            if sum(row.get("rank_counts",{}).values())!=row.get("mission_tasks"):
                raise ValueError("missing mission ranks")
            post=row.get("post_mission_tasks")
            rate=row.get("post_deadline_miss_rate")
            if not isinstance(post,int) or post<1 or not isinstance(rate,(int,float)) or not math.isfinite(rate) or not 0<=rate<=1:
                raise ValueError("invalid primary endpoint")
            mapped[key]=row
        if set(mapped)!={(c,p) for c in SCENARIOS for p in POLICIES}:
            raise ValueError("missing original policy/scenario")
        for scenario in SCENARIOS:
            mission={(r["mission_tasks"],r["post_mission_tasks"])
                     for (s,p),r in mapped.items() if s==scenario}
            if len(mission)!=1:raise ValueError("within-seed task cohort mismatch")
        documents[seed]=mapped
    if set(documents)!=set(SEEDS):
        raise ValueError("INCOMPLETE PRIMARY HOLDOUT: require all seed indices 60..69")
    pairs=[]
    all_rows=[]
    rank_totals=Counter()
    for seed in SEEDS:
        effects=[]
        for scenario in SCENARIOS:
            g=documents[seed][(scenario,"PRED_GREEDY")]
            f=documents[seed][(scenario,"CASPER_FULL")]
            effect=g["post_deadline_miss_rate"]-f["post_deadline_miss_rate"]
            effects.append(effect)
            pairs.append({"seed":seed,"scenario":scenario,
                          "greedy_post_miss_rate":g["post_deadline_miss_rate"],
                          "full_post_miss_rate":f["post_deadline_miss_rate"],
                          "post_mission_count":f["post_mission_tasks"],
                          "greedy_minus_full":effect})
        for scenario in SCENARIOS:
            for policy in POLICIES:
                row=documents[seed][(scenario,policy)]
                all_rows.append({
                  "seed":seed,"scenario":scenario,"policy":policy,
                  "mission_tasks":row["mission_tasks"],
                  "post_mission_tasks":row["post_mission_tasks"],
                  "mission_deadline_misses":row["mission_deadline_misses"],
                  "post_deadline_miss_rate":row["post_deadline_miss_rate"],
                  "post_cert_rate":row["post_cert_rate"],
                  "post_false_cert_rate":row["post_false_cert_rate"],
                  "post_abstention_rate":row["post_abstention_rate"],
                  "post_family_covered_rate":row["post_family_covered_rate"],
                  "rank_counts":row["rank_counts"],
                  "health_alarm_transitions":row["health_alarm_transitions"],
                  "eta_gt_one_dispatches":row["eta_gt_one_dispatches"],
                  "probes":row["probes"],
                  "probe_violations":row["probe_violations"],
                  "postshock_affected_dispatches":row["postshock_affected_dispatches"],
                })
                for k,v in row["rank_counts"].items():
                    rank_totals[(policy,k)]+=v
    effects=[sum(p["greedy_minus_full"] for p in pairs if p["seed"]==seed)/2 for seed in SEEDS]
    stats=exact_sign_test(effects)
    rng=random.Random(20261104)
    bootstrap=[sum(effects[rng.randrange(10)] for _ in range(10))/10 for _ in range(10000)]
    bootstrap.sort()
    mean=sum(effects)/10
    med=(sorted(effects)[4]+sorted(effects)[5])/2
    return {
      "status":"PASS","interpretation_scope":"independent native STRICT-FCFS model, not YAFS or CloudSim queue parity",
      "primary_contrast":"CASPER_FULL vs PRED_GREEDY: equal-weight S2/S3 seed-level postshock MISSION miss rate benefit",
      "unit":"scientific seed (n=10)",
      "positive_benefit_means":"CASPER_FULL lower postshock MISSION deadline miss rate",
      "seed_effects":[{"seed":s,"benefit_greedy_minus_full":v} for s,v in zip(SEEDS,effects)],
      "scenario_pairs":pairs,
      "mean_benefit":mean,"median_benefit":med,
      "exact_two_sided_sign_test":stats,
      "nominal_primary_alpha":0.05,
      "primary_significant":stats["p_two_sided"]<0.05,
      "bootstrap_95_percentile_mean_benefit":[bootstrap[249],bootstrap[9749]],
      "bootstrap_note":"descriptive fixed-PRNG paired seed bootstrap only; exact sign p remains primary",
      "native_all_eight_secondary":all_rows,
      "rank_counts_across_all_seeds":{p:{rank:rank_totals[(p,rank)] for rank in ("1","2","3")}
                                     for p in POLICIES},
      "complete_source_seed_count":10,"complete_arms":160,
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--seed-files",nargs="+",required=True)
    ap.add_argument("--out",required=True)
    args=ap.parse_args()
    result=analyze(args.seed_files)
    p=Path(args.out);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+"\n",encoding="utf-8")
    print("JPDC_NATIVE_HOLDOUT_PRIMARY_EXACT_SIGN_P",result["exact_two_sided_sign_test"]["p_two_sided"])
    print("JPDC_NATIVE_HOLDOUT_PRIMARY_MEAN_BENEFIT",result["mean_benefit"])
    print("JPDC_NATIVE_HOLDOUT_PRIMARY_SEED_EFFECTS",result["seed_effects"])
    print("JPDC_NATIVE_HOLDOUT_SIGNIFICANT",result["primary_significant"])
    print("JPDC_NATIVE_HOLDOUT_COMPLETE_PREREGISTERED_ANALYSIS_PASS")
if __name__=="__main__":main()
