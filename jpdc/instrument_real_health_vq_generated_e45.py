#!/usr/bin/env python3
"""Observational event tracing, *generated* E45 only, for independent Python replay."""
from pathlib import Path
p=Path("src/main/java/org/casperiiot/e45/E45Campaign.java")
s=p.read_text(encoding="utf-8")
patches=[
('''        for(int j=0;j<NODES;j++) health[j]=new NodeHealthDetector(cal.serviceThresholdByNode[j]);''',
'''        for(int j=0;j<NODES;j++) health[j]=new NodeHealthDetector(cal.serviceThresholdByNode[j]);
        if(policy==Policy.CASPER_FULL && scenario==Scenario.S3_HIDDEN_NETWORK_50LOSS){
            for(int node=0;node<NODES;node++)
                System.out.printf(Locale.US,"JPDC_HV_THRESHOLD,%d,%d,%.17g%n",seed,node,cal.serviceThresholdByNode[node]);
        }'''),
('''                    health[m.node].observe(serviceMs,m.nominalServiceMs);''',
'''                    health[m.node].observe(serviceMs,m.nominalServiceMs);
                    if(policy==Policy.CASPER_FULL && scenario==Scenario.S3_HIDDEN_NETWORK_50LOSS)
                        System.out.printf(Locale.US,"JPDC_HV_FINISH,%d,%d,%d,%.17g,%.17g,%b%n",
                            seed,m.task.index(),m.node,serviceMs,m.nominalServiceMs,health[m.node].isAlarmed());'''),
('''            if(now>=nextTelemetry[0]){
                vq.resetFromTelemetry(trueNextFree);''',
'''            if(now>=nextTelemetry[0]){
                if(policy==Policy.CASPER_FULL && scenario==Scenario.S3_HIDDEN_NETWORK_50LOSS)
                    System.out.printf(Locale.US,"JPDC_HV_TELEMETRY,%d,%d,%s%n",
                        seed,t.index(),Arrays.toString(trueNextFree).replace(",",";"));
                vq.resetFromTelemetry(trueNextFree);'''),
('''            final double[] pred=predictedLatency(t,nodes,vq,now);
            final boolean[] alarmMask=new boolean[NODES];''',
'''            final double[] pred=predictedLatency(t,nodes,vq,now);
            final boolean[] alarmMask=new boolean[NODES];'''),
('''            if(policy.health) for(int j=0;j<NODES;j++) alarmMask[j]=health[j].isAlarmed();

            final IntPredicate baseEligible''',
'''            if(policy.health) for(int j=0;j<NODES;j++) alarmMask[j]=health[j].isAlarmed();
            if(policy==Policy.CASPER_FULL && scenario==Scenario.S3_HIDDEN_NETWORK_50LOSS){
                final double[] backlogSnapshot=new double[NODES];
                for(int node=0;node<NODES;node++)backlogSnapshot[node]=vq.predictedBacklogMs(node,now);
                System.out.printf(Locale.US,"JPDC_HV_PRE,%d,%d,%.17g,%s,%s%n",
                    seed,t.index(),now,Arrays.toString(backlogSnapshot).replace(",",";"),
                    Arrays.toString(alarmMask).replace(",",";"));
            }

            final IntPredicate baseEligible'''),
('''            vq.onDispatch(j,now,nominal);

            final long ns=System.nanoTime()-wall0;''',
'''            vq.onDispatch(j,now,nominal);
            if(policy==Policy.CASPER_FULL && scenario==Scenario.S3_HIDDEN_NETWORK_50LOSS)
                System.out.printf(Locale.US,"JPDC_HV_POST,%d,%d,%d,%.17g,%.17g,%.17g%n",
                    seed,t.index(),j,now,nominal,vq.predictedNextFreeMs(j));

            final long ns=System.nanoTime()-wall0;''')
]
# The pred no-op entry intentionally excluded from the rewrite.
for old,new in patches:
    if old==new:continue
    if s.count(old)!=1:raise SystemExit("JPDC_HV_PATCH_FAIL anchor count="+str(s.count(old))+" "+old[:90])
    s=s.replace(old,new)
if s.count("JPDC_HV_THRESHOLD")!=1 or s.count("JPDC_HV_PRE")!=1 or s.count("JPDC_HV_POST")!=1:
    raise SystemExit("JPDC_HV_PATCH_FAIL missing logger after replacement")
p.write_text(s,encoding="utf-8")
print("JPDC_HV_GENERATED_ONLY_INSTRUMENT_PASS")
