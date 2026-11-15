#!/usr/bin/env python3
"""Stage62 original artifacts-only cohort; failure preserved independently of CI."""
import argparse,json
from pathlib import Path
SEEDS=(1511,1512)
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
POLICIES=("PRED_GREEDY","CASPER_FULL")

def aggregate(original):
    assert set(original)==set(SEEDS)
    rows={}
    for seed in SEEDS:
        x=original[seed]
        assert x["status"]=="PASS" and x["source_seed"]==seed
        assert x["no_route_changes"] and x["original_source_parity"]
        assert x["source_task_observations"]==48000
        assert len(x["rows"])==4
        for v in x["rows"]:
            key=(seed,v["scenario"],v["policy"])
            assert key not in rows and v["seed"]==seed
            assert v["scenario"] in SCENARIOS and v["policy"] in POLICIES
            sh=v["shadow"]
            assert sh["stage62_scope"]=="restricted_observed_candidate_subset_only"
            assert sh["stage60_all_21_node_builder_not_relaxed"]
            assert sh["original_source_task_count"]==12000
            assert sh["CPU_completion_deliveries"]==sh["E2E_delivered_feedback"]==12000
            assert sum(sh["eligible_count_histogram"].values())==sh["mission_arrivals"]
            assert sh["coverage_empirically_calibrated"] is False
            assert 0<=sh["ready_mission_arrivals"]<=sh["two_eligible_mission"]<=sh["any_eligible_mission"]<=sh["mission_arrivals"]
            assert sh["ready_mission_arrivals"]<=sh["nominal_greedy_observed_mission"]
            rows[key]=sh
    assert len(rows)==8
    summary=[]
    for sc in SCENARIOS:
        for policy in POLICIES:
            source_rows=[rows[(seed,sc,policy)] for seed in SEEDS]
            n=sum(x["mission_arrivals"] for x in source_rows)
            ready=sum(x["ready_mission_arrivals"] for x in source_rows)
            post_n=sum(x["post_mission_arrivals"] for x in source_rows)
            post_ready=sum(x["ready_post_mission_arrivals"] for x in source_rows)
            rates=[x["ready_mission_arrivals"]/x["mission_arrivals"] for x in source_rows]
            hist={str(k):sum(x["eligible_count_histogram"][str(k)] for x in source_rows)
                    for k in range(22)}
            summary.append(dict(scenario=sc,policy=policy,
                source_seed_counts=[dict(seed=seed,mission=sh["mission_arrivals"],
                    ready=sh["ready_mission_arrivals"],
                    post_mission=sh["post_mission_arrivals"],
                    post_ready=sh["ready_post_mission_arrivals"],
                    any_eligible=sh["any_eligible_mission"],
                    two_eligible=sh["two_eligible_mission"],
                    greedy_observed=sh["nominal_greedy_observed_mission"],
                    hypothetical_switches=sh["shadow_mission_different_from_greedy"])
                    for seed,sh in zip(SEEDS,source_rows)],
                ready_mission=ready,mission_arrivals=n,
                ready_fraction=ready/n,
                post_ready_mission=post_ready,post_mission_arrivals=post_n,
                post_ready_fraction=post_ready/post_n,
                any_eligible=sum(x["any_eligible_mission"] for x in source_rows),
                two_eligible=sum(x["two_eligible_mission"] for x in source_rows),
                greedy_observed=sum(x["nominal_greedy_observed_mission"] for x in source_rows),
                candidate_count_histogram=hist,
                prereg_at_least_10pct_each_seed_gate="PASS" if min(rates)>=.10 else "FAIL"))
    fail=any(x["prereg_at_least_10pct_each_seed_gate"]=="FAIL" for x in summary)
    return dict(status="PASS",software_evidence="PASS",prereg_operational_feasibility="FAIL" if fail else "PASS",
        original_source_seeds=list(SEEDS),scientific_independent_source_n=2,
        all_dependent_policy_task_observations=96000,no_new_policy_efficacy_holdout=True,
        calibrated_uncertainty_coverage=False,original_Stage61_all_21_node_failure_preserved=True,
        original_Java_SpaceShared_parity_still_failed=True,rows=summary)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--source-dir",required=True)
    p.add_argument("--out",required=True)
    a=p.parse_args();root=Path(a.source_dir)
    original={}
    for seed in SEEDS:
        d=root/f"jpdc-stage62-partial-shadow-seed-{seed}"
        assert (d/"source.json").read_bytes()==(d/"repeat.json").read_bytes()
        assert (d/"source.log").read_bytes()==(d/"repeat.log").read_bytes()
        original[seed]=json.loads((d/"source.json").read_text())
    r=aggregate(original)
    out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(r,indent=2,sort_keys=True,allow_nan=False)+"\n")
    for x in r["rows"]:
        print("JPDC_STAGE62_SUBSET_SHADOW_COHORT",json.dumps(x,sort_keys=True))
    print("JPDC_STAGE62_ORIGINAL_COHORT_AUDIT_PASS")
