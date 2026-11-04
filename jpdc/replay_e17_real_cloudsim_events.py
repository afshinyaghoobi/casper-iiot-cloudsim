#!/usr/bin/env python3
"""Independent E1.7 replay on original CloudSim event chronology (stdlib only).

Uses Java-provided calibration *raw scores* and actual realized residual *scores*
as exogenous inputs; recomputes E1.7 internal state and eta independently.
"""
import argparse,csv,json,math
from pathlib import Path
from independent_casper_state import DualMemory

def equal(x,y,description):
    if not math.isfinite(x) or not math.isclose(x,y,rel_tol=0,abs_tol=1e-10):
        raise ValueError(f"{description}: observed {x}, independent {y}")

def audit(log,results,tasks):
    reference=[]
    events=[]
    seed_values=set()
    event_started=False
    with open(log,encoding="utf-8") as f:
        for line in f:
            if not line.startswith(("JPDC_E17_REFERENCE,","JPDC_E17_DISPATCH,","JPDC_E17_OBSERVE,")):
                continue
            r=next(csv.reader([line]))
            tag=r[0]
            if tag=="JPDC_E17_REFERENCE":
                if len(r)!=4 or event_started:raise ValueError("reference stream reordered or malformed")
                seed_values.add(int(r[1]))
                index=int(r[2])
                if index!=len(reference):raise ValueError("missing/reordered calibration reference")
                value=float(r[3])
                if not math.isfinite(value) or value<0:raise ValueError("invalid calibration reference")
                reference.append(value)
            else:
                if len(r)!=6:raise ValueError("event stream shape")
                event_started=True
                seed_values.add(int(r[1]))
                task=int(r[2])
                if task<0 or task>=tasks:raise ValueError("task index invalid")
                value=float(r[3])
                if not math.isfinite(value) or value<0:raise ValueError("negative or nonfinite E17 event")
                if r[4] not in ("true","false"):raise ValueError("bad detector state")
                age=int(r[5])
                if age < -1:raise ValueError("bad transition age")
                events.append((tag,task,value,r[4]=="true",age))
    if len(reference)<200 or len(seed_values)!=1:
        raise ValueError("reference/seed incomplete")
    model=DualMemory(reference)
    dispatch_tasks=set()
    outcome_tasks=set()
    outcome_count=0
    adaptive_eta_count=0
    alarm_activations=0
    for tag,task,val,alarm,age in events:
        if tag=="JPDC_E17_DISPATCH":
            if task in dispatch_tasks:raise ValueError("duplicate dispatch")
            dispatch_tasks.add(task)
            equal(val,model.eta_before_outcome(),f"dispatch eta task={task}")
            if alarm!=model.alarm_ever or age!=model.transition_age:
                raise ValueError(f"dispatch detector mismatch task={task}")
            if val>1+1e-12:adaptive_eta_count+=1
        else:
            if task in outcome_tasks:raise ValueError("duplicate outcome score")
            outcome_tasks.add(task)
            if task not in dispatch_tasks:raise ValueError("outcome before task dispatch")
            before_alarm=model.alarm_ever
            model.observe(val)
            outcome_count+=1
            if not before_alarm and model.alarm_ever:alarm_activations+=1
            if alarm!=model.alarm_ever or age!=model.transition_age:
                raise ValueError(f"outcome detector mismatch task={task}")
    if dispatch_tasks!=set(range(tasks)) or not outcome_tasks:
        raise ValueError("incomplete dispatch or no mission feedback")
    if not outcome_tasks.issubset(dispatch_tasks):raise ValueError("orphan feedback")
    with open(results,encoding="utf-8",newline="") as f:
        rows=list(csv.DictReader(f))
    if len(rows)!=8 or len({r["policy"] for r in rows})!=8:
        raise ValueError("official scientific CSV incomplete")
    full=next(r for r in rows if r["policy"]=="CASPER_FULL")
    if outcome_count!=int(full["mission_n"]):
        raise ValueError(f"feedback mission event count mismatch {outcome_count} vs {full['mission_n']}")
    return {"scope":"independent E17 state transitions driven by Java raw calibration and actual outcome residuals",
            "scientific_seed":next(iter(seed_values)),"calibration_reference_count":len(reference),
            "full_task_dispatches":len(dispatch_tasks),"mission_outcome_feedback_events":outcome_count,
            "dispatch_eta_greater_than_one":adaptive_eta_count,
            "detector_alarm_transitions":alarm_activations,
            "final_detector_alarm":model.alarm_ever,"final_transition_age":model.transition_age,
            "status":"PASS"}

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--log",required=True);p.add_argument("--results",required=True)
    p.add_argument("--tasks",type=int,default=30000)
    p.add_argument("--out",required=True)
    a=p.parse_args()
    result=audit(a.log,a.results,a.tasks)
    Path(a.out).write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))
    print("JPDC_E17_REAL_EVENT_INDEPENDENT_REPLAY_PASS")
