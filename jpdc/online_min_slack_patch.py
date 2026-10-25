#!/usr/bin/env python3
"""Add a genuine online least-slack-first feasible-dispatch heuristic, NOT original HEFT."""
from pathlib import Path
p=Path("src/main/java/org/casperiiot/e45/E45Campaign.java")
s=p.read_text()
old="        PRED_GREEDY(false,false,false,false),"
assert s.count(old)==1
s=s.replace(old,old+"\n        ONLINE_MIN_FEASIBLE_SLACK(false,false,false,false),")
old="            if(!policy.cp){\n                j=argMin(pred,eligible);\n            }else{"
new="""            if(!policy.cp){
                if(policy==Policy.ONLINE_MIN_FEASIBLE_SLACK){
                    // Of nodes predicted to meet deadline, choose minimum nonnegative slack.
                    // If none predicted feasible, minimize predicted latency as fallback.
                    int best=-1;
                    double bestSlack=Double.POSITIVE_INFINITY;
                    for(int node=0;node<NODES;node++){
                        if(!eligible.test(node))continue;
                        final double slack=t.deadlineMs()-pred[node];
                        if(slack>=0 && slack<bestSlack){
                            best=node;bestSlack=slack;
                        }
                    }
                    j=best>=0?best:argMin(pred,eligible);
                }else{
                    j=argMin(pred,eligible);
                }
            }else{"""
assert s.count(old)==1
s=s.replace(old,new)
p.write_text(s)
print("ONLINE_MIN_FEASIBLE_SLACK_PATCH_PASS")
