#!/usr/bin/env python3
"""Strict seed29 per-task dispatch/outcome comparison; run on real CloudSim trace."""
import argparse,csv,json,math
from pathlib import Path
POLICIES=("CASPER_FULL","CASPER_HEALTH_STATIC")
SEED="4202202629"
SCENARIO="S3_HIDDEN_NETWORK_50LOSS"
def read_trace(path,label,count):
    out={}
    with Path(path).open(newline="") as f:
        for row in csv.reader(f):
            if len(row)!=10 or row[0]!=label: raise ValueError("malformed trace row")
            if label=="JPDC_TASK_DISPATCH":
                _,seed,scenario,policy,task,node,eta,value,deadline,flag=row
                extra="false"
                if not math.isfinite(float(eta)) or not 1<=float(eta)<=3:
                    raise ValueError("invalid eta")
            else:
                _,seed,scenario,policy,task,node,value,deadline,flag,extra=row
            if seed!=SEED or scenario!=SCENARIO or policy not in POLICIES:
                raise ValueError("unexpected seed/scenario/policy")
            task,node=int(task),int(node)
            if not 0<=task<count or not 0<=node<24:raise ValueError("invalid task/node")
            v,d=float(value),float(deadline)
            if not math.isfinite(v) or not math.isfinite(d) or v<0 or d<=0:
                raise ValueError("invalid numeric value")
            if flag not in ("true","false") or extra not in ("true","false"):
                raise ValueError("invalid boolean")
            key=(policy,task)
            if key in out:raise ValueError("duplicate task")
            out[key]=(node,v,d,flag=="true",extra=="true")
    if len(out)!=2*count or any((p,t) not in out for p in POLICIES for t in range(count)):
        raise ValueError("missing tasks")
    return out
def analyze(dispatch,outcome,count=30000,results_csv=None):
    d=read_trace(dispatch,"JPDC_TASK_DISPATCH",count)
    o=read_trace(outcome,"JPDC_TASK_OUTCOME",count)
    for key in d:
        dn,_,dd,_,_=d[key]
        on,latency,od,miss,_=o[key]
        if dn!=on or abs(dd-od)>1e-6 or miss!=(latency>od):
            raise ValueError(f"dispatch/outcome mismatch: {key}")
    different=[]; changed=[]; missions=[]
    for t in range(count):
        full=(POLICIES[0],t);static=(POLICIES[1],t)
        if d[full][0]!=d[static][0]:different.append(t)
        if o[full][4]!=o[static][4] or o[full][2]!=o[static][2]:
            raise ValueError("task metadata differs between policies")
        if o[full][3]!=o[static][3] and o[full][4]:changed.append(t)
        if t>=10000 and o[full][4]:missions.append(t)
    late=missions[-250:]
    if len(late)!=250:raise ValueError("not enough post-change mission tasks")
    rate=lambda p:sum(o[(p,t)][3] for t in late)/len(late)
    distinct=set(different)
    if results_csv is not None:
        with Path(results_csv).open(newline="") as file:
            official=list(csv.DictReader(file))
        expected={p for p in POLICIES}
        matched=[r for r in official if r.get("policy") in expected]
        if len(matched)!=2 or {r["policy"] for r in matched}!=expected:
            raise ValueError("missing/duplicate official policy rows")
        for row in matched:
            if row.get("seed")!=SEED or row.get("scenario")!=SCENARIO or int(row["tasks"])!=count:
                raise ValueError("official task metadata mismatch")
            computed=rate(row["policy"])
            official_rate=float(row["late_dvr"])
            if not math.isfinite(official_rate) or abs(computed-official_rate)>5e-9:
                raise ValueError(f"late_dvr trace/official mismatch {row['policy']}: {computed} != {official_rate}")
    return {"seed":int(SEED),"scenario":SCENARIO,"tasks_per_policy":count,
      "different_node_count":len(different),"different_node_rate":len(different)/count,
      "mission_deadline_disagreements":len(changed),"late_mission_count":len(late),
      "late_dvr_full":rate(POLICIES[0]),"late_dvr_static":rate(POLICIES[1]),
      "late_dvr_delta_full_minus_static":rate(POLICIES[0])-rate(POLICIES[1]),
      "late_mission_disagreements":sum(o[(POLICIES[0],t)][3]!=o[(POLICIES[1],t)][3] for t in late),
      "late_mission_different_nodes":sum(t in distinct for t in late),
      "example_different_tasks":different[:20],"example_mission_disagreements":changed[:20]}
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--dispatch",required=True);p.add_argument("--outcome",required=True)
    p.add_argument("--out",required=True);p.add_argument("--tasks",type=int,default=30000)
    p.add_argument("--results",help="Official CloudSim result CSV for outcome reconciliation")
    a=p.parse_args();result=analyze(a.dispatch,a.outcome,a.tasks,a.results)
    Path(a.out).write_text(json.dumps(result,indent=2)+"\n")
    print("SEED29_TASK_TRACE_AUDIT_PASS",result["different_node_count"],result["late_dvr_delta_full_minus_static"])
