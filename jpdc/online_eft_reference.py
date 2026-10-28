#!/usr/bin/env python3
"""Reference online earliest-finish-time (EFT), independent-task baseline.

No future tasks, no DAG ranking, no privileged failure/shock information.
This is a standalone semantic test, NOT yet integrated into CASPER Java simulator.
"""
from dataclasses import dataclass
from math import isfinite

@dataclass(frozen=True)
class Task:
    arrival: float
    work: float
    transfer: tuple[float, ...]
    deadline: float

def choose_eft(task, free_at, speeds):
    """Return (node, estimated_finish), with deterministic lowest-index ties."""
    if len(free_at) != len(speeds) or len(task.transfer) != len(speeds) or not speeds:
        raise ValueError("node dimensions must match and be nonempty")
    if not all(isfinite(v) and v >= 0 for v in (task.arrival, task.work, *task.transfer)):
        raise ValueError("nonnegative finite arrival, work and transfer required")
    if not isfinite(task.deadline) or task.deadline < task.arrival:
        raise ValueError("deadline must follow arrival")
    if not all(isfinite(f) and f >= 0 for f in free_at):
        raise ValueError("invalid free times")
    if not all(isfinite(s) and s > 0 for s in speeds):
        raise ValueError("positive finite speeds required")
    options=[(max(task.arrival+task.transfer[i],free_at[i])+task.work/speeds[i],i) for i in range(len(speeds))]
    finish,i=min(options)
    return i,finish

def online_dispatch(tasks, speeds):
    """Deterministic arrival-order dispatcher; returns assignments and projected finishes."""
    items=list(tasks)
    if any(items[j].arrival > items[j+1].arrival for j in range(len(items)-1)):
        raise ValueError("tasks must be in nondecreasing arrival order")
    free=[0.0]*len(speeds)
    out=[]
    for task in items:
        i,finish=choose_eft(task,free,speeds)
        free[i]=finish
        out.append({"node":i,"finish":finish,"deadline_missed_pred":finish>task.deadline})
    return out

if __name__=="__main__":
    items=[Task(0,8,(0,0),10),Task(0,4,(0,0),10),Task(1,4,(2,0),9)]
    print(online_dispatch(items,(1,2)))
