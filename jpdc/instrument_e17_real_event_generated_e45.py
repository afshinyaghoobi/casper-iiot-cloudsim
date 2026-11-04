#!/usr/bin/env python3
"""Read-only E17 event stream instrumentation on generated E45, never E42/E4.6."""
from pathlib import Path
p=Path("src/main/java/org/casperiiot/e45/E45Campaign.java")
s=p.read_text(encoding="utf-8")
ref='''        final E17DualMemory e17=policy.adaptive?new E17DualMemory(cal.referenceScores):null;'''
refnew=ref+'''
        if(policy==Policy.CASPER_FULL && scenario==Scenario.S3_HIDDEN_NETWORK_50LOSS){
            for(int i=0;i<cal.referenceScores.length;i++)
                System.out.printf(Locale.US,"JPDC_E17_REFERENCE,%d,%d,%.17g%n",seed,i,cal.referenceScores[i]);
        }'''
eta='''            final double eta=policy.adaptive?e17.etaBeforeOutcome():1.0;'''
etanew=eta+'''
            if(policy==Policy.CASPER_FULL && scenario==Scenario.S3_HIDDEN_NETWORK_50LOSS){
                System.out.printf(Locale.US,"JPDC_E17_DISPATCH,%d,%d,%.17g,%b,%d%n",
                    seed,t.index(),eta,e17.alarmEver(),e17.transitionAge());
            }'''
observed='''                    e17.observe(score);'''
observednew=observed+'''
                    if(policy==Policy.CASPER_FULL && scenario==Scenario.S3_HIDDEN_NETWORK_50LOSS){
                        System.out.printf(Locale.US,"JPDC_E17_OBSERVE,%d,%d,%.17g,%b,%d%n",
                            seed,m.task.index(),score,e17.alarmEver(),e17.transitionAge());
                    }'''
for anchor in (ref,eta,observed):
    if s.count(anchor)!=1:raise SystemExit("JPDC_E17_EVENT_PATCH_FAIL: expected one source anchor")
if "JPDC_E17_REFERENCE" in s:raise SystemExit("JPDC_E17_EVENT_PATCH_FAIL: duplicate")
s=s.replace(ref,refnew).replace(eta,etanew).replace(observed,observednew)
p.write_text(s,encoding="utf-8")
print("JPDC_E17_REAL_EVENT_PATCH_PASS")
