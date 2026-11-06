#!/usr/bin/env python3
"""Full fixed Stage35 cohort, includes every adverse independent seed."""
import argparse,json,statistics
from pathlib import Path
SEEDS=(513,514,515,516)
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
POLICIES=("PRED_GREEDY","CASPER_FULL")
p=argparse.ArgumentParser()
p.add_argument("--directory",required=True);p.add_argument("--out",required=True)
args=p.parse_args()
byseed={}
for path in Path(args.directory).rglob("seed_*.json"):
    data=json.loads(path.read_text())
    seed=data["scientific_seed"]
    assert seed in SEEDS and seed not in byseed
    assert data["status"]=="PASS" and data["independent_units"]==1
    assert data["task_policy_observations"]==48000 and data["all_original_policy_parity"]
    rows={(r["scenario"],r["policy"]):r for r in data["rows"]}
    assert len(rows)==4 and set(rows)=={(a,b) for a in SCENARIOS for b in POLICIES}
    byseed[seed]=rows
assert tuple(sorted(byseed))==SEEDS,("incomplete cohort",sorted(byseed))
summaries=[]
for scenario in SCENARIOS:
    for policy in POLICIES:
        science=[]
        for seed in SEEDS:
            x=byseed[seed][(scenario,policy)]
            m=x["proxy_post_mission"];old=x["original_strict_post_mission"]
            assert m["n"]==old["n"]
            science.append(dict(seed=seed,post_mission_jobs=m["n"],
                old_exact_own_available=old["available_fraction"],
                proxy_available=m["available_fraction"],
                proxy_issued=m["proxy_issued"],
                proxy_included=m["proxy_covered"],
                proxy_missed=m["proxy_missed"],
                proxy_empirical_inclusion=m["proxy_inclusion"],
                proxy_max_violation_ms=m["max_interval_violation_ms"],
                post_high_available=x["proxy_post_high"]["available_fraction"],
                post_all_available=x["proxy_post_all"]["available_fraction"],
                alarm_clock_ms=x["alarm_clock_ms"],
                gates=x["preregistered_operational_gates"]))
        is_s2=scenario==SCENARIOS[0]
        keys=("S2_post_MISSION_at_least_50pct_issued",
              "S2_at_least10_proxy_and_at_least90pct_proxy_inclusion") if is_s2 else (
              "S3_no_cpu_alarm_and_no_proxy","S3_post_MISSION_at_least90pct_issued")
        row=dict(scenario=scenario,policy=policy,scientific_replicates=4,
                 mission_own_availability_mean=statistics.mean(x["old_exact_own_available"] for x in science),
                 mission_proxy_availability_mean=statistics.mean(x["proxy_available"] for x in science),
                 mission_proxy_availability_min=min(x["proxy_available"] for x in science),
                 mission_proxy_issued_counts=[x["proxy_issued"] for x in science],
                 proxy_coverage_only_where_issued=[
                     dict(seed=x["seed"],issued=x["proxy_issued"],included=x["proxy_included"],
                          coverage=x["proxy_empirical_inclusion"]) for x in science],
                 seed_level=science,
                 preregistered_gate_pass_counts={k:sum(bool(x["gates"][k]) for x in science) for k in keys})
        summaries.append(row)
        print("JPDC_STAGE35_COMPLETE_PROXY_COHORT_RESULT",json.dumps(row,sort_keys=True),flush=True)
out=dict(status="PASS",complete_four_source_seed_cohort=True,
         source_seeds=list(SEEDS),independent_scientific_replicates=4,
         dependent_task_policy_observations=192000,
         formal_coverage_guarantee=False,policy_scheduler_not_modified=True,
         note="A descriptive proxy may increase issuance while invalidating MISSION interval; do not cherry-pick",
         rows=summaries)
path=Path(args.out);path.parent.mkdir(parents=True,exist_ok=True)
path.write_text(json.dumps(out,sort_keys=True,indent=2,allow_nan=False)+"\n")
print("JPDC_STAGE35_FOUR_SEED_PROXY_COHORT_AUDIT_COMPLETE_PASS")
