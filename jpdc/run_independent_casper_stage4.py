#!/usr/bin/env python3
"""Fixed known-development-seed Stage4 three-policy native 12-run matrix."""
import argparse,json,math
from pathlib import Path
from independent_physical_calibration_stage3 import calibrate
from independent_casper_deployment_stage4 import simulate,POLICIES

SEEDS=(50,51)
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
N=12000

def run_all():
    rows=[];calibration_summary=[]
    for seed in SEEDS:
        cal=calibrate(seed,80000,include_reference=True)
        assert len(cal["reference_scores"])==cal["mission_score_count"]
        # Raw native E17 input must never be written to results in derived summaries.
        calibration_summary.append({k:v for k,v in cal.items() if k!="reference_scores"})
        for scenario in SCENARIOS:
            for policy in POLICIES:
                r=simulate(seed,scenario,policy,cal,N)
                assert r["status"]=="PASS" and r["deployment_tasks"]==N
                assert sum(r["node_dispatch_counts"])==N
                assert 0<=r["mission_deadline_misses"]<=r["mission_tasks"]
                assert sum(r["rank_counts"].values())==r["mission_tasks"]
                if policy=="CASPER_FULL":
                    assert r["adaptive_feedback_events"]==r["mission_tasks"]
                elif r["adaptive_feedback_events"]!=0:raise AssertionError("nonadaptive feedback")
                if policy=="CASPER_HEALTH_STATIC" and r["eta_gt_one_dispatches"]!=0:
                    raise AssertionError("health-static eta not one")
                if policy=="PRED_GREEDY" and r["post_cert_rate"]!=0:
                    raise AssertionError("baseline issued certificate")
                rows.append(r)
                print("NATIVE_STAGE4_RESULT",seed,scenario,policy,
                      "mission",r["mission_tasks"],"misses",r["mission_deadline_misses"],
                      "cert_rate",r["post_cert_rate"],"rank",r["rank_counts"],
                      "health_alarms",r["health_alarm_transitions"],
                      "eta_gt1",r["eta_gt_one_dispatches"])
    if len(rows)!=12 or sum(r["deployment_tasks"] for r in rows)!=144000:
        raise AssertionError("missing stage4 native deployment run")
    return {"status":"PASS","scope":"known-development-seed mechanics, NOT confirmatory holdout",
            "stage":"native independent physical ranked CASPER deployment",
            "seeds":list(SEEDS),"scenarios":list(SCENARIOS),
            "calibration":calibration_summary,
            "total_deployment_task_policy_observations":144000,
            "rows":rows}

if __name__=="__main__":
    parser=argparse.ArgumentParser();parser.add_argument("--out",required=True)
    args=parser.parse_args();res=run_all()
    target=Path(args.out);target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(res,sort_keys=True,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    print("JPDC_NATIVE_STAGE4_FULL_POLICY_DEPLOYMENT_PASS")
