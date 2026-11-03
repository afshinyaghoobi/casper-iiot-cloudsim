#!/usr/bin/env python3
"""Audited per-phase mission certificate metrics from REAL E45 CSV traces."""
import argparse,csv,json,math
from collections import defaultdict

SCENARIO="S3_HIDDEN_NETWORK_50LOSS"
POLICIES=("CASPER_FULL","CASPER_HEALTH_STATIC")
FIELDS=("fwc","air","far","dvr")

def audit(dispatch,outcome,official,seed_index,task_count=30000):
    seed=str(4202202600+seed_index)
    d={}; o={}
    def read_file(path,label,n):
        result={}
        with open(path,newline="") as f:
            for row in csv.reader(f):
                if len(row)!=n or row[0]!=label: raise ValueError(f"malformed {label} row")
                if row[1]!=seed or row[2]!=SCENARIO or row[3] not in POLICIES:raise ValueError("trace provenance mismatch")
                t=int(row[4]);node=int(row[5])
                if not 0<=t<task_count or not 0<=node<24:raise ValueError("invalid task/node")
                key=(row[3],t)
                if key in result: raise ValueError("duplicate trace event")
                result[key]=row
        if len(result)!=2*task_count:raise ValueError("missing trace events")
        return result
    d=read_file(dispatch,"JPDC_TASK_DISPATCH",12)
    o=read_file(outcome,"JPDC_TASK_OUTCOME",10)
    metrics=defaultdict(lambda:defaultdict(int))
    late_ids={}
    all_missions={}
    for policy in POLICIES:
        mission_ids=[]
        for t in range(task_count):
            dr=d[(policy,t)]; oc=o[(policy,t)]
            if dr[5]!=oc[5] or abs(float(dr[8])-float(oc[7]))>1e-6:raise ValueError("dispatch/outcome discrepancy")
            if any(x not in ("true","false") for x in (dr[9],dr[11],oc[8],oc[9])):raise ValueError("invalid boolean")
            lat=float(oc[6]);deadline=float(oc[7])
            if not math.isfinite(lat) or not math.isfinite(deadline) or lat<0 or deadline<=0:raise ValueError("invalid latency")
            miss=oc[8]=="true"
            if (lat>deadline and not miss) or (lat<deadline-1e-8 and miss):raise ValueError("miss flag inconsistent")
            if oc[9]=="true":mission_ids.append(t)
        late_ids[policy]=mission_ids[-250:];all_missions[policy]=mission_ids
    if late_ids[POLICIES[0]]!=late_ids[POLICIES[1]] or all_missions[POLICIES[0]]!=all_missions[POLICIES[1]]:
        raise ValueError("task indices not matched")
    output=[]
    for policy in POLICIES:
        mission=all_missions[policy]
        groups={"pre":[t for t in mission if t<10000],"post":[t for t in mission if t>=10000],"late":late_ids[policy]}
        for phase,ids in groups.items():
            vals=defaultdict(int)
            for t in ids:
                dr=d[(policy,t)];oc=o[(policy,t)]
                cert=dr[9]=="true";cover=dr[11]=="true";miss=oc[8]=="true"
                vals["n"]+=1;vals["fwc"]+=int(cover);vals["issued"]+=int(cert)
                vals["air"]+=int(not cert);vals["far"]+=int(cert and miss);vals["dvr"]+=int(miss)
            if vals["n"]==0:raise ValueError("empty phase")
            output.append({"seed_index":seed_index,"scientific_seed":seed,"policy":policy,"phase":phase,**dict(vals),
                 **{name+"_rate":vals[name]/vals["n"] for name in FIELDS}})
    with open(official,newline="") as f:rows=list(csv.DictReader(f))
    matched={r["policy"]:r for r in rows if r.get("policy") in POLICIES}
    if len(rows)!=8 or len(matched)!=2:raise ValueError("invalid official results")
    for row in output:
        if row["phase"] not in ("late","post"):continue
        prefix=row["phase"]
        for name in FIELDS:
            col=prefix+"_"+name
            computed=row[name+"_rate"];ref=float(matched[row["policy"]][col])
            if abs(computed-ref)>5e-9:raise ValueError(f"official mismatch {row['policy']} {col}: {computed} != {ref}")
    return output

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--dispatch",required=True);p.add_argument("--outcome",required=True)
    p.add_argument("--official",required=True);p.add_argument("--seed-index",type=int,required=True)
    p.add_argument("--output",required=True)
    args=p.parse_args()
    result=audit(args.dispatch,args.outcome,args.official,args.seed_index)
    with open(args.output,"w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(result[0]));w.writeheader();w.writerows(result)
    print("JPDC_PHASE_AUDIT_PASS",args.seed_index,len(result))
