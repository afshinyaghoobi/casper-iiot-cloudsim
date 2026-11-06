#!/usr/bin/env python3
"""Stage28 CPU-finish-only FULL nonnetwork q interval estimator, descriptive only.

q = (actual service start - dispatch - predicted wait)
  + (actual CPU finish - service start - predicted CPU).
No network measurements enter these scores. Output NEVER certified.
"""
from collections import defaultdict,deque
from dataclasses import dataclass
import math

CONTEXT="native_python_strict_fcfs_vq_telemetry50ms"
CLASSES=("NORMAL","HIGH","MISSION")
MIN_SCORES=40
MAX_SCORES=200

@dataclass(frozen=True)
class PendingQ:
    task_index:int
    node:int
    task_class:str
    dispatched_ms:float
    telemetry_band:str
    predicted_wait_ms:float
    predicted_cpu_ms:float

@dataclass(frozen=True)
class QEstimate:
    context:str
    task_class:str
    telemetry_band:str
    sample_count:int
    lower_ms:float | None
    upper_ms:float | None
    available:bool
    descriptive_only:bool=True
    certified:bool=False

class CausalNonnetworkCalibrator:
    def __init__(self):
        self.pending={}
        self.completed=set()
        self.samples=defaultdict(lambda:deque(maxlen=MAX_SCORES))
        self.last_time=0.
        self.dispatches=0
        self.finishes=0

    @staticmethod
    def number(v,label):
        if isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v) or v<0:
            raise ValueError("invalid "+label)
        return float(v)
    @staticmethod
    def band(v):
        age=CausalNonnetworkCalibrator.number(v,"telemetry age")
        return "age_0_10ms" if age<10 else ("age_10_25ms" if age<25 else "age_25plus_ms")
    @staticmethod
    def klass(v):
        if not isinstance(v,str) or v not in CLASSES:raise ValueError("invalid task class")
        return v
    @staticmethod
    def identifier(v):
        if isinstance(v,bool) or not isinstance(v,int) or v<0:raise ValueError("invalid task id")
        return v
    @staticmethod
    def node_id(v):
        if isinstance(v,bool) or not isinstance(v,int) or not 0<=v<21:
            raise ValueError("invalid node")
        return v

    def query(self,now_ms,task_class,telemetry_age_ms):
        now=self.number(now_ms,"query time")
        cls=self.klass(task_class)
        band=self.band(telemetry_age_ms)
        if now<self.last_time:raise ValueError("retroactive estimate")
        values=self.samples[(cls,band)]
        n=len(values)
        lower=upper=None
        if n>=MIN_SCORES:
            ordered=sorted(values)
            lower=ordered[math.floor((n-1)*.05)]
            upper=ordered[math.ceil((n-1)*.95)]
        self.last_time=now
        return QEstimate(CONTEXT,cls,band,n,lower,upper,n>=MIN_SCORES)

    def dispatch(self,index,node,task_class,dispatch_ms,telemetry_age_ms,
                 predicted_wait_ms,predicted_cpu_ms):
        idx=self.identifier(index)
        node=self.node_id(node)
        cls=self.klass(task_class)
        clock=self.number(dispatch_ms,"dispatch time")
        band=self.band(telemetry_age_ms)
        wait=self.number(predicted_wait_ms,"predicted wait")
        cpu=self.number(predicted_cpu_ms,"predicted CPU")
        if cpu<=0:raise ValueError("nonpositive nominal CPU")
        if clock<self.last_time or idx in self.pending or idx in self.completed:
            raise ValueError("duplicate or retroactive task dispatch")
        point=PendingQ(idx,node,cls,clock,band,wait,cpu)
        self.pending[idx]=point
        self.last_time=clock
        self.dispatches+=1
        return point

    def finish(self,index,node,start_ms,finish_ms):
        idx=self.identifier(index)
        node=self.node_id(node)
        item=self.pending.get(idx)
        if item is None or item.node!=node:
            raise ValueError("unknown or wrong-node completion")
        start=self.number(start_ms,"service start")
        finish=self.number(finish_ms,"CPU finish")
        if start<item.dispatched_ms or finish<start or finish<self.last_time:
            raise ValueError("noncausal CPU label")
        wait=start-item.dispatched_ms
        cpu=finish-start
        if cpu<=0:raise ValueError("nonpositive actual CPU")
        qwait=wait-item.predicted_wait_ms
        qcpu=cpu-item.predicted_cpu_ms
        total=(finish-item.dispatched_ms)-(item.predicted_wait_ms+item.predicted_cpu_ms)
        if not math.isclose(total,qwait+qcpu,rel_tol=0,abs_tol=1e-8):
            raise AssertionError("q total decomposition")
        self.samples[(item.task_class,item.telemetry_band)].append(total)
        self.completed.add(idx)
        del self.pending[idx]
        self.finishes+=1
        self.last_time=finish
        return total

    def invariant(self):
        assert self.dispatches==self.finishes+len(self.pending)
        assert self.finishes==len(self.completed)
        assert all(len(v)<=MAX_SCORES for v in self.samples.values())
