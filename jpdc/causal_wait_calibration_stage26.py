#!/usr/bin/env python3
"""Stage26 strictly causal descriptive WAIT-residual calibrator.

No empirical coverage guarantee. Not a certified Stage24 queue envelope.
WAIT-only residual, delivered at CPU finish (never at dispatch).
"""
from collections import defaultdict,deque
from dataclasses import dataclass
import math

SOURCE_CONTEXT="native_python_strict_fcfs_vq_telemetry50ms"
CLASSES=("NORMAL","HIGH","MISSION")
MIN_SCORES=40
MAX_SCORES=200

@dataclass(frozen=True)
class WaitPoint:
    task_index:int
    node:int
    task_class:str
    dispatch_ms:float
    telemetry_age_ms:float
    predicted_wait_ms:float
    band:str

@dataclass(frozen=True)
class WaitInterval:
    context:str
    task_class:str
    telemetry_band:str
    samples:int
    lower_ms:float | None
    upper_ms:float | None
    available:bool
    descriptive_only:bool=True
    certified:bool=False

class CausalWaitCalibrator:
    """Observes completed jobs only, in CPU finish-time delivery order."""
    def __init__(self):
        self.pending={}
        self.completed=set()
        self.scores=defaultdict(lambda:deque(maxlen=MAX_SCORES))
        self.last_clock=0.0
        self.delivered=0
        self.dispatched=0

    @staticmethod
    def time(value,name):
        if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value) or value<0:
            raise ValueError("invalid "+name)
        return float(value)

    @staticmethod
    def band(age):
        age=CausalWaitCalibrator.time(age,"telemetry age")
        if age<10:return "age_0_10ms"
        if age<25:return "age_10_25ms"
        return "age_25plus_ms"

    @staticmethod
    def cls(value):
        if value not in CLASSES:raise ValueError("invalid task class")
        return value

    @staticmethod
    def index(idx):
        if isinstance(idx,bool) or not isinstance(idx,int) or idx<0:raise ValueError("invalid task id")
        return idx

    def dispatch(self,task_index,node,task_class,dispatch_ms,telemetry_age_ms,predicted_wait_ms):
        idx=self.index(task_index)
        if isinstance(node,bool) or not isinstance(node,int) or not 0<=node<21:
            raise ValueError("invalid node")
        cls=self.cls(task_class)
        now=self.time(dispatch_ms,"dispatch")
        age=self.time(telemetry_age_ms,"telemetry age")
        pred=self.time(predicted_wait_ms,"predicted wait")
        if now<self.last_clock or idx in self.pending or idx in self.completed:
            raise ValueError("retroactive or duplicate dispatch")
        point=WaitPoint(idx,node,cls,now,age,pred,self.band(age))
        self.pending[idx]=point
        self.last_clock=now
        self.dispatched+=1
        return point

    def finish(self,task_index,node,service_start_ms,cpu_finish_ms,actual_wait_ms):
        idx=self.index(task_index)
        if idx not in self.pending or idx in self.completed:
            raise ValueError("no pending unique task")
        point=self.pending[idx]
        if isinstance(node,bool) or not isinstance(node,int) or node!=point.node:
            raise ValueError("finish node mismatch")
        start=self.time(service_start_ms,"service start")
        finish=self.time(cpu_finish_ms,"CPU finish")
        wait=self.time(actual_wait_ms,"actual wait")
        if (finish<self.last_clock or start<point.dispatch_ms or start>finish
                or not math.isclose(wait,start-point.dispatch_ms,rel_tol=0,abs_tol=1e-8)):
            raise ValueError("future/retroactive/inconsistent queue label")
        residual=wait-point.predicted_wait_ms
        self.scores[(point.task_class,point.band)].append(residual)
        self.completed.add(idx)
        del self.pending[idx]
        self.last_clock=finish
        self.delivered+=1
        return residual

    def query(self,now_ms,task_class,telemetry_age_ms):
        now=self.time(now_ms,"query")
        cls=self.cls(task_class)
        band=self.band(telemetry_age_ms)
        if now<self.last_clock:raise ValueError("retroactive query")
        scores=self.scores[(cls,band)]
        n=len(scores)
        low=high=None
        if n>=MIN_SCORES:
            vals=sorted(scores)
            low=vals[math.floor((n-1)*.05)]
            high=vals[math.ceil((n-1)*.95)]
        # Explicitly never certify these numbers as bounds.
        self.last_clock=now
        return WaitInterval(SOURCE_CONTEXT,cls,band,n,low,high,n>=MIN_SCORES)

    def invariant(self):
        assert self.dispatched==self.delivered+len(self.pending)
        assert len(self.completed)==self.delivered
        assert all(0<=len(x)<=MAX_SCORES for x in self.scores.values())
