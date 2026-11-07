#!/usr/bin/env python3
"""Adversarial causal full-anchored reranking with strict fallbacks."""
from casper_full_anchored_reranker_stage40 import CausalFullAnchoredReranker

def fixture():
    a=CausalFullAnchoredReranker()
    v=[100.+i for i in range(21)]
    v[0]=100.;v[1]=101.;v[2]=102.
    sig=[1.]*21
    q=[1.,1.,1.]
    return a,v,sig,q

def take(a,v,sig,q,now=1000.,is_mission=True,mode="E2E",base=0,cert=True,deadline=120.):
    return a.choose(now,v,sig,deadline,1.,q,base,1,cert,(0,1,2),is_mission,mode)

def run():
    a,v,sig,q=fixture()
    assert take(a,v,sig,q).reason=="reference_evidence_missing_or_stale"
    # CPU finished alone cannot leak E2E evidence.
    for i in range(10):
        a.observe_cpu(0,30.,10.,10.+i)
    assert take(a,v,sig,q).node==0
    for i in range(8):
        a.observe_network(0,actual=31.,nominal=10.,delivered_ms=200.+i)
        a.observe_network(1,actual=10.,nominal=10.,delivered_ms=200.1+i)
    candidate=take(a,v,sig,q,now=210.,mode="E2E")
    assert candidate.changed and candidate.node==1 and candidate.rank==2
    assert candidate.extra_nominal_ms==1.
    # Original screening and health-family restriction.
    assert not take(a,v,sig,q,now=210.,is_mission=False).changed
    assert not take(a,v,sig,q,now=210.,cert=False).changed
    assert not take(a,v,sig,q,now=210.,deadline=101.5).changed
    assert not take(a,v,sig,q,now=6000.).changed
    v[1]=103.
    assert not take(a,v,sig,q,now=210.).changed
    v[1]=101.
    assert take(a,v,sig,q,now=210.,mode="BOTH").node==0 # CPU candidate evidence missing
    for i in range(4):
        a.observe_cpu(1,10.,10.,300.+i)
    assert take(a,v,sig,q,now=310.,mode="BOTH").node==1
    assert a.switches<=a.mission_decisions and a.reasons["nonmission_original_full"]==1
    # invalid future/out-of-order observations are rejected
    try:a.observe_network(1,12.,10.,-1.)
    except ValueError:pass
    else:raise AssertionError("retrograde E2E incorrectly accepted")
    print("JPDC_STAGE40_FULL_ANCHORED_FRESHNESS_CP_CPU_E2E_UNIT_PASS")
if __name__=="__main__":run()
