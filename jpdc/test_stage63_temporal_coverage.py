#!/usr/bin/env python3
"""Stage63 negative leakage and frozen one-step-ahead chosen-node caps."""
import json
from shadow_chosen_node_coverage_stage63 import ChosenNodeTemporalAudit
from causal_ambiguity_builder_stage60 import NODES

def main():
    a=ChosenNodeTemporalAudit()
    t=100.
    # Historical samples for node0 only; no fabricated data for other nodes.
    for i in range(4):
        t+=1
        a.cpu_finish(100+i,0,5.,6.,t)
    for i in range(8):
        t+=1
        a.e2e_finish(200+i,0,2.,3.,t,t)
    a.builder.observe_telemetry(t,[0.]*NODES)
    mission=("S2_HIDDEN_COMPUTE_40LOSS",4000,"MISSION",20.,1.,.1,.1,t)
    a.capture_selected(t,mission,0,5.,2.)
    saved=a.records[4000]
    assert saved["cpu_bound"]==1 and saved["net_bound"]==1
    assert saved["cpu_eligible"] and saved["net_eligible"]
    # A large *future* report enters history only after this snapshot.
    t+=1
    a.cpu_finish(300,0,5.,105.,t)
    a.e2e_finish(301,0,2.,102.,t,t)
    assert a.records[4000]["cpu_bound"]==1
    assert a.records[4000]["net_bound"]==1
    # Actual outcome violates BOTH frozen caps, although a future-snooping
    # implementation could have called the historic sample max 100 instead.
    t+=1
    a.cpu_finish(4000,0,5.,8.,t)
    a.e2e_finish(4000,0,2.,5.,t,t)
    assert a.records[4000]["cpu_hit"] is False
    assert a.records[4000]["net_hit"] is False
    assert a.records[4000]["cpu_overrun"]==2
    assert a.records[4000]["net_overrun"]==2
    # A chosen unobserved node is NOT evaluated as covered.
    t+=1
    mission2=("S2_HIDDEN_COMPUTE_40LOSS",4001,"MISSION",20.,1.,.1,.1,t)
    a.capture_selected(t,mission2,3,5.,2.)
    assert a.records[4001]["cpu_bound"] is None
    assert a.records[4001]["net_bound"] is None
    assert not a.records[4001]["cpu_eligible"]
    assert not a.records[4001]["net_eligible"]
    t+=1
    a.cpu_finish(4001,3,5.,100.,t)
    a.e2e_finish(4001,3,2.,100.,t,t)
    assert a.records[4001]["cpu_hit"] is None and a.records[4001]["net_hit"] is None
    assert a.by_phase["ALL_MISSION"]["mission"]==2
    assert a.by_phase["ALL_MISSION"]["joint_eligible"]==1
    print("JPDC_STAGE63_FROZEN_CHOSEN_NODE_CONTRACT",json.dumps(dict(
        historical_cpu_bound=1,historical_network_bound=1,
        future_cpu_excess=3,future_network_excess=3,
        fully_observed_test_tasks=1,unobserved_tasks_not_assessed=1,
        no_counterfactual_claim=True),sort_keys=True))
    print("JPDC_STAGE63_TEMPORAL_LEAKAGE_CONTRACT_PASS")

if __name__=="__main__":main()
