#!/usr/bin/env python3
"""Stage47 causal queue-externality budget gate. Heuristic, NOT a hard bound."""
from collections import Counter
from dataclasses import dataclass
import math

@dataclass(frozen=True)
class QueueGateDecision:
    node:int
    switched:bool
    reason:str
    corrected_gain_ms:float
    candidate_minus_full_backlog_ms:float

class QueueExternalityGate:
    def __init__(self):
        self.calls=0
        self.switches=0
        self.reasons=Counter()

    def choose(self,baseline_node,proposed,nominal,backlog,deadline,alarmed,
               network_penalty,cpu_penalty,mode):
        if mode not in ("E2E","BOTH"):
            raise ValueError("unknown preregistered correction mode")
        if (len(nominal)!=21 or len(backlog)!=21 or len(alarmed)!=21 or
            len(network_penalty)!=21 or len(cpu_penalty)!=21 or
            type(baseline_node) is not int or not 0<=baseline_node<21 or
            type(proposed.node) is not int or not 0<=proposed.node<21):
            raise ValueError("invalid issue-time node vectors")
        if (any(type(v) not in (int,float) or not math.isfinite(v) or v<=0 for v in nominal)
            or any(type(v) not in (int,float) or not math.isfinite(v) or v<0
                   for vals in (backlog,network_penalty,cpu_penalty) for v in vals)
            or any(type(v) is not bool for v in alarmed)
            or type(deadline) not in (int,float) or not math.isfinite(deadline)):
            raise ValueError("invalid causal evidence / predicted score")
        j=proposed.node
        base=baseline_node
        basepen=network_penalty[base]+(cpu_penalty[base] if mode=="BOTH" else 0.)
        gain=nominal[base]+basepen-proposed.corrected_pred_ms
        delta=backlog[j]-backlog[base]
        reason="accepted"
        if j==base:reason="unchanged_original_full"
        elif alarmed[j]:reason="candidate_health_alarm"
        elif nominal[j]>nominal[base]+2.0+1e-10:reason="extra_nominal_vs_full"
        elif delta>1e-10:reason="extra_virtual_backlog"
        elif gain+1e-10<3.0:reason="insufficient_delivered_gain"
        elif proposed.corrected_pred_ms>deadline-2.0+1e-10:reason="no_candidate_deadline_slack"
        elif nominal[base]>deadline+1e-10:reason="original_full_nominal_unfeasible"
        self.calls+=1
        self.reasons[reason]+=1
        if reason=="accepted":
            self.switches+=1
            return QueueGateDecision(j,True,reason,gain,delta)
        return QueueGateDecision(base,False,reason,gain,delta)

    def invariant(self):
        assert self.calls==sum(self.reasons.values())
        assert self.switches==self.reasons["accepted"]
        assert 0<=self.switches<=self.calls
