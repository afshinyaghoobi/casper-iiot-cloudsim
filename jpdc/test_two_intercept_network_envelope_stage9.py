#!/usr/bin/env python3
"""Adversarial exact compression vs Stage8 ledger, shock and ordering fixtures.

No scientific seeds, original simulations, performance claims or statistical tests.
"""
import math
from age_aware_network_interval_stage8 import (
    AgeAwareResidualIntervals,AssumptionViolation,NODES)
from two_intercept_network_envelope_stage9 import TwoInterceptNetworkEnvelope

def instantiate(L=.1,eps=1.):
    v=[L]*NODES;w=[eps]*NODES
    return [TwoInterceptNetworkEnvelope(v,w,mode=m)
            for m in ("audited","chronological","unaudited")]

def equal(a,b,atol=1e-8):
    assert math.isclose(a.low_ms,b.low_ms,abs_tol=atol,rel_tol=0),(a,b)
    if math.isfinite(a.high_ms) or math.isfinite(b.high_ms):
        assert math.isclose(a.high_ms,b.high_ms,abs_tol=atol,rel_tol=0),(a,b)
    assert a.report_count==b.report_count and a.identifiable==b.identifiable
    assert a.latest_measurement_time_ms==b.latest_measurement_time_ms

def run():
    models=instantiate()
    original=AgeAwareResidualIntervals([.1]*NODES,[1.]*NODES)
    for x in models:
        assert x.constant_state_fields()==105
        assert x.total_record_memory()==0
        st=x.envelope(0,0.)
        assert not st.envelope.identifiable and math.isinf(st.envelope.high_ms)
        assert st.historical_consistency_audited==(x.mode!="unaudited")
    print("PASS unobserved node remains unknown, not low-risk; compact summary fixed 21-node state")

    measurements=((0,8.,10.,20.),(0,9.,35.,40.),(0,8.,40.,50.),
                  (1,5.,60.,70.),(1,5.25,70.,80.),(0,8.4,80.,90.))
    for record in measurements:
        original.deliver(*record)
        for x in models:x.deliver(*record)
        t=record[3]+12.
        for j in range(NODES):
            expected=original.envelope(j,t)
            for x in models:equal(x.envelope(j,t).envelope,expected)
    assert models[0].total_record_memory()==len(measurements)
    assert models[1].total_record_memory()==models[2].total_record_memory()==0
    print("PASS all-node exact O(1)-query age interval parity versus full Stage8 ledger")

    # Due to delivery reordering, measurement generation may go BACKWARD.
    late=instantiate()
    late[0].deliver(0,8.,20.,30.)
    late[2].deliver(0,8.,20.,30.)
    for x in (late[0],late[2]):x.deliver(0,7.5,15.,35.)
    try:late[1].deliver(0,8.,20.,30.);late[1].deliver(0,7.5,15.,35.)
    except ValueError:pass
    else:raise AssertionError("chronological-only incorrectly accepted older delivered measurement")
    equal(late[0].envelope(0,40.).envelope,late[2].envelope(0,40.).envelope)
    print("PASS out-of-order measurement supported with audit; chronological compact contract rejects")

    # An abrupt risk jump is NOT consistent with a gentle global drift bound.
    jump=instantiate(L=.1,eps=0.)
    for x in jump:x.deliver(0,0.,0.,1.)
    for x in jump[:2]:
        try:x.deliver(0,20.,10.,11.)
        except AssumptionViolation:pass
        else:raise AssertionError("abrupt 20ms jump accepted under L=.1")
        assert x.count[0]==1 and x.last_delivery==1.
    # Unsafe mode intentionally does NOT assert historical compatibility.
    jump[2].deliver(0,20.,10.,11.)
    assert jump[2].count[0]==2
    # At late t, widened cones can overlap despite the physical jump
    # having violated source-time constraints.
    st=jump[2].envelope(0,200.)
    assert st.envelope.low_ms<=st.envelope.high_ms
    assert st.historical_consistency_audited is False
    print("PASS abrupt-shift contradiction detected in audited modes; unaudited future interval cannot certify history")

    # Same node, simultaneous time, different task-specific transfer size.
    # If eps=0, a node-only r(t) cannot explain the discrepancy.
    size=instantiate(L=.02,eps=0.)
    for x in size:x.deliver(3,3.,10.,20.)
    for x in size[:2]:
        try:x.deliver(3,18.,10.,21.)
        except AssumptionViolation:pass
        else:raise AssertionError("size-dependent excess with identical node-time wrongly accepted")
    print("PASS incompatible task-specific excess requires broader physical model/error budget")

    # More than 1000 delivered reports: exact 2-intercept O(1)-memory
    # chronological mode, but reference stores each report to perform audit.
    stress=instantiate(L=.03,eps=.25)
    for i in range(1001):
        # Exact latent r(t)=5+0.01t; bounded by chosen L=.03.
        node=i%NODES
        t=float(i*5+1)
        value=5.+.01*t+(.1 if i%2 else -.1)
        report=(node,value,t,t+2.)
        for x in stress:x.deliver(*report)
    for j in range(NODES):
        ref=stress[0].envelope(j,5200.).envelope
        for x in stress[1:]:equal(x.envelope(j,5200.).envelope,ref,1e-7)
    assert stress[0].total_record_memory()==1001
    assert stress[1].total_record_memory()==stress[2].total_record_memory()==0
    assert stress[1].constant_state_fields()==105
    print("PASS 1001-feedback all-node envelope parity; audited ledger grows, chronological summary constant")

    # Selector must never certify unaudited drift model history.
    preds=[10.+j*.01 for j in range(NODES)]
    for x in stress:
        choice,margin,available,history_ok,coverage=x.choose(preds,5200.)
        assert available and coverage==NODES and math.isfinite(margin)
        assert history_ok==(x.mode!="unaudited")
    print("PASS decision returns separate observed-interval vs audited-assumption status")
    print("JPDC_STAGE9_EXACT_COMPRESSION_AND_SHOCK_FALSIFICATION_PASS")

if __name__=="__main__":run()
