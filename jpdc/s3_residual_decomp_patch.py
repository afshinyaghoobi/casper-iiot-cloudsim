#!/usr/bin/env python3
"""Passive candidate-level S3 residual decomposition; no policy decision changes."""
from pathlib import Path
p=Path("src/main/java/org/casperiiot/e45/E45Campaign.java")
s=p.read_text()
a="        final Acc acc=new Acc();"
assert s.count(a)==1
s=s.replace(a,a+"""
        final double[] s3sums=new double[8]; // missing candidate: network increment, queue error, service error, eta, upper gap, affected, count, all candidate count
""")
a="                    for(int p=0;p<family.length;p++) if(actualAudit[p]>upper[p]) familyCovered=false;"
assert s.count(a)==1
s=s.replace(a,"""                    if(policy==Policy.CASPER_FULL && scenario==Scenario.S3_HIDDEN_NETWORK_50LOSS && t.index()>=CHANGE_TASK && t.crit()==Crit.MISSION){
                        for(int ix=0;ix<family.length;ix++){
                            int node=family[ix];
                            s3sums[7]++;
                            if(actualAudit[ix]<=upper[ix])continue;
                            double nominalNet=nominalNetworkMs(t,nodes[node]);
                            double bm=affected[node]?1.0/scenario.bwRetained:1.0;
                            double netError=nominalNet*(bm-1.0);
                            double queueError=Math.max(0.0,trueNextFree[node]-now)-vq.predictedBacklogMs(node,now);
                            double serviceError=actualServiceMs(seed,t,node,nominalServiceMs(t,nodes[node]),1.0)-nominalServiceMs(t,nodes[node]);
                            s3sums[0]+=netError;
                            s3sums[1]+=queueError;
                            s3sums[2]+=serviceError;
                            s3sums[3]+=eta;
                            s3sums[4]+=actualAudit[ix]-upper[ix];
                            if(affected[node])s3sums[5]++;
                            s3sums[6]++;
                        }
                    }
"""+a)
a="        return summarize(seed,n,scenario,policy,acc,affected);"
assert s.count(a)==1
s=s.replace(a,"""        if(policy==Policy.CASPER_FULL && scenario==Scenario.S3_HIDDEN_NETWORK_50LOSS)
            System.out.printf(java.util.Locale.US,"S3_DECOMP seed=%d missingCandidates=%.0f affectedMissCandidates=%.0f allCandidates=%.0f netIncrementSum=%.9f queueResidualSum=%.9f serviceResidualSum=%.9f etaSum=%.9f excessAboveUpperSum=%.9f%n",
                seed,s3sums[6],s3sums[5],s3sums[7],s3sums[0],s3sums[1],s3sums[2],s3sums[3],s3sums[4]);
"""+a)
p.write_text(s)
print("S3_DECOMP_PATCH_PASS")
