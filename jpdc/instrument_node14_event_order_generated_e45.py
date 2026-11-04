#!/usr/bin/env python3
"""Forensic logger, generated E45 only: task 10898..10902 arrival/mapper/derived start.

CloudSimPlus 8.5.7 Cloudlet does not expose getExecStartTime() here; 
finish row derives effective start from arrival + getStartWaitTime().
This is NOT an independent scheduler start event.
"""
from pathlib import Path

campaign=Path("src/main/java/org/casperiiot/e45/E45Campaign.java")
s=campaign.read_text(encoding="utf-8")
mapper="""            meta.put(cl,new DispatchMeta(t,chosenRank,j,predj,sigma,nominal,actualNet,eta,
                    certified,familyCovered,probe));
            return vms.get(j);"""
newmapper="""            meta.put(cl,new DispatchMeta(t,chosenRank,j,predj,sigma,nominal,actualNet,eta,
                    certified,familyCovered,probe));
            if(scenario==Scenario.S3_HIDDEN_NETWORK_50LOSS &&
               (policy==Policy.CASPER_FULL || policy==Policy.CASPER_HEALTH_STATIC) &&
               t.index()>=10898 && t.index()<=10902){
                System.out.printf(Locale.US,
                    "JPDC_FORENSIC_MAPPER,%d,%s,%s,%d,%d,%.12f,%.12f,%d,%d%n",
                    seed,scenario,policy,t.index(),j,t.arrivalMs(),
                    sim.clock()*1000.0,cl.getId(),vms.get(j).getId());
            }
            return vms.get(j);"""
finished="""                final double actualLatency=m.actualNetworkMs+cl.getStartWaitTime()*1000.0+serviceMs;"""
newfinished=finished+"""
                if(scenario==Scenario.S3_HIDDEN_NETWORK_50LOSS &&
                   (policy==Policy.CASPER_FULL || policy==Policy.CASPER_HEALTH_STATIC) &&
                   m.task.index()>=10898 && m.task.index()<=10902){
                    System.out.printf(Locale.US,
                        "JPDC_FORENSIC_FINISH,%d,%s,%s,%d,%d,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%d%n",
                        seed,scenario,policy,m.task.index(),m.node,
                        m.task.arrivalMs(),m.task.arrivalMs()+cl.getStartWaitTime()*1000.0,
                        sim.clock()*1000.0,cl.getStartWaitTime()*1000.0,
                        serviceMs,actualLatency,cl.getId());
                }"""
if s.count(mapper)!=1 or s.count(finished)!=1 or "JPDC_FORENSIC_" in s:
    raise SystemExit("JPDC_FORENSIC_CAMPAIGN_PATCH_FAIL")
s=s.replace(mapper,newmapper).replace(finished,newfinished)
campaign.write_text(s,encoding="utf-8")

arrival=Path("src/main/java/org/casperiiot/e45/E45ArrivalSource.java")
a=arrival.read_text(encoding="utf-8")
anchor="""        submitTask.accept(task);"""
newanchor="""        if(task>=10898 && task<=10902){
            System.out.printf(java.util.Locale.US,
                "JPDC_FORENSIC_ARRIVAL,%d,%.12f,%.12f%n",
                task,arrivalSec[task]*1000.0,getSimulation().clock()*1000.0);
        }
        submitTask.accept(task);"""
if a.count(anchor)!=1 or "JPDC_FORENSIC_" in a:
    raise SystemExit("JPDC_FORENSIC_ARRIVAL_PATCH_FAIL")
arrival.write_text(a.replace(anchor,newanchor),encoding="utf-8")
print("JPDC_FORENSIC_INSTRUMENT_PASS")
