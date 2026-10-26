#!/usr/bin/env python3
from pathlib import Path
p=Path("src/main/java/org/casperiiot/e45/E45Campaign.java")
s=p.read_text()
a="        final Acc acc=new Acc();"
assert s.count(a)==1
s=s.replace(a,a+"""
        final long[] s3audit=new long[6]; // post mission families, families with affected, misses, misses affected, candidate audits, affected candidates
""")
a="                    for(int p=0;p<family.length;p++) if(actualAudit[p]>upper[p]) familyCovered=false;"
assert s.count(a)==1
s=s.replace(a,"""                    if(policy==Policy.CASPER_FULL && scenario==Scenario.S3_HIDDEN_NETWORK_50LOSS && t.index()>=CHANGE_TASK && t.crit()==Crit.MISSION){
                        s3audit[0]++;
                        boolean anyAffected=false;
                        boolean missAffected=false;
                        for(int ix=0;ix<family.length;ix++){
                            int node=family[ix];
                            s3audit[4]++;
                            if(affected[node]){s3audit[5]++;anyAffected=true;}
                            if(actualAudit[ix]>upper[ix] && affected[node])missAffected=true;
                        }
                        if(anyAffected)s3audit[1]++;
                        if(missAffected)s3audit[3]++;
                    }
"""+a+"""
                    if(policy==Policy.CASPER_FULL && scenario==Scenario.S3_HIDDEN_NETWORK_50LOSS && t.index()>=CHANGE_TASK && t.crit()==Crit.MISSION && !familyCovered)s3audit[2]++;
""")
a="        return summarize(seed,n,scenario,policy,acc,affected);"
assert s.count(a)==1
s=s.replace(a,"""        if(policy==Policy.CASPER_FULL && scenario==Scenario.S3_HIDDEN_NETWORK_50LOSS)
            System.out.printf(java.util.Locale.US,"S3_AUDIT seed=%d postMission=%d familyAffected=%d familyMiss=%d affectedMiss=%d candidates=%d affectedCandidates=%d%n",
                seed,s3audit[0],s3audit[1],s3audit[2],s3audit[3],s3audit[4],s3audit[5]);
"""+a)
p.write_text(s)
print("S3_AUDIT_PATCH_PASS")
