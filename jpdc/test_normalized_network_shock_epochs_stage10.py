#!/usr/bin/env python3
"""Stage10 bounded observational model checks, no new simulator seeds.

Synthetic network task sizes reproduce only frozen physical_network algebra:
nominal=RTT+(input+output)*8000/BW; post-shock actual=nominal*2.
"""
import math
from normalized_network_shock_epochs_stage10 import NormalizedObservedNetworkEpochs,NODES
from independent_stochastic_physics import SCENARIOS

def make(L=.0001,eps=0.):
    return NormalizedObservedNetworkEpochs([L]*NODES,[eps]*NODES)

def near(a,b):
    assert math.isclose(a,b,rel_tol=0,abs_tol=1e-9),(a,b)

def main():
    assert SCENARIOS["S3_HIDDEN_NETWORK_50LOSS"]==(1.0,.50)
    assert SCENARIOS["S2_HIDDEN_COMPUTE_40LOSS"]==(.60,1.0)
    nsmall=3.+(1+1)*8000/20000
    nlarge=3.+(20+20)*8000/20000
    assert nlarge>nsmall
    m=make()
    e=m.deliver(0,nsmall,nsmall,0.,5.)
    assert e.kind=="compatible_delivered_feedback" and e.slowdown==0
    old=m.bounds(0,9.9,nlarge)
    assert old.samples==1 and old.epoch==0
    near(old.normalized_high,.0001*9.9)
    assert old.conditionally_audited
    print("PASS initial no-shock and age-aware conditional interval")

    # Shock has physically happened, but its outcome has NOT been delivered.
    # Nothing in this policy takes a true scenario mask or shock timestamp.
    before=m.bounds(0,19.9,nlarge)
    assert before.epoch==0 and m.alarms[0]==0
    # New task at t=10 with different bytes, actual network factor2,
    # network outcome visible only on E2E feedback delivery t=20.
    event=m.deliver(0,2*nlarge,nlarge,10.,20.)
    assert event.kind=="observed_incompatible_change_alarm"
    assert event.delivered_time==20. and event.epoch==1
    near(event.slowdown,1.)
    assert m.alarms[0]==1
    first=m.bounds(0,20.,nsmall)
    assert first.epoch==1 and first.samples==1 and first.unverified_after_alarm
    near(first.excess_latency_low_ms,nsmall*(1.-.0001*(20.-10.)))
    assert first.conditionally_audited
    print("PASS 2x whole-network shock triggers observation-only E2E epoch alarm (not at hidden change)")

    # Distinct task sizes receive exactly the same normalized slowdown.
    event2=m.deliver(0,2*nsmall,nsmall,22.,30.)
    assert event2.kind=="compatible_delivered_feedback" and m.alarms[0]==1
    near(event2.slowdown,1.)
    nextbounds=m.bounds(0,30.,nlarge)
    assert not nextbounds.unverified_after_alarm and nextbounds.samples==2
    assert nextbounds.excess_latency_high_ms>first.excess_latency_high_ms
    j,identified,coverage,margin=m.choose([10.]*21,[nsmall]*21,30.)
    assert j==0 and identified and coverage==1 and margin>=0
    print("PASS normalized slowdown equal for distinct task sizes; task-specific ms conversion exact")

    # Truly delayed E2E feedback of a generation-older task must not erase
    # the current observed epoch or retroactively trigger a new alarm.
    prev_count=m.memory_size()
    old=m.deliver(0,nsmall,nsmall,6.,35.)
    assert old.kind=="late_measurement_quarantined"
    assert m.late_quarantined[0]==1 and m.alarms[0]==1
    assert m.memory_size()==prev_count
    print("PASS late delivered older-generation observation quarantined without state contamination")

    # Restoration to pre-fault factor1 only known at future E2E arrival.
    restore=m.deliver(0,nsmall,nsmall,40.,50.)
    assert restore.kind=="observed_incompatible_change_alarm" and restore.epoch==2
    assert m.bounds(0,50.,nsmall).unverified_after_alarm
    assert m.alarms[0]==2
    print("PASS restoration is detected only after completed E2E feedback")

    # With epsilon>=.5 the two z values 0 and1 are compatible (2eps>=1).
    weak=make(L=0.,eps=.5)
    weak.deliver(0,nsmall,nsmall,0.,1.)
    ev=weak.deliver(0,2*nsmall,nsmall,10.,20.)
    assert ev.kind=="compatible_delivered_feedback" and weak.alarms[0]==0
    assert weak.bounds(0,30.,nsmall).normalized_low==0.
    assert weak.bounds(0,30.,nsmall).normalized_high==.5
    print("PASS change alarm NOT guaranteed under weak measurement precision")

    # A full 21-node toy fixture with truth used for tests ONLY, never
    # passed to the inference policy. All nodes have their own nominal
    # network latency and only some have a 2x multiplier after shock.
    twentyone=make(L=.0001)
    for j in range(NODES):
        rtt=2.+j/10
        bw=15000.+j*800
        bytes_mib=2.+j/3
        nominal=rtt+bytes_mib*8000./bw
        twentyone.deliver(j,nominal,nominal,0.,1.+j*.01)
    for j in range(NODES):
        rtt=2.+j/10
        bw=15000.+j*800
        bytes_mib=2.+j/3
        nominal=rtt+bytes_mib*8000./bw
        actually_affected=(j%4==0)
        factor=2. if actually_affected else 1.
        twentyone.deliver(j,nominal*factor,nominal,10.,40.+j*.01)
        assert twentyone.alarms[j]==int(actually_affected)
        b=twentyone.bounds(j,41.,nominal)
        assert b.unverified_after_alarm==actually_affected
    assert sum(twentyone.alarms)==6
    print("PASS source-formula 21-node toy shock only detects actually observed incompatible feedback")

    noobs=make()
    b=noobs.bounds(2,0,10.)
    assert b.samples==0 and math.isinf(b.excess_latency_high_ms)
    j,ok,coverage,penalty=noobs.choose([10.+j for j in range(NODES)],[nsmall]*NODES,0.)
    assert j==0 and not ok and coverage==0 and math.isinf(penalty)
    print("PASS unknown nodes cannot be mistaken for zero-risk certified nodes")

    # Important: input validation must not corrupt accepted history.
    snapshot=(m.memory_size(),m.total_delivered,m.epoch[0],m.last_delivery)
    invalid=((0,-1.,10.,60.,70.),(0,math.nan,10.,60.,70.),
             (0,10.,0.,60.,70.),(0,10.,10.,80.,70.),
             (0,10.,10.,60.,49.),(21,10.,10.,60.,70.))
    for args in invalid:
        try:m.deliver(*args)
        except ValueError:pass
        else:raise AssertionError("accepted invalid input "+str(args))
    assert snapshot==(m.memory_size(),m.total_delivered,m.epoch[0],m.last_delivery)
    print("PASS invalid feedback fails closed without changing state")
    print("JPDC_STAGE10_NORMALIZED_NETWORK_EPOCH_AND_SHOCK_FIXTURES_PASS")

if __name__=="__main__":main()
