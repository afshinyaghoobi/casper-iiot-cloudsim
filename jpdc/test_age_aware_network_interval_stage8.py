#!/usr/bin/env python3
"""Adversarial finite fixtures for conditional age-aware interval algebra.

No held-out seed, physical event simulation, regression fit or p-value.
"""
import math
from age_aware_network_interval_stage8 import (
    AgeAwareResidualIntervals,AssumptionViolation,NODES)

def model(L=.1,epsilon=1.):
    return AgeAwareResidualIntervals([L]*NODES,[epsilon]*NODES)

def close(actual,expected):
    assert math.isclose(actual,expected,rel_tol=0,abs_tol=1e-9),(actual,expected)

def run():
    m=model()
    first=m.envelope(0,19.)
    assert not first.identifiable and first.report_count==0
    assert first.low_ms==0.0 and math.isinf(first.high_ms)
    pred=[20.]*NODES
    pred[0]=10.
    j,pen,identified,coverage,regret=m.choose(pred,19.)
    assert j==0 and not identified and coverage==0
    assert math.isinf(pen) and math.isinf(regret)
    print("PASS zero delivered reports => unknown high=inf, explicit uncertified fallback")

    m.deliver(0,8,10,20)
    try:m.envelope(0,19.99)
    except ValueError:pass
    else:raise AssertionError("queried past state after observing future feedback")
    b=m.envelope(0,30)
    close(b.low_ms,5.);close(b.high_ms,11.)
    assert b.latest_measurement_time_ms==10 and b.report_count==1
    assert m.choose(pred,30.)[:4]==(0,11.,True,1)
    print("PASS age measured from generation m=10, not feedback delivery d=20")

    # At time 40, a newly delivered report from a later task generated at 35
    # can tighten the interval without changing the source assumptions.
    m.deliver(0,9.,35.,40.)
    b=m.envelope(0,40.)
    close(b.low_ms,7.5);close(b.high_ms,10.5)
    assert b.latest_measurement_time_ms==35
    # Report delivered even later but generated earlier MUST NOT reset age.
    m.deliver(0,8.,12.,45.)
    b=m.envelope(0,45.)
    assert b.latest_measurement_time_ms==35
    assert b.low_ms<=9<=b.high_ms
    print("PASS multi-report intersection, delayed out-of-order generation never looks fresh")

    invalids=((0,8.,50.,49.),(0,8.,10.,44.),
              (21,8.,10.,50.),(0,-1.,10.,50.),
              (0,math.nan,10.,50.))
    for item in invalids:
        try:m.deliver(*item)
        except ValueError:pass
        else:raise AssertionError("accepted premature or malformed observation "+str(item))
    assert m.report_count==3
    print("PASS future generation, nonmonotone delivery, invalid node/excess rejected")

    inconsistent=model(0.,.1)
    inconsistent.deliver(2,2.,0.,10.)
    try:inconsistent.deliver(2,5.,0.,11.)
    except AssumptionViolation:pass
    else:raise AssertionError("physically inconsistent reports accepted")
    assert inconsistent.report_count==1
    print("PASS violated drift/noise assumptions fail closed without changing state")

    exact=model(0.,0.)
    for j in range(NODES):
        exact.deliver(j,float(j),0.,10.+j)
    pred=[20.]*NODES
    pred[0]=12.;pred[1]=10.5;pred[2]=8.
    choice,margin,identified,coverage,regret_bound=exact.choose(pred,100.)
    assert choice==2 and identified and coverage==NODES
    close(margin,2.)
    close(regret_bound,0.)
    for j in range(NODES):
        b=exact.envelope(j,100.)
        close(b.low_ms,float(j));close(b.high_ms,float(j))
    print("PASS zero drift/error means point-identified network risk across 21 nodes")

    # An assumed nonstationary 21-node latent network excess world, all
    # constructed observations satisfy |error|<=epsilon and bounded drift L.
    L=.02; eps=.3; t=100.
    world=model(L,eps)
    actual=[1.+(j%5)*.6 for j in range(NODES)]
    for j in range(NODES):
        observed=max(0.,actual[j]-L*(t-10)+.1)
        world.deliver(j,observed,10.,20.+j)
    for j,btrue in enumerate(actual):
        b=world.envelope(j,t)
        assert b.low_ms-1e-9<=btrue<=b.high_ms+1e-9,(j,b,btrue)
    pred=[10.+j*.15 for j in range(NODES)]
    selected,margin,identified,coverage,upper_regret=world.choose(pred,t)
    realized=pred[selected]+actual[selected]
    oracle=min(x+y for x,y in zip(pred,actual))
    assert identified and coverage==NODES
    assert 0<=realized-oracle<=upper_regret+1e-8
    print("PASS conditional 21-node latent state covered; one-step exogenous regret bounded")

    # Missing-feedback alternative cannot make the selected node a claimed
    # globally certified optimum; the regret interval becomes weak.
    partial=model(0.,0.)
    partial.deliver(0,15.,0.,10.)
    pred=[10.]*NODES
    j,margin,identified,coverage,regret=partial.choose(pred,20.)
    assert (j,margin,identified,coverage)==(0,15.,True,1)
    close(regret,15.)
    assert math.isinf(partial.envelope(1,20.).high_ms)
    print("PASS selected finite interval does not imply all nodes identified")

    for invalid in (([-1.]*21,[0.]*21),([0.]*20,[0.]*21),
                    ([math.nan]*21,[0.]*21)):
        try:AgeAwareResidualIntervals(*invalid)
        except ValueError:pass
        else:raise AssertionError("invalid drift/noise bounds accepted")
    try:world.choose([math.nan]+[1.]*20,100.)
    except ValueError:pass
    else:raise AssertionError("invalid predictions accepted")
    assert world.memory_size()==21
    print("JPDC_STAGE8_CONDITIONAL_AGE_AWARE_INTERVAL_UNIT_PASS")

if __name__=="__main__":run()
