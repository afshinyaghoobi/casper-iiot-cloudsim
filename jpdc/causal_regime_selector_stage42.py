#!/usr/bin/env python3
"""Stage42 causal resource-disturbance classification, NOT an oracle/guarantee.

CPU evidence at CPU FINISH only; network evidence at E2E delivery only.
First 256 per-channel reports freeze baseline, last64 give current share.
No scenario, task index or hidden affected-node identifier is an input.
"""
from collections import deque
from dataclasses import dataclass
import math

BASELINE=256
RECENT=64
FACTOR=1.5
MIN_RECENT_SHARE=.35
MIN_INCREASE=.20

@dataclass(frozen=True)
class RegimeDecision:
    regime:str
    cpu_bad_share:float|None
    network_bad_share:float|None
    cpu_baseline_share:float|None
    network_baseline_share:float|None
    cpu_signal:bool
    network_signal:bool

class CausalRegimeSelector:
    def __init__(self):
        self.baseline_cpu=[]
        self.baseline_network=[]
        self.cpu_recent=deque(maxlen=RECENT)
        self.network_recent=deque(maxlen=RECENT)
        self.last_cpu_clock=-math.inf
        self.last_net_clock=-math.inf
        self.cpu_observations=0
        self.network_observations=0
        self.dispatches=0
        self.network_dispatches=0
        self.ambiguous_dispatches=0
        self.first_network_dispatch_clock=None

    @staticmethod
    def _check(actual,nominal,now,last):
        if (any(type(v) not in (int,float) or not math.isfinite(v)
                for v in (actual,nominal,now)) or
            actual<=0 or nominal<=0 or now<last):
            raise ValueError("invalid, retrograde or premature observation")
        return int(actual/nominal>=FACTOR)

    def observe_cpu_finish(self,actual_cpu,nominal_cpu,finished_ms):
        bad=self._check(actual_cpu,nominal_cpu,finished_ms,self.last_cpu_clock)
        self.cpu_observations+=1
        if len(self.baseline_cpu)<BASELINE:self.baseline_cpu.append(bad)
        self.cpu_recent.append(bad)
        self.last_cpu_clock=finished_ms

    def observe_network_e2e(self,actual_net,nominal_net,delivered_ms):
        bad=self._check(actual_net,nominal_net,delivered_ms,self.last_net_clock)
        self.network_observations+=1
        if len(self.baseline_network)<BASELINE:self.baseline_network.append(bad)
        self.network_recent.append(bad)
        self.last_net_clock=delivered_ms

    def select(self,now_ms):
        if type(now_ms) not in (int,float) or not math.isfinite(now_ms):
            raise ValueError("invalid issue clock")
        if now_ms<max(self.last_cpu_clock,self.last_net_clock):
            raise ValueError("cannot issue in the past")
        baseline_complete=(len(self.baseline_cpu)==BASELINE and
                           len(self.baseline_network)==BASELINE)
        cbase=sum(self.baseline_cpu)/BASELINE if len(self.baseline_cpu)==BASELINE else None
        nbase=sum(self.baseline_network)/BASELINE if len(self.baseline_network)==BASELINE else None
        cshare=sum(self.cpu_recent)/RECENT if len(self.cpu_recent)==RECENT else None
        nshare=sum(self.network_recent)/RECENT if len(self.network_recent)==RECENT else None
        cpu=bool(baseline_complete and cshare>=MIN_RECENT_SHARE and
                 cshare>=cbase+MIN_INCREASE)
        network=bool(baseline_complete and nshare>=MIN_RECENT_SHARE and
                     nshare>=nbase+MIN_INCREASE)
        # CPU signal takes priority; ambiguity and insufficient history
        # fall back to source CASPER_FULL, not self-declared safe.
        regime="NETWORK" if network and not cpu else "FULL"
        self.dispatches+=1
        self.network_dispatches+=int(regime=="NETWORK")
        self.ambiguous_dispatches+=int(network and cpu)
        if regime=="NETWORK" and self.first_network_dispatch_clock is None:
            self.first_network_dispatch_clock=now_ms
        return RegimeDecision(regime,cshare,nshare,cbase,nbase,cpu,network)

    def invariant(self,count):
        assert self.dispatches==count
        assert self.cpu_observations==self.network_observations==count
        assert len(self.cpu_recent)<=RECENT and len(self.network_recent)<=RECENT
        assert len(self.baseline_cpu)<=BASELINE and len(self.baseline_network)<=BASELINE
        assert 0<=self.ambiguous_dispatches<=self.dispatches
        assert 0<=self.network_dispatches<=self.dispatches
