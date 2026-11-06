#!/usr/bin/env python3
"""Stage22 conditional robust interval dominance, unit-stage algorithm ONLY.

Causal E2E-only observer. A nonconformal assumption-conditioned comparison:
only switch away from greedy when upper(candidate) < lower(greedy).
No explicit probing, no access to hidden node masks or physical service truth.
"""
from dataclasses import dataclass
import math
from normalized_network_shock_epochs_stage10 import NormalizedObservedNetworkEpochs

NODES=21
DRIFT=.0001             # Synthetic exploratory source assumption; uncalibrated.
EPS=0.0
MAX_FRESHNESS_MS=10000.0
NUMERICAL_MARGIN_MS=1e-9

@dataclass(frozen=True)
class RobustChoice:
    node:int
    reference_node:int
    switched:bool
    conditionally_dominated:bool
    mission_deadline_feasible:bool
    unverified:bool
    candidate_upper_ms:float | None
    reference_lower_ms:float | None
    fresh_eligible_nodes:int
    probe:bool=False

class RobustDominanceController:
    """Does not claim true queue/latency bounds or conformal coverage."""
    def __init__(self):
        self.observer=NormalizedObservedNetworkEpochs([DRIFT]*NODES,[EPS]*NODES)
        self.last_time=0.0
        self.decisions=0
        self.switches=0
        self.unverified_decisions=0
        self.mission_switches=0

    @staticmethod
    def _positive_vector(pred,nom):
        if len(pred)!=NODES or len(nom)!=NODES:
            raise ValueError("requires exactly 21 nodes")
        for x in (*pred,*nom):
            if isinstance(x,bool) or not isinstance(x,(int,float)) or not math.isfinite(x) or x<=0:
                raise ValueError("all predictions and nominal network durations must be finite positive")

    def deliver_e2e(self,node,actual_ms,nominal_ms,generated_ms,delivered_ms):
        # The underlying observer independently validates generation <= delivery
        # and source ordering. Reject retroactive delivery after decision time.
        if not isinstance(delivered_ms,(int,float)) or not math.isfinite(delivered_ms):
            raise ValueError("invalid delivery time")
        if delivered_ms<self.last_time:raise ValueError("retroactive feedback")
        event=self.observer.deliver(node,actual_ms,nominal_ms,generated_ms,delivered_ms)
        self.last_time=delivered_ms
        return event

    def select(self,now_ms,predicted_ms,nominal_network_ms,deadline_ms,is_normal):
        self._positive_vector(predicted_ms,nominal_network_ms)
        if not isinstance(is_normal,bool) or any(
            isinstance(v,bool) or not isinstance(v,(int,float)) or
            not math.isfinite(v) or v<0 for v in (now_ms,deadline_ms)):
            raise ValueError("invalid decision inputs")
        if now_ms<self.last_time:raise ValueError("retroactive routing decision")
        # No state change until all source-model bounds are evaluated.
        lower_and_upper=[self.observer.bounds(j,now_ms,nominal_network_ms[j])
                         for j in range(NODES)]
        g=min(range(NODES),key=lambda j:(predicted_ms[j],j))
        eligible=[]
        for j,b in enumerate(lower_and_upper):
            age=(now_ms-b.last_observed_measurement_time
                 if b.last_observed_measurement_time is not None else math.inf)
            if (b.samples>0 and not b.unverified_after_alarm and
                age<=MAX_FRESHNESS_MS and
                math.isfinite(b.excess_latency_low_ms) and
                math.isfinite(b.excess_latency_high_ms)):
                eligible.append(j)
        eligible_set=set(eligible)
        if g in eligible_set:
            reference_lower=predicted_ms[g]+lower_and_upper[g].excess_latency_low_ms
            options=[]
            for j in eligible:
                if j==g:continue
                upper=predicted_ms[j]+lower_and_upper[j].excess_latency_high_ms
                if upper+NUMERICAL_MARGIN_MS>=reference_lower:continue
                if not is_normal and upper>deadline_ms:continue
                options.append((upper,j))
            if options:
                upper,j=min(options)
                switched=True
                verified=True
            else:
                j=g;upper=None;switched=False;verified=False
        else:
            j=g;upper=None;switched=False;verified=False
            reference_lower=None
        self.last_time=now_ms
        self.decisions+=1
        self.switches+=int(switched)
        self.mission_switches+=int(switched and not is_normal)
        self.unverified_decisions+=int(not verified)
        return RobustChoice(
            node=j,reference_node=g,switched=switched,
            conditionally_dominated=verified,
            mission_deadline_feasible=bool(switched and not is_normal and upper<=deadline_ms),
            unverified=not verified,
            candidate_upper_ms=upper,
            reference_lower_ms=reference_lower,
            fresh_eligible_nodes=len(eligible),probe=False)

    def invariant(self):
        assert 0<=self.mission_switches<=self.switches<=self.decisions
        assert 0<=self.unverified_decisions<=self.decisions
