#!/usr/bin/env python3
"""Stage42 prospective adversarial unit tests of causal regime evidence timing."""
from causal_regime_selector_stage42 import CausalRegimeSelector

def bad(f):
    try:f()
    except ValueError:return
    raise AssertionError("accepted an invalid or future observation")

def run():
    d=CausalRegimeSelector()
    assert d.select(0.).regime=="FULL"
    for i in range(255):
        d.observe_cpu_finish(10.,10.,float(i+1))
        d.observe_network_e2e(10.,10.,float(i+1))
    assert d.select(256.).regime=="FULL"
    d.observe_cpu_finish(10.,10.,256.)
    d.observe_network_e2e(10.,10.,256.)
    r=d.select(256.)
    assert r.cpu_baseline_share==r.network_baseline_share==0.
    assert r.regime=="FULL"
    for i in range(64):
        before=d.select(256.5+i).regime
        d.observe_cpu_finish(10.,10.,257.+i)
        # A CPU completion alone may not change the network hypothesis;
        # previously delivered E2E reports can already have activated it.
        assert d.select(257.+i).regime==before
        d.observe_network_e2e(20.,10.,257.+i)
    r=d.select(321.)
    assert r.regime=="NETWORK" and r.network_signal and not r.cpu_signal
    assert r.network_bad_share==1.
    assert d.first_network_dispatch_clock is not None
    # CPU shock unobserved until CPU FINISH event occurs.
    assert d.select(321.).regime=="NETWORK"
    for i in range(64):
        d.observe_cpu_finish(20.,10.,321.+i)
        d.observe_network_e2e(20.,10.,321.+i)
    r=d.select(385.)
    assert r.regime=="FULL" and r.cpu_signal and r.network_signal
    assert d.ambiguous_dispatches>=1
    for i in range(64):
        d.observe_cpu_finish(20.,10.,385.+i)
        d.observe_network_e2e(10.,10.,385.+i)
    r=d.select(449.)
    assert r.cpu_signal and not r.network_signal and r.regime=="FULL"
    bad(lambda:d.observe_network_e2e(20.,10.,1.))
    bad(lambda:d.observe_cpu_finish(0.,10.,449.))
    bad(lambda:d.observe_cpu_finish(20.,0.,449.))
    bad(lambda:d.observe_network_e2e(float("nan"),10.,449.))
    bad(lambda:d.select(0.))
    # A no-shift sequence with the same historical share never declares a regime.
    q=CausalRegimeSelector()
    for i in range(320):
        val=20. if i%5==0 else 10.
        q.observe_cpu_finish(val,10.,i+1.)
        q.observe_network_e2e(val,10.,i+1.)
    x=q.select(400.)
    assert x.regime=="FULL" and not x.cpu_signal and not x.network_signal
    print("JPDC_STAGE42_CAUSAL_CPU_NETWORK_REGIME_ADVERSARIAL_UNIT_PASS")
if __name__=="__main__":run()
