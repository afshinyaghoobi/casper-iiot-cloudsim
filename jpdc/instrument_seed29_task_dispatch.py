#!/usr/bin/env python3
"""Instrument generated E45 only for seed29 task-level dispatch comparison.

Writes per-task dispatch event CSV to stdout with a unique prefix. Filter the
two policies of interest to limit output; do not modify frozen E42/E4.6.
"""
from pathlib import Path
p=Path("src/main/java/org/casperiiot/e45/E45Campaign.java")
s=p.read_text()
anchor='            meta.put(cl,new DispatchMeta(t,chosenRank,j,predj,sigma,nominal,actualNet,eta,\n                    certified,familyCovered,probe));'
if s.count(anchor)!=1:
    raise SystemExit("TASK_TRACE_FAIL: deployment anchor mismatch")
trace='''            if(policy==Policy.CASPER_FULL || policy==Policy.CASPER_HEALTH_STATIC){
                System.out.printf(Locale.US,
                    "JPDC_TASK_DISPATCH,%d,%s,%s,%d,%d,%.9f,%.9f,%.9f,%b%n",
                    seed,scenario,policy,t.index(),j,eta,predj,t.deadlineMs(),certified);
            }
'''
s=s.replace(anchor,trace+anchor)
p.write_text(s)
print("TASK_TRACE_INSTRUMENTATION_PASS")
