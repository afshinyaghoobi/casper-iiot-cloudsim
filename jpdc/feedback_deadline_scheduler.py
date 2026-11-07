#!/usr/bin/env python3
"""Stage37 lightweight CAUSAL source-feedback deadline scheduling prototype.

Uses only CPU-finish and E2E-delivered observations. No valid hard bound,
no guaranteed deadline or calibrated uncertainty estimate is claimed.
"""
from collections import deque
from dataclasses import dataclass
import math

NODES=21
CPU_WINDOW=32
CPU_MIN=4
CPU_QUANTILE=.75

def kth_positive_quantile(xs):
    if len(xs)<CPU_MIN:return 0.
    ordered=sorted(xs)
    return max(0.,ordered[math.ceil(len(ordered)*CPU_QUANTILE)-1])

@dataclass(frozen=True)
class DispatchDecision:
    node:int
    nominal_greedy:int
    nominal_extra_ms:float
    corrected_pred_ms:float
    predicted_deadline_feasible:bool
    cpu_penalty_ms:float
    network_penalty_ms:float

class CausalFeedbackDeadlineScheduler:
    def __init__(self):
        self.cpu_errors=[deque(maxlen=CPU_WINDOW) for _ in range(NODES)]
        self.cpu_finishes=0
        self.last_cpu_time=-math.inf
        self.decisions=0
        self.changed=0
        self.mission_changed=0
        self.predicted_feasible=0
        self.budget_violations=0

    def observe_cpu(self,node,actual_cpu_ms,nominal_cpu_ms,finished_ms):
        if (isinstance(node,bool) or not isinstance(node,int) or not 0<=node<NODES):
            raise ValueError("invalid CPU node")
        if not all(isinstance(v,(int,float)) and not isinstance(v,bool)
                   and math.isfinite(v) for v in (actual_cpu_ms,nominal_cpu_ms,finished_ms)):
            raise ValueError("invalid CPU feedback")
        if actual_cpu_ms<=0 or nominal_cpu_ms<=0 or finished_ms<self.last_cpu_time:
            raise ValueError("invalid CPU completion timestamp/service")
        self.cpu_errors[node].append(max(0.,actual_cpu_ms-nominal_cpu_ms))
        self.cpu_finishes+=1
        self.last_cpu_time=finished_ms

    def cpu_penalties(self):
        return tuple(kth_positive_quantile(a) for a in self.cpu_errors)

    def select(self,predicted_ms,deadline_ms,task_class,network_penalties_ms,mode):
        if mode not in ("CPU","E2E","BOTH"):
            raise ValueError("invalid ablation mode")
        if task_class not in ("NORMAL","HIGH","MISSION"):
            raise ValueError("unknown task class")
        if (len(predicted_ms)!=NODES or len(network_penalties_ms)!=NODES
                or not all(isinstance(v,(int,float)) and not isinstance(v,bool)
                    and math.isfinite(v) and v>0 for v in predicted_ms)
                or not all(isinstance(v,(int,float)) and not isinstance(v,bool)
                    and math.isfinite(v) and v>=0 for v in network_penalties_ms)
                or not isinstance(deadline_ms,(int,float)) or not math.isfinite(deadline_ms)):
            raise ValueError("invalid current dispatch inputs")
        original=min(range(NODES),key=lambda j:(predicted_ms[j],j))
        budget=2.0 if task_class=="MISSION" else 5.0
        options=[j for j in range(NODES)
                 if predicted_ms[j]<=predicted_ms[original]+budget+1e-10]
        cpu=self.cpu_penalties() if mode in ("CPU","BOTH") else (0.,)*NODES
        net=network_penalties_ms if mode in ("E2E","BOTH") else (0.,)*NODES
        def adjusted(j):return predicted_ms[j]+cpu[j]+net[j]
        j=min(options,key=lambda k:(int(adjusted(k)>deadline_ms),
                                     adjusted(k),predicted_ms[k],k))
        extra=predicted_ms[j]-predicted_ms[original]
        if extra>budget+1e-8:self.budget_violations+=1
        self.decisions+=1
        self.changed+=int(j!=original)
        self.mission_changed+=int(task_class=="MISSION" and j!=original)
        self.predicted_feasible+=int(adjusted(j)<=deadline_ms)
        return DispatchDecision(j,original,extra,adjusted(j),
                                adjusted(j)<=deadline_ms,cpu[j],net[j])

    def invariant(self,count):
        assert self.decisions==count
        assert self.cpu_finishes==count
        assert self.budget_violations==0
        assert 0<=self.mission_changed<=self.changed<=self.decisions
        assert all(len(x)<=CPU_WINDOW for x in self.cpu_errors)
