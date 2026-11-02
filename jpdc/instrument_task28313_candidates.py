#!/usr/bin/env python3
"""Log the actual ranked candidates and certificate upper bounds for task 28313; generated E45 only."""
from pathlib import Path
p=Path("src/main/java/org/casperiiot/e45/E45Campaign.java")
s=p.read_text()
anchor="                    for(int p=0;p<family.length;p++) if(actualAudit[p]>upper[p]) familyCovered=false;"
assert s.count(anchor)==1, "candidate anchor missing/duplicated"
extra='''                    if(t.index()==28313 && scenario==Scenario.S3_HIDDEN_NETWORK_50LOSS &&
                       (policy==Policy.CASPER_FULL || policy==Policy.CASPER_HEALTH_STATIC)){
                        for(int p=0;p<family.length;p++){
                            System.out.printf(Locale.US,
                                "JPDC_28313_CANDIDATE,%d,%s,%s,%d,%d,%.12f,%.12f,%.12f,%.12f,%.12f,%b%n",
                                seed,scenario,policy,p+1,family[p],eta,pred[family[p]],upper[p],
                                t.deadlineMs(),actualAudit[p],upper[p]<=t.deadlineMs());
                        }
                    }
'''
s=s.replace(anchor,extra+anchor)
p.write_text(s)
print("CANDIDATE_28313_INSTRUMENT_PASS")
