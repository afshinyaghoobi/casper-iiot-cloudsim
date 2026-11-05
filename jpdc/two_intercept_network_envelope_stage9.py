#!/usr/bin/env python3
"""Stage9 two-intercept algebra for conditional delivered-E2E network envelopes.

Three explicit validation contracts:
 - AUDITED: original Stage8 historical ledger + exact O(1) envelope summary
 - CHRONOLOGICAL: constant memory, exact pairwise historical audit ONLY when
   per-node measurement GENERATION times are nondecreasing in delivery order
 - UNAUDITED: constant memory arithmetic, NO drift-model validation claim

Not a conformal certificate, verified traffic model, or time-invariant risk.
"""
from dataclasses import dataclass
import math
from age_aware_network_interval_stage8 import (
    AgeAwareResidualIntervals,AssumptionViolation,NODES,Envelope)

@dataclass(frozen=True)
class SummaryStatus:
    envelope: Envelope
    historical_consistency_audited: bool
    contract: str

class TwoInterceptNetworkEnvelope:
    def __init__(self,drift_ms_per_ms,noise_ms,mode="audited"):
        if mode not in ("audited","chronological","unaudited"):
            raise ValueError("invalid validation mode")
        if len(drift_ms_per_ms)!=NODES or len(noise_ms)!=NODES:
            raise ValueError("21-node drift/noise bounds required")
        if not all(isinstance(x,(int,float)) and math.isfinite(x) and x>=0
                   for x in (*drift_ms_per_ms,*noise_ms)):
            raise ValueError("finite nonnegative drift and error bounds required")
        self.drift=tuple(float(x) for x in drift_ms_per_ms)
        self.noise=tuple(float(x) for x in noise_ms)
        self.mode=mode
        self.reference=(AgeAwareResidualIntervals(self.drift,self.noise)
                        if mode=="audited" else None)
        self.A=[-math.inf]*NODES
        self.B=[math.inf]*NODES
        self.count=[0]*NODES
        self.latest_measurement=[-math.inf]*NODES
        self.last_delivery=-math.inf

    def deliver(self,node,value_ms,measurement_time_ms,delivery_time_ms):
        if not isinstance(node,int) or isinstance(node,bool) or not 0<=node<NODES:
            raise ValueError("invalid node")
        for name,x in (("observed excess",value_ms),("generation",measurement_time_ms),
                       ("delivery",delivery_time_ms)):
            if not isinstance(x,(int,float)) or not math.isfinite(x) or x<0:
                raise ValueError(f"invalid {name}")
        y=float(value_ms);m=float(measurement_time_ms);d=float(delivery_time_ms)
        if m>d or d<self.last_delivery:
            raise ValueError("noncausal or out-of-order E2E feedback delivery")
        if self.mode=="chronological" and self.count[node] and m<self.latest_measurement[node]:
            raise ValueError("chronological-only mode cannot audit late older measurement")
        L=self.drift[node];eps=self.noise[node]
        # For all previous measurement times mi<=m, the two necessary and
        # sufficient pairwise constraints for every earlier observation are:
        # y-Lm <= min_i(yi - Lmi)+2eps = B+eps
        # y+Lm >= max_i(yi + Lmi)-2eps = A-eps.
        if self.mode=="chronological" and self.count[node]:
            if y-L*m>self.B[node]+eps+1e-9 or y+L*m<self.A[node]-eps-1e-9:
                raise AssumptionViolation("chronological reports violate drift/noise history")
        if self.reference is not None:
            # Original full ledger rejects arbitrary older-measurement
            # contradictions. Rejection leaves both states unmodified.
            self.reference.deliver(node,y,m,d)
        self.A[node]=max(self.A[node],y-eps+L*m)
        self.B[node]=min(self.B[node],y+eps-L*m)
        self.count[node]+=1
        self.latest_measurement[node]=max(self.latest_measurement[node],m)
        self.last_delivery=d

    def envelope(self,node,now_ms):
        if not isinstance(node,int) or isinstance(node,bool) or not 0<=node<NODES:
            raise ValueError("invalid node")
        if not isinstance(now_ms,(int,float)) or not math.isfinite(now_ms) or now_ms<0:
            raise ValueError("invalid decision time")
        now=float(now_ms)
        if now<self.last_delivery:
            raise ValueError("cannot query a past state after future feedback")
        if self.count[node]==0:
            e=Envelope(0.0,math.inf,0,None,False)
        else:
            L=self.drift[node]
            low=max(0.0,self.A[node]-L*now)
            high=self.B[node]+L*now
            if low>high+1e-8:
                raise AssumptionViolation("interval empty; delivered assumptions inconsistent")
            e=Envelope(low,max(0.0,high),self.count[node],
                       self.latest_measurement[node],True)
        if self.reference is not None:
            from_ledger=self.reference.envelope(node,now)
            if (abs(e.low_ms-from_ledger.low_ms)>1e-8
                or (math.isfinite(e.high_ms) != math.isfinite(from_ledger.high_ms))
                or (math.isfinite(e.high_ms)
                    and abs(e.high_ms-from_ledger.high_ms)>1e-8)
                or e.report_count!=from_ledger.report_count):
                raise AssertionError("compressed envelope deviated from original audited source")
        return SummaryStatus(e,self.mode!="unaudited",self.mode)

    def choose(self,predicted_latencies,now_ms):
        if len(predicted_latencies)!=NODES or not all(
            isinstance(x,(int,float)) and math.isfinite(x) and x>0
            for x in predicted_latencies):
            raise ValueError("invalid nominal latency vector")
        states=[self.envelope(j,now_ms) for j in range(NODES)]
        usable=[j for j,s in enumerate(states) if s.envelope.identifiable]
        if not usable:
            j=min(range(NODES),key=lambda k:(predicted_latencies[k],k))
            return j,math.inf,False,False,0
        j=min(usable,key=lambda k:(
            predicted_latencies[k]+states[k].envelope.high_ms,k))
        return j,states[j].envelope.high_ms,True,all(
            states[k].historical_consistency_audited for k in usable),len(usable)

    def constant_state_fields(self):
        return 5*NODES

    def total_record_memory(self):
        if self.reference is None:return 0
        return self.reference.memory_size()
