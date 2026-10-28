#!/usr/bin/env python3
"""Experimental deadline-feasible minimum-uncertainty policy, generated E45 only.
Standalone algorithmic control, NOT a literature-faithful SOTA baseline.
"""
from pathlib import Path
p=Path("src/main/java/org/casperiiot/e45/E45Campaign.java")
s=p.read_text()
old="        PRED_GREEDY(false,false,false,false),"
assert s.count(old)==1
s=s.replace(old,old+"\n        DEADLINE_FEASIBLE_MIN_UNCERTAINTY(false,false,false,false),")
old="""            if(!policy.cp){
                j=argMin(pred,eligible);
            }else{"""
new="""            if(!policy.cp){
                if(policy==Policy.DEADLINE_FEASIBLE_MIN_UNCERTAINTY){
                    // Online lexicographic rule: if any predicted candidate meets
                    // the deadline, minimize fixedSigma among feasible candidates.
                    // Otherwise minimize predicted latency. Never read actual shock.
                    int choice=-1;
                    double bestSigma=Double.POSITIVE_INFINITY;
                    double bestLatency=Double.POSITIVE_INFINITY;
                    boolean foundFeasible=false;
                    for(int node=0;node<NODES;node++){
                        if(!eligible.test(node))continue;
                        double latency=pred[node];
                        double sig=fixedSigma(latency,nodes[node].sigmaMult());
                        boolean feasible=latency<=t.deadlineMs();
                        if(feasible){
                            if(!foundFeasible || sig<bestSigma ||
                                    (sig==bestSigma && latency<bestLatency)){
                                choice=node;bestSigma=sig;bestLatency=latency;
                            }
                            foundFeasible=true;
                        }else if(!foundFeasible && latency<bestLatency){
                            choice=node;bestLatency=latency;bestSigma=sig;
                        }
                    }
                    j=choice>=0?choice:argMin(pred,eligible);
                }else j=argMin(pred,eligible);
            }else{"""
assert s.count(old)==1
p.write_text(s.replace(old,new))
print("DEADLINE_FEASIBLE_PATCH_PASS")
