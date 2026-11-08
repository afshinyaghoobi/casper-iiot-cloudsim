#!/usr/bin/env python3
"""Stage44 deterministic adversarial tests of node-local causal evidence."""
from causal_node_regime_selector_stage44 import CausalNodeRegimeSelector

def invalid(fn):
    try:fn()
    except ValueError:return
    raise AssertionError("invalid evidence accepted")

def pred():
    return [100.+i for i in range(21)]

def run():
    d=CausalNodeRegimeSelector()
    assert d.select(0.,pred(),True).regime=="FULL"
    # Sparse sources cannot emit a statistical alarm.
    for k in range(11):
        d.observe_cpu_finish(1,10.,10.,k+1.)
        d.observe_network_e2e(1,10.,10.,k+1.)
    assert d.select(12.,pred(),True).regime=="FULL"
    d.observe_cpu_finish(1,10.,10.,12.)
    d.observe_network_e2e(1,10.,10.,12.)
    assert d.select(12.,pred(),True).regime=="FULL"
    # Simulated localized network shift at candidate node1, but 20 other
    # nodes unaffected. No future network is visible at CPU-finish.
    for k in range(12):
        t=13.+k
        before=d.select(t-.25,pred(),True).regime
        d.observe_cpu_finish(1,10.,10.,t)
        assert d.select(t,pred(),True).regime==before
        d.observe_network_e2e(1,20.,10.,t)
    result=d.select(25.,pred(),True)
    assert result.regime=="NETWORK" and result.network_alert_nodes==(1,)
    assert result.cpu_alert_nodes==()
    assert 1 in result.candidate_nodes
    # The node is excluded from issue-relevant top6, and cannot trigger.
    altered=pred()
    altered[1]=1000.
    assert d.select(25.,altered,True).regime=="FULL"
    # Deterministic tie break picks low indexes.
    ties=[100.]*21
    assert d.select(25.,ties,True).candidate_nodes==(0,1,2,3,4,5)
    # CPU source shock on same node creates ambiguity and full fallback.
    for k in range(12):
        t=26.+k
        d.observe_cpu_finish(1,20.,10.,t)
        d.observe_network_e2e(1,20.,10.,t)
    r=d.select(38.,pred(),True)
    assert r.regime=="FULL" and r.cpu_alert_nodes==(1,) and r.network_alert_nodes==(1,)
    assert d.ambiguous_decisions>=1
    # Other nodes' CPU labels cannot be borrowed as node1's own history.
    d2=CausalNodeRegimeSelector()
    for i in range(12):
        d2.observe_cpu_finish(3,10.,10.,i+1.)
        d2.observe_network_e2e(3,10.,10.,i+1.)
    for i in range(12):
        d2.observe_cpu_finish(3,20.,10.,i+13.)
        d2.observe_network_e2e(3,10.,10.,i+13.)
    assert d2.select(25.,pred(),True).regime=="FULL"
    invalid(lambda:d.observe_network_e2e(1,10.,10.,-1.))
    invalid(lambda:d.observe_cpu_finish(21,10.,10.,40.))
    invalid(lambda:d.observe_cpu_finish(1,0.,10.,40.))
    invalid(lambda:d.observe_network_e2e(1,float('nan'),10.,40.))
    invalid(lambda:d.select(0.,pred(),True))
    invalid(lambda:d.select(38.,[1.]*20,True))
    invalid(lambda:d.select(38.,pred(),1))
    assert d.first_network_mode_clock is not None
    print("JPDC_STAGE44_CAUSAL_NODE_LOCAL_AND_SPATIALLY_DILUTED_HOTSPOT_UNIT_PASS")
if __name__=="__main__":run()
