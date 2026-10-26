#!/usr/bin/env python3
"""Experimental queue-averse dispatch; not a claim of published algorithm reproduction."""
from pathlib import Path
p=Path("src/main/java/org/casperiiot/e45/E45Campaign.java")
s=p.read_text()
old="        PRED_GREEDY(false,false,false,false),"
assert s.count(old)==1
s=s.replace(old,old+"\n        QUEUE_AWARE_WEIGHTED_COMPLETION(false,false,false,false),")
old="            if(!policy.cp){\n                j=argMin(pred,eligible);\n            }else{"
new="""            if(!policy.cp){
                if(policy==Policy.QUEUE_AWARE_WEIGHTED_COMPLETION){
                    // Queue-aware expected completion score: nominal transfer
                    // + nominal service + 2 x estimated queue wait.
                    // Factor 2 is pre-specified, exploratory, not fitted.
                    // All quantities are available at task arrival.
                    int choice=-1;
                    double best=Double.POSITIVE_INFINITY;
                    for(int node=0;node<NODES;node++){
                        if(!eligible.test(node))continue;
                        double score=pred[node]+vq.predictedBacklogMs(node,now);
                        if(score<best){best=score;choice=node;}
                    }
                    j=choice>=0?choice:argMin(pred,eligible);
                }else j=argMin(pred,eligible);
            }else{"""
assert s.count(old)==1
s=s.replace(old,new)
p.write_text(s)
print("QUEUE_AWARE_WEIGHTED_COMPLETION_PATCH_PASS")
