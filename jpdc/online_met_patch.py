#!/usr/bin/env python3
"""Online arrival-by-arrival adaptation of Braun et al. MET mapping; NOT static MET batch."""
from pathlib import Path
p=Path("src/main/java/org/casperiiot/e45/E45Campaign.java")
s=p.read_text()
token="        PRED_GREEDY(false,false,false,false),"
assert s.count(token)==1
s=s.replace(token,token+"\n        ONLINE_MET_ADAPTED(false,false,false,false),")
old="            if(!policy.cp){\n                j=argMin(pred,eligible);\n            }else{"
new="""            if(!policy.cp){
                if(policy==Policy.ONLINE_MET_ADAPTED){
                    // Minimum execution-time mapping: ignore transfer and queue.
                    // Adapted to single job online arrivals; this is not an
                    // implementation of Braun et al.'s complete static batch setting.
                    int selected=-1;
                    double minCompute=Double.POSITIVE_INFINITY;
                    for(int node=0;node<NODES;node++){
                        if(!eligible.test(node))continue;
                        final double duration=nominalServiceMs(t,nodes[node]);
                        if(duration<minCompute){
                            minCompute=duration;
                            selected=node;
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
print("ONLINE_MET_ADAPTED_PATCH_PASS")
