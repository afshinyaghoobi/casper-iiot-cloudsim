#!/usr/bin/env python3
"""Stage6 synthetic no-oracle bounded NORMAL probes with full feedback timing."""
import math
from normal_network_probe_stage6 import NormalNetworkProbe,NODES
from independent_network_probe_stage6 import PROBE_POLICY,NEW_POLICY
a=NormalNetworkProbe()
pred=[30.0]*NODES
pred[0]=10.0;pred[1]=11.0
for _ in range(50):a.observe_completed_e2e(0)
for k in range(99):
    j,attempted,changed=a.pick(pred,40,0,True)
    assert (j,attempted,changed)==(0,False,False)
j,attempted,changed=a.pick(pred,40,0,True)
assert (j,attempted,changed)==(1,True,True)
a.assert_valid()
assert a.opportunities==a.attempts==a.changed_decisions==1
print("PASS starvation case: bounded probe reroutes NORMAL to previously unobserved eligible node")
for _ in range(99):a.pick(pred,40,0,True)
j,attempted,changed=a.pick(pred,1,0,True)
assert (j,attempted,changed)==(0,False,False)
assert a.skipped_empty==1 and a.opportunities==2
print("PASS empty nominal deadline-eligible set skips probe, counts opportunity")
for _ in range(500):
    j,attempt,changed=a.pick(pred,40,0,False)
    assert (j,attempt,changed)==(0,False,False)
assert a.normal_arrivals==200 and a.opportunities==2
assert a.attempts<=a.normal_arrivals//100
print("PASS MISSION never probed, fixed <=1% NORMAL budget")
for malformed in ([-1.0]*21,[1.0]*20,[math.nan]+[1.]*20):
    try:a.pick(malformed,30,0,True)
    except ValueError:pass
    else:raise AssertionError("malformed predictor vector accepted")
for node in (-1,21):
    try:a.observe_completed_e2e(node)
    except ValueError:pass
    else:raise AssertionError("invalid feedback node accepted")
print("PASS no affected-node mask, no physical future input, malformed state fail closed")
print("JPDC_STAGE6_PROBE_POLICY_UNIT_PASS")
