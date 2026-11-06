#!/usr/bin/env python3
"""Stage30 preregistered adversarial causal drift alarm contract tests."""
from causal_cpu_shift_guard_stage30 import (
    CausalCpuShiftGuard,POSITIVE_CPU_ERROR_THRESHOLD_MS)

def task(g,i,at,cpu_err=0.,cls="MISSION"):
    # No work/service labels observable until AFTER simulated task dispatch.
    q=g.query(at,cls,5.)
    g.dispatch(i,i%21,cls,at,5.,0.,2.)
    start=at
    finish=at+2.+cpu_err
    assert finish>at
    r=g.finish(i,i%21,start,finish)
    assert abs(r-cpu_err)<1e-9
    return q

def invalid(fn):
    try:fn()
    except ValueError:return
    raise AssertionError("invalid operation accepted")

def test():
    g=CausalCpuShiftGuard()
    assert not g.query(0.,"MISSION",5.).issued
    assert g.sparse_abstentions==1
    for i in range(39):
        task(g,i,50.*(i+1),11. if i>=36 else 0.)
    assert g.finished_cpu_labels==39 and not g.alarmed
    assert sum(hit for _,hit in g.last_window)==3
    # Min 40 completed label gate, not task arrivals.
    task(g,39,2000.,0.)
    assert g.alarmed and g.first_alarm_task_index==39
    assert g.first_alarm_delivery_ms==2002.
    assert len(g.alarm_positive_evidence)==3
    a=g.query(2005.,"MISSION",5.)
    assert a.original.available and not a.issued
    assert a.abstention_reason=="cpu_shift_alarm" and not a.certified
    print("PASS 39 labels cannot alarm; three of last eight at 40 triggers at CPU finish")

    g=CausalCpuShiftGuard()
    for i in range(40):
        task(g,i,50.*(i+1),10. if i in (36,37,38) else 0.)
    assert not g.alarmed
    first=g.query(2005.,"MISSION",5.)
    assert first.issued and first.abstention_reason is None
    # Query snapshot is frozen, even when alarm subsequently fires.
    task(g,40,2050.,11.)
    task(g,41,2100.,11.)
    assert not g.alarmed
    task(g,42,2150.,11.)
    assert g.alarmed and g.alarm_count==1
    assert first.issued and first.original.available and not first.certified
    post=g.query(2165.,"MISSION",5.)
    assert post.abstention_reason=="cpu_shift_alarm"
    task(g,43,2200.,0.)
    assert g.alarm_count==1 and g.alarmed
    assert g.base.dispatches==44 and g.base.finishes==44
    print("PASS threshold strictly >10, two >10 outliers insufficient, irrevocable issue-time status")

    g=CausalCpuShiftGuard()
    for i in range(39):
        task(g,i,50.*(i+1),-1. if i%3==0 else 0.)
    assert not g.alarmed
    # Pending task's extremely high future CPU error is NOT observable at dispatch.
    g.query(2001.,"MISSION",5.)
    g.dispatch(39,18,"MISSION",2001.,5.,0.,2.)
    assert not g.alarmed
    # Intruder earlier event / wrong node / duplicate cannot alter monitor state.
    before=(g.finished_cpu_labels,g.alarmed,len(g.last_window),g.base.finishes)
    invalid(lambda:g.finish(39,17,2001.,2021.))
    invalid(lambda:g.finish(39,18,2000.,2021.))
    assert before==(g.finished_cpu_labels,g.alarmed,len(g.last_window),g.base.finishes)
    g.finish(39,18,2001.,2021.)
    assert not g.alarmed
    invalid(lambda:g.finish(39,18,2001.,2022.))
    print("PASS future CPU truth and invalid completion cannot mutate alarm")

    g=CausalCpuShiftGuard()
    g.query(1.,"HIGH",5.);g.dispatch(1,1,"HIGH",1.,5.,0.,2.)
    g.query(2.,"MISSION",5.);g.dispatch(2,2,"MISSION",2.,5.,0.,2.)
    g.finish(2,2,2.,4.)
    assert g.finished_cpu_labels==1
    g.finish(1,1,5.,6.)
    assert g.finished_cpu_labels==2
    g.invariant()
    print("PASS finish order (not dispatch order), class-independent observation")
    print("JPDC_STAGE30_CAUSAL_CPU_SHIFT_ALARM_UNIT_CONTRACT_PASS")

if __name__=="__main__":test()
