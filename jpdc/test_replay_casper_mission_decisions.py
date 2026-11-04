#!/usr/bin/env python3
"""Falsification tests: independent cross-language CASPER rank/certificate replay."""
import csv,tempfile
from pathlib import Path
from replay_casper_mission_decisions import replay,audit

POLS=("CASPER_FULL","CASPER_HEALTH_STATIC")
def arrays(x):
    return "["+"; ".join(map(str,x))+"]"
pred=[10.0+float(i) for i in range(21)]
sigma=[1.0]*21
allclear=[False]*21
q=[4.0,0.01,0.01]
assert replay(pred,allclear,sigma,q,11.1,1)==(1,2,True)
assert replay(pred,allclear,sigma,q,9,1)==(0,1,False)
assert replay(pred,[True]*21,sigma,q,100,1)==(0,1,False)
assert replay(pred,allclear,sigma,[0.0,0.0,0.0],10,1)==(0,1,True)

with tempfile.TemporaryDirectory() as tmp:
    log=Path(tmp)/"events.log"
    lines=[]
    for policy in POLS:
        for t in range(250):
            alarms=[True]*21 if t%13==0 else allclear
            deadline=11.1 if t%5==0 else 9.0
            eta=1.0 if policy=="CASPER_HEALTH_STATIC" else (1.25 if t%7==0 else 1.0)
            selected=replay(pred,alarms,sigma,q,deadline,eta)
            lines.append(["JPDC_POLICY_DECISION",4202202640,"S3_HIDDEN_NETWORK_50LOSS",policy,t,"MISSION",
                          deadline,eta,*[selected[0],selected[1],str(selected[2]).lower()],
                          arrays(pred),arrays([str(a).lower() for a in alarms]),arrays(sigma),arrays(q)])
    def write(rows):
        with log.open("w",encoding="utf-8",newline="") as f:
            csv.writer(f).writerows(rows)
    write(lines)
    assert audit(log,30000)["status"]=="PASS"
    print("PASS: 500 synthetic mission decisions; rank2, abstention, empty family, adaptive eta")
    corrupt=[r.copy() for r in lines]
    corrupt[1][8]=(int(corrupt[1][8])+1)%21
    write(corrupt)
    try: audit(log,30000)
    except ValueError as e: assert "policy decision mismatch" in str(e)
    else:raise AssertionError("invalid selected node was accepted")
    print("PASS: incorrect node rejected")
    write(lines[:-1])
    try:audit(log,30000)
    except ValueError as e:assert "population mismatch" in str(e)
    else:raise AssertionError("incomplete policy task cohort accepted")
    print("PASS: missing policy mission decision rejected")
print("JPDC_POLICY_DECISION_SYNTHETIC_CONTRACT_PASS")
