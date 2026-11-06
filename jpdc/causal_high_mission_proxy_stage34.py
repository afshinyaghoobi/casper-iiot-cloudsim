#!/usr/bin/env python3
"""Stage34 post-alarm HIGH-to-MISSION SAME-BAND descriptive proxy experiment.

A proxy is NOT a calibrated, deterministic, conformal or deadline-safe bound.
Preserves original Stage30 alarm and Stage28/32 causal CPU-finish history.
"""
from dataclasses import dataclass
from statistics import median
from causal_nonnetwork_calibration_stage28 import QEstimate
from causal_recovery_epoch_stage32 import CausalRecoveryGuard

MIN_OWN=10
MIN_DONOR=40
MAX_SIGNED_MEDIAN_DIFFERENCE_MS=2.

@dataclass(frozen=True)
class ProxyDecision:
    original:QEstimate
    issued:bool
    phase:str
    abstention_reason:str | None
    proxy_source:str
    certified:bool=False

class CausalClassProxyRecovery(CausalRecoveryGuard):
    def __init__(self):
        super().__init__()
        self.proxy_issued=0
        self.proxy_recovery_times={}

    def query(self,now_ms,task_class,telemetry_age_ms):
        old=super().query(now_ms,task_class,telemetry_age_ms)
        if (not self.frozen.alarmed or task_class!="MISSION"
                or old.phase!="postalarm_rebuild"):
            return old
        assert self.epoch is not None
        ageband=old.original.telemetry_band
        own=self.epoch.samples[("MISSION",ageband)]
        donor=self.epoch.samples[("HIGH",ageband)]
        if len(own)<MIN_OWN or len(donor)<MIN_DONOR:
            return old
        donor_interval=self.epoch.query(now_ms,"HIGH",telemetry_age_ms)
        assert donor_interval.available and not donor_interval.certified
        high_med=median(donor)
        mission_med=median(own)
        if abs(high_med-mission_med)>MAX_SIGNED_MEDIAN_DIFFERENCE_MS:
            return old
        if not all(donor_interval.lower_ms<=e<=donor_interval.upper_ms
                   for e in list(own)[-MIN_OWN:]):
            return old
        proxy=QEstimate(
            context=donor_interval.context,task_class="MISSION",
            telemetry_band=ageband,sample_count=donor_interval.sample_count,
            lower_ms=donor_interval.lower_ms,upper_ms=donor_interval.upper_ms,
            available=True,descriptive_only=True,certified=False)
        # The original observer-only Stage32 method has just reported a
        # rebuild abstention. Replace ONE dispatch's bookkeeping only.
        self.abstained_rebuilding-=1
        self.issued_recovered+=1
        self.proxy_issued+=1
        key=("MISSION",ageband)
        if key not in self.proxy_recovery_times:
            self.proxy_recovery_times[key]=now_ms
        return ProxyDecision(proxy,True,"postalarm_proxy_descriptive",
                             None,"HIGH",False)

    def invariant(self):
        super().invariant()
        assert 0<=self.proxy_issued<=self.issued_recovered
        assert len(self.proxy_recovery_times)<=3
