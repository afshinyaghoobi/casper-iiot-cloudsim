#!/usr/bin/env python3
"""Stage31 all-or-nothing preregistered independent four-seed alarm utility audit."""
import argparse,json,statistics
from pathlib import Path
SEEDS=(505,506,507,508)
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
POLICIES=("PRED_GREEDY","CASPER_FULL")
parser=argparse.ArgumentParser()
parser.add_argument("--input",required=True);parser.add_argument("--out",required=True)
args=parser.parse_args()
byseed={}
for p in Path(args.input).rglob("seed_*.json"):
    x=json.loads(p.read_text())
    s=x["seed"]
    assert s in SEEDS and s not in byseed,(s,"unexpected duplicate/seed")
    assert x["status"]=="PASS" and x["source_scientific_units"]==1
    assert x["task_policy_evaluations"]==48000 and x["original_stage6_parity_all_four"]
    rows={(a["scenario"],a["policy"]):a for a in x["rows"]}
    assert len(rows)==4 and set(rows)=={(z,y) for z in SCENARIOS for y in POLICIES}
    byseed[s]=rows
assert tuple(sorted(byseed))==SEEDS,("cohort incomplete",sorted(byseed))
out=[]
for scenario in SCENARIOS:
    for policy in POLICIES:
        items=[byseed[seed][(scenario,policy)] for seed in SEEDS]
        s2=scenario==SCENARIOS[0]
        rows=[]
        for seed,r in zip(SEEDS,items):
            alarm=r["alarm"];m=r["post_mission"];p=r["post"]
            checks=r["frozen_operational_gate_results"]
            vals=dict(seed=seed,alarm_count=alarm["alarm_count"],
                      pre_shock_false_alarm=alarm["pre_shock_false_alarm"],
                      alarm_lag_ms=alarm["first_alarm_delivery_lag_vs_postshock_arrival_ms"],
                      alarm_trigger_task_index=alarm["alarm_trigger_task_index"],
                      post_revoked_fraction=p["revoked"]/p["n"],
                      post_mission_revoked_fraction=m["revoked"]/m["n"],
                      post_mission_issued_fraction=m["issued"]/m["n"],
                      post_mission_n=m["n"],
                      post_mission_issued=m["issued"],
                      post_mission_empirical_inclusion_conditional=m["conditional_inclusion_only_issued"],
                      gate_results=checks)
            rows.append(vals)
        gate_keys=("S2_alarm_after_shock_no_pre_alarm","S2_at_most_50pct_post_MISSION_revocation") if s2 else ("S3_no_CPU_false_alarm","S3_at_least_90pct_post_MISSION_issued")
        summary=dict(scenario=scenario,policy=policy,seed_level=rows,
                     independent_scientific_units=4,
                     post_mission_revocation_mean=statistics.mean(v["post_mission_revoked_fraction"] for v in rows),
                     post_mission_availability_mean=statistics.mean(v["post_mission_issued_fraction"] for v in rows),
                     post_revocation_mean=statistics.mean(v["post_revoked_fraction"] for v in rows),
                     alarm_count_by_seed=[r["alarm_count"] for r in rows],
                     operational_gate_pass_counts={key:sum(bool(r["gate_results"][key]) for r in rows) for key in gate_keys})
        print("JPDC_STAGE31_FULL_COHORT_ALARM_RESULT",json.dumps(summary,sort_keys=True),flush=True)
        out.append(summary)
res=dict(status="PASS",all_four_seed_jobs_complete=True,source_seeds=list(SEEDS),
         scientific_replicates=4,dependent_task_policy_observations=192000,
         source_scheduler_original_parity=True,
         science="Stage30 frozen detector abstention/detection performance; NO queue certificate or new scheduler efficacy",
         rows=out)
dest=Path(args.out);dest.parent.mkdir(parents=True,exist_ok=True)
dest.write_text(json.dumps(res,sort_keys=True,indent=2)+"\n")
print("JPDC_STAGE31_ALL_FOUR_SEEDS_ALARM_UTILITY_AUDIT_COMPLETE_PASS")
