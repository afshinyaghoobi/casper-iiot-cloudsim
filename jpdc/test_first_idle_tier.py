#!/usr/bin/env python3
"""Deterministic behavior and patch anchor tests; no CloudSim claims."""
from pathlib import Path
import ast

def choose(pred, backlog):
    if len(pred)!=24 or len(backlog)!=24: raise ValueError("24 nodes required")
    for i in range(18):
        if backlog[i] <= 1e-9: return i
    return min(range(18,24),key=lambda i:(pred[i],i))

def test():
    p=[100.0]*24
    p[1]=1.0
    b=[0.0]*24
    assert choose(p,b)==0, "fixed first-idle order differs from greedy"
    b[:18]=[10.0]*18
    b[4]=0.0
    assert choose(p,b)==4
    b[4]=10.0
    p[19]=8.0
    p[22]=3.0
    assert choose(p,b)==22, "cloud spillover picks min predicted"
    b[0]=1e-9
    assert choose(p,b)==0
    b[0]=1e-8
    assert choose(p,b)==22
    source=Path("src/main/java/org/casperiiot/e42/E42Campaign.java").read_text()
    patch=Path("jpdc/first_idle_tier_patch.py").read_text()
    assert source.count("        PRED_GREEDY(false,false,false,false),")==1
    assert source.count("            if(!policy.cp){\n                j=argMin(pred,eligible);\n            }else{")==1
    assert "vq.predictedBacklogMs(node,now)<=1e-9" in patch
    ast.parse(patch)
    print("FIRST_IDLE_TIER_SEMANTICS_PASS 5 fixtures and 2 unique anchors")

if __name__=="__main__": test()
