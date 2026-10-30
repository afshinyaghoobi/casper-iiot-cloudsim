#!/usr/bin/env python3
"""Metamorphic permutation test for FIRST_IDLE_TIER; not CloudSim evidence."""
def first_idle(pred, backlog):
    if len(pred)!=24 or len(backlog)!=24: raise ValueError("24 nodes")
    for i in range(18):
        if backlog[i] <= 1e-9:
            return i
    return min(range(18,24), key=lambda i:(pred[i],i))

def greedy(pred):
    return min(range(len(pred)), key=lambda i:(pred[i],i))

def swap(xs,a,b):
    ys=list(xs)
    ys[a],ys[b]=ys[b],ys[a]
    return ys

def test():
    pred=[150.]*24; pred[0]=100.; pred[1]=20.
    backlog=[10.]*24; backlog[0]=backlog[1]=0.
    before=first_idle(pred,backlog)
    after=first_idle(swap(pred,0,1),swap(backlog,0,1))
    # After relabeling, index 0 represents the former physical node 1.
    assert before==0 and after==0
    assert after!=1, "first-idle breaks physical-node equivariance"
    assert greedy(pred)==1 and greedy(swap(pred,0,1))==0
    print("PERMUTATION_COUNTEREXAMPLE_PASS")

if __name__=="__main__": test()
