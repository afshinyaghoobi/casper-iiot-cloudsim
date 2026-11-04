#!/usr/bin/env python3
"""Extend the generated-only forensic finish logger with native Cloudlet getStartTime.

Run AFTER jpdc/instrument_node14_event_order_generated_e45.py.
Never changes frozen E42/E4.6; refuse unexpected generated E45 sources.
"""
from pathlib import Path
p=Path("src/main/java/org/casperiiot/e45/E45Campaign.java")
s=p.read_text(encoding="utf-8")
old='''"JPDC_FORENSIC_FINISH,%d,%s,%s,%d,%d,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%d%n",
                        seed,scenario,policy,m.task.index(),m.node,
                        m.task.arrivalMs(),m.task.arrivalMs()+cl.getStartWaitTime()*1000.0,
                        sim.clock()*1000.0,cl.getStartWaitTime()*1000.0,
                        serviceMs,actualLatency,cl.getId());'''
new='''"JPDC_FORENSIC_FINISH_NATIVE,%d,%s,%s,%d,%d,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%d%n",
                        seed,scenario,policy,m.task.index(),m.node,
                        m.task.arrivalMs(),m.task.arrivalMs()+cl.getStartWaitTime()*1000.0,
                        cl.getStartTime()*1000.0,sim.clock()*1000.0,
                        cl.getStartWaitTime()*1000.0,
                        serviceMs,actualLatency,cl.getId());'''
if s.count(old)!=1 or "JPDC_FORENSIC_FINISH_NATIVE" in s:
    raise SystemExit("JPDC_NATIVE_START_INSTRUMENT_FAIL")
p.write_text(s.replace(old,new),encoding="utf-8")
print("JPDC_NATIVE_START_INSTRUMENT_PASS")
