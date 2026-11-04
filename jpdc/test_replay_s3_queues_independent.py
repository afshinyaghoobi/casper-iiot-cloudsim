#!/usr/bin/env python3
"""Synthetic positive/negative tests for the external FCFS mechanical queue replay."""
import csv,json,tempfile
from pathlib import Path
from replay_s3_queues_independent import run,load,simulate

P=("CASPER_FULL","CASPER_HEALTH_STATIC")
S="4202202640"
CASE=[
  (0,"NORMAL",0,0,10,0,2,12,100),
  (1,"MISSION",2,0,5,8,3,16,14),
  (2,"HIGH",3,1,4,0,1,5,100),
  (3,"MISSION",10,0,2,5,1,8,7),
]
def record(policy,row):
    task,crit,arr,node,svc,wait,net,observed,deadline=row
    return ["JPDC_QUEUE_REPLAY",S,"S3_HIDDEN_NETWORK_50LOSS",policy,
            task,crit,arr,node,svc,wait,net,observed,deadline]
def emit(path,lines):
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.writer(f)
        w.writerows(lines)
def rejects(path,fragment):
    try: load(path,4)
    except ValueError as e: assert fragment in str(e), (fragment,str(e))
    else: raise AssertionError("invalid queue cohort accepted: "+fragment)

with tempfile.TemporaryDirectory() as td:
    p=Path(td)/"trace.log"
    rows=[record(policy,row) for policy in P for row in CASE]
    # Completion logs need not be emitted in dispatch order.
    emit(p,list(reversed(rows)))
    result=run(p,4)
    for policy in P:
        data=result["policies"][policy]
        assert data["tasks"]==4 and data["wait_mae_ms"]==0
        assert data["latency_mae_ms"]==0 and data["wait_abs_error_gt_1ms"]==0
    print("PASS deterministic FCFS queue replay: two policies, four tasks each including HIGH")
    # Dropping NORMAL work would create false "zero wait" for later MISSION.
    omit=[r for r in rows if not (r[3]==P[0] and r[4]==0)]
    emit(p,omit);rejects(p,"full task population")
    mutate=[r.copy() for r in rows]
    mutate[4][6]=1
    emit(p,mutate);rejects(p,"task input differs")
    mutate=[r.copy() for r in rows]
    mutate[1][9]=7;mutate[1][11]=15
    emit(p,mutate)
    result=run(p,4)
    assert result["policies"][P[0]]["wait_mae_ms"]==.25
    assert result["policies"][P[1]]["wait_mae_ms"]==0
    print("PASS mismatch detected when observed queue wait is perturbed")
print("JPDC_INDEPENDENT_QUEUE_SYNTHETIC_CONTRACT_PASS")
