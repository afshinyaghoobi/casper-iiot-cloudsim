#!/usr/bin/env python3
"""FiFSA-inspired arrival-only first-idle-tier control for generated E45.

NOT a reproduction of FiFSA: original FiFSA sorts a job queue and uses
capacity reservations. This adaptation uses current virtual backlog only.
"""
from pathlib import Path
p = Path("src/main/java/org/casperiiot/e45/E45Campaign.java")
s = p.read_text()
enum = "        PRED_GREEDY(false,false,false,false),"
dispatch = """            if(!policy.cp){
                j=argMin(pred,eligible);
            }else{"""
assert s.count(enum) == 1, "enum anchor changed"
assert s.count(dispatch) == 1, "dispatch anchor changed"
s = s.replace(enum, enum + "\n        FIRST_IDLE_TIER(false,false,false,false),")
replacement = """            if(!policy.cp){
                if(policy==Policy.FIRST_IDLE_TIER){
                    // Adaptation only: fixed index order edge 0..11, middle
                    // 12..17. No queue sorting, no future tasks, no true state.
                    // A node is idle iff its online virtual backlog is zero.
                    // If all fog nodes busy, send to best predicted cloud node.
                    int choice=-1;
                    for(int node=0;node<18;node++){
                        if(eligible.test(node) &&
                                vq.predictedBacklogMs(node,now)<=1e-9){
                            choice=node;break;
                        }
                    }
                    if(choice<0) choice=argMin(pred,node->node>=18 && eligible.test(node));
                    j=choice>=0?choice:argMin(pred,eligible);
                }else j=argMin(pred,eligible);
            }else{"""
s = s.replace(dispatch, replacement)
p.write_text(s)
print("FIRST_IDLE_TIER_PATCH_PASS")
