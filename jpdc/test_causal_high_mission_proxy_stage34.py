#!/usr/bin/env python3
"""Stage34 causal proxy and adversarial negative transfer contract."""
from causal_high_mission_proxy_stage34 import CausalClassProxyRecovery

def task(g,i,t,cls="MISSION",age=5.,resid=0.):
    d=g.query(t,cls,age)
    g.dispatch(i,i%21,cls,t,age,0.,2.)
    actual_end=t+2.+resid
    assert actual_end>t
    e=g.finish(i,i%21,t,actual_end)
    assert abs(e-resid)<1e-8
    return d

def start_alarm():
    g=CausalClassProxyRecovery()
    for i in range(40):
        d=task(g,i,50.*(i+1),resid=(11. if i in (36,37,38) else 0.))
        assert not d.issued
    assert g.frozen.alarmed and g.epoch.finishes==0
    return g

def prepare(own_error=0.,donor_error=0.):
    g=start_alarm()
    k=40
    for _ in range(40):
        task(g,k,50.*(k+1),cls="HIGH",resid=donor_error)
        k+=1
    for _ in range(10):
        task(g,k,50.*(k+1),cls="MISSION",resid=own_error)
        k+=1
    assert g.epoch.finishes==50
    return g,k

def test():
    g=start_alarm()
    for i in range(40,80):
        task(g,i,50.*(i+1),cls="HIGH")
    assert g.query(4050.,"MISSION",5.).phase=="postalarm_rebuild"
    assert g.proxy_issued==0
    print("PASS HIGH donor 40 without MISSION own 10 never transfers")

    g=start_alarm()
    for i in range(40,50):
        task(g,i,50.*(i+1),cls="MISSION")
    assert g.query(2550.,"MISSION",5.).phase=="postalarm_rebuild"
    print("PASS MISSION own 10 without HIGH donor 40 never transfers")

    g,k=prepare()
    z=g.query(50.*(k+1),"MISSION",5.)
    assert z.issued and z.phase=="postalarm_proxy_descriptive"
    assert z.proxy_source=="HIGH" and not z.certified
    assert z.original.lower_ms==z.original.upper_ms==0.
    assert z.original.task_class=="MISSION" and z.original.descriptive_only
    g.dispatch(k,k%21,"MISSION",50.*(k+1),5.,0.,2.)
    g.finish(k,k%21,50.*(k+1),50.*(k+1)+2.)
    assert g.query(50.*(k+2),"MISSION",15.).phase=="postalarm_rebuild"
    assert g.query(50.*(k+2),"NORMAL",5.).phase=="postalarm_rebuild"
    g.invariant()
    print("PASS 40 HIGH plus 10 compatible MISSION emits same-age labeled uncertified proxy only")

    g,k=prepare(own_error=20.,donor_error=0.)
    z=g.query(50.*(k+1),"MISSION",5.)
    assert not z.issued and z.phase=="postalarm_rebuild"
    assert g.proxy_issued==0
    print("PASS negative transfer HIGH zero vs MISSION +20ms rejected")

    g,k=prepare(own_error=0.,donor_error=0.)
    t=50.*(k+1)
    z=g.query(t,"MISSION",5.)
    assert z.issued and z.original.upper_ms==0.
    g.dispatch(k,k%21,"MISSION",t,5.,0.,2.)
    unseen_future_error=20.
    g.finish(k,k%21,t,t+2.+unseen_future_error)
    assert unseen_future_error>z.original.upper_ms
    assert z.original.upper_ms==0. and not z.certified
    g.invariant()
    print("PASS future CPU regime jump invalidates issued proxy despite prior perfect own/donor match")

    g,k=prepare()
    # A fresh exact-own 40 score interval always takes precedence.
    for i in range(k,k+30):
        task(g,i,50.*(i+1),"MISSION",5.,0.)
    own=g.query(50.*(k+31),"MISSION",5.)
    assert own.phase=="postalarm_recovered_descriptive" and own.original.sample_count>=40
    assert not own.certified
    print("PASS exact MISSION own 40 takes precedence over HIGH proxy")
    print("JPDC_STAGE34_CAUSAL_HIGH_MISSION_NEGATIVE_TRANSFER_UNIT_PASS")

if __name__=="__main__":test()
