#!/usr/bin/env python3
"""Append CloudSim-native datacenter arrival to already generated native-start forensic logger."""
from pathlib import Path
p=Path("src/main/java/org/casperiiot/e45/E45Campaign.java")
s=p.read_text(encoding="utf-8")
old='''"JPDC_FORENSIC_FINISH_NATIVE,%d,%s,%s,%d,%d,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%d%n",
                        seed,scenario,policy,m.task.index(),m.node,
                        m.task.arrivalMs(),m.task.arrivalMs()+cl.getStartWaitTime()*1000.0,
                        cl.getStartTime()*1000.0,sim.clock()*1000.0,
                        cl.getStartWaitTime()*1000.0,
                        serviceMs,actualLatency,cl.getId());'''
new='''"JPDC_FORENSIC_FINISH_DC,%d,%s,%s,%d,%d,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%d%n",
                        seed,scenario,policy,m.task.index(),m.node,
                        m.task.arrivalMs(),m.task.arrivalMs()+cl.getStartWaitTime()*1000.0,
                        cl.getStartTime()*1000.0,cl.getDcArrivalTime()*1000.0,sim.clock()*1000.0,
                        cl.getStartWaitTime()*1000.0,
                        serviceMs,actualLatency,cl.getId());'''
if s.count(old)!=1 or "JPDC_FORENSIC_FINISH_DC" in s:
    raise SystemExit("JPDC_DC_ARRIVAL_PATCH_FAIL")
p.write_text(s.replace(old,new),encoding="utf-8")
print("JPDC_DC_ARRIVAL_INSTRUMENT_PASS")
