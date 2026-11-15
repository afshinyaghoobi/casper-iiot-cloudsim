#!/usr/bin/env python3
"""Stage62 passive subset observer. Reuses original Stage61 causal delivery hooks."""
from collections import Counter
from shadow_causal_feasibility_stage61 import ShadowFeasibility
from partial_observation_selector_stage62 import choose_partial
from causal_ambiguity_builder_stage60 import NODES

class ShadowPartialFeasibility(ShadowFeasibility):
    def __init__(self):
        super().__init__()
        self.any_eligible_mission=0
        self.two_eligible_mission=0
        self.greedy_observed_mission=0
        self.eligible_histogram=Counter()
        self.partial_abstention_reasons=Counter()
        self.ready_post_mission_eligible_histogram=Counter()

    def arrived(self,now,task,pred,nominal_net):
        result=choose_partial(self.builder,now,pred,nominal_net,task[3])
        self.all_arrivals+=1
        ready=result.status=="READY_PARTIAL_UNCALIBRATED"
        self.ready_all+=int(ready)
        if task[2]!="MISSION":
            return
        post=task[1]>=10000
        self.all_mission+=1
        self.post_mission+=int(post)
        self.ready_mission+=int(ready)
        self.ready_post_mission+=int(ready and post)
        self.eligible_histogram[len(result.eligible_nodes)]+=1
        self.any_eligible_mission+=int(len(result.eligible_nodes)>=1)
        self.two_eligible_mission+=int(len(result.eligible_nodes)>=2)
        self.greedy_observed_mission+=int(result.nominal_greedy in result.eligible_nodes)
        if ready:
            assert result.proposed_node in result.eligible_nodes
            self.ready_post_mission_eligible_histogram[len(result.eligible_nodes)]+=int(post)
            self.shadow_different+=int(result.proposed_node!=result.nominal_greedy)
            return
        assert result.proposed_node is None
        for reason in result.unavailable:
            self.mission_reasons[reason]+=1
            self.partial_abstention_reasons[reason]+=1
            if post:self.post_mission_reasons[reason]+=1
            if reason.startswith("CPU_NODE_"):
                self.node_cpu_missing[int(reason.split("_")[2])]+=1
            elif reason.startswith("E2E_NODE_"):
                self.node_e2e_missing[int(reason.split("_")[2])]+=1

    def finalize(self,count,mission_count,post_mission_count):
        result=super().finalize(count,mission_count,post_mission_count)
        result["stage62_scope"]="restricted_observed_candidate_subset_only"
        result["stage60_all_21_node_builder_not_relaxed"]=True
        result["any_eligible_mission"]=self.any_eligible_mission
        result["two_eligible_mission"]=self.two_eligible_mission
        result["nominal_greedy_observed_mission"]=self.greedy_observed_mission
        result["eligible_count_histogram"]={str(k):self.eligible_histogram[k]
             for k in range(NODES+1)}
        result["ready_post_mission_eligible_histogram"]={
            str(k):self.ready_post_mission_eligible_histogram[k]
            for k in range(NODES+1)}
        result["partial_abstention_reasons"]=dict(sorted(self.partial_abstention_reasons.items()))
        result["ready_semantics"]="READY_PARTIAL_UNCALIBRATED only"
        assert sum(self.eligible_histogram.values())==mission_count
        assert self.any_eligible_mission>=self.two_eligible_mission>=self.ready_mission
        assert self.greedy_observed_mission>=self.ready_mission
        return result
