#!/usr/bin/env python3
"""Stage60 fail-closed causality and hypothetical-world contract, no efficacy."""
import json
import math
from causal_ambiguity_builder_stage60 import (
    CausalAmbiguityBuilder,NODES,CPU_MIN,NETWORK_MIN,
    MAX_AGE_MS,TELEMETRY_MAX_AGE_MS)
from finite_ambiguity_deadline_stage59 import select

def rejected(fn):
    try:fn()
    except ValueError:return
    raise AssertionError("invalid or future state accepted")

def main():
    p=[10.0,12.0]+[100.0]*(NODES-2)
    netnom=[2.0]*NODES
    b=CausalAmbiguityBuilder()
    cold=b.construct(0.0,p,netnom)
    assert cold.status=="ABSTAIN_UNVERIFIED" and cold.world_count==0
    assert cold.empirically_calibrated is False
    rejected(lambda:b.e2e_delivered(1,0,2.,3.,101.,100.))
    rejected(lambda:b.cpu_complete(True,0,4.,5.,1.,2.))
    rejected(lambda:b.observe_telemetry(0,[0]*20))
    rejected(lambda:b.observe_telemetry(0,[-1]+[0]*20))
    rejected(lambda:b.observe_telemetry(0,[float("nan")]+[0]*20))
    rejected(lambda:b.construct(0,p[:-1],netnom))

    # Before E2E delivery, the feedback is simply unavailable.
    probe=CausalAmbiguityBuilder()
    probe.cpu_complete(11,0,5.,6.,10.,10.)
    assert probe.construct(10,p,netnom).status=="ABSTAIN_UNVERIFIED"
    rejected(lambda:probe.e2e_delivered(12,0,2.,10.,11.,10.))
    probe.e2e_delivered(12,0,2.,10.,10.,20.)
    rejected(lambda:probe.construct(19,p,netnom))  # cannot rewind after seeing future
    rejected(lambda:probe.e2e_delivered(13,0,2.,4.,12.,19.))
    rejected(lambda:probe.e2e_delivered(12,0,2.,4.,10.,21.))
    assert probe.e2e_delivered(14,0,2.,4.,9.,21.) is False
    assert probe.quarantined==1 and probe.accepted_e2e==1
    assert probe.net[0][0]==8.0
    rejected(lambda:probe.cpu_complete(15,0,5.,7.,8.,20.))
    rejected(lambda:probe.observe_telemetry(20,[0]*21))

    # Populate all 21 nodes with legally delivered, valid chronological data.
    clk=1000.
    for j in range(NODES):
        for k in range(CPU_MIN):
            clk+=1.
            # Node0 receives prior observed 30 ms CPU excess, others no excess.
            b.cpu_complete(j*1000+k,j,5.,35. if j==0 else 5.,clk,clk)
        for k in range(NETWORK_MIN):
            clk+=1.
            b.e2e_delivered(j*1000+100+k,j,2.,2.,clk,clk)
    assert b.accepted_cpu==NODES*CPU_MIN
    assert b.accepted_e2e==NODES*NETWORK_MIN
    assert b.construct(clk,p,netnom).status=="ABSTAIN_UNVERIFIED"
    b.observe_telemetry(clk,[0.]*NODES)
    ready=b.construct(clk,p,netnom)
    assert ready.status=="READY_UNCALIBRATED"
    assert not ready.unavailable and ready.world_count==4
    assert not ready.empirically_calibrated and ready.conditional_only
    assert len(ready.worlds)==4 and all(len(w)==NODES for w in ready.worlds)
    assert ready.worlds[0]==tuple(p)
    assert ready.worlds[1][0]==40. and ready.worlds[1][1]==12.
    assert ready.worlds[2]==tuple(p)
    assert ready.worlds[3]==ready.worlds[1]
    choice=select(p,ready.worlds,20.)
    assert choice.nominal_greedy_node==0 and choice.node==1
    assert choice.robust_feasible_in_given_worlds
    assert choice.conditional_only and ready.true_future_coverage_guaranteed is False
    # A fresh E2E observation that has not been delivered yet cannot update this state.
    rejected(lambda:b.e2e_delivered(999999,0,2.,50.,clk+1,clk))
    assert b.construct(clk,p,netnom).worlds==ready.worlds
    # Gate without falsifying feedback: stale telemetry, then stale CPU/E2E.
    assert b.construct(clk+TELEMETRY_MAX_AGE_MS+1,p,netnom).status=="ABSTAIN_UNVERIFIED"
    b.observe_telemetry(clk+MAX_AGE_MS+1,[0.]*NODES)
    stale=b.construct(clk+MAX_AGE_MS+1,p,netnom)
    assert stale.status=="ABSTAIN_UNVERIFIED"
    assert any(x.startswith("CPU_NODE_0") for x in stale.unavailable)
    assert any(x.startswith("E2E_NODE_0") for x in stale.unavailable)
    rejected(lambda:b.construct(clk+MAX_AGE_MS,p,netnom))
    rejected(lambda:b.construct(clk+MAX_AGE_MS+1,[math.inf]+p[1:],netnom))
    info=dict(status="PASS",test="Stage60 non-oracle causal world construction",
              observed_cpu=NODES*CPU_MIN,observed_e2e=NODES*NETWORK_MIN,
              world_count=ready.world_count,nominal_greedy=choice.nominal_greedy_node,
              ambiguity_selector=choice.node,
              no_empirical_coverage_claim=True,scientific_source_seeds=0,
              original_java_python_queue_parity_still_failed=True)
    print("JPDC_STAGE60_CAUSAL_AMBIGUITY_CONTRACT",json.dumps(info,sort_keys=True))
    print("JPDC_STAGE60_CAUSAL_FAIL_CLOSED_PASS")

if __name__=="__main__":
    main()
