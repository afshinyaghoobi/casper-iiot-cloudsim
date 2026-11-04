#!/usr/bin/env python3
"""Observed actual completion outcomes of unmodified rank2-selected MISSION tasks.

Exploratory POST-SELECTION analysis: do not treat upper-bound feasibility as
observed deadline success, or as rank1 counterfactual comparison.
"""
import argparse,csv,json,math
from pathlib import Path
POLS=("CASPER_FULL","CASPER_HEALTH_STATIC")
EXPECTED={41:{"CASPER_FULL":9,"CASPER_HEALTH_STATIC":0},
          44:{"CASPER_FULL":4,"CASPER_HEALTH_STATIC":1}}
def audit(log,seed_index):
    if seed_index not in EXPECTED:raise ValueError("seed not predeclared")
    decisions={p:{} for p in POLS}
    completed={p:{} for p in POLS}
    src_seed=4_202_202_600+seed_index
    with open(log,encoding="utf-8") as f:
        for line in f:
            if line.startswith("JPDC_POLICY_DECISION,"):
                r=next(csv.reader([line]))
                if len(r)!=15:raise ValueError("policy snapshot field count")
                _,seed,scenario,p,t,crit,deadline,eta,node,rank,cert,*_=r
                if int(seed)!=src_seed or scenario!="S3_HIDDEN_NETWORK_50LOSS" or p not in POLS or crit!="MISSION":
                    raise ValueError("bad policy identity")
                t=int(t)
                if t in decisions[p]:raise ValueError("duplicate mission decision")
                if cert not in ("true","false"):raise ValueError("bad policy cert")
                decisions[p][t]={"node":int(node),"rank":int(rank),"certified":cert=="true","deadline":float(deadline),"eta":float(eta)}
            elif line.startswith("JPDC_OBSERVED_OUTCOME,"):
                r=next(csv.reader([line]))
                if len(r)!=17:raise ValueError("actual outcome field count")
                _,seed,scenario,p,t,node,eta,pred,net,queue,service,latency,deadline,cert,family,miss,far=r
                if int(seed)!=src_seed or scenario!="S3_HIDDEN_NETWORK_50LOSS" or p not in POLS:
                    raise ValueError("bad outcome identity")
                t=int(t)
                if t in completed[p]:raise ValueError("duplicate task completion")
                if any(v not in ("true","false") for v in (cert,family,miss,far)):
                    raise ValueError("bad outcome boolean")
                values=list(map(float,(eta,pred,net,queue,service,latency,deadline)))
                if not all(math.isfinite(v) for v in values):raise ValueError("nonfinite observed value")
                if abs(float(net)+float(queue)+float(service)-float(latency))>5e-8:
                    raise ValueError("realized latency decomposition")
                if (cert=="true" and miss=="true")!=(far=="true"):raise ValueError("incorrect false certificate")
                completed[p][t]={"node":int(node),"eta":float(eta),"prediction_ms":float(pred),
                    "network_ms":float(net),"wait_ms":float(queue),"service_ms":float(service),
                    "observed_ms":float(latency),"deadline":float(deadline),
                    "certified":cert=="true","miss":miss=="true","false_certificate":far=="true"}
    if any(set(decisions[p])!=set(completed[p]) for p in POLS):
        raise ValueError("incomplete mission decision vs actual completion coverage")
    if set(decisions[POLS[0]])!=set(decisions[POLS[1]]):raise ValueError("policy mission cohorts differ")
    result={"seed_index":seed_index,"scientific_seed":src_seed,"scope":"exploratory outcomes, NO rank1 counterfactual",
            "policies":{}}
    for p in POLS:
        entries=[]
        for t,d in sorted(decisions[p].items()):
            o=completed[p][t]
            if d["node"]!=o["node"] or abs(d["deadline"]-o["deadline"])>1e-7 or                d["certified"]!=o["certified"] or abs(d["eta"]-o["eta"])>1e-7:
                raise ValueError(f"join decision/outcome identity mismatch {p} task {t}")
            if d["rank"]==2:
                if not d["certified"]:raise ValueError("rank2 selection unexpectedly uncertified")
                entries.append({"task":t,"node":d["node"],"rank":2,
                    "certified":d["certified"],"actual_deadline_miss":o["miss"],
                    "false_certificate":o["false_certificate"],"deadline_ms":o["deadline"],
                    "actual_latency_ms":o["observed_ms"],"prediction_ms":o["prediction_ms"],
                    "slack_ms":o["deadline"]-o["observed_ms"]})
        if len(entries)!=EXPECTED[seed_index][p]:raise ValueError(f"rank2 count differs from prescreen {p}: {len(entries)}")
        result["policies"][p]={"mission_n":len(decisions[p]),"rank2_n":len(entries),
            "rank2_observed_misses":sum(x["actual_deadline_miss"] for x in entries),
            "rank2_observed_on_time":sum(not x["actual_deadline_miss"] for x in entries),
            "rank2_task_outcomes":entries}
    return result
if __name__=="__main__":
    a=argparse.ArgumentParser();a.add_argument("--log",required=True)
    a.add_argument("--seed-index",type=int,required=True);a.add_argument("--out",required=True)
    args=a.parse_args();r=audit(args.log,args.seed_index)
    Path(args.out).write_text(json.dumps(r,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(r,indent=2))
    print("JPDC_RANK2_OBSERVED_OUTCOMES_JOIN_PASS")
