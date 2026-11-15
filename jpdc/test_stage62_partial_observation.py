#!/usr/bin/env python3
"""Stage62 subset-only causality and non-alias tests, no efficacy simulations."""
import json
from causal_ambiguity_builder_stage60 import CausalAmbiguityBuilder,NODES
from partial_observation_selector_stage62 import choose_partial

def rejected(fn):
    try:fn()
    except ValueError:return
    raise AssertionError("accepted invalid/future observation")

def main():
    p=[10.,12.]+[100.]*19
    b=CausalAmbiguityBuilder()
    cold=choose_partial(b,0.,p,[2.]*NODES,20.)
    assert cold.status=="ABSTAIN_UNVERIFIED" and len(cold.eligible_nodes)==0
    assert "GLOBAL_NOMINAL_GREEDY_NOT_OBSERVED" in cold.unavailable
    now=1000.
    for j in (0,1):
        for k in range(4):
            now+=1
            b.cpu_complete(j*100+k,j,5.,35. if j==0 else 5.,now,now)
        for k in range(8):
            now+=1
            b.e2e_delivered(j*100+40+k,j,2.,2.,now,now)
    b.observe_telemetry(now,[0.]*NODES)
    r=choose_partial(b,now,p,[2.]*NODES,20.)
    assert r.status=="READY_PARTIAL_UNCALIBRATED"
    assert r.eligible_nodes==(0,1)
    assert r.nominal_greedy==0 and r.proposed_node==1
    assert not r.empirically_calibrated and r.conditional_only
    assert 19==len(set(range(NODES))-set(r.eligible_nodes))
    # Full Stage60 remains unusable on exactly this data; no threshold changes.
    full=b.construct(now,p,[2.]*NODES)
    assert full.status=="ABSTAIN_UNVERIFIED"
    # If nominal greedy is missing, we do NOT rank only observed alternatives
    # as if they were globally safe/optimal.
    p2=[100.]*NODES
    p2[2]=1.
    g=choose_partial(b,now,p2,[2.]*NODES,20.)
    assert g.status=="ABSTAIN_UNVERIFIED" and g.proposed_node is None
    assert "GLOBAL_NOMINAL_GREEDY_NOT_OBSERVED" in g.unavailable
    assert g.eligible_nodes==(0,1)
    # Restricted pool can contain only one node (still not ready).
    one=CausalAmbiguityBuilder()
    t=20.
    for k in range(4):
        t+=1;one.cpu_complete(k,0,5.,5.,t,t)
    for k in range(8):
        t+=1;one.e2e_delivered(40+k,0,2.,2.,t,t)
    one.observe_telemetry(t,[0.]*NODES)
    s=choose_partial(one,t,p,[2.]*NODES,20.)
    assert s.status=="ABSTAIN_UNVERIFIED" and len(s.eligible_nodes)==1
    assert "FEWER_THAN_TWO_ELIGIBLE_NODES" in s.unavailable
    assert choose_partial(b,now+101,p,[2.]*NODES,20.).status=="ABSTAIN_UNVERIFIED"
    rejected(lambda:choose_partial(b,now-1,p,[2.]*NODES,20.))
    rejected(lambda:choose_partial(b,now,[float("nan")]+p[1:],[2.]*NODES,20.))
    rejected(lambda:choose_partial(b,now,p,[2.]*20,20.))
    rejected(lambda:choose_partial(b,now,p,[2.]*NODES,0.))
    rejected(lambda:choose_partial(b,now,p,[2.]*NODES,20.,actual_hidden_world=1))
    print("JPDC_STAGE62_PARTIAL_OBSERVATION_CONTRACT",json.dumps(dict(
        full_node_ready=False,partial_ready=True,partial_node_count=2,
        same_state_greedy=0,partial_hypothetical_choice=1,
        unobserved_node_count=19,
        true_coverage_guarantee=False,independent_source_seeds=0),sort_keys=True))
    print("JPDC_STAGE62_PARTIAL_CAUSAL_CONTRACT_PASS")

if __name__=="__main__":main()
