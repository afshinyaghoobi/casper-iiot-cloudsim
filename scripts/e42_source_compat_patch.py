#!/usr/bin/env python3
from pathlib import Path

p = Path('src/main/java/org/casperiiot/e42/E42Campaign.java')
s = p.read_text()

repls = [
    (2,
        'final double serviceMs=cl.getActualCpuTime()*1000.0;',
        'final double serviceMs=(cl.getFinishTime()-cl.getStartTime())*1000.0;'
    ),
    (1,
        'm.actualNetworkMs + cl.getWaitingTime()*1000.0 + serviceMs',
        'm.actualNetworkMs + cl.getStartWaitTime()*1000.0 + serviceMs'
    ),
    (1,
        'm.actualNetworkMs+cl.getWaitingTime()*1000.0+serviceMs',
        'm.actualNetworkMs+cl.getStartWaitTime()*1000.0+serviceMs'
    ),
    (1,
        'final double predictedLatencyMs, sigmaMs, nominalServiceMs, actualNetworkMs;\n        final boolean certified, familyCovered, probe;\n        DispatchMeta(Task t,int rank,int node,double pred,double sigma,double nominal,double net,\n                     boolean cert,boolean fwc,boolean probe){\n            task=t;this.rank=rank;this.node=node;predictedLatencyMs=pred;sigmaMs=sigma;\n            nominalServiceMs=nominal;actualNetworkMs=net;certified=cert;familyCovered=fwc;this.probe=probe;',
        'final double predictedLatencyMs, sigmaMs, nominalServiceMs, actualNetworkMs, etaAtDispatch;\n        final boolean certified, familyCovered, probe;\n        DispatchMeta(Task t,int rank,int node,double pred,double sigma,double nominal,double net,double eta,\n                     boolean cert,boolean fwc,boolean probe){\n            task=t;this.rank=rank;this.node=node;predictedLatencyMs=pred;sigmaMs=sigma;\n            nominalServiceMs=nominal;actualNetworkMs=net;etaAtDispatch=eta;certified=cert;familyCovered=fwc;this.probe=probe;'
    ),
    (1,
        'meta.put(cl,new DispatchMeta(t,rank,j,predj,sigma,nominal,\n                    nominalNetworkMs(t,nodes[j]),false,true,probe));',
        'meta.put(cl,new DispatchMeta(t,rank,j,predj,sigma,nominal,\n                    nominalNetworkMs(t,nodes[j]),1.0,false,true,probe));'
    ),
    (1,
        'meta.put(cl,new DispatchMeta(t,chosenRank,j,predj,sigma,nominal,actualNet,\n                    certified,familyCovered,probe));',
        'meta.put(cl,new DispatchMeta(t,chosenRank,j,predj,sigma,nominal,actualNet,eta,\n                    certified,familyCovered,probe));'
    ),
    (1,
        'policy.adaptive?e17.etaBeforeOutcome():1.0));',
        'm.etaAtDispatch));'
    ),
    (1,
        'final List<MissionRec> post=a.mission.stream().filter(MissionRec::post).toList();',
        'final List<MissionRec> ordered=a.mission.stream().sorted(Comparator.comparingInt(MissionRec::taskIndex)).toList();\n        final List<MissionRec> post=ordered.stream().filter(MissionRec::post).toList();'
    ),
    (1,
        'if(health[m.node].isAlarmed() && !affected[m.node] && !acc.countedFalseAlarm[m.node]){\n                        acc.countedFalseAlarm[m.node]=true;\n                        acc.healthyFalseAlarmNodes++;\n                    }',
        'final boolean trueComputeDegraded = scenario.computeRetained < 1.0 && affected[m.node];\n                    if(health[m.node].isAlarmed() && !trueComputeDegraded && !acc.countedFalseAlarm[m.node]){\n                        acc.countedFalseAlarm[m.node]=true;\n                        acc.healthyFalseAlarmNodes++;\n                    }'
    )
]

for expected, old, new in repls:
    count = s.count(old)
    if count != expected:
        raise SystemExit(f'PATCH REFUSED: expected {expected} occurrence(s), found {count}: {old[:80]!r}')
    s = s.replace(old, new)

if 'getActualCpuTime()' in s or 'getWaitingTime()' in s:
    raise SystemExit('PATCH REFUSED: legacy Cloudlet API remains')

required = [
    'getFinishTime()-cl.getStartTime()',
    'getStartWaitTime()',
    'etaAtDispatch',
    'Comparator.comparingInt(MissionRec::taskIndex)',
    'trueComputeDegraded = scenario.computeRetained < 1.0 && affected[m.node]'
]
for token in required:
    if token not in s:
        raise SystemExit(f'PATCH REFUSED: required token missing after patch: {token}')

p.write_text(s)
print('E42_SOURCE_COMPAT_PATCH PASS')
print('Scientific parameters changed: NO')
print('Fixes: Cloudlet 8.5.7 API, arrival-order reporting, dispatch-time eta provenance, health false-positive truth label')
