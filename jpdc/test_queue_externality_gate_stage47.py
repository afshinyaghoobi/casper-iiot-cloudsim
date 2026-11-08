#!/usr/bin/env python3
"""Stage47 adversarial queue-gate tests, no stochastic physical source needed."""
from dataclasses import dataclass
from queue_externality_gate_stage47 import QueueExternalityGate

@dataclass(frozen=True)
class Proposed:
    node:int
    corrected_pred_ms:float

def run():
    g=QueueExternalityGate()
    pred=[100.+i for i in range(21)]
    pred[0]=100.;pred[1]=101.
    wait=[0.]*21
    alarms=[False]*21
    network=[0.]*21
    cpu=[0.]*21
    network[0]=15.
    def take(j=1,corrected=102.,p=pred,w=wait,a=alarms,
             deadline=130.,net=network,cp=cpu,mode="E2E"):
        return g.choose(0,Proposed(j,corrected),p,w,deadline,a,net,cp,mode)
    assert take().switched and take().node==1
    assert take(0).reason=="unchanged_original_full"
    alarms[1]=True
    assert take().reason=="candidate_health_alarm"
    alarms[1]=False
    pred[1]=103.
    assert take().reason=="extra_nominal_vs_full"
    pred[1]=101.
    wait[1]=.1
    assert take().reason=="extra_virtual_backlog"
    wait[1]=0.
    network[0]=3.
    assert take().reason=="insufficient_delivered_gain"
    network[0]=15.
    assert take(deadline=103.).reason=="no_candidate_deadline_slack"
    pred[0]=140.

    pred[0]=100.
    # CPU signal is observed only when the caller supplies FINISHED service labels.
    network[0]=0.
    cpu[0]=15.
    assert not take(mode="E2E").switched
    assert take(mode="BOTH").switched
    try:
        take(mode="ORACLE")
        raise AssertionError("accepted oracle method")
    except ValueError:
        pass
    try:
        g.choose(0,Proposed(1,102.),pred,wait,130.,alarms,[0.]*20,cpu,"BOTH")
        raise AssertionError("accepted missing node observation")
    except ValueError:
        pass
    g.invariant()
    print("JPDC_STAGE47_CAUSAL_QUEUE_EXTERNALITY_GATE_ADVERSARIAL_UNIT_PASS")
if __name__=="__main__":run()
