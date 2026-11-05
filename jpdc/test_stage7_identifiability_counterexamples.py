#!/usr/bin/env python3
"""Finite mathematical identification fixtures; NOT source simulation results.

Every world is deterministic, task-level, without queue coupling.
The first-paper CASPER code and physical source are not imported.
"""
import math
from dataclasses import dataclass

PROBES_PER_NORMAL=100
NODES=21

@dataclass(frozen=True)
class ObservedHistory:
    """Only arrived and delivered E2E observations, no latent outcomes."""
    delivered:tuple
    completed_feedback_time:float

@dataclass(frozen=True)
class LatentWorld:
    a_ms:float
    b_ms:float

GOOD=LatentWorld(10.0,6.0)
BAD=LatentWorld(10.0,14.0)

def world_regret(world:LatentWorld,probability_choose_b:float):
    if not all(math.isfinite(v) for v in (world.a_ms,world.b_ms,probability_choose_b)):
        raise ValueError("nonfinite latent world or probability")
    if min(world.a_ms,world.b_ms)<=0 or not 0<=probability_choose_b<=1:
        raise ValueError("invalid latency/probability")
    optimum=min(world.a_ms,world.b_ms)
    observed_policy_expected=((1-probability_choose_b)*world.a_ms+
                              probability_choose_b*world.b_ms)
    return observed_policy_expected-optimum

def is_distinguishable(history_good,history_bad,now):
    if not math.isfinite(now):raise ValueError("invalid decision time")
    def available(h):
        return tuple((received,node,value) for received,node,value in h.delivered
                     if received<=now)
    return available(history_good)!=available(history_bad)

def max_possible_first_observed_nodes(normal_count,nodes=NODES):
    if not isinstance(normal_count,int) or normal_count<0 or nodes<0:
        raise ValueError("nonnegative counts required")
    return min(nodes,normal_count//PROBES_PER_NORMAL)

def assert_two_world_minimax():
    for p in (0.,.1,.25,.5,.75,.9,1.):
        a=world_regret(GOOD,p)
        b=world_regret(BAD,p)
        assert math.isclose(a,4*(1-p),abs_tol=1e-12)
        assert math.isclose(b,4*p,abs_tol=1e-12)
        assert max(a,b)>=2-1e-12
    assert world_regret(GOOD,0)==4
    assert world_regret(BAD,1)==4
    assert max(world_regret(GOOD,.5),world_regret(BAD,.5))==2
    return True

def run():
    assert assert_two_world_minimax()
    print("PASS two-world common-history randomized minimax 2ms and deterministic worst-world 4ms")
    # Different latent b must NOT be visible before b's own E2E observation.
    hgood=ObservedHistory(((5.,0,10.),(100.,1,6.)),100.)
    hbad=ObservedHistory(((5.,0,10.),(100.,1,14.)),100.)
    for t in (0.,5.,50.,99.999999):
        assert not is_distinguishable(hgood,hbad,t)
    assert is_distinguishable(hgood,hbad,100.)
    print("PASS delayed feedback indistinguishable until actual completed E2E delivery")
    for m in (0,1,99,100,101,199,200,2100,9600):
        cap=max_possible_first_observed_nodes(m)
        assert cap==min(NODES,m//100)
        assert cap<=m//100
    assert max_possible_first_observed_nodes(9600)==21
    print("PASS 1-in-100 NORMAL budget only upper bounds first-new-node feedback coverage")
    # There is NO lower bound if feedback never arrives by horizon.
    never_delivered=ObservedHistory(((200.,1,6.),),200.)
    no_probe=ObservedHistory((),math.inf)
    assert not is_distinguishable(never_delivered,no_probe,199.)
    print("PASS before E2E report, dispatched exploratory task does not identify latent network state")
    for invalid in (-1,1.5,math.nan):
        try:
            if invalid<0:max_possible_first_observed_nodes(invalid)
            else:world_regret(GOOD,invalid)
        except ValueError:pass
        else:raise AssertionError("invalid world or probability accepted")
    print("JPDC_STAGE7_IDENTIFIABILITY_FINITE_COUNTEREXAMPLE_PASS")

if __name__=="__main__":run()
