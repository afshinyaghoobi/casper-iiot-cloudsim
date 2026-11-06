#!/usr/bin/env python3
"""Stage28 full nonnetwork q CPU-finish-only causal tests (no efficacy claims)."""
from causal_nonnetwork_calibration_stage28 import CausalNonnetworkCalibrator,MAX_SCORES

def invalid(fn):
    try:fn()
    except ValueError:return
    raise AssertionError("invalid state accepted")

def complete(c,i,at,cls="MISSION",age=5.,pred_wait=1.,pred_cpu=2.,wait=0.,cpu=3.):
    c.dispatch(i,i%21,cls,at,age,pred_wait,pred_cpu)
    return c.finish(i,i%21,at+wait,at+wait+cpu)

def test():
    c=CausalNonnetworkCalibrator()
    q=c.query(0.,"MISSION",5.)
    assert q.sample_count==0 and not q.available and not q.certified
    c.dispatch(0,0,"MISSION",1.,5.,0.,3.)
    assert c.query(1.,"MISSION",5.).sample_count==0
    assert c.finish(0,0,1.,4.)==0.
    print("PASS no future CPU or waiting score at dispatch")

    c=CausalNonnetworkCalibrator()
    for i in range(39):
        complete(c,i,10.*i,pred_cpu=3.,cpu=1.)
    assert c.query(390.,"MISSION",5.).sample_count==39 and not c.query(390.,"MISSION",5.).available
    complete(c,39,400.,pred_cpu=3.,cpu=1.)
    q=c.query(405.,"MISSION",5.)
    assert q.available and q.sample_count==40 and q.lower_ms==q.upper_ms==-3.
    assert q.descriptive_only and not q.certified
    print("PASS sparse abstention and signed CPU+WAIT error despite deterministic point interval")

    c=CausalNonnetworkCalibrator()
    c.dispatch(0,0,"HIGH",1.,9.99,0.,3.)
    c.dispatch(1,1,"HIGH",2.,10.,1.,3.)
    assert c.finish(1,1,2.,4.)==-2.
    assert c.query(4.,"HIGH",9.99).sample_count==0
    assert c.finish(0,0,5.,6.)==2.
    assert c.query(6.,"HIGH",9.99).sample_count==1
    assert c.query(6.,"HIGH",10.).sample_count==1
    assert c.query(6.,"MISSION",10.).sample_count==0
    print("PASS finish-order queue residual observations, classes and age bands isolated")

    c=CausalNonnetworkCalibrator()
    for i in range(MAX_SCORES+12):
        complete(c,i,10.*i,pred_wait=0.,pred_cpu=2.,cpu=(2. if i<12 else 3.))
    v=c.query(3000.,"MISSION",5.)
    assert v.sample_count==MAX_SCORES and v.lower_ms==v.upper_ms==1.
    old=v
    complete(c,MAX_SCORES+12,3010.,pred_wait=0.,pred_cpu=2.,cpu=13.)
    assert old.upper_ms==1.
    print("PASS rolling last 200 completed labels and immutable prior issue-time estimate")

    c=CausalNonnetworkCalibrator()
    c.dispatch(7,2,"NORMAL",10.,5.,1.,5.)
    snapshot=(c.last_time,c.dispatches,c.finishes,len(c.pending))
    bad=(
        lambda:c.dispatch(7,2,"NORMAL",11.,5.,1.,5.),
        lambda:c.dispatch(8,2,"NORMAL",9.,5.,1.,5.),
        lambda:c.dispatch(8,2,"NORMAL",11.,5.,1.,0.),
        lambda:c.query(9.,"NORMAL",5.),
        lambda:c.finish(7,2,9.,20.),
        lambda:c.finish(7,2,15.,14.),
        lambda:c.finish(7,3,12.,18.),
        lambda:c.finish(8,2,12.,18.),
    )
    for f in bad:
        invalid(f)
        assert snapshot==(c.last_time,c.dispatches,c.finishes,len(c.pending))
    assert c.finish(7,2,13.,18.)== (3.-1.)+(5.-5.)
    invalid(lambda:c.finish(7,2,13.,19.))
    c.invariant()
    print("PASS strict clock, duplicates, node mismatch and no mutation after rejection")

    # A source regime shift invalidates descriptive historical q intervals.
    c=CausalNonnetworkCalibrator()
    for i in range(40):
        complete(c,i,10.*i,pred_wait=0.,pred_cpu=2.,cpu=2.)
    q=c.query(400.,"MISSION",5.)
    assert q.available and q.lower_ms==q.upper_ms==0. and not q.certified
    new_true_error=25.
    assert not q.lower_ms<=new_true_error<=q.upper_ms
    print("PASS compute-regime shock counterexample defeats guarantee")
    print("JPDC_STAGE28_FULL_NONNETWORK_CAUSAL_UNIT_CONTRACT_PASS")

if __name__=="__main__":test()
