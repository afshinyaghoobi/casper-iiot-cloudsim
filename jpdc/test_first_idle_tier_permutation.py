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
    # Inverse permutation maps the new index back to the original physical ID.
    physical_before=before
    physical_after=1-after if after in (0,1) else after
    assert physical_before==0 and physical_after==1
    assert physical_before!=physical_after, "first-idle is not permutation-equivariant"
    greedy_before=greedy(pred)
    greedy_after=greedy(swap(pred,0,1))
    greedy_physical_after=1-greedy_after if greedy_after in (0,1) else greedy_after
    assert greedy_before==1 and greedy_after==0
    assert greedy_before==greedy_physical_after, "greedy preserves the physical choice"
    print("PERMUTATION_COUNTEREXAMPLE_PASS")

if __name__=="__main__": test()
