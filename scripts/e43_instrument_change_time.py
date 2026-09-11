#!/usr/bin/env python3
"""Second deterministic E4.3 observability patch: add exact change arrival time."""
from pathlib import Path
p=Path('src/main/java/org/casperiiot/e42/E42Campaign.java')
s=p.read_text()

def rep(a,b,label):
    global s
    n=s.count(a)
    if n!=1: raise SystemExit(f'{label}: expected 1 anchor, found {n}')
    s=s.replace(a,b,1)

rep(
'        final boolean[] affected=affectedMask(seed,scenario);\n',
'        final boolean[] affected=affectedMask(seed,scenario);\n        final double changeArrivalMs=tasks.get(CHANGE_TASK).arrivalMs();\n',
'change arrival')
rep(
'                    appendTrace(seed,scenario,policy,m,actualLatency,dvr,healthAlarmTrigger,e17AlarmTrigger);\n',
'                    appendTrace(seed,scenario,policy,m,changeArrivalMs,actualLatency,dvr,healthAlarmTrigger,e17AlarmTrigger);\n',
'append call')
rep(
'candidate_family_nodes,candidate_family_affected_mask,alarm_mask_at_dispatch,selected_node_alarm_at_dispatch,probe,probe_target,eta_at_dispatch',
'candidate_family_nodes,candidate_family_affected_mask,alarm_mask_at_dispatch,selected_node_alarm_at_dispatch,probe,probe_target,change_arrival_ms,eta_at_dispatch',
'header')
rep(
'private static synchronized void appendTrace(long seed,Scenario s,Policy p,DispatchMeta m,double actualLatency,boolean dvr,boolean healthTrigger,boolean e17Trigger){',
'private static synchronized void appendTrace(long seed,Scenario s,Policy p,DispatchMeta m,double changeArrivalMs,double actualLatency,boolean dvr,boolean healthTrigger,boolean e17Trigger){',
'signature')
rep(
'"%d,%s,%s,%d,%s,%.9f,%d,%s,%s,%s,%s,%s,%s,%d,%.9f,%s,%d,%s,%s,%.9f,%.9f,%s,%d,%s,%s,%s,%s",',
'"%d,%s,%s,%d,%s,%.9f,%d,%s,%s,%s,%s,%s,%s,%d,%.9f,%.9f,%s,%d,%s,%s,%.9f,%.9f,%s,%d,%s,%s,%s,%s",',
'format')
rep(
'm.selectedNodeAlarmAtDispatch,m.probe,m.probeTarget,m.etaAtDispatch,m.e17AlarmAtDispatch,',
'm.selectedNodeAlarmAtDispatch,m.probe,m.probeTarget,changeArrivalMs,m.etaAtDispatch,m.e17AlarmAtDispatch,',
'format args')
p.write_text(s)
print('E43_CHANGE_TIME_INSTRUMENTATION PASS')
