#!/usr/bin/env python3
"""Stage24 externally provided signed queue-error envelopes + causal E2E bounds.

This is an assumption-conditioned controller with *no calibrated queue oracle*.
It does NOT estimate queue residuals, demonstrate coverage or promise performance.
"""
from dataclasses import dataclass
import math
from robust_interval_dominance_stage22 import (
    RobustDominanceController, NODES, MAX_FRESHNESS_MS, NUMERICAL_MARGIN_MS
)

@dataclass(frozen=True)
class QueueErrorEnvelope:
    node: int
    context: str
    lower_ms: float
    upper_ms: float
    measured_ms: float
    delivered_ms: float
    valid_until_ms: float

@dataclass(frozen=True)
class QueueDominanceDecision:
    node: int
    reference_node: int
    switched: bool
    uncertified: bool
    mission_upper_feasible: bool
    context: str
    candidate_upper_ms: float | None
    reference_lower_ms: float | None
    eligible_nodes: int
    probe: bool = False

class QueueErrorAwareController(RobustDominanceController):
    def __init__(self):
        super().__init__()
        self.queue_evidence = {}
        self.queue_deliveries = 0
        self.queue_expirations_encountered = 0

    @staticmethod
    def _time(value, name):
        if (isinstance(value,bool) or not isinstance(value,(int,float))
                or not math.isfinite(value) or value<0):
            raise ValueError("invalid "+name)
        return float(value)

    @staticmethod
    def _context(context):
        if not isinstance(context,str) or not context.strip() or len(context)>128:
            raise ValueError("nonblank bounded context is required")
        return context

    def deliver_queue_envelope(self,node,context,lower_ms,upper_ms,
                               measured_ms,delivered_ms,valid_until_ms):
        if isinstance(node,bool) or not isinstance(node,int) or not 0<=node<NODES:
            raise ValueError("invalid node")
        context=self._context(context)
        if any(isinstance(x,bool) or not isinstance(x,(int,float)) or not math.isfinite(x)
               for x in (lower_ms,upper_ms)):
            raise ValueError("signed error bounds must be finite numbers")
        if lower_ms>upper_ms:
            raise ValueError("inverted error bounds")
        measured=self._time(measured_ms,"measurement clock")
        delivered=self._time(delivered_ms,"delivery clock")
        expiry=self._time(valid_until_ms,"expiry clock")
        if measured>delivered or delivered<self.last_time or expiry<delivered:
            raise ValueError("noncausal or already-expired queue evidence")
        key=(node,context)
        old=self.queue_evidence.get(key)
        if old is not None and measured<old.measured_ms:
            raise ValueError("older measurement cannot overwrite newer queue evidence")
        report=QueueErrorEnvelope(node,context,float(lower_ms),float(upper_ms),
                                  measured,delivered,expiry)
        self.queue_evidence[key]=report
        self.last_time=delivered
        self.queue_deliveries+=1
        return report

    def select(self,now_ms,predicted_ms,nominal_network_ms,deadline_ms,
               is_normal,is_mission=False,context_key=""):
        self._positive_vector(predicted_ms,nominal_network_ms)
        now=self._time(now_ms,"dispatch clock")
        deadline=self._time(deadline_ms,"deadline")
        context=self._context(context_key)
        if not isinstance(is_normal,bool) or not isinstance(is_mission,bool) or (is_normal and is_mission):
            raise ValueError("invalid task class")
        if now<self.last_time:raise ValueError("retroactive dispatch")
        network=[self.observer.bounds(j,now,nominal_network_ms[j]) for j in range(NODES)]
        reference=min(range(NODES),key=lambda j:(predicted_ms[j],j))
        valid={}
        expired=0
        for j,b in enumerate(network):
            evidence=self.queue_evidence.get((j,context))
            if evidence is None:continue
            if now>evidence.valid_until_ms:
                expired+=1
                continue
            age=(now-b.last_observed_measurement_time
                 if b.last_observed_measurement_time is not None else math.inf)
            if (b.samples>0 and not b.unverified_after_alarm
                    and age<=MAX_FRESHNESS_MS
                    and math.isfinite(b.excess_latency_low_ms)
                    and math.isfinite(b.excess_latency_high_ms)):
                valid[j]=(b,evidence)
        selected=reference
        selected_upper=None
        ref_lower=None
        if reference in valid:
            ref_net,ref_queue=valid[reference]
            ref_lower=(predicted_ms[reference]+ref_net.excess_latency_low_ms
                       +ref_queue.lower_ms)
            alternatives=[]
            for j,(net,queue) in valid.items():
                if j==reference:continue
                upper=predicted_ms[j]+net.excess_latency_high_ms+queue.upper_ms
                if upper+NUMERICAL_MARGIN_MS>=ref_lower:continue
                if is_mission and upper>deadline:continue
                alternatives.append((upper,j))
            if alternatives:
                selected_upper,selected=min(alternatives)
        switched=selected!=reference
        self.last_time=now
        self.decisions+=1
        self.switches+=int(switched)
        self.mission_switches+=int(switched and is_mission)
        self.unverified_decisions+=int(not switched)
        self.queue_expirations_encountered+=expired
        return QueueDominanceDecision(
            node=selected,reference_node=reference,switched=switched,
            uncertified=not switched,
            mission_upper_feasible=bool(switched and is_mission and selected_upper<=deadline),
            context=context,candidate_upper_ms=selected_upper,
            reference_lower_ms=ref_lower,
            eligible_nodes=len(valid),probe=False)
