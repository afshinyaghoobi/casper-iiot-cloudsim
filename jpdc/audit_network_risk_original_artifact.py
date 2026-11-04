#!/usr/bin/env python3
"""Audit new-network-risk pilot writeup against the immutable ORIGINAL artifact.

This runs NO simulation and performs NO selection or statistical inference.
"""
import argparse,json,math
from pathlib import Path

REPORT=Path(__file__).resolve().parents[1]/"jpdc/NEW_NETWORK_RESIDUAL_POLICY_PILOT_VERIFIED_2026-11-04.md"
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
POLICIES=("PRED_GREEDY","CASPER_FULL","NEW_NETWORK_RESIDUAL")
EXPECTED={
 ("S2_HIDDEN_COMPUTE_40LOSS","PRED_GREEDY"):(23,0,1050,0),
 ("S2_HIDDEN_COMPUTE_40LOSS","CASPER_FULL"):(22,0,22,0),
 ("S2_HIDDEN_COMPUTE_40LOSS","NEW_NETWORK_RESIDUAL"):(23,0,1050,0),
 ("S3_HIDDEN_NETWORK_50LOSS","PRED_GREEDY"):(21,153,153,0),
 ("S3_HIDDEN_NETWORK_50LOSS","CASPER_FULL"):(21,158,158,0),
 ("S3_HIDDEN_NETWORK_50LOSS","NEW_NETWORK_RESIDUAL"):(21,9,9,253),
}
def run(p):
    data=json.loads(Path(p).read_text(encoding="utf-8"))
    report=REPORT.read_text(encoding="utf-8")
    assert data["status"]=="PASS" and data["scope"].startswith("seed80 exploratory")
    assert data["seed_index"]==80 and data["deployment_task_policy_observations"]==72000
    assert data["policies"]==list(POLICIES) and data["scenarios"]==list(SCENARIOS)
    assert len(data["rows"])==6
    mapped={(x["scenario"],x["policy"]):x for x in data["rows"]}
    assert set(mapped)==set(EXPECTED)
    for key,(misses,pos,affected,reroutes) in EXPECTED.items():
        x=mapped[key]
        assert x["mission_deadline_misses"]==misses,(key,"mission miss")
        assert x["network_positive_excess_feedback"]==pos,(key,"positive feedback")
        assert x["postshock_affected_dispatches"]==affected,(key,"affected dispatch")
        assert x["risk_changed_node_selections"]==reroutes,(key,"relative greedy reroutes")
        assert x["network_feedback_events"]==12000
        assert x["network_feedback_strictly_delayed"] is True
        assert x["deployment_tasks"]==12000
        assert sum(x["node_dispatch_counts"])==12000
        assert sum(x["rank_counts"].values())==x["mission_tasks"]
        assert math.isfinite(x["post_deadline_miss_rate"])
        print("PASS immutable pilot exact original arm:",*key)
    s3=mapped[("S3_HIDDEN_NETWORK_50LOSS","NEW_NETWORK_RESIDUAL")]
    assert s3["risk_positive_penalty_arrivals"]==1943
    assert all(mapped[(sc,"NEW_NETWORK_RESIDUAL")]["post_deadline_miss_rate"]==
               mapped[(sc,"PRED_GREEDY")]["post_deadline_miss_rate"]
               for sc in SCENARIOS)
    assert "no deadline improvement established" in report.lower()
    assert "cpu finish" in report.lower() and "not packet-level" in report.lower()
    assert "NOT a new" not in report or "not a new published algorithm" in report.lower()
    assert "p=1.000" in report and "p=.0625" in report and "p=.125" in report
    assert "9.1214ms >5ms" in report
    print("JPDC_NEW_NETWORK_PILOT_IMMUTABLE_ARTIFACT_AND_CLAIM_AUDIT_PASS")

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--pilot-json",required=True)
    run(p.parse_args().pilot_json)
