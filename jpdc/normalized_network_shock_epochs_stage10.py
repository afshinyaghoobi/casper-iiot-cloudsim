#!/usr/bin/env python3
"""Completed-E2E normalized network excess with observable shock epochs.

A simple *assumption-conditioned diagnostic*. No hidden source fault masks,
future network outcomes, physical CPU next-free or source shock index enters
this state. All accepted report history is retained per node for exact audits.
No real deadline or conditional stationary-regime guarantee is claimed.
"""
from dataclasses import dataclass
import math

NODES=21

@dataclass(frozen=True)
class NormalizedObservation:
    z:float
    measurement_time:float
    delivery_time:float

@dataclass(frozen=True)
class FeedbackEvent:
    kind:str
    node:int
    epoch:int
    slowdown:float
    delivered_time:float

@dataclass(frozen=True)
class NetworkBounds:
    node:int
    epoch:int
    samples:int
    normalized_low:float
    normalized_high:float
    excess_latency_low_ms:float
    excess_latency_high_ms:float
    conditionally_audited:bool
    unverified_after_alarm:bool
    last_observed_measurement_time:float | None

def _num(value,name,positive=False):
    if isinstance(value,bool) or not isinstance(value,(float,int)) or not math.isfinite(value) or value<0 or (positive and value==0):
        raise ValueError(f"invalid {name}")
    return float(value)

class NormalizedObservedNetworkEpochs:
    def __init__(self,drift_per_ms,epsilon,min_post_alarm_samples=2):
        if len(drift_per_ms)!=NODES or len(epsilon)!=NODES:
            raise ValueError("21-node externally specified parameters required")
        self.L=tuple(_num(x,"drift") for x in drift_per_ms)
        self.eps=tuple(_num(x,"normalized-error") for x in epsilon)
        if not isinstance(min_post_alarm_samples,int) or min_post_alarm_samples<2:
            raise ValueError("minimum post-alarm observations must be >=2")
        self.min_after_alarm=min_post_alarm_samples
        self.history=[[] for _ in range(NODES)]
        self.epoch=[0]*NODES
        self.alarms=[0]*NODES
        self.late_quarantined=[0]*NODES
        self.last_measurement=[-math.inf]*NODES
        self.last_delivery=-math.inf
        self.total_delivered=0

    def deliver(self,node,actual_network_ms,nominal_network_ms,generated_ms,delivered_ms):
        if not isinstance(node,int) or isinstance(node,bool) or not 0<=node<NODES:
            raise ValueError("invalid node")
        a=_num(actual_network_ms,"actual network duration",positive=True)
        n=_num(nominal_network_ms,"nominal network duration",positive=True)
        m=_num(generated_ms,"generation timestamp")
        d=_num(delivered_ms,"delivery timestamp")
        if m>d or d<self.last_delivery:
            raise ValueError("noncausal or nonmonotonic E2E feedback")
        z=max(0.,a/n-1.)
        if not math.isfinite(z):
            raise ValueError("unbounded normalized observation")
        # First classify a late-delivered older-generated event. It is not
        # allowed to erase newer accepted models or trigger historical alarm.
        if m<self.last_measurement[node]:
            self.late_quarantined[node]+=1
            self.last_delivery=d
            self.total_delivered+=1
            return FeedbackEvent("late_measurement_quarantined",node,self.epoch[node],z,d)
        new=NormalizedObservation(z,m,d)
        for old in self.history[node]:
            allowance=self.L[node]*abs(m-old.measurement_time)+2*self.eps[node]
            if abs(z-old.z)>allowance+1e-10:
                self.epoch[node]+=1
                self.alarms[node]+=1
                self.history[node]=[new]
                self.last_measurement[node]=m
                self.last_delivery=d
                self.total_delivered+=1
                return FeedbackEvent("observed_incompatible_change_alarm",node,self.epoch[node],z,d)
        self.history[node].append(new)
        self.last_measurement[node]=m
        self.last_delivery=d
        self.total_delivered+=1
        return FeedbackEvent("compatible_delivered_feedback",node,self.epoch[node],z,d)

    def bounds(self,node,now_ms,nominal_network_ms):
        if not isinstance(node,int) or isinstance(node,bool) or not 0<=node<NODES:
            raise ValueError("invalid node")
        t=_num(now_ms,"decision timestamp")
        nominal=_num(nominal_network_ms,"nominal task network duration",positive=True)
        if t<self.last_delivery:
            raise ValueError("cannot query time before already-delivered feedback")
        history=self.history[node]
        post_alarm=self.alarms[node]>0
        if not history:
            return NetworkBounds(node,self.epoch[node],0,0.,math.inf,0.,math.inf,
                                 False,False,None)
        low=0.
        high=math.inf
        for r in history:
            if r.delivery_time>t or r.measurement_time>t:
                raise AssertionError("future observation leaked into model state")
            radius=self.eps[node]+self.L[node]*(t-r.measurement_time)
            low=max(low,r.z-radius)
            high=min(high,r.z+radius)
        if low>high+1e-9:
            raise AssertionError("accepted epoch incompatible at decision")
        high=max(0.,high)
        return NetworkBounds(node,self.epoch[node],len(history),
                             max(low,0.),high,nominal*max(low,0.),nominal*high,
                             True,post_alarm and len(history)<self.min_after_alarm,
                             self.last_measurement[node])

    def choose(self,nominal_pred_ms,nominal_network_ms,now_ms):
        if len(nominal_pred_ms)!=NODES or len(nominal_network_ms)!=NODES:
            raise ValueError("all 21 nodes required")
        if not all(isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x) and x>0
                   for x in (*nominal_pred_ms,*nominal_network_ms)):
            raise ValueError("positive finite nominal predictions required")
        bounds=[self.bounds(j,now_ms,nominal_network_ms[j]) for j in range(NODES)]
        finite=[j for j,b in enumerate(bounds) if b.samples>0 and
                not b.unverified_after_alarm and math.isfinite(b.excess_latency_high_ms)]
        if not finite:
            j=min(range(NODES),key=lambda k:(nominal_pred_ms[k],k))
            return j,False,0,math.inf
        j=min(finite,key=lambda k:(nominal_pred_ms[k]+bounds[k].excess_latency_high_ms,k))
        return j,True,len(finite),bounds[j].excess_latency_high_ms

    def memory_size(self):
        return sum(len(history) for history in self.history)
