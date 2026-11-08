#!/usr/bin/env python3
"""Stage44 node-local causal resource alarm. NO oracle, no statistical guarantee."""
from collections import deque
from dataclasses import dataclass
import math

NODES=21
BASELINE=12
RECENT=12
CANDIDATES=6
SEVERITY=1.5
ALERT_RECENT_COUNT=5
ALERT_DELTA=.25

@dataclass(frozen=True)
class LocalDecision:
    regime:str
    candidate_nodes:tuple
    network_alert_nodes:tuple
    cpu_alert_nodes:tuple

class CausalNodeRegimeSelector:
    def __init__(self):
        self.cpu_baseline=[[] for _ in range(NODES)]
        self.net_baseline=[[] for _ in range(NODES)]
        self.cpu_recent=[deque(maxlen=RECENT) for _ in range(NODES)]
        self.net_recent=[deque(maxlen=RECENT) for _ in range(NODES)]
        self.cpu_last=-math.inf
        self.net_last=-math.inf
        self.cpu_observations=0
        self.network_observations=0
        self.decisions=0
        self.network_mode_decisions=0
        self.ambiguous_decisions=0
        self.first_network_mode_clock=None
        self.mission_network_decisions=0
        self.mission_full_decisions=0
        self.network_node_observation_counts=[0]*NODES
        self.cpu_node_observation_counts=[0]*NODES

    @staticmethod
    def _classify(node,actual,nominal,clock,latest):
        if type(node) is not int or not 0<=node<NODES:
            raise ValueError("invalid evidence node")
        if (any(type(x) not in (float,int) or not math.isfinite(x)
                for x in (actual,nominal,clock)) or
            actual<=0 or nominal<=0 or clock<latest):
            raise ValueError("invalid, noncausal, or retrograde evidence")
        return int(actual/nominal>=SEVERITY)

    def observe_cpu_finish(self,node,actual_cpu,nominal_cpu,finished_ms):
        x=self._classify(node,actual_cpu,nominal_cpu,finished_ms,self.cpu_last)
        if len(self.cpu_baseline[node])<BASELINE:self.cpu_baseline[node].append(x)
        self.cpu_recent[node].append(x)
        self.cpu_last=finished_ms
        self.cpu_observations+=1
        self.cpu_node_observation_counts[node]+=1

    def observe_network_e2e(self,node,actual_network,nominal_network,delivered_ms):
        x=self._classify(node,actual_network,nominal_network,delivered_ms,self.net_last)
        if len(self.net_baseline[node])<BASELINE:self.net_baseline[node].append(x)
        self.net_recent[node].append(x)
        self.net_last=delivered_ms
        self.network_observations+=1
        self.network_node_observation_counts[node]+=1

    @staticmethod
    def _alert(baseline,recent):
        if len(baseline)<BASELINE or len(recent)<RECENT:return False
        return (sum(recent)>=ALERT_RECENT_COUNT and
                sum(recent)/RECENT>=sum(baseline)/BASELINE+ALERT_DELTA)

    def select(self,now_ms,predicted_ms,mission):
        if (type(now_ms) not in (float,int) or not math.isfinite(now_ms) or
            now_ms<max(self.cpu_last,self.net_last)):
            raise ValueError("invalid dispatch clock")
        if (len(predicted_ms)!=NODES or
            any(type(x) not in (float,int) or not math.isfinite(x) or x<=0
                for x in predicted_ms)):
            raise ValueError("invalid issue-time predicted latency")
        if type(mission) is not bool:raise ValueError("mission must be boolean")
        close=tuple(sorted(range(NODES),key=lambda j:(predicted_ms[j],j))[:CANDIDATES])
        n=tuple(j for j in close
                if self._alert(self.net_baseline[j],self.net_recent[j]))
        c=tuple(j for j in close
                if self._alert(self.cpu_baseline[j],self.cpu_recent[j]))
        regime="NETWORK" if n and not c else "FULL"
        self.decisions+=1
        self.network_mode_decisions+=int(regime=="NETWORK")
        self.ambiguous_decisions+=int(bool(n) and bool(c))
        if regime=="NETWORK" and self.first_network_mode_clock is None:
            self.first_network_mode_clock=now_ms
        if mission:
            self.mission_network_decisions+=int(regime=="NETWORK")
            self.mission_full_decisions+=int(regime=="FULL")
        return LocalDecision(regime,close,n,c)

    def invariant(self,count,expected_mission):
        assert self.decisions==count
        assert self.cpu_observations==self.network_observations==count
        assert sum(self.cpu_node_observation_counts)==count
        assert sum(self.network_node_observation_counts)==count
        assert self.mission_network_decisions+self.mission_full_decisions==expected_mission
        assert 0<=self.ambiguous_decisions<=self.decisions
        assert 0<=self.network_mode_decisions<=self.decisions
        assert all(len(a)<=BASELINE for a in self.cpu_baseline+self.net_baseline)
        assert all(len(a)<=RECENT for a in self.cpu_recent+self.net_recent)
