#!/usr/bin/env python3
"""Rebuild health and VirtualQueue state on real CloudSim event chronology.

Only exogenous observed service/nominal and physical telemetry are copied;
all alarm history and virtual queue states are independently updated in Python.
"""
import argparse,csv,json,math
from pathlib import Path
from independent_casper_state import NodeHealth,VirtualQueue

NODES=21
TAGS=("JPDC_HV_THRESHOLD","JPDC_HV_TELEMETRY","JPDC_HV_FINISH","JPDC_HV_PRE","JPDC_HV_POST")

def numeric(s):
    x=float(s)
    if not math.isfinite(x):raise ValueError("nonfinite numeric field")
    return x

def near(actual,predicted,label):
    if not math.isclose(numeric(actual),predicted,abs_tol=1e-8,rel_tol=0):
        raise ValueError(f"{label}: Java={actual} Python={predicted}")

def array(raw,boolean=False):
    if not raw.startswith("[") or not raw.endswith("]"):raise ValueError("array bracket")
    items=[p.strip() for p in raw[1:-1].split(";")]
    if len(items)!=NODES:raise ValueError("not 21 nodes")
    return [{"true":True,"false":False}[p] for p in items] if boolean else [numeric(p) for p in items]

def audit(path,tasks=30000):
    thresholds=[]
    health=None
    queue=VirtualQueue(NODES)
    seed_seen=set()
    seen_pre=set();seen_post=set();seen_finish=set()
    pending=None;next_pre=0;telemetry_count=0;alarm_transitions=0
    max_backlog_error=0.0;max_next_free_error=0.0
    for line in Path(path).open(encoding="utf-8"):
        if not line.startswith(tuple(tag+"," for tag in TAGS)):continue
        row=next(csv.reader([line]))
        tag=row[0]
        lengths={"JPDC_HV_THRESHOLD":4,"JPDC_HV_TELEMETRY":4,
                 "JPDC_HV_FINISH":7,"JPDC_HV_PRE":6,"JPDC_HV_POST":7}
        if len(row)!=lengths[tag]:raise ValueError("incorrect field count "+tag)
        seed_seen.add(int(row[1]))
        if len(seed_seen)>1:raise ValueError("mixed scientific seeds")
        if tag=="JPDC_HV_THRESHOLD":
            if health is not None:raise ValueError("threshold after first event")
            node=int(row[2]);value=numeric(row[3])
            if node!=len(thresholds) or value<=0:raise ValueError("threshold identity/order")
            thresholds.append(value)
            if len(thresholds)==NODES:
                health=[NodeHealth(v) for v in thresholds]
            continue
        if health is None:raise ValueError("event before 21 health thresholds")
        task=int(row[2])
        if not 0<=task<tasks:raise ValueError("task out of range")
        if tag=="JPDC_HV_FINISH":
            if pending is not None:raise ValueError("unexpected finish within dispatch")
            node=int(row[3]);actual=numeric(row[4]);nominal=numeric(row[5])
            if not 0<=node<NODES or actual<0 or nominal<=0:raise ValueError("invalid health observation")
            if row[6] not in ("true","false"):raise ValueError("health boolean")
            if task in seen_finish or task not in seen_post:raise ValueError("duplicate or undispatched completion")
            seen_finish.add(task)
            old=health[node].alarmed
            expected=health[node].observe(actual,nominal)
            if not old and expected:alarm_transitions+=1
            if (row[6]=="true")!=expected:raise ValueError(f"health alarm mismatch task={task}, node={node}")
        elif tag=="JPDC_HV_TELEMETRY":
            if pending is not None or task!=next_pre:raise ValueError("telemetry event placement")
            observed=array(row[3])
            if min(observed)<0:raise ValueError("negative telemetry")
            queue.reset_from_telemetry(observed)
            telemetry_count+=1
        elif tag=="JPDC_HV_PRE":
            now=numeric(row[3])
            if task!=next_pre or task in seen_pre or pending is not None or now<0:
                raise ValueError("pre event order")
            backlogs=array(row[4]);alarms=array(row[5],boolean=True)
            for i in range(NODES):
                expected=queue.predicted_backlog(i,now)
                max_backlog_error=max(max_backlog_error,abs(backlogs[i]-expected))
                near(backlogs[i],expected,f"task{task} node{i} backlog")
                if alarms[i]!=health[i].alarmed:
                    raise ValueError(f"task{task} node{i} health mask mismatch")
            seen_pre.add(task);pending=(task,now)
        else:
            node=int(row[3]);now=numeric(row[4]);service=numeric(row[5]);next_free=numeric(row[6])
            if pending is None or pending[0]!=task or task in seen_post:
                raise ValueError("post event without corresponding pre")
            near(now,pending[1],f"task{task} arrival")
            if not 0<=node<NODES or service<=0 or next_free<0:raise ValueError("invalid dispatch")
            queue.on_dispatch(node,now,service)
            delta=abs(queue.next_free[node]-next_free)
            max_next_free_error=max(max_next_free_error,delta)
            near(next_free,queue.next_free[node],f"task{task} node{node} next free")
            seen_post.add(task);next_pre+=1;pending=None
    if seed_seen!={4202202640}:raise ValueError(f"unexpected scientific seed {seed_seen}")
    if len(thresholds)!=NODES or pending is not None or telemetry_count<1:
        raise ValueError("incomplete threshold/dispatch/telemetry")
    expected=set(range(tasks))
    if seen_pre!=expected or seen_post!=expected or seen_finish!=expected:
        raise ValueError(f"missing task events: pre={len(seen_pre)},post={len(seen_post)},finish={len(seen_finish)}")
    return {"scope":"independent Python health/virtual-queue transitions on Java outcome and telemetry input stream",
            "seed":4202202640,"health_threshold_nodes":NODES,
            "real_task_dispatches":len(seen_post),"real_finish_health_updates":len(seen_finish),
            "telemetry_resets":telemetry_count,"health_alarm_transitions":alarm_transitions,
            "alarmed_nodes_at_end":sum(h.alarmed for h in health),
            "max_backlog_error_ms":max_backlog_error,
            "max_selected_queue_next_free_error_ms":max_next_free_error,"status":"PASS"}

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--log",required=True);p.add_argument("--out",required=True);p.add_argument("--tasks",type=int,default=30000)
    a=p.parse_args()
    result=audit(a.log,a.tasks)
    Path(a.out).write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))
    print("JPDC_REAL_HEALTH_VQ_INDEPENDENT_REPLAY_PASS")
