#!/usr/bin/env python3
"""Independent semantic fixture of deadline-feasible policy (not CloudSim)."""
def choose(pred,sigma,deadline):
    if not pred or len(pred)!=len(sigma):raise ValueError("shape")
    feasible=[i for i,p in enumerate(pred) if p<=deadline]
    if feasible:return min(feasible,key=lambda i:(sigma[i],pred[i],i))
    return min(range(len(pred)),key=lambda i:(pred[i],i))
def test():
    assert choose([10,12],[8,1],15)==1
    assert choose([10,12],[8,1],11)==0
    assert choose([10,12],[8,1],9)==0
    assert choose([10,10],[1,1],15)==0
    assert choose([10,12],[8,1],20)==1
    print("DEADLINE_FEASIBLE_REFERENCE_PASS 5 cases")
if __name__=="__main__":test()
