#!/usr/bin/env python3
"""Stage24 causal queue-error envelope unit fixtures, NOT empirical validation."""
from queue_error_aware_dominance_stage24 import QueueErrorAwareController,NODES

def vectors():
    p=[50.]*NODES;n=[4.]*NODES
    p[0]=9.;p[1]=10.
    return p,n

def controller(queue=True,context="factory-A"):
    x=QueueErrorAwareController()
    assert x.deliver_e2e(0,8.,4.,10.,20.).kind=="compatible_delivered_feedback"
    assert x.deliver_e2e(1,4.,4.,11.,21.).kind=="compatible_delivered_feedback"
    if queue:
        x.deliver_queue_envelope(0,context,-1.,1.,10.,21.,100.)
        x.deliver_queue_envelope(1,context,-.5,.5,11.,21.,100.)
    return x

def test():
    p,n=vectors()
    # Compelling network signal alone must NEVER impersonate queue certainty.
    x=controller(queue=False)
    d=x.select(22.,p,n,20.,False,True,"factory-A")
    assert d.node==0 and d.uncertified and d.eligible_nodes==0
    print("PASS missing queue estimates abstain despite strong network evidence")

    x=controller()
    d=x.select(22.,p,n,20.,False,True,"factory-A")
    assert d.node==1 and d.switched and d.mission_upper_feasible
    assert d.candidate_upper_ms+1e-9<d.reference_lower_ms
    assert not d.probe and x.mission_switches==1
    print("PASS jointly valid network and signed queue intervals establish conditional dominance")

    x=controller()
    x.deliver_queue_envelope(1,"factory-A",-.5,5.,12.,22.,100.)
    d=x.select(23.,p,n,20.,False,True,"factory-A")
    assert d.node==0 and d.uncertified
    print("PASS broad candidate queue error bound invalidates network-only switch")

    x=controller()
    d=x.select(22.,p,n,10.1,False,True,"factory-A")
    assert d.node==0 and d.uncertified and not d.mission_upper_feasible
    print("PASS MISSION deadline-upper constraint blocks unsafe candidate")

    x=controller()
    d=x.select(22.,p,n,20.,False,True,"factory-B")
    assert d.node==0 and d.uncertified
    print("PASS wrong workload/queue context cannot reuse source evidence")

    x=controller()
    d=x.select(101.,p,n,20.,False,True,"factory-A")
    assert d.node==0 and d.uncertified
    assert x.queue_expirations_encountered==2
    print("PASS expiry never silently extends queue-error evidence")

    x=controller(queue=False)
    x.deliver_queue_envelope(0,"factory-A",-4.,-3.,10.,21.,100.)
    x.deliver_queue_envelope(1,"factory-A",-2.,-1.,11.,21.,100.)
    d=x.select(22.,p,n,20.,True,False,"factory-A")
    assert d.node==0 and not d.switched and not d.probe
    print("PASS signed negative queue residual bounds supported (not clipped to zero)")

    x=controller()
    assert x.deliver_e2e(1,8.,4.,25.,30.).kind=="observed_incompatible_change_alarm"
    d=x.select(31.,p,n,20.,False,True,"factory-A")
    assert d.node==0 and d.uncertified
    print("PASS post-alarm unverified network cannot certify a candidate")

    x=controller()
    previous=(x.last_time,x.decisions,x.queue_deliveries)
    bad=[
        lambda:x.deliver_queue_envelope(1,"factory-A",2.,1.,11.,21.,100.),
        lambda:x.deliver_queue_envelope(1,"factory-A",0.,1.,11.,20.,100.),
        lambda:x.deliver_queue_envelope(1,"factory-A",0.,1.,23.,22.,100.),
        lambda:x.deliver_queue_envelope(1,"factory-A",0.,1.,11.,22.,21.),
        lambda:x.deliver_queue_envelope(1,"factory-A",0.,1.,9.,22.,100.),
        lambda:x.select(20.,p,n,20.,False,True,"factory-A"),
        lambda:x.select(22.,p,n,20.,False,True,""),
    ]
    for fn in bad:
        try:fn()
        except ValueError:pass
        else:raise AssertionError("invalid input unexpectedly accepted")
        assert (x.last_time,x.decisions,x.queue_deliveries)==previous
    print("PASS fail-closed invalid evidence, retroactive clocks and missing provenance")

    x=controller()
    d=x.select(22.,p,n,20.,False,True,"factory-A")
    # Explicit falsification of the CONDITIONAL theorem when q actual is
    # outside its externally supplied error interval.
    true_candidate=10.+0.+10.
    true_reference=9.+4.+0.
    assert d.switched and true_candidate>true_reference
    print("PASS adversarial miscalibrated queue envelope defeats unconditional guarantee")

    x=controller()
    for k in range(22,32):
        d=x.select(float(k),p,n,20.,True,False,"factory-A")
        assert not d.probe
    x.invariant()
    print("PASS no active probing, monotonic scheduler time and cumulative invariants")
    print("JPDC_STAGE24_SIGNED_QUEUE_ERROR_INTERVAL_CAUSAL_CONTRACT_PASS")

if __name__=="__main__":test()
