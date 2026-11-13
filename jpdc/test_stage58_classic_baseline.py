#!/usr/bin/env python3
"""Stage58 deterministic selection and causal observable contract."""
import math
from classic_least_inflight_stage58 import choose,LEAST,WEIGHTED,NODES

def main():
    counts=[0]*NODES
    capacity=[2.0]*NODES
    assert choose(counts,capacity,LEAST)==0
    assert choose(counts,capacity,WEIGHTED)==0
    counts[0]=1
    assert choose(counts,capacity,LEAST)==1
    assert choose(counts,capacity,WEIGHTED)==1
    # Weighted minimum outstanding is not the same as raw least connections.
    counts=[0]*NODES
    capacity=[1.0]*NODES
    capacity[1]=10.0
    assert choose(counts,capacity,LEAST)==0
    assert choose(counts,capacity,WEIGHTED)==1
    # After assigning one to node1, it can remain lower weighted pressure.
    counts[1]=1
    assert choose(counts,capacity,WEIGHTED)==1
    # No prediction, task deadline or hidden fault mask accepted in API.
    invalid=[
        (counts[:-1],capacity,LEAST), (counts,capacity[:-1],WEIGHTED),
        ([1.2]+counts[1:],capacity,LEAST),([-1]+counts[1:],capacity,LEAST),
        ([True]+counts[1:],capacity,LEAST),(counts,[0]+capacity[1:],WEIGHTED),
        (counts,[math.inf]+capacity[1:],LEAST),(counts,capacity,"CASPER_FULL")]
    for a in invalid:
        try:choose(*a)
        except ValueError:continue
        raise AssertionError("invalid causal baseline state accepted")
    # Deliberate distinctness from a nominal end-to-end prediction argmin.
    greedy_prediction=[9.0]+[100.0]*20
    outstanding=[7]+[0]*20
    j=min(range(NODES),key=lambda k:(greedy_prediction[k],k))
    assert j==0 and choose(outstanding,[1.0]*NODES,LEAST)!=j
    print("JPDC_STAGE58_LEAST_INFLIGHT_CAUSAL_CONTRACT_PASS")
if __name__=="__main__":main()
