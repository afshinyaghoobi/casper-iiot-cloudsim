#!/usr/bin/env python3
"""Stage13 controlled fixtures only: no scientific seed or efficacy experiment."""
import math
from freshness_active_observation_stage13 import (
    FreshnessAwareController,NODES,PROBE_CADENCE,MAX_FRESHNESS_MS)

def vec(default=15.):
    p=[default+j*.1 for j in range(NODES)]
    n=[4.]*NODES
    return p,n

def main():
    p,n=vec()
    ctl=FreshnessAwareController()
    a=ctl.select(0.,p,n,25.,False)
    assert a.node==0 and a.fallback and not a.verified and not a.probe
    assert a.selected_age_ms is None and a.upper_extra_ms is None
    assert ctl.mission_unverified==1
    print("PASS unknown histories treated as unknown, not known safe")

    # Same node receives result only at completed E2E delivery.
    e=ctl.deliver_e2e(7,4.,4.,10.,20.)
    assert e.kind=="compatible_delivered_feedback"
    mid=ctl.select(21.,p,n,25.,False)
    assert mid.node==7 and mid.verified and mid.selected_age_ms==11.
    # All data stale: deterministic nominal fallback, not zero risk.
    stale=ctl.select(10011.,p,n,25.,False)
    assert stale.node==0 and stale.fallback and stale.fresh_candidates==0
    print("PASS E2E causal freshness, finite risk when recent, stale fallback")

    # A long gap with stated L cannot identify a real normalized unit jump.
    evt=ctl.deliver_e2e(7,8.,4.,11020.,11030.)
    assert evt.kind=="compatible_delivered_feedback" and ctl.observer.alarms[7]==0
    print("PASS long-gap change can be formally unidentifiable")

    # New contradictory recent observation alarms, then is unverified.
    evt=ctl.deliver_e2e(7,4.,4.,11040.,11050.)
    assert evt.kind=="observed_incompatible_change_alarm"
    post=ctl.select(11050.,p,n,25.,False)
    assert post.fallback and not post.verified
    evt=ctl.deliver_e2e(7,4.,4.,11060.,11070.)
    assert evt.kind=="compatible_delivered_feedback"
    recovered=ctl.select(11070.,p,n,25.,False)
    assert recovered.verified and recovered.node==7
    print("PASS post-alarm uncertainty until two delivered epoch samples")

    # Late generated report cannot rewrite newer accepted history.
    before=ctl.observer.memory_size()
    evt=ctl.deliver_e2e(7,4.,4.,11030.,11080.)
    assert evt.kind=="late_measurement_quarantined"
    assert ctl.observer.memory_size()==before
    print("PASS older-generated delayed reports quarantined")

    # New instance keeps probing isolated from MISSION class.
    b=FreshnessAwareController()
    base=b.select(0.,p,n,25.,False)
    assert not base.probe
    for k in range(1,301):
        r=b.select(float(k),p,n,25.,True)
        if k%PROBE_CADENCE:assert not r.probe
        else:assert r.probe and r.node!=base.node
    b.assert_budget()
    assert b.normal_arrivals==300 and b.probe_attempts==3
    assert b.probe_changed==3
    assert b.mission_unverified==1
    print("PASS <=1% NORMAL probe cadence, no MISSION probe, real changed node")

    c=FreshnessAwareController()
    for k in range(1,101):
        r=c.select(float(k),p,n,1.,True)
    assert not r.probe and c.probe_skipped==1
    c.assert_budget()
    print("PASS no deadline-eligible probes are skipped")

    # Feedback in the past must fail closed.
    old=(b.last_time,b.observer.total_delivered,b.normal_arrivals)
    try:b.deliver_e2e(0,4.,4.,1.,50.)
    except ValueError:pass
    else:raise AssertionError("accepted a retroactive feedback")
    assert old==(b.last_time,b.observer.total_delivered,b.normal_arrivals)
    print("PASS reject retroactive E2E feedback")
    print("JPDC_STAGE13_CAUSAL_CONTROLLER_FIXTURES_PASS")

if __name__=="__main__":main()
