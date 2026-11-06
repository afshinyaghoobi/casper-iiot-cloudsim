#!/usr/bin/env python3
"""Stage26 deterministic causal WAIT calibration falsification fixtures."""
import math
from causal_wait_calibration_stage26 import CausalWaitCalibrator,MAX_SCORES,MIN_SCORES

def emit(c,idx,at,cls="MISSION",age=5.,pred=2.,actual=1.):
    c.dispatch(idx,idx%21,cls,at,age,pred)
    return c.finish(idx,idx%21,at+actual,at+actual+1.,actual)

def invalid(action):
    try:action()
    except ValueError:return
    raise AssertionError("invalid action unexpectedly accepted")

def test():
    c=CausalWaitCalibrator()
    x=c.query(0.,"MISSION",5.)
    assert not x.available and not x.certified and x.samples==0
    c.dispatch(0,0,"MISSION",1.,5.,2.)
    q=c.query(1.,"MISSION",5.)
    assert q.samples==0 and not q.available and 0 in c.pending
    c.finish(0,0,2.,3.,1.)
    assert c.query(3.,"MISSION",5.).samples==1
    print("PASS missing scores and unfinished tasks never become evidence")

    c=CausalWaitCalibrator()
    for i in range(39):
        emit(c,i,float(10*i),actual=1. if i%2 else 0.,pred=2.)
    x=c.query(390.,"MISSION",5.)
    assert x.samples==39 and not x.available
    emit(c,39,400.,actual=1.,pred=2.)
    y=c.query(402.,"MISSION",5.)
    assert y.available and y.samples==40 and not y.certified
    assert y.lower_ms<=-1. and y.upper_ms<0
    print("PASS 39 abstain, 40 descriptive interval, signed negative residual")

    # Completion order rather than dispatch order must determine scores.
    c=CausalWaitCalibrator()
    c.dispatch(1,1,"HIGH",1.,10.,0.)
    c.dispatch(2,2,"HIGH",2.,10.,0.)
    c.finish(2,2,2.,3.,0.)
    assert c.query(3.,"HIGH",10.).samples==1 and 1 in c.pending
    c.finish(1,1,4.,5.,3.)
    assert c.query(5.,"HIGH",10.).samples==2
    c.invariant()
    print("PASS delayed out-of-order completion never leaks pending labels")

    c=CausalWaitCalibrator()
    emit(c,1,10.,"NORMAL",9.999,pred=0.,actual=1.)
    emit(c,2,20.,"NORMAL",10.,pred=0.,actual=1.)
    emit(c,3,30.,"NORMAL",24.999,pred=0.,actual=1.)
    emit(c,4,40.,"NORMAL",25.,pred=0.,actual=1.)
    assert c.query(42.,"NORMAL",9.999).samples==1
    assert c.query(42.,"NORMAL",10.).samples==2
    assert c.query(42.,"NORMAL",25.).samples==1
    assert c.query(42.,"HIGH",9.999).samples==0
    print("PASS class and [0,10), [10,25), [25,+inf) bands isolated")

    c=CausalWaitCalibrator()
    for i in range(MAX_SCORES+12):
        emit(c,i,10.*i,pred=0.,actual=1. if i>=12 else 0.)
    z=c.query(10.*(MAX_SCORES+12), "MISSION",5.)
    assert z.samples==MAX_SCORES and z.lower_ms==z.upper_ms==1.
    c.invariant()
    print("PASS rolling window last 200 CPU-finish labels, not dispatches")

    c=CausalWaitCalibrator()
    for i in range(40):
        emit(c,i,float(i*10),pred=0.,actual=1.)
    old=c.query(400.,"MISSION",5.)
    emit(c,40,410.,pred=0.,actual=25.)
    assert old.lower_ms==old.upper_ms==1. and old.samples==40
    assert c.query(436.,"MISSION",5.).samples==41
    print("PASS immutable issued intervals cannot be retroactively changed")

    c=CausalWaitCalibrator()
    c.dispatch(1,1,"HIGH",10.,0.,1.)
    before=(c.last_clock,c.delivered,len(c.pending))
    invalid(lambda:c.dispatch(2,2,"HIGH",9.,0.,1.))
    invalid(lambda:c.dispatch(1,1,"HIGH",11.,0.,1.))
    invalid(lambda:c.finish(1,1,12.,11.,2.))
    invalid(lambda:c.finish(1,1,12.,13.,5.))
    invalid(lambda:c.finish(1,2,11.,13.,1.))
    invalid(lambda:c.query(9.,"HIGH",0.))
    invalid(lambda:c.dispatch(3,3,"HIGH",11.,-1.,1.))
    invalid(lambda:c.dispatch(3,3,"HIGH",11.,1.,float("nan")))
    assert before==(c.last_clock,c.delivered,len(c.pending))
    c.finish(1,1,12.,13.,2.)
    invalid(lambda:c.finish(1,1,12.,14.,2.))
    invalid(lambda:c.dispatch(1,1,"HIGH",14.,0.,1.))
    c.invariant()
    print("PASS reject retroactive clocks, duplicate ID, incompatible wait arithmetic and invalid source")

    c=CausalWaitCalibrator()
    for i in range(40):
        emit(c,i,10.*i,pred=0.,actual=1.)
    v=c.query(400.,"MISSION",5.)
    assert v.descriptive_only and not v.certified and v.available
    assert (v.lower_ms,v.upper_ms)==(1.,1.)
    print("PASS point intervals are still NEVER certified physical-error guarantees")
    print("JPDC_STAGE26_CAUSAL_WAIT_CALIBRATION_UNIT_CONTRACT_PASS")

if __name__=="__main__":test()
