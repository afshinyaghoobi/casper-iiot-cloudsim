#!/usr/bin/env python3
"""Diagnostic only: identify FCFS start-order inversions in ORIGINAL observed CloudSim queue logs.

Usage: python3 jpdc/diagnose_queue_start_order_inversions.py --log instrumented.log
Uses recorded waits solely to diagnose actual start ordering, NOT to change or
'correct' the preregistered independent replay. Never alters acceptance criteria.
"""
import argparse,csv,json
from collections import defaultdict

def scan(log):
    queues=defaultdict(list)
    with open(log,encoding="utf-8") as f:
        for line in f:
            if not line.startswith("JPDC_QUEUE_REPLAY,"):continue
            r=next(csv.reader([line]))
            if len(r)!=13:raise ValueError("unexpected queue trace column count")
            policy,node=r[3],int(r[7])
            queues[policy,node].append(dict(task=int(r[4]),crit=r[5],node=node,
                                           arrival_ms=float(r[6]),service_ms=float(r[8]),
                                           observed_wait_ms=float(r[9])))
    result={}
    for (policy,node),rows in sorted(queues.items()):
        by_arrival=sorted(rows,key=lambda x:(x["arrival_ms"],x["task"]))
        by_start=sorted(rows,key=lambda x:(x["arrival_ms"]+x["observed_wait_ms"],x["task"]))
        ai={x["task"]:i for i,x in enumerate(by_arrival)}
        si={x["task"]:i for i,x in enumerate(by_start)}
        mismatches=[dict(task=x["task"],arrival_rank=ai[x["task"]],
                         observed_start_rank=si[x["task"]],
                         node=node,arrival_ms=x["arrival_ms"],
                         observed_wait_ms=x["observed_wait_ms"])
                    for x in by_arrival if ai[x["task"]]!=si[x["task"]]]
        if mismatches:
            result.setdefault(policy,[]).append(dict(node=node,inversion_task_count=len(mismatches),
                                                       tasks=mismatches))
    return result

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--log",required=True)
    args=p.parse_args()
    print(json.dumps(scan(args.log),indent=2))
    print("JPDC_QUEUE_ORDER_INVERSION_DIAGNOSTIC_ONLY")
