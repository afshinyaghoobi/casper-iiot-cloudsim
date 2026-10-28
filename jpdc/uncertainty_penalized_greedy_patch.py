#!/usr/bin/env python3
"""Experimental online uncertainty-penalized greedy dispatch; not literature SOTA.

Apply after tools/e45_generate.py, only to generated E45Campaign.
Fixed lambda=1.0. Strict source anchors; no post-hoc tuning.
"""
from pathlib import Path
p=Path("src/main/java/org/casperiiot/e45/E45Campaign.java")
s=p.read_text()
anchor="        PRED_GREEDY(false,false,false,false),"
assert s.count(anchor)==1, "expected unique policy enum anchor"
s=s.replace(anchor,anchor+"\n        UNCERTAINTY_PENALIZED_GREEDY(false,false,false,false),")
anchor2="""            if(!policy.cp){
                j=argMin(pred,eligible);
            }else{"""
replacement="""            if(!policy.cp){
                if(policy==Policy.UNCERTAINTY_PENALIZED_GREEDY){
                    // Fixed lambda = 1.0; uses nominal predicted latency and
                    // source-frozen fixedSigma (no lookahead, no affected mask).
                    int choice=-1;
                    double best=Double.POSITIVE_INFINITY;
                    for(int node=0;node<NODES;node++){
                        if(!eligible.test(node))continue;
                        double score=pred[node]+fixedSigma(pred[node],nodes[node].sigmaMult());
                        if(score<best){best=score;choice=node;}
                    }
                    j=choice>=0?choice:argMin(pred,eligible);
                }else j=argMin(pred,eligible);
            }else{"""
assert s.count(anchor2)==1, "expected unique dispatch anchor"
s=s.replace(anchor2,replacement)
p.write_text(s)
print("UNCERTAINTY_PENALIZED_GREEDY_PATCH_PASS")
