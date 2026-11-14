#!/usr/bin/env python3
"""Stage61 all-or-nothing descriptive feasibility audit: two original DEV sources."""
import argparse,json
from pathlib import Path

SEEDS=(1411,1412)
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
POLICIES=("PRED_GREEDY","CASPER_FULL")

def audit(d):
    assert set(d)==set(SEEDS)
    r={}
    for seed in SEEDS:
        obj=d[seed]
        assert obj["status"]=="PASS" and obj["source_seed"]==seed
        assert obj["no_route_changes"] and obj["original_source_parity"]
        assert obj["source_task_observations"]==48000
        assert len(obj["rows"])==4
        for row in obj["rows"]:
            key=(seed,row["scenario"],row["policy"])
            assert row["seed"]==seed and key not in r
            assert row["scenario"] in SCENARIOS and row["policy"] in POLICIES
            sh=row["shadow"]
            assert sh["shadow_only_no_routing_effect"]
            assert sh["CPU_completion_deliveries"]==sh["E2E_delivered_feedback"]==12000
            assert sh["original_source_task_count"]==12000
            assert 0<=sh["ready_mission_arrivals"]<=sh["mission_arrivals"]
            assert 0<=sh["ready_post_mission_arrivals"]<=sh["post_mission_arrivals"]
            assert sh["coverage_empirically_calibrated"] is False
            r[key]=sh
    assert len(r)==8
    summary=[]
    for scenario in SCENARIOS:
        for policy in POLICIES:
            vals=[r[(seed,scenario,policy)] for seed in SEEDS]
            ready=sum(x["ready_mission_arrivals"] for x in vals)
            missions=sum(x["mission_arrivals"] for x in vals)
            post_ready=sum(x["ready_post_mission_arrivals"] for x in vals)
            post_missions=sum(x["post_mission_arrivals"] for x in vals)
            assert missions>0 and post_missions>0
            seed_rates=[x["ready_mission_arrivals"]/x["mission_arrivals"] for x in vals]
            reasons={}
            for x in vals:
                for k,n in x["missing_reasons_at_mission"].items():
                    reasons[k]=reasons.get(k,0)+n
            summary.append(dict(scenario=scenario,policy=policy,
               ready_mission=ready,total_mission=missions,
               ready_fraction=ready/missions,
               ready_post_mission=post_ready,total_post_mission=post_missions,
               ready_post_fraction=post_ready/post_missions,
               seed_ready_fractions=seed_rates,
               late_E2E_quarantined=sum(x["late_generated_quarantined"] for x in vals),
               missing_reasons=dict(sorted(reasons.items())),
               prereg_min_ten_percent_feasibility_gate="PASS" if min(seed_rates)>=.10 else "FAIL"))
    status="FAIL" if any(x["prereg_min_ten_percent_feasibility_gate"]=="FAIL" for x in summary) else "PASS"
    return dict(status="PASS",software_evidence="PASS",
        declared_operational_feasibility_gate=status,
        scientific_independent_DEV_source_n=2,no_new_efficacy_holdout=True,
        original_stage6_route_parity=True,worlds_empirically_calibrated=False,
        rows=summary)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--source-dir",required=True)
    p.add_argument("--out",required=True)
    x=p.parse_args()
    d={}
    for seed in SEEDS:
        folder=Path(x.source_dir)/f"jpdc-stage61-shadow-feasibility-seed-{seed}"
        assert (folder/"source.json").read_bytes()==(folder/"repeat.json").read_bytes()
        assert (folder/"source.log").read_bytes()==(folder/"repeat.log").read_bytes()
        d[seed]=json.loads((folder/"source.json").read_text())
    report=audit(d)
    target=Path(x.out);target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(report,sort_keys=True,indent=2,allow_nan=False)+"\n")
    for row in report["rows"]:
        print("JPDC_STAGE61_SHADOW_FEASIBILITY",json.dumps(row,sort_keys=True))
    print("JPDC_STAGE61_ORIGINAL_COHORT_AUDIT_PASS")
