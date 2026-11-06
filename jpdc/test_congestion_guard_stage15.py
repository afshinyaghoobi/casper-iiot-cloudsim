#!/usr/bin/env python3
"""Stage15 deterministic guard-only contract tests; no random physical seeds."""
from congestion_guarded_freshness_stage15 import BoundedFreshnessController,NODES
from freshness_active_observation_stage13 import FreshnessAwareController

def main():
    n=[4.0]*NODES
    # Baseline node0 nominal 10, node7 nominal 15: fresh but too expensive.
    p=[30.0]*NODES
    p[0]=10.0;p[7]=15.0
    guarded=BoundedFreshnessController()
    unguarded=FreshnessAwareController()
    for c in (guarded,unguarded):
        evt=c.deliver_e2e(7,4.,4.,0.,5.)
        assert evt.kind=="compatible_delivered_feedback"
    x=guarded.select(10.,p,n,30.,False)
    y=unguarded.select(10.,p,n,30.,False)
    assert x.node==0 and x.fallback and not x.verified
    assert y.node==7 and y.verified
    assert p[x.node]<=min(p)+2.
    print("PASS MISSION guard refuses 5ms nominal detour even with fresh data")
    # Within 2ms nominal budget, recent evidence can influence routing.
    q=list(p);q[7]=11.0
    x=guarded.select(11.,q,n,30.,False)
    assert x.node==7 and x.verified and not x.probe
    assert q[x.node]<=min(q)+2.
    print("PASS fresh MISSION candidate inside 2ms budget can be selected")
    # No observations and no deadline-feasible probing.
    b=BoundedFreshnessController()
    for k in range(1,101):
        z=b.select(float(k),p,n,1.,True)
        assert p[z.node]<=min(p)+2.
        assert z.probe is False
    assert b.probe_skipped==1
    b.assert_budget()
    print("PASS NORMAL probing skips when no feasible deadline")
    # With feasible probes, no more than 1% and no impossible action costs.
    c=BoundedFreshnessController()
    for k in range(1,301):
        z=c.select(float(k),p,n,25.,True)
        assert p[z.node]<=min(p)+2.+1e-12
        if z.probe:assert p[z.node]<=25.
    c.assert_budget()
    assert c.probe_attempts==3 and c.normal_arrivals==300
    print("PASS <=1% NORMAL and bounded route detour for controlled costs")
    print("JPDC_STAGE15_GUARD_UNIT_CONTRACT_PASS")

if __name__=="__main__":main()
