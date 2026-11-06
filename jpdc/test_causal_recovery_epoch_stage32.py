#!/usr/bin/env python3
"""Stage32 causal recovery counterexamples and context-specific reset tests."""
from causal_recovery_epoch_stage32 import CausalRecoveryGuard

def do(g,i,clock,cls="MISSION",age=5.,cpu_error=0.,wait=0.):
    decision=g.query(clock,cls,age)
    g.dispatch(i,i%21,cls,clock,age,0.,2.)
    label=g.finish(i,i%21,clock+wait,clock+wait+2.+cpu_error)
    assert abs(label-(wait+cpu_error))<1e-8
    return decision

def alarm_fixture():
    g=CausalRecoveryGuard()
    for i in range(40):
        d=do(g,i,50.*(i+1),cpu_error=(11. if i in (36,37,38) else 0.))
        assert d.phase=="prealarm_sparse"
    assert g.frozen.alarmed and g.epoch is not None
    assert g.epoch_started_ms==2002. and g.epoch.finishes==0
    assert g.abstained_pre_sparse==40
    return g

def invalid(fn):
    try:fn()
    except ValueError:return
    raise AssertionError("invalid input accepted")

def test():
    g=CausalRecoveryGuard()
    for i in range(39):
        d=do(g,i,50.*(i+1),cpu_error=0.)
        assert d.phase=="prealarm_sparse"
    assert not g.frozen.alarmed and g.epoch is None
    g.invariant()
    print("PASS without alarm original baseline remains and recovery epoch never exists")

    g=alarm_fixture()
    for i in range(40,79): # exactly39 fresh MISSION age5 post-alarm labels
        d=do(g,i,50.*(i+1))
        assert d.phase=="postalarm_rebuild" and not d.issued
    assert g.epoch.finishes==39
    snapshot=g.query(4000.,"MISSION",5.)
    assert snapshot.phase=="postalarm_rebuild" and snapshot.original.sample_count==39
    g.dispatch(79,79%21,"MISSION",4000.,5.,0.,2.)
    g.finish(79,79%21,4000.,4002.)
    assert g.epoch.finishes==40
    d=g.query(4050.,"MISSION",5.)
    assert d.issued and d.phase=="postalarm_recovered_descriptive"
    assert d.original.sample_count==40 and d.original.lower_ms==d.original.upper_ms==0.
    assert not d.certified and not d.original.certified
    g.dispatch(80,80%21,"MISSION",4050.,5.,0.,2.)
    g.finish(80,80%21,4050.,4052.)
    assert g.recovery_times[("MISSION","age_0_10ms")]==4050.
    other=g.query(4100.,"MISSION",15.)
    assert other.phase=="postalarm_rebuild" and not other.issued
    g.dispatch(81,81%21,"MISSION",4100.,15.,0.,2.)
    g.finish(81,81%21,4100.,4102.)
    high=g.query(4150.,"HIGH",5.)
    assert high.phase=="postalarm_rebuild" and not high.issued
    g.dispatch(82,82%21,"HIGH",4150.,5.,0.,2.)
    g.finish(82,82%21,4150.,4152.)
    g.invariant()
    print("PASS 39 finished labels abstain, 40 recover only matching class-age; never certified")

    g=alarm_fixture()
    # Verify prealarm-dispatched job that CPU-finishes AFTER alarm cannot
    # enter post-alarm estimator even though its finish is chronologically new.
    # Separate fixture: insert pending before last alarm trigger.
    g=CausalRecoveryGuard()
    g.query(1.,"MISSION",5.)
    g.dispatch(999,1,"MISSION",1.,5.,0.,2.)
    for i in range(40):
        do(g,i,50.*(i+1),cpu_error=(11. if i in (36,37,38) else 0.))
    assert g.frozen.alarmed and g.epoch.finishes==0
    pre=g.query(2050.,"MISSION",5.)
    assert pre.phase=="postalarm_rebuild"
    g.dispatch(1001,1,"MISSION",2050.,5.,0.,2.)
    # Prealarm job can complete after the alarm but is excluded from epoch.
    g.finish(999,1,2100.,2102.)
    assert g.epoch.finishes==0
    g.finish(1001,1,2110.,2112.)
    assert g.epoch.finishes==1 and g.epoch.dispatches==1
    g.invariant()
    print("PASS CPU finishes of prealarm-dispatched jobs never contaminate new epoch")

    g=alarm_fixture()
    before=(g.frozen.base.finishes,g.epoch.finishes,len(g.epoch.samples))
    invalid(lambda:g.finish(666,0,2003.,2010.))
    invalid(lambda:g.dispatch(99,99%21,"HIGH",2001.,5.,0.,2.))
    assert before==(g.frozen.base.finishes,g.epoch.finishes,len(g.epoch.samples))
    print("PASS reject unknown CPU future evidence and retrograde dispatch")
    print("JPDC_STAGE32_POSTALARM_EPOCH_CAUSAL_RECOVERY_UNIT_PASS")

if __name__=="__main__":test()
