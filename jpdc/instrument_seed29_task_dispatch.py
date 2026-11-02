#!/usr/bin/env python3
"""Instrument generated E45 only for seed29 task-level dispatch comparison.

Writes per-task dispatch event CSV to stdout with a unique prefix. Filter the
two policies of interest to limit output; do not modify frozen E42/E4.6.
"""
from pathlib import Path
p=Path("src/main/java/org/casperiiot/e45/E45Campaign.java")
s=p.read_text()
anchor='            final long ns=System.nanoTime()-wall0;\n            acc.mapperNsSum+=ns; acc.mapperCalls++;\n            meta.put(cl,new DispatchMeta(t,chosenRank,j,predj,sigma,nominal,actualNet,eta,\n                    certified,familyCovered,probe));'
if s.count(anchor)!=1:
    raise SystemExit("TASK_TRACE_FAIL: deployment anchor mismatch")
trace='''            if(policy==Policy.CASPER_FULL || policy==Policy.CASPER_HEALTH_STATIC){
                System.out.printf(Locale.US,
                    "JPDC_TASK_DISPATCH,%d,%s,%s,%d,%d,%.9f,%.9f,%.9f,%b,%.3f,%b%n",
                    seed,scenario,policy,t.index(),j,eta,predj,t.deadlineMs(),certified,ns/1000.0,familyCovered);
            }
'''
s=s.replace(anchor,anchor.replace('            meta.put(',trace+'            meta.put('))
finish_anchor='''                final double actualLatency=m.actualNetworkMs+cl.getStartWaitTime()*1000.0+serviceMs;'''
finish_trace='''                if(policy==Policy.CASPER_FULL || policy==Policy.CASPER_HEALTH_STATIC){
                    System.out.printf(Locale.US,
                        "JPDC_TASK_OUTCOME,%d,%s,%s,%d,%d,%.9f,%.9f,%b,%b%n",
                        seed,scenario,policy,m.task.index(),m.node,
                        actualLatency,m.task.deadlineMs(),
                        actualLatency>m.task.deadlineMs(),
                        m.task.crit()==Crit.MISSION);
                }
'''
if s.count(finish_anchor)!=1:
    raise SystemExit("TASK_TRACE_FAIL: finish anchor mismatch")
s=s.replace(finish_anchor,finish_anchor+"\n"+finish_trace)

p.write_text(s)
print("TASK_TRACE_INSTRUMENTATION_PASS")
