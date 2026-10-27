#!/usr/bin/env python3
"""Passive S3 all-candidate residual measurements and chronological eta windows."""
from pathlib import Path
p=Path("src/main/java/org/casperiiot/e45/E45Campaign.java")
s=p.read_text()
anchor="        final Acc acc=new Acc();"
assert s.count(anchor)==1
s=s.replace(anchor,anchor+"""
        // Three sequential post-shock index windows: [10000,16667), [16667,23334), [23334,30000).
        final double[][] s3all=new double[3][8]; // count,affected,miss,net,absQueue,absService,eta,etaSquared
""")
anchor="                    for(int p=0;p<family.length;p++) if(actualAudit[p]>upper[p]) familyCovered=false;"
assert s.count(anchor)==1
s=s.replace(anchor,"""                    if(policy==Policy.CASPER_FULL && scenario==Scenario.S3_HIDDEN_NETWORK_50LOSS && t.index()>=CHANGE_TASK && t.crit()==Crit.MISSION){
                        final int window=t.index()<16667?0:(t.index()<23334?1:2);
                        for(int ix=0;ix<family.length;ix++){
                            final int node=family[ix];
                            final double nomNet=nominalNetworkMs(t,nodes[node]);
                            final double shock=affected[node]?1.0/scenario.bwRetained:1.0;
                            final double queueErr=Math.max(0.0,trueNextFree[node]-now)-vq.predictedBacklogMs(node,now);
                            final double nomSvc=nominalServiceMs(t,nodes[node]);
                            final double svcErr=actualServiceMs(seed,t,node,nomSvc,1.0)-nomSvc;
                            s3all[window][0]++;
                            if(affected[node])s3all[window][1]++;
                            if(actualAudit[ix]>upper[ix])s3all[window][2]++;
                            s3all[window][3]+=nomNet*(shock-1.0);
                            s3all[window][4]+=Math.abs(queueErr);
                            s3all[window][5]+=Math.abs(svcErr);
                            s3all[window][6]+=eta;
                            s3all[window][7]+=eta*eta;
                        }
                    }
"""+anchor)
anchor="        return summarize(seed,n,scenario,policy,acc,affected);"
assert s.count(anchor)==1
s=s.replace(anchor,"""        if(policy==Policy.CASPER_FULL && scenario==Scenario.S3_HIDDEN_NETWORK_50LOSS){
            for(int win=0;win<3;win++){
                double[] x=s3all[win];
                System.out.printf(java.util.Locale.US,"S3_ALL seed=%d window=%d count=%.0f affected=%.0f misses=%.0f networkMs=%.9f absQueueMs=%.9f absServiceMs=%.9f etaSum=%.9f etaSqSum=%.9f%n",
                  seed,win,x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7]);
            }
        }
"""+anchor)
p.write_text(s)
print("S3_ALL_CANDIDATE_PATCH_PASS")
