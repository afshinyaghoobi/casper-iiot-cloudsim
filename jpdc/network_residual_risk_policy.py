#!/usr/bin/env python3
"""Prototype new network-risk scheduling state, entirely completion-observed.

Distinct from original rank-conditioned conformal screening. No source model,
simulation physics, fault labels or task outcomes can be read by choose().
"""
from collections import deque
import math

NODES=21
WINDOW=32
MIN_SAMPLES=8
Q=.90

def nearest_rank_quantile(values,tau=Q):
    if not values or not 0<tau<1 or not all(math.isfinite(x) and x>=0 for x in values):
        raise ValueError("nonempty finite nonnegative observations required")
    v=sorted(values)
    return v[math.ceil(tau*len(v))-1]

class NetworkResidualRisk:
    def __init__(self,nodes=NODES):
        if nodes!=NODES:raise ValueError("fixed 21-node pilot topology")
        self.observations=[deque(maxlen=WINDOW) for _ in range(nodes)]
        self.total_feedback=0
        self.positive_feedback=0
        self.last_time=-math.inf

    def observe_e2e(self,node,actual_network_ms,nominal_network_ms,feedback_time):
        if not isinstance(node,int) or not 0<=node<NODES:
            raise ValueError("invalid observed node ID")
        if not all(math.isfinite(x) for x in (actual_network_ms,nominal_network_ms,feedback_time)):
            raise ValueError("nonfinite feedback")
        if actual_network_ms<=0 or nominal_network_ms<=0 or feedback_time<self.last_time:
            raise ValueError("negative/early/out-of-order feedback")
        excess=max(0.0,actual_network_ms-nominal_network_ms)
        self.observations[node].append(excess)
        self.total_feedback+=1
        self.positive_feedback+=int(excess>0)
        self.last_time=feedback_time
        return excess

    def penalties(self):
        return tuple(nearest_rank_quantile(xs) if len(xs)>=MIN_SAMPLES else 0.0
                     for xs in self.observations)

    def choose(self,predicted_latencies):
        if len(predicted_latencies)!=NODES or not all(
                math.isfinite(v) and v>0 for v in predicted_latencies):
            raise ValueError("invalid pre-dispatch model vector")
        risk=self.penalties()
        chosen=min(range(NODES),key=lambda j:(predicted_latencies[j]+risk[j],j))
        return chosen,risk[chosen],any(x>0 for x in risk)
