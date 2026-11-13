#!/usr/bin/env python3
"""Contract tests for transparent, purely issue-time Stage51 comparators."""
import math
from queue_pressure_baseline_stage51 import choose, QUEUE_ONLY, QUEUE_E2E

def main():
    pred=[100.0+i for i in range(21)]
    q=[0.0]*21
    e=[0.0]*21
    assert choose(pred,q,e,QUEUE_ONLY)==(0,0.0,0.0)
    assert choose(pred,q,e,QUEUE_E2E)==(0,0.0,0.0)
    tie=[100.0]*21
    assert choose(tie,q,e,QUEUE_ONLY)[0]==0
    # Queue-only pressure changes dispatch without any hidden fault state.
    q[0]=30.0
    assert choose(pred,q,e,QUEUE_ONLY)[0]==1
    # Delayed E2E feedback is a distinct input, not a scenario or oracle mask.
    q=[0.0]*21
    e[0]=15.0
    assert choose(pred,q,e,QUEUE_ONLY)[0]==0
    assert choose(pred,q,e,QUEUE_E2E)[0]==1
    # Both penalties are capped at 20ms, as preregistered.
    q[0]=1e5
    e[0]=1e5
    n,b,p=choose(pred,q,e,QUEUE_E2E)
    assert n==1 and b==0 and p==0
    allq=[1e6]*21
    alle=[1e6]*21
    n,b,p=choose(tie,allq,alle,QUEUE_E2E)
    assert n==0 and b==20 and p==20
    invalid=[
        (pred[:-1],q,e,QUEUE_ONLY),
        (pred,q,e,"CASPER_FULL"),
        ([float("nan")]+pred[1:],q,e,QUEUE_ONLY),
        (pred,[-1.0]+q[1:],e,QUEUE_ONLY),
        (pred,q,[math.inf]+e[1:],QUEUE_E2E)
    ]
    for args in invalid:
        try:choose(*args)
        except ValueError:continue
        raise AssertionError("Stage51 accepted illegal issue-time state")
    print("JPDC_STAGE51_CAUSAL_SELECTOR_CONTRACT_PASS")

if __name__=="__main__":main()
