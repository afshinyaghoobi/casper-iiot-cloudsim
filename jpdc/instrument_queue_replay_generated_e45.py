#!/usr/bin/env python3
"""Generate E45-only ALL-task queue replay trace; never edits E42 or E4.6.

Invoke after tools/e45_generate.py and optional S3 mask patch, alongside (or
independently of) the MISSION outcome sidecar. Each row is observational only.
"""
from pathlib import Path
p=Path("src/main/java/org/casperiiot/e45/E45Campaign.java")
s=p.read_text(encoding="utf-8")
anchor="""                acc.maxServiceParityErrorMs=Math.max(acc.maxServiceParityErrorMs,Math.abs(serviceMs-planned));
                final double actualLatency=m.actualNetworkMs+cl.getStartWaitTime()*1000.0+serviceMs;"""
insert=anchor+"""
                // Trace input to an independent single-server queue replay.
                // Include NORMAL tasks: they compete for the same VM capacity.
                if(scenario==Scenario.S3_HIDDEN_NETWORK_50LOSS &&
                   (policy==Policy.CASPER_FULL || policy==Policy.CASPER_HEALTH_STATIC)){
                    System.out.printf(Locale.US,
                        "JPDC_QUEUE_REPLAY,%d,%s,%s,%d,%s,%.12f,%d,%.12f,%.12f,%.12f,%.12f,%.12f%n",
                        seed,scenario,policy,m.task.index(),m.task.crit(),
                        m.task.arrivalMs(),m.node,serviceMs,
                        cl.getStartWaitTime()*1000.0,m.actualNetworkMs,
                        actualLatency,m.task.deadlineMs());
                }"""
if s.count(anchor)!=1 or "JPDC_QUEUE_REPLAY" in s:
    raise SystemExit("JPDC_QUEUE_REPLAY_PATCH_FAIL: unique generated-E45 anchor required")
p.write_text(s.replace(anchor,insert),encoding="utf-8")
print("JPDC_QUEUE_REPLAY_PATCH_PASS")
