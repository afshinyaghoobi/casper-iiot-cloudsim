#!/usr/bin/env python3
"""Stage37 deterministic causal deadline-score selection adversarial tests."""
from feedback_deadline_scheduler import CausalFeedbackDeadlineScheduler

def vector(a,b):
    x=[100.+2.*i for i in range(21)]
    x[0]=a;x[1]=b
    return x

def invalid(f):
    try:f()
    except ValueError:return
    raise AssertionError("invalid input accepted")

def run():
    c=CausalFeedbackDeadlineScheduler()
    net=[0.]*21
    v=vector(100.,101.)
    z=c.select(v,102.,"MISSION",net,"BOTH")
    assert z.node==0 and z.nominal_extra_ms==0
    assert c.cpu_finishes==0 and c.decisions==1
    # Future CPU truth before physical completion is NOT readable.
    a=c.select(v,102.,"MISSION",net,"CPU")
    assert a.node==0
    # CPU label at observed finish, not at dispatch: min four evidence.
    for i in range(3):
        c.observe_cpu(0,30.,10.,float(i+1))
    assert c.cpu_penalties()[0]==0.
    for i in range(3,4):
        c.observe_cpu(0,30.,10.,float(i+1))
    assert c.cpu_penalties()[0]==20.
    switched=c.select(v,102.,"MISSION",net,"CPU")
    assert switched.node==1 and switched.nominal_extra_ms==1
    # Network-only arm cannot look into CPU sensor.
    unaffected=c.select(v,102.,"MISSION",net,"E2E")
    assert unaffected.node==0
    # Network issue-time observations must be provided by e2e network observer.
    net[0]=10.
    switched_net=c.select(v,102.,"MISSION",net,"E2E")
    assert switched_net.node==1
    assert c.select(v,102.,"MISSION",net,"BOTH").node==1
    # Deadline logic cannot rescue infeasible predicted routes; no false claim.
    infeasible=c.select(v,30.,"MISSION",net,"BOTH")
    assert infeasible.predicted_deadline_feasible is False
    # Hard nominal routing budget prevents very distant alternatives even if
    # observed high errors make a distant node look better.
    v=vector(100.,103.)
    assert c.select(v,102.,"MISSION",net,"BOTH").node==0
    assert c.select(v,102.,"HIGH",net,"BOTH").node==1
    assert c.budget_violations==0
    invalid(lambda:c.select([1.]*20,10.,"MISSION",[0.]*21,"CPU"))
    invalid(lambda:c.select([1.]*21,10.,"MISSION",[-1.]*21,"CPU"))
    invalid(lambda:c.select([1.]*21,10.,"MISSION",[0.]*21,"UNKNOWN"))
    invalid(lambda:c.observe_cpu(0,30.,10.,3.))
    invalid(lambda:c.observe_cpu(21,30.,10.,8.))
    invalid(lambda:c.observe_cpu(0,0.,10.,8.))
    assert c.cpu_finishes==4
    assert c.changed>0 and c.mission_changed>0
    print("JPDC_STAGE37_CAUSAL_CPU_E2E_DEADLINE_SELECTION_UNIT_PASS")
    print("STAGE37_BUDGET_CAUSALITY_AND_NEGATIVE_DEADLINE_COUNTEREXAMPLE_PASS")

if __name__=="__main__":run()
