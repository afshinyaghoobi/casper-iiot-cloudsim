#!/usr/bin/env python3
"""Deterministic <=1%-NORMAL network-observation probe choice.

Node selection uses ONLY completed E2E feedback counts, last observed ordinal,
nominal pre-dispatch virtual-queue predictions and current NORMAL deadline.
"""
import math

NODES=21
NORMAL_CADENCE=100

class NormalNetworkProbe:
    def __init__(self):
        self.completed_feedback=[0]*NODES
        self.last_feedback_ordinal=[-1]*NODES
        self.global_ordinal=0
        self.normal_arrivals=0
        self.opportunities=0
        self.attempts=0
        self.skipped_empty=0
        self.changed_decisions=0

    def observe_completed_e2e(self,node):
        if not isinstance(node,int) or node<0 or node>=NODES:
            raise ValueError("invalid completed node")
        self.completed_feedback[node]+=1
        self.last_feedback_ordinal[node]=self.global_ordinal
        self.global_ordinal+=1

    def pick(self,predicted,deadline,default_node,is_normal):
        if len(predicted)!=NODES or not all(math.isfinite(v) and v>0 for v in predicted):
            raise ValueError("invalid nominal predictions")
        if not math.isfinite(deadline) or deadline<=0:
            raise ValueError("invalid deadline")
        if not isinstance(default_node,int) or default_node not in range(NODES):
            raise ValueError("invalid default node")
        if not isinstance(is_normal,bool):raise ValueError("task class must be boolean")
        if not is_normal:
            return default_node,False,False
        self.normal_arrivals+=1
        if self.normal_arrivals%NORMAL_CADENCE:
            return default_node,False,False
        self.opportunities+=1
        eligible=[j for j in range(NODES) if predicted[j]<=deadline]
        if not eligible:
            self.skipped_empty+=1
            return default_node,False,False
        self.attempts+=1
        selected=min(eligible,key=lambda j:(
            self.completed_feedback[j],self.last_feedback_ordinal[j],
            predicted[j],j))
        changed=selected!=default_node
        self.changed_decisions+=int(changed)
        return selected,True,changed

    def assert_valid(self):
        assert self.opportunities==self.normal_arrivals//NORMAL_CADENCE
        assert self.attempts+self.skipped_empty==self.opportunities
        assert 0<=self.changed_decisions<=self.attempts
        assert sum(self.completed_feedback)==self.global_ordinal
