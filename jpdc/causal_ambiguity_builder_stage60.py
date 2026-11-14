#!/usr/bin/env python3
"""Stage60 time-causal finite-world constructor. SAMPLE MAX != true upper bound.

No hidden faults, future service, oracle counterfactuals or physical engine imports.
Fails CLOSED if any of the 21 nodes has insufficient fresh CPU/E2E feedback.
"""
from collections import deque
from dataclasses import dataclass
import math

NODES=21
WINDOW=32
CPU_MIN=4
NETWORK_MIN=8
MAX_AGE_MS=5000.0
TELEMETRY_MAX_AGE_MS=100.0

def num(x,positive=False):
    if (isinstance(x,bool) or not isinstance(x,(int,float))
            or not math.isfinite(x) or x<0 or (positive and x==0)):
        raise ValueError("finite nonnegative numeric required")
    return float(x)

def nodeid(j):
    if type(j) is not int or not 0<=j<NODES:
        raise ValueError("invalid node id")
    return j

def taskid(i):
    if type(i) is not int or i<0:
        raise ValueError("invalid task id")
    return i

@dataclass(frozen=True)
class Worlds:
    status:str
    worlds:tuple
    unavailable:tuple
    world_count:int
    conditional_only:bool=True
    empirically_calibrated:bool=False
    true_future_coverage_guaranteed:bool=False

class CausalAmbiguityBuilder:
    def __init__(self):
        self.cpu=[deque(maxlen=WINDOW) for _ in range(NODES)]
        self.net=[deque(maxlen=WINDOW) for _ in range(NODES)]
        self.last_cpu_measurement=[None]*NODES
        self.last_net_measurement=[None]*NODES
        self.seen=set()
        self.last_event=-1.0
        self.telemetry_time=None
        self.virtual_backlog=None
        self.quarantined=0
        self.accepted_cpu=0
        self.accepted_e2e=0

    def _event(self,channel,task,node,measurement,delivery):
        taskid(task);nodeid(node)
        measurement=num(measurement)
        delivery=num(delivery)
        if measurement>delivery or delivery<self.last_event:
            raise ValueError("future measurement or out-of-order delivery")
        key=(channel,task)
        if key in self.seen: raise ValueError("duplicate completed feedback event")
        self.seen.add(key)
        self.last_event=delivery
        last=self.last_cpu_measurement if channel=="CPU" else self.last_net_measurement
        if last[node] is not None and measurement<last[node]:
            self.quarantined+=1
            return False
        last[node]=measurement
        return True

    def cpu_complete(self,task_id,node,nominal_ms,actual_ms,finished_ms,delivered_ms):
        nominal=num(nominal_ms,positive=True)
        actual=num(actual_ms,positive=True)
        accepted=self._event("CPU",task_id,node,finished_ms,delivered_ms)
        if accepted:
            self.cpu[node].append(max(0.,actual-nominal))
            self.accepted_cpu+=1
        return accepted

    def e2e_delivered(self,task_id,node,nominal_network_ms,actual_network_ms,
                      cpu_finished_ms,delivered_ms):
        nominal=num(nominal_network_ms,positive=True)
        actual=num(actual_network_ms,positive=True)
        accepted=self._event("E2E",task_id,node,cpu_finished_ms,delivered_ms)
        if accepted:
            self.net[node].append(max(0.,actual-nominal))
            self.accepted_e2e+=1
        return accepted

    def observe_telemetry(self,now_ms,virtual_backlog_ms):
        now=num(now_ms)
        if now<self.last_event:raise ValueError("retroactive telemetry")
        if not isinstance(virtual_backlog_ms,(list,tuple)) or len(virtual_backlog_ms)!=NODES:
            raise ValueError("21 virtual backlog entries required")
        vals=tuple(num(v) for v in virtual_backlog_ms)
        self.virtual_backlog=vals
        self.telemetry_time=now
        self.last_event=now

    def construct(self,now_ms,predicted_ms,nominal_network_ms):
        now=num(now_ms)
        if now<self.last_event:raise ValueError("retroactive decision")
        if not isinstance(predicted_ms,(list,tuple)) or len(predicted_ms)!=NODES:
            raise ValueError("21 predicted latency values required")
        if not isinstance(nominal_network_ms,(list,tuple)) or len(nominal_network_ms)!=NODES:
            raise ValueError("21 nominal network values required")
        pred=tuple(num(x,positive=True) for x in predicted_ms)
        tuple(num(x,positive=True) for x in nominal_network_ms)
        unavailable=[]
        if self.telemetry_time is None or now-self.telemetry_time>TELEMETRY_MAX_AGE_MS:
            unavailable.append("TELEMETRY_MISSING_OR_STALE")
        for j in range(NODES):
            if len(self.cpu[j])<CPU_MIN or self.last_cpu_measurement[j] is None or (
                    now-self.last_cpu_measurement[j]>MAX_AGE_MS):
                unavailable.append(f"CPU_NODE_{j}_UNKNOWN_OR_STALE")
            if len(self.net[j])<NETWORK_MIN or self.last_net_measurement[j] is None or (
                    now-self.last_net_measurement[j]>MAX_AGE_MS):
                unavailable.append(f"E2E_NODE_{j}_UNKNOWN_OR_STALE")
        if unavailable:
            return Worlds("ABSTAIN_UNVERIFIED",(),tuple(unavailable),0)
        c=tuple(max(self.cpu[j]) for j in range(NODES))
        n=tuple(max(self.net[j]) for j in range(NODES))
        worlds=(pred,tuple(pred[j]+c[j] for j in range(NODES)),
                tuple(pred[j]+n[j] for j in range(NODES)),
                tuple(pred[j]+c[j]+n[j] for j in range(NODES)))
        if any(not math.isfinite(x) or x<=0 for world in worlds for x in world):
            raise ValueError("nonfinite historical-residual candidate cost")
        return Worlds("READY_UNCALIBRATED",worlds,(),len(worlds))
