#!/usr/bin/env python3
"""Two classic causal least-outstanding-task baseline adaptations.

Neither is Wu et al. DFAQ-LB; no elastic queues, health score or migration.
"""
import math

NODES=21
LEAST="LEAST_INFLIGHT"
WEIGHTED="CAPACITY_WEIGHTED_LEAST_INFLIGHT"
POLICIES=(LEAST,WEIGHTED)

def choose(outstanding,capacities,policy):
    if policy not in POLICIES:
        raise ValueError("unknown baseline")
    if len(outstanding)!=NODES or len(capacities)!=NODES:
        raise ValueError("need 21 node observations")
    if not all(type(v) is int and v>=0 for v in outstanding):
        raise ValueError("outstanding tasks must be nonnegative integers")
    if not all(isinstance(v,(int,float)) and math.isfinite(v) and v>0
               for v in capacities):
        raise ValueError("nominal capacity must be finite positive")
    if policy==LEAST:
        return min(range(NODES),key=lambda j:(outstanding[j],j))
    return min(range(NODES),key=lambda j:((outstanding[j]+1.0)/capacities[j],j))
