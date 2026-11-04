#!/usr/bin/env python3
"""Independent Python ports of frozen CASPER state logic, no Java dependencies.

These components deliberately expose state-machine behavior; NOT a full policy,
simulator, calibration or independent performance validation.
"""
from collections import deque
import math

def empirical_quantile(values, tau):
    a=sorted(values)
    if not a:raise ValueError("empty quantile sample")
    return a[math.ceil((len(a)-1)*tau)]

def clip_eta(eta):
    return max(1.0,min(3.0,eta))

class DualMemory:
    def __init__(self,reference):
        if len(reference)<200:raise ValueError("need >=200 reference")
        a=sorted(reference)
        self.slow=deque((a[math.floor(i*(len(a)-1)/199)] for i in range(200)),maxlen=200)
        self.recent=deque(maxlen=200)
        self.detector=deque(maxlen=50)
        self.reference_q95=empirical_quantile(self.slow,.95)
        self.alarm_ever=False
        self.transition_age=-1

    def eta_before_outcome(self):
        slow_eta=clip_eta(empirical_quantile(self.slow,.95)/self.reference_q95 if self.reference_q95>0 else 1.0)
        if 0<=self.transition_age<200 and len(self.recent)>=50:
            fast_eta=clip_eta(empirical_quantile(list(self.recent)[-50:],.95)/self.reference_q95 if self.reference_q95>0 else 1.0)
            return max(slow_eta,fast_eta)
        return slow_eta

    def observe(self,score):
        self.slow.append(score)
        self.recent.append(score)
        self.detector.append(score>self.reference_q95)
        if not self.alarm_ever and len(self.detector)==50 and sum(self.detector)>=12:
            self.alarm_ever=True
            self.transition_age=0
        if self.transition_age>=0:self.transition_age+=1

class NodeHealth:
    def __init__(self,threshold,window=8,exceedances=5):
        if window<=0 or not 0<exceedances<=window:raise ValueError("invalid health window")
        self.threshold=threshold
        self.window=window
        self.exceedances=exceedances
        self.recent=deque(maxlen=window)
        self.alarmed=False

    def observe(self,service_ms,nominal_ms):
        if self.alarmed:return True
        ratio=service_ms/max(nominal_ms,1e-12)
        self.recent.append(ratio>self.threshold)
        if len(self.recent)==self.window and sum(self.recent)>=self.exceedances:
            self.alarmed=True
        return self.alarmed

class VirtualQueue:
    def __init__(self,nodes):
        if nodes<=0:raise ValueError("nonpositive node count")
        self.next_free=[0.0]*nodes

    def reset_from_telemetry(self,actual_next_free):
        if len(actual_next_free)!=len(self.next_free):raise ValueError("telemetry size")
        self.next_free=list(actual_next_free)

    def predicted_backlog(self,node,now_ms):
        return max(0.0,self.next_free[node]-now_ms)

    def on_dispatch(self,node,now_ms,predicted_service_ms):
        self.next_free[node]=max(self.next_free[node],now_ms)+predicted_service_ms
