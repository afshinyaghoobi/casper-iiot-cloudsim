#!/usr/bin/env python3
"""Stage40 causal FULL-anchored MISSION feedback reranker (NOT certified)."""
from collections import deque
import math
from dataclasses import dataclass

NODES=21
WINDOW=32
MAX_AGE_MS=5000.
MIN_NETWORK=8
MIN_CPU=4
MIN_GAIN_MS=1.
MAX_NOMINAL_EXTRA_MS=2.

def nearest_rank(xs,level):
    vals=sorted(xs)
    return vals[math.ceil(len(vals)*level)-1]

@dataclass(frozen=True)
class FullRerank:
    node:int
    rank:int
    screened:bool
    changed:bool
    reason:str
    extra_nominal_ms:float
    predicted_gain_ms:float

class CausalFullAnchoredReranker:
    def __init__(self):
        self.network=[deque(maxlen=WINDOW) for _ in range(NODES)]
        self.cpu=[deque(maxlen=WINDOW) for _ in range(NODES)]
        self.network_last=[-math.inf]*NODES
        self.cpu_last=[-math.inf]*NODES
        self.total_network_e2e=0
        self.total_cpu_finish=0
        self.last_network_clock=-math.inf
        self.last_cpu_clock=-math.inf
        self.decisions=0
        self.mission_decisions=0
        self.switches=0
        self.reasons={}

    def observe_network(self,node,actual,nominal,delivered_ms):
        self._validate(node,actual,nominal,delivered_ms,self.last_network_clock)
        self.network[node].append(max(0.,actual-nominal))
        self.network_last[node]=delivered_ms
        self.last_network_clock=delivered_ms
        self.total_network_e2e+=1

    def observe_cpu(self,node,actual,nominal,finished_ms):
        self._validate(node,actual,nominal,finished_ms,self.last_cpu_clock)
        self.cpu[node].append(max(0.,actual-nominal))
        self.cpu_last[node]=finished_ms
        self.last_cpu_clock=finished_ms
        self.total_cpu_finish+=1

    @staticmethod
    def _validate(node,actual,nominal,stamp,last):
        if (type(node) is not int or not 0<=node<NODES or
            not all(type(x) in (float,int) and math.isfinite(x) for x in
                (actual,nominal,stamp)) or actual<=0 or nominal<=0 or stamp<last):
            raise ValueError("early, noncausal or invalid feedback")

    def _evidence(self,node,now,mode):
        if (len(self.network[node])<MIN_NETWORK or
                not 0<=now-self.network_last[node]<=MAX_AGE_MS):
            return None
        net=nearest_rank(self.network[node],.90)
        if mode=="E2E":return net
        if (len(self.cpu[node])<MIN_CPU or
                not 0<=now-self.cpu_last[node]<=MAX_AGE_MS):
            return None
        return net+nearest_rank(self.cpu[node],.75)

    def choose(self,now,pred,sigma,deadline,eta,qrank,base_node,base_rank,
               base_cert,family,mission,mode):
        if mode not in ("E2E","BOTH"):raise ValueError("unregistered mode")
        if (len(pred)!=NODES or len(sigma)!=NODES or
                not math.isfinite(now) or not math.isfinite(deadline) or
                not math.isfinite(eta) or eta<=0 or len(qrank)!=3 or
                not all(math.isfinite(x) and x>0 for x in pred) or
                not all(math.isfinite(x) and x>0 for x in sigma)):
            raise ValueError("invalid issue-time score")
        if family and base_node not in family:raise AssertionError("baseline outside frozen family")
        self.decisions+=1
        if mission:self.mission_decisions+=1
        def return_base(reason):
            self.reasons[reason]=self.reasons.get(reason,0)+1
            return FullRerank(base_node,base_rank,base_cert,False,reason,0.,0.)
        if not mission:return return_base("nonmission_original_full")
        if not base_cert:return return_base("baseline_no_screened_candidate")
        if len(family)!=3:return return_base("no_full_family")
        base=self._evidence(base_node,now,mode)
        if base is None:return return_base("reference_evidence_missing_or_stale")
        baseline_adjusted=pred[base_node]+base
        offers=[]
        for pos,j in enumerate(family):
            if j==base_node:continue
            if pred[j]>pred[base_node]+MAX_NOMINAL_EXTRA_MS+1e-10:continue
            # Original CASPER_FULL rank-conditioned CP screen (not a guarantee).
            if pred[j]+eta*qrank[pos]*sigma[j]>deadline:continue
            penalty=self._evidence(j,now,mode)
            if penalty is None:continue
            gain=baseline_adjusted-(pred[j]+penalty)
            if gain+1e-10<MIN_GAIN_MS:continue
            offers.append((pred[j]+penalty,pos,j,gain))
        if not offers:return return_base("no_eligible_fresh_gain")
        _,pos,j,gain=min(offers,key=lambda z:(z[0],z[1],z[2]))
        self.switches+=1
        self.reasons["mission_switched"]=self.reasons.get("mission_switched",0)+1
        return FullRerank(j,pos+1,True,True,"mission_switched",
                          pred[j]-pred[base_node],gain)

    def invariant(self,count):
        assert self.decisions==count
        assert self.total_cpu_finish==count
        assert self.total_network_e2e==count
        assert sum(self.reasons.values())==count
        assert self.switches==self.reasons.get("mission_switched",0)
        assert 0<=self.switches<=self.mission_decisions<=self.decisions
        assert all(len(x)<=WINDOW for x in [*self.network,*self.cpu])
