#!/usr/bin/env python3
"""Stage22 deterministic falsification and conditional theorem fixtures only."""
from robust_interval_dominance_stage22 import RobustDominanceController,NODES

def vectors():
    p=[50.0]*NODES
    n=[4.0]*NODES
    p[0]=9.0
    p[1]=10.0
    return p,n

def setup_pair():
    c=RobustDominanceController()
    assert c.deliver_e2e(0,8.,4.,10.,20.).kind=="compatible_delivered_feedback"
    assert c.deliver_e2e(1,4.,4.,11.,21.).kind=="compatible_delivered_feedback"
    return c

def test():
    p,n=vectors()
    c=RobustDominanceController()
    x=c.select(1.,p,n,11.,False)
    assert x.node==0 and x.unverified and not x.switched and not x.probe
    print("PASS no-history fallback no false verification")

    c=RobustDominanceController()
    c.deliver_e2e(1,4.,4.,10.,20.)
    x=c.select(21.,p,n,11.,False)
    assert x.node==0 and x.unverified and x.reference_lower_ms is None
    print("PASS cannot displace unknown greedy node")

    c=setup_pair()
    x=c.select(22.,p,n,11.,False)
    assert x.node==1 and x.switched and x.conditionally_dominated
    assert x.candidate_upper_ms+1e-9<x.reference_lower_ms
    assert x.mission_deadline_feasible and not x.probe
    # The theorem is CONDITIONAL on accurate nominal predictions and bounds.
    assert x.candidate_upper_ms < x.reference_lower_ms
    predicted_candidate_actual=10.0 # residual inside candidate interval
    predicted_reference_actual=13.0  # residual inside reference interval
    assert predicted_candidate_actual < predicted_reference_actual
    # A 10ms unmodeled queue error on candidate refutes an unconditional promise.
    actual_candidate_with_queue_error=predicted_candidate_actual+10.
    assert actual_candidate_with_queue_error > predicted_reference_actual
    print("PASS nominal and network-bound conditional dominance; queue-model counterexample")

    c=setup_pair()
    x=c.select(22.,p,n,9.5,False)
    assert x.node==0 and not x.switched and x.unverified
    print("PASS reject candidate whose conditional upper exceeds MISSION deadline")

    c=setup_pair()
    x=c.select(22.,p,n,11.,True)
    assert x.node==1 and x.switched and not x.probe and not x.mission_deadline_feasible
    assert c.mission_switches==0
    print("PASS NORMAL robust routing has no artificial probing")

    c=setup_pair()
    event=c.deliver_e2e(1,8.,4.,25.,30.)
    assert event.kind=="observed_incompatible_change_alarm"
    x=c.select(31.,p,n,11.,False)
    assert x.node==0 and not x.switched
    assert c.observer.bounds(1,31.,4.).unverified_after_alarm
    print("PASS incompatible epoch cannot certify a one-sample replacement node")

    c=setup_pair()
    # At this time both last samples are stale; reference unknown too.
    x=c.select(10051.,p,n,200.,False)
    assert x.node==0 and not x.switched and x.fresh_eligible_nodes==0
    print("PASS stale model does not prove robust change")

    c=setup_pair()
    original=(c.last_time,c.decisions,c.observer.total_delivered)
    for bad in (lambda:c.deliver_e2e(1,4.,4.,2.,20.),
                lambda:c.select(20.,p,n,11.,False),
                lambda:c.select(22.,p,n,-1.,False)):
        try:bad()
        except ValueError:pass
        else:raise AssertionError("causal validator accepted invalid input")
    assert original==(c.last_time,c.decisions,c.observer.total_delivered)
    print("PASS reject feedback or decisions before latest observed delivery")

    c=setup_pair()
    c.select(22.,p,n,11.,False)
    c.invariant()
    assert c.decisions==c.switches==c.mission_switches==1
    assert c.unverified_decisions==0
    print("JPDC_STAGE22_ROBUST_DOMINANCE_CAUSAL_CONTRACT_PASS")

if __name__=="__main__":test()
