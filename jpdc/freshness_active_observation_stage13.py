#!/usr/bin/env python3
"""Stage13 standalone CAUSAL decision prototype; not validated scheduling efficacy.

Development-only design constants are hypotheses, NOT learned network guarantees.
No hidden affected-node masks, future service times or E42 changes.
"""
from dataclasses import dataclass
import math
from normalized_network_shock_epochs_stage10 import NormalizedObservedNetworkEpochs

NODES=21
DRIFT=.0001
EPS=0.0
MAX_FRESHNESS_MS=10000.0
PROBE_CADENCE=100
MAX_PROBE_EXTRA_MS=2.0

@dataclass(frozen=True)
class Selection:
    node:int
    verified:bool
    fresh_candidates:int
    fallback:bool
    probe:bool
    changed:bool
    selected_age_ms:float|None
    upper_extra_ms:float|None

class FreshnessAwareController:
    def __init__(self):
        self.observer=NormalizedObservedNetworkEpochs([DRIFT]*NODES,[EPS]*NODES)
        self.normal_arrivals=0
        self.probe_opportunities=0
        self.probe_attempts=0
        self.probe_skipped=0
        self.probe_changed=0
        self.mission_unverified=0
        self.last_time=0.0

    @staticmethod
    def _vector(pred,net):
        if len(pred)!=NODES or len(net)!=NODES or any(
            not isinstance(v,(int,float)) or isinstance(v,bool) or
            not math.isfinite(v) or v<=0 for v in (*pred,*net)):
            raise ValueError("positive finite 21-node predictions required")

    def deliver_e2e(self,node,actual_ms,nominal_ms,generated_ms,delivered_ms):
        if delivered_ms<self.last_time:
            raise ValueError("feedback earlier than already evaluated decision time")
        event=self.observer.deliver(node,actual_ms,nominal_ms,generated_ms,delivered_ms)
        self.last_time=delivered_ms
        return event

    def select(self,now_ms,predicted_ms,nominal_network_ms,deadline_ms,is_normal):
        self._vector(predicted_ms,nominal_network_ms)
        if not isinstance(is_normal,bool) or not all(
            isinstance(v,(int,float)) and math.isfinite(v) and v>=0
            for v in (now_ms,deadline_ms)):
            raise ValueError("invalid time, deadline or class")
        if now_ms<self.last_time:
            raise ValueError("retroactive decisions forbidden")
        self.last_time=now_ms
        fallback=min(range(NODES),key=lambda j:(predicted_ms[j],j))
        # Only estimates from E2E-delivered data, no internal physical engine.
        bs=[self.observer.bounds(j,now_ms,nominal_network_ms[j]) for j in range(NODES)]
        ages=[(now_ms-b.last_observed_measurement_time
               if b.last_observed_measurement_time is not None else math.inf)
              for b in bs]
        fresh=[j for j in range(NODES) if bs[j].samples and
               not bs[j].unverified_after_alarm and
               ages[j]<=MAX_FRESHNESS_MS and
               math.isfinite(bs[j].excess_latency_high_ms)]
        if fresh:
            chosen=min(fresh,key=lambda j:(predicted_ms[j]+bs[j].excess_latency_high_ms,j))
        else:
            chosen=fallback
        verified=chosen in fresh
        probe=False
        if is_normal:
            self.normal_arrivals+=1
            if self.normal_arrivals%PROBE_CADENCE==0:
                self.probe_opportunities+=1
                # The extra nominal delay is relative to the normal policy
                # decision, not an imagined zero-cost request.
                admissible=[j for j in range(NODES)
                    if predicted_ms[j]<=deadline_ms and
                    predicted_ms[j]-predicted_ms[chosen]<=MAX_PROBE_EXTRA_MS]
                if admissible:
                    # Prefer unknown/stale nodes, not nodes based on hidden truth.
                    candidate=max(admissible,key=lambda j:(
                        int(bs[j].samples==0),int(bs[j].unverified_after_alarm),
                        ages[j],-predicted_ms[j],-j))
                    probe=True
                    self.probe_attempts+=1
                    self.probe_changed+=int(candidate!=chosen)
                    chosen=candidate
                    verified=chosen in fresh
                else:
                    self.probe_skipped+=1
        else:
            self.mission_unverified+=int(not verified)
        self.probe_changed<=self.probe_attempts or (_ for _ in ()).throw(AssertionError("invalid probe count"))
        return Selection(chosen,verified,len(fresh),not verified,probe,
                         chosen!=fallback,ages[chosen] if math.isfinite(ages[chosen]) else None,
                         bs[chosen].excess_latency_high_ms if verified else None)

    def assert_budget(self):
        assert self.probe_opportunities==self.normal_arrivals//PROBE_CADENCE
        assert self.probe_attempts+self.probe_skipped==self.probe_opportunities
        assert 0<=self.probe_changed<=self.probe_attempts
