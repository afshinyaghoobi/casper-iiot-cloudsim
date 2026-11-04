#!/usr/bin/env python3
"""Independent stdlib CASPER mission decision replay on frozen E45 input snapshots.

This independently recomputes top3 + rank-wise conformal bound + cert decision.
It uses the recorded input states (prediction, alarm, calibration, eta), so it is
NOT a second environment, predictor/health/feedback implementation or efficacy test.
"""
import argparse,csv,json,math
from pathlib import Path
POLS=("CASPER_FULL","CASPER_HEALTH_STATIC")
FIELDS=("tag","seed","scenario","policy","task","crit","deadline","eta",
        "node","rank","cert","pred","alarms","sigma","qrank")

def array(value,cast=float):
    if not value.startswith("[") or not value.endswith("]"):
        raise ValueError("invalid array syntax")
    parts=[p.strip() for p in value[1:-1].split(";")]
    if any(not p for p in parts):raise ValueError("empty array element")
    result=[cast(part) for part in parts]
    return result

def replay(pred,alarms,sigma,qrank,deadline,eta):
    candidates=sorted((i for i in range(21) if not alarms[i]),
                      key=lambda i:(pred[i],i))[:3]
    if not candidates:
        return min(range(21),key=lambda i:(pred[i],i)),1,False
    safe=None
    for rank,node in enumerate(candidates):
        bound=pred[node]+eta*qrank[rank]*(3.0+0.1*pred[node])*sigma[node]
        if bound<=deadline:
            safe=rank
            break
    rank=0 if safe is None else safe
    return candidates[rank],rank+1,safe is not None

def audit(log,tasks):
    seen={p:{} for p in POLS}
    with open(log,encoding="utf-8") as f:
        for line in f:
            if not line.startswith("JPDC_POLICY_DECISION,"):
                continue
            r=next(csv.reader([line]))
            if len(r)!=len(FIELDS):raise ValueError("decision column count")
            x=dict(zip(FIELDS,r))
            if (x["scenario"]!="S3_HIDDEN_NETWORK_50LOSS" or
                x["policy"] not in POLS or x["crit"]!="MISSION"):
                raise ValueError("scenario/policy/criticality identity")
            policy=x["policy"];task=int(x["task"])
            if task<0 or task>=tasks or task in seen[policy]:
                raise ValueError("task duplicate or out of range")
            pred=array(x["pred"]);alarm=array(x["alarms"],
                lambda a: {"true":True,"false":False}[a])
            sigma=array(x["sigma"]);qrank=array(x["qrank"])
            if len(pred)!=21 or len(alarm)!=21 or len(sigma)!=21 or len(qrank)!=3:
                raise ValueError("candidate array cardinality mismatch")
            deadline=float(x["deadline"]);eta=float(x["eta"])
            values=[*pred,*sigma,*qrank,deadline,eta]
            if (not all(math.isfinite(v) for v in values)
                or min(pred)<0 or min(sigma)<=0 or min(qrank)<0 or
                deadline<=0 or not 1<=eta<=3):
                raise ValueError("nonphysical/nonfinite candidate state")
            if policy=="CASPER_HEALTH_STATIC" and eta!=1:
                raise ValueError("static policy must have eta=1")
            actual=(int(x["node"]),int(x["rank"]),x["cert"]=="true")
            if x["cert"] not in ("true","false"):raise ValueError("invalid certificate")
            expected=replay(pred,alarm,sigma,qrank,deadline,eta)
            if actual!=expected:
                raise ValueError(f"policy decision mismatch {policy} task={task} observed={actual} replay={expected}")
            seen[policy][task]={"node":actual[0],"rank":actual[1],"cert":actual[2],
                                "deadline":deadline,"pred":pred,"eta":eta,
                                "alarm":alarm,"qrank":qrank}
    a,b=(seen[p] for p in POLS)
    if len(a)<250 or set(a)!=set(b):raise ValueError("mission task population mismatch")
    seeds=set()
    result={}
    for policy,data in seen.items():
        result[policy]=dict(mission_decisions=len(data),
            postshock=sum(t>=10000 for t in data),
            certified=sum(row["cert"] for row in data.values()),
            ranks={str(rank):sum(row["rank"]==rank for row in data.values()) for rank in (1,2,3)})
    return {"scope":"cross-language policy-decision semantics conditional on Java-sourced state",
            "tasks_per_policy":tasks,"policies":result,"status":"PASS"}

if __name__=="__main__":
    arg=argparse.ArgumentParser()
    arg.add_argument("--log",required=True)
    arg.add_argument("--out",required=True)
    arg.add_argument("--tasks",type=int,default=30000)
    x=arg.parse_args()
    result=audit(x.log,x.tasks)
    Path(x.out).write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))
    print("JPDC_POLICY_DECISION_CROSS_LANGUAGE_PARITY_PASS")
