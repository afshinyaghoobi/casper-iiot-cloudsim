#!/usr/bin/env python3
"""Unfrozen, independent JPDC pilot baseline. Never edits E42 frozen source."""
from pathlib import Path
p=Path("src/main/java/org/casperiiot/e45/E45Campaign.java")
s=p.read_text()
old="        PRED_GREEDY(false,false,false,false),"
assert s.count(old)==1
s=s.replace(old,old+"\n        DEADLINE_CAPACITY_PRESERVING(false,false,false,false),")
old="            if(!policy.cp){\n                j=argMin(pred,eligible);\n            }else{"
new="""            if(!policy.cp){
                if(policy==Policy.DEADLINE_CAPACITY_PRESERVING){
                    // Reserve faster nodes when a slower node is predicted to
                    // satisfy the task deadline; fallback to greedy.
                    int selected=-1;
                    double capacity=Double.POSITIVE_INFINITY;
                    for(int node=0;node<NODES;node++){
                        if(!eligible.test(node))continue;
                        if(pred[node]<=t.deadlineMs() && nodes[node].cap()<capacity){
                            selected=node;
                            capacity=nodes[node].cap();
                        }
                    }
                    j=selected>=0?selected:argMin(pred,eligible);
                }else{
                    j=argMin(pred,eligible);
                }
            }else{"""
assert s.count(old)==1
s=s.replace(old,new)
p.write_text(s)
print("JPDC_UNFROZEN_BASELINE_PATCH_PASS")
