#!/usr/bin/env python3
"""Generated E45-only observation-time eta feedback instrumentation (no scientific changes)."""
from pathlib import Path
p=Path("src/main/java/org/casperiiot/e45/E45Campaign.java")
s=p.read_text()
old="""                if(policy.adaptive && m.task.crit()==Crit.MISSION){
                    final double score=Math.max(0.0,(actualLatency-m.predictedLatencyMs)/(m.sigmaMs+1e-12));
                    e17.observe(score);
                }"""
new="""                if(policy.adaptive && m.task.crit()==Crit.MISSION){
                    final double score=Math.max(0.0,(actualLatency-m.predictedLatencyMs)/(m.sigmaMs+1e-12));
                    final double jpdcEtaBefore=e17.etaBeforeOutcome();
                    final boolean jpdcAlarmBefore=e17.alarmEver();
                    final int jpdcAgeBefore=e17.transitionAge();
                    final double jpdcReference=e17.referenceQ95();
                    e17.observe(score);
                    System.out.printf(Locale.US,
                        "JPDC_ETA_FEEDBACK,%d,%s,%s,%d,%.12f,%.12f,%.12f,%.12f,%.12f,%b,%b,%d,%d%n",
                        seed,scenario,policy,m.task.index(),score,jpdcReference,
                        m.etaAtDispatch,jpdcEtaBefore,e17.etaBeforeOutcome(),
                        jpdcAlarmBefore,e17.alarmEver(),jpdcAgeBefore,e17.transitionAge());
                }"""
assert s.count(old)==1, f"instrument anchor mismatch: {s.count(old)}"
p.write_text(s.replace(old,new))
print("JPDC_ETA_FEEDBACK_INSTRUMENT_PASS")
