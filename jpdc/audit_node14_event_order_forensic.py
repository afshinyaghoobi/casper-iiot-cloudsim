#!/usr/bin/env python3
"""Audit S3 forensic event-stage logs without inventing queue scheduling semantics."""
import argparse,csv,json,math
from collections import defaultdict
from pathlib import Path
IDS=set(range(10898,10903))
POLICIES=("CASPER_FULL","CASPER_HEALTH_STATIC")
LABELS={"JPDC_FORENSIC_ARRIVAL":4,"JPDC_FORENSIC_MAPPER":10,
        "JPDC_FORENSIC_FINISH":13}

def audit(path):
    arrivals=defaultdict(list)
    mapped=defaultdict(dict)
    finished=defaultdict(dict)
    with open(path,encoding="utf-8") as f:
        for line in f:
            if not line.startswith(tuple(LABELS)):continue
            r=next(csv.reader([line]))
            if len(r)!=LABELS[r[0]]:raise ValueError(f"incorrect {r[0]} arity")
            if r[0]=="JPDC_FORENSIC_ARRIVAL":
                t=int(r[1]);arrivals[t].append({"planned_ms":float(r[2]),"event_ms":float(r[3])})
            elif r[0]=="JPDC_FORENSIC_MAPPER":
                seed,scenario,policy,tid,node,arrival,clock,cl_id,vm_id=r[1:]
                if scenario!="S3_HIDDEN_NETWORK_50LOSS" or policy not in POLICIES:raise ValueError("wrong mapper identity")
                t=int(tid)
                if t in mapped[policy]:raise ValueError("duplicate mapper")
                mapped[policy][t]={"seed":seed,"node":int(node),"arrival_ms":float(arrival),
                                   "mapper_clock_ms":float(clock),"cloudlet_id":int(cl_id),"vm_id":int(vm_id)}
            else:
                seed,scenario,policy,tid,node,arrival,start,end,wait,service,actual,cl_id=r[1:]
                if scenario!="S3_HIDDEN_NETWORK_50LOSS" or policy not in POLICIES:raise ValueError("wrong finish identity")
                t=int(tid)
                if t in finished[policy]:raise ValueError("duplicate finish")
                finished[policy][t]={"seed":seed,"node":int(node),"arrival_ms":float(arrival),
                                     "derived_start_ms":float(start),"callback_clock_ms":float(end),
                                     "observed_wait_ms":float(wait),"service_ms":float(service),
                                     "actual_latency_ms":float(actual),"cloudlet_id":int(cl_id)}
    if set(arrivals)!=IDS or any(len(arrivals[i])!=9 for i in IDS):
        raise ValueError("missing per-policy arrival records")
    for p in POLICIES:
        if set(mapped[p])!=IDS or set(finished[p])!=IDS:raise ValueError("missing forensic stage")
        for t in IDS:
            m,o=mapped[p][t],finished[p][t]
            # The nine arrivals comprise one calibration pass and eight policy deployments.
            # Match target deployment by its source-frozen planned timestamp.
            match=[e for e in arrivals[t] if abs(e["planned_ms"]-m["arrival_ms"])<=1e-8]
            if len(match)!=8 or any(abs(e["event_ms"]-e["planned_ms"])>1e-8 for e in match):
                raise ValueError(f"deployment arrival/event timing mismatch task={t}")
            if (m["node"]!=o["node"] or m["seed"]!=o["seed"] or
                m["cloudlet_id"]!=o["cloudlet_id"] or
                abs(m["arrival_ms"]-o["arrival_ms"])>1e-8):
                raise ValueError(f"inconsistent forensic task identity {p} {t}")
            for value in list(m.values())+list(o.values()):
                if isinstance(value,float) and not math.isfinite(value):raise ValueError("nonfinite times")
    details={}
    for p in POLICIES:
        order=lambda field,source:sorted(IDS,key=lambda t:(source[p][t][field],t))
        details[p]={
            "planned_task_order":sorted(IDS,key=lambda t:(mapped[p][t]["arrival_ms"],t)),
            "mapper_event_order":order("mapper_clock_ms",mapped),
            "derived_start_order":order("derived_start_ms",finished),
            "actual_wait_recorded":{str(t):finished[p][t]["observed_wait_ms"] for t in sorted(IDS)},
            "tasks":{str(t):{"mapper":mapped[p][t],"finish":finished[p][t]} for t in sorted(IDS)}}
    return {"origin":"actual logged event stages; diagnostic only (nine arrival-source invocations: calibration + eight deployment policies)", "arrival_events_by_task":dict(arrivals),
            "per_policy":details}

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--log",required=True);p.add_argument("--out",required=True)
    a=p.parse_args()
    result=audit(a.log)
    Path(a.out).write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({p:{k:v for k,v in x.items() if k.endswith("_order")}
                      for p,x in result["per_policy"].items()},indent=2))
    print("JPDC_FORENSIC_STAGE_AUDIT_PASS")
