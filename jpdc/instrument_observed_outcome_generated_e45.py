#!/usr/bin/env python3
"""Observational only: instrument actual MISSION outcomes in GENERATED E45.

Apply after tools/e45_generate.py and any mask/eta intervention patches.
Fails closed against unexpected generated source; never edits frozen E42/E4.6.
"""
from pathlib import Path

path = Path("src/main/java/org/casperiiot/e45/E45Campaign.java")
src = path.read_text(encoding="utf-8")
old = """                    acc.mission.add(new MissionRec(m.task.index(),m.task.index()>=CHANGE_TASK,
                            m.familyCovered,!m.certified,far,dvr,actualLatency,
                            m.etaAtDispatch));"""
new = old + """
                    // JPDC observational sidecar only; no dispatch/feedback modification.
                    if(scenario==Scenario.S3_HIDDEN_NETWORK_50LOSS &&
                       (policy==Policy.CASPER_FULL || policy==Policy.CASPER_HEALTH_STATIC)){
                        System.out.printf(Locale.US,
                            "JPDC_OBSERVED_OUTCOME,%d,%s,%s,%d,%d,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%b,%b,%b,%b%n",
                            seed,scenario,policy,m.task.index(),m.node,m.etaAtDispatch,
                            m.predictedLatencyMs,m.actualNetworkMs,cl.getStartWaitTime()*1000.0,
                            serviceMs,actualLatency,m.task.deadlineMs(),m.certified,
                            m.familyCovered,dvr,far);
                    }"""
if src.count(old) != 1 or "JPDC_OBSERVED_OUTCOME" in src:
    raise SystemExit("JPDC_OUTCOME_INSTRUMENT_FAIL: expected one uninstrumented E45 anchor")
path.write_text(src.replace(old, new), encoding="utf-8")
print("JPDC_OUTCOME_INSTRUMENT_PASS")
