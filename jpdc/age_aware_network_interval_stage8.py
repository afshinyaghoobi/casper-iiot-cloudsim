#!/usr/bin/env python3
"""Conditionally valid, age-aware residual envelopes from DELIVERED E2E reports.

Not an FGCS conformal certificate, distribution-free statement, or verified
real network model. Assumptions must be externally justified:
 |r_j(t)-r_j(s)| <= L_j |t-s| and |y_i-r_j(m_i)| <= epsilon_j.
The measurement GENERATION timestamp m_i, not delayed DELIVERY d_i, drives
the envelope width. Never route from future or undelivered feedback.
"""
from dataclasses import dataclass
import math

NODES=21

@dataclass(frozen=True)
class Report:
    node:int
    value_ms:float
    measurement_time_ms:float
    delivery_time_ms:float

@dataclass(frozen=True)
class Envelope:
    low_ms:float
    high_ms:float
    report_count:int
    latest_measurement_time_ms:float | None
    identifiable:bool

class AssumptionViolation(ValueError):
    """Delivered reports have no common latent trajectory under fixed bounds."""

def _nonnegative(x,name):
    if not isinstance(x,(float,int)) or not math.isfinite(x) or x<0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return float(x)

class AgeAwareResidualIntervals:
    def __init__(self,drift_ms_per_ms,noise_ms):
        if len(drift_ms_per_ms)!=NODES or len(noise_ms)!=NODES:
            raise ValueError("expect 21 externally justified node bounds")
        self.drift=tuple(_nonnegative(x,"drift") for x in drift_ms_per_ms)
        self.noise=tuple(_nonnegative(x,"noise") for x in noise_ms)
        self.reports=[[] for _ in range(NODES)]
        self.last_delivery_ms=-math.inf
        self.report_count=0

    def deliver(self,node,value_ms,measurement_time_ms,delivery_time_ms):
        if not isinstance(node,int) or isinstance(node,bool) or not 0<=node<NODES:
            raise ValueError("invalid node")
        y=_nonnegative(value_ms,"observed excess")
        m=_nonnegative(measurement_time_ms,"measurement generation time")
        d=_nonnegative(delivery_time_ms,"E2E feedback delivery time")
        if m>d or d<self.last_delivery_ms:
            raise ValueError("future-generated or nonmonotonic feedback")
        # Check the candidate against prior observations already delivered
        # at the same node, before mutating model state.
        incoming=Report(node,y,m,d)
        for previous in self.reports[node]:
            max_delta=(self.drift[node]*abs(m-previous.measurement_time_ms)
                       +2*self.noise[node])
            if abs(y-previous.value_ms)>max_delta+1e-9:
                raise AssumptionViolation("observations contradict bounded-noise and drift assumptions")
        self.reports[node].append(incoming)
        self.last_delivery_ms=d
        self.report_count+=1
        return incoming

    def envelope(self,node,now_ms):
        if not isinstance(node,int) or isinstance(node,bool) or not 0<=node<NODES:
            raise ValueError("invalid node")
        now=_nonnegative(now_ms,"decision time")
        if now<self.last_delivery_ms:
            raise ValueError("cannot query a past decision from future-ingested feedback")
        reports=self.reports[node]
        if not reports:
            return Envelope(0.0,math.inf,0,None,False)
        low=0.0
        high=math.inf
        newest=-math.inf
        for r in reports:
            age=now-r.measurement_time_ms
            if age<0 or r.delivery_time_ms>now:
                raise AssertionError("premature feedback made available")
            width=self.noise[node]+self.drift[node]*age
            low=max(low,r.value_ms-width)
            high=min(high,r.value_ms+width)
            newest=max(newest,r.measurement_time_ms)
        if low>high+1e-8:
            raise AssumptionViolation("no latent value satisfies observed bounds")
        return Envelope(max(low,0.0),max(high,0.0),len(reports),newest,True)

    def choose(self,predicted_latencies,now_ms):
        """Minimize finite nominal+worst-credible network excess, fail open explicitly.

        Returns (node, network_margin_ms, identified_decision,
                 observable_node_count, regret_ceiling_ms).
        Regret ceiling is only for exogenous one-step exact p_j + r_j.
        """
        if len(predicted_latencies)!=NODES or not all(
            isinstance(x,(int,float)) and math.isfinite(x) and x>0
            for x in predicted_latencies):
            raise ValueError("invalid nominal prediction vector")
        bounds=[self.envelope(j,now_ms) for j in range(NODES)]
        eligible=[j for j,b in enumerate(bounds) if b.identifiable]
        if not eligible:
            default=min(range(NODES),key=lambda j:(predicted_latencies[j],j))
            return default,math.inf,False,0,math.inf
        selected=min(eligible,key=lambda j:(
            predicted_latencies[j]+bounds[j].high_ms,j))
        upper=predicted_latencies[selected]+bounds[selected].high_ms
        global_lower=min(predicted_latencies[j]+bounds[j].low_ms
                         for j in range(NODES))
        return selected,bounds[selected].high_ms,True,len(eligible),max(0.0,upper-global_lower)

    def memory_size(self):
        return sum(len(a) for a in self.reports)
