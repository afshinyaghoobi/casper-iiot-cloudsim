#!/usr/bin/env python3
"""Independent, stdlib-only FCFS single-VM queue trace replay for E45 S3.

Does NOT reimplement CASPER policy or claim independent scheduling efficacy.
Consumes ALL tasks (MISSION and NORMAL); never uses observed wait to PREDICT wait.
Usage: python3 jpdc/replay_s3_queues_independent.py --log queue.log --out results.json --tasks 30000
"""
import argparse,csv,json,math
from pathlib import Path

SCENARIO="S3_HIDDEN_NETWORK_50LOSS"
POLICIES=("CASPER_FULL","CASPER_HEALTH_STATIC")
COLUMNS=("tag","seed","scenario","policy","task","crit","arrival_ms","node",
         "service_ms","observed_wait_ms","network_ms","observed_latency_ms","deadline_ms")
FLOATS=("arrival_ms","service_ms","observed_wait_ms","network_ms",
        "observed_latency_ms","deadline_ms")

def load(path,tasks):
    entries={p:{} for p in POLICIES}
    with open(path,encoding="utf-8") as file:
        for line in file:
            if not line.startswith("JPDC_QUEUE_REPLAY,"): continue
            fields=next(csv.reader([line]))
            if len(fields)!=len(COLUMNS):raise ValueError("queue trace shape")
            r=dict(zip(COLUMNS,fields))
            if r["scenario"]!=SCENARIO or r["policy"] not in POLICIES:
                raise ValueError("queue trace identity")
            if r["crit"] not in ("MISSION","NORMAL"):
                raise ValueError("unexpected criticality")
            r["task"]=int(r["task"]);r["node"]=int(r["node"])
            if r["task"]<0 or r["task"]>=tasks or not 0<=r["node"]<21:
                raise ValueError("task or node out of bounds")
            for k in FLOATS:
                r[k]=float(r[k])
                if not math.isfinite(r[k]):raise ValueError("nonfinite "+k)
            if any(r[k]<0 for k in ("arrival_ms","service_ms","observed_wait_ms",
                                  "network_ms","observed_latency_ms")) or r["deadline_ms"]<=0:
                raise ValueError("nonphysical queue trace")
            if abs(r["network_ms"]+r["service_ms"]+r["observed_wait_ms"]-
                   r["observed_latency_ms"])>1e-7:
                raise ValueError("observed latency decomposition invalid")
            if r["task"] in entries[r["policy"]]:raise ValueError("duplicate task")
            entries[r["policy"]][r["task"]]=r
    if any(set(entries[p])!=set(range(tasks)) for p in POLICIES):
        raise ValueError("full task population not recorded for both policies")
    seeds={r["seed"] for p in POLICIES for r in entries[p].values()}
    if len(seeds)!=1:raise ValueError("seed inconsistency")
    for t in range(tasks):
        a,b=(entries[p][t] for p in POLICIES)
        for k in ("arrival_ms","deadline_ms","crit"):
            if a[k]!=b[k]:raise ValueError("task input differs between policies: "+str((t,k)))
    return entries,seeds.pop()

def simulate(rows):
    # 21 deterministic FCFS single-core servers. Simulate busy state from
    # every task's arrival+realized service demand, ignoring observed wait.
    free=[0.0]*21
    out=[]
    for r in sorted(rows.values(),key=lambda a:(a["arrival_ms"],a["task"])):
        start=max(r["arrival_ms"],free[r["node"]])
        predicted_wait=start-r["arrival_ms"]
        free[r["node"]]=start+r["service_ms"]
        replay_latency=r["network_ms"]+predicted_wait+r["service_ms"]
        out.append((r,predicted_wait,replay_latency))
    return out

def run(log,tasks):
    cohorts,seed=load(log,tasks)
    answer={"scientific_scope":"independent queue mechanics only, fixed original policy decisions",
            "seed":seed,"scenario":SCENARIO,"tasks_per_policy":tasks,"policies":{}}
    for policy,rows in cohorts.items():
        replay=simulate(rows)
        wait_abs=[abs(w-r["observed_wait_ms"]) for r,w,l in replay]
        lat_abs=[abs(l-r["observed_latency_ms"]) for r,w,l in replay]
        missed_obs=sum(r["observed_latency_ms"]>r["deadline_ms"] for r,w,l in replay
                       if r["crit"]=="MISSION" and r["task"]>=10000)
        missed_replay=sum(l>r["deadline_ms"] for r,w,l in replay
                          if r["crit"]=="MISSION" and r["task"]>=10000)
        answer["policies"][policy]={
            "tasks":len(replay),
            "mission_post_actual_miss_count":missed_obs,
            "mission_post_queue_replay_miss_count":missed_replay,
            "wait_mae_ms":sum(wait_abs)/len(wait_abs),
            "wait_max_absolute_error_ms":max(wait_abs),
            "latency_mae_ms":sum(lat_abs)/len(lat_abs),
            "latency_max_absolute_error_ms":max(lat_abs),
            "wait_abs_error_gt_1ms":sum(e>1 for e in wait_abs)}
    return answer

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--log",required=True)
    p.add_argument("--out",required=True)
    p.add_argument("--tasks",type=int,default=30000)
    a=p.parse_args()
    result=run(a.log,a.tasks)
    Path(a.out).write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))
    print("JPDC_QUEUE_REPLAY_COMPUTED_NOT_VALIDATED")
