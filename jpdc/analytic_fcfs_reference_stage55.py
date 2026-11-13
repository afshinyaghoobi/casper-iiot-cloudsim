#!/usr/bin/env python3
"""Stage55 reference-formula audit for frozen-route, realized-service FCFS.

Analytic recurrence uses task arrival/node/CPU/network *inputs* only, never
event-engine queue, event loop, observed waits, starts, finishes or deadlines.
Not Java SpaceShared equivalence and not new CASPER algorithm evidence.
"""
import math

TOL = 1e-7


def audit(trace, source_tasks, node_count=21):
    if not isinstance(node_count,int) or node_count<1:
        raise ValueError("invalid node count")
    if len(trace)!=len(source_tasks) or not trace:
        raise ValueError("task count mismatch")
    task_map = {}
    for t in source_tasks:
        i=t[1]
        if i in task_map or i<0:
            raise ValueError("duplicate or negative original task ID")
        task_map[i]=t
    grouped=[[] for _ in range(node_count)]
    observed={}
    for r in trace:
        i=r["task"]
        if i in observed or i not in task_map:
            raise ValueError("duplicate or unknown trace task")
        j=r["node"]
        if type(j) is not int or not 0<=j<node_count:
            raise ValueError("bad node")
        a=float(r["arrival_ms"])
        cpu=float(r["cpu_ms"])
        net=float(r["network_ms"])
        if not all(math.isfinite(v) for v in (a,cpu,net)) or a<0 or cpu<=0 or net<0:
            raise ValueError("bad analytic input")
        if not math.isclose(a,task_map[i][7],abs_tol=1e-8,rel_tol=0):
            raise AssertionError("source task arrival changed")
        observed[i]=r
        grouped[j].append((a,i,cpu,net))
    if set(observed)!=set(task_map):
        raise ValueError("missing original task")
    maxerr={k:0.0 for k in ("start_ms","finish_ms","wait_ms","latency_ms")}
    reference_miss={"NORMAL":0,"HIGH":0,"MISSION":0}
    count_by_type={"NORMAL":0,"HIGH":0,"MISSION":0}
    node_counts=[]
    for node,rows in enumerate(grouped):
        rows.sort(key=lambda x:(x[0],x[1]))
        previous_finish=0.0
        for arrive,i,cpu,net in rows:
            reference_start=max(arrive,previous_finish)
            reference_finish=reference_start+cpu
            reference_wait=reference_start-arrive
            reference_latency=reference_wait+cpu+net
            reference=dict(start_ms=reference_start,finish_ms=reference_finish,
                           wait_ms=reference_wait,latency_ms=reference_latency)
            for key,value in reference.items():
                error=abs(float(observed[i][key])-value)
                if not math.isfinite(error):
                    raise AssertionError("nonfinite observed engine result")
                maxerr[key]=max(maxerr[key],error)
                if error>TOL:
                    raise AssertionError(("analytic FIFO mismatch",node,i,key,error))
            t=task_map[i]
            crit=t[2]
            if crit not in count_by_type:
                raise ValueError("unknown task class")
            count_by_type[crit]+=1
            reference_miss[crit]+=int(reference_latency>t[3])
            previous_finish=reference_finish
        node_counts.append(len(rows))
    assert sum(node_counts)==len(trace)
    return dict(status="PASS",analytical_model="single-server per-node Lindley FCFS",
                source_tasks=len(trace),node_counts=node_counts,
                max_absolute_error_ms=maxerr,
                deadline_misses=reference_miss,
                criticality_counts=count_by_type,
                non_independent_of_input_routes_and_services=True,
                original_cloudsim_space_shared_equivalence=False)
