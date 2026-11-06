#!/usr/bin/env python3
"""Immutable Stage12 archived-artifact-only per-node diagnostic summary.
No simulation, no training, no seed changes. Input: archived episodes.json.
"""
import json,sys,math
from pathlib import Path
x=json.loads(Path(sys.argv[1]).read_text())
assert x["status"]=="PASS" and x["seed_index"]==83 and len(x["arms"])==2
for a in x["arms"]:
    print("STAGE12_ARCHIVED_POLICY",a["policy"])
    episodes=a["affected_node_episodes"]
    assert len(episodes)==6
    for e in episodes:
        records=e["records"]
        post=[r for r in records if r["postshock_task_offline"]]
        accepted=[r for r in post if r["kind"]!="late_measurement_quarantined"]
        with_pre=[r for r in accepted if r["prior_pre_accepted_at_delivery"]>0]
        # a positive margin must trigger alarm (allow numerical 1e-10)
        bad=[r for r in accepted if r["max_prior_incompatibility_margin"] is not None
             and r["max_prior_incompatibility_margin"]>1e-10]
        assert len(bad)==sum(r["kind"]=="observed_incompatible_change_alarm" for r in accepted)
        max_margin=max((r["max_prior_incompatibility_margin"] for r in with_pre
                        if r["max_prior_incompatibility_margin"] is not None),default=None)
        min_gap=min((r["prior_pre_min_generation_gap_ms"] for r in with_pre
                    if r["prior_pre_min_generation_gap_ms"] is not None),default=None)
        print("STAGE12_ARCHIVED_NODE",json.dumps(dict(node=e["node"],
           pre_delivered=e["pre_delivered"],post_delivered=e["post_delivered"],
           post_quarantined=e["post_quarantined"],
           prepost_pairs=e["comparable_accepted_post_pairs"],
           max_margin=max_margin,min_generation_gap_ms=min_gap,
           alarms=e["alarms"],reason=e["no_alarm_reason_offline"]),sort_keys=True))
    assert sum(e["alarms"]>0 for e in episodes)==1
print("JPDC_STAGE12_IMMUTABLE_NODE_MARGIN_AUDIT_PASS")
