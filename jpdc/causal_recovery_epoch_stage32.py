#!/usr/bin/env python3
"""Stage32 observational causal post-alarm NEW-EPOCH interval reconstruction.

Uses Stage30 detector and Stage28 quantiles WITHOUT changing either.
Recovered intervals are DESCRIPTIVE, NEVER certified for deadlines or coverage.
"""
from dataclasses import dataclass
import math
from causal_cpu_shift_guard_stage30 import CausalCpuShiftGuard
from causal_nonnetwork_calibration_stage28 import CausalNonnetworkCalibrator,QEstimate

@dataclass(frozen=True)
class RecoveryDecision:
    original:QEstimate
    issued:bool
    phase:str
    abstention_reason:str | None
    certified:bool=False

class CausalRecoveryGuard:
    def __init__(self):
        self.frozen=CausalCpuShiftGuard()
        self.epoch=None
        self.epoch_started_ms=None
        self.epoch_registered_ids=set()
        self.issued_original=0
        self.issued_recovered=0
        self.abstained_pre_sparse=0
        self.abstained_rebuilding=0
        self.epoch_finished=0
        self.recovery_times={}
        self.epoch_created_at_finished_count=None

    def query(self,now_ms,task_class,telemetry_age_ms):
        old=self.frozen.query(now_ms,task_class,telemetry_age_ms)
        assert old.original.descriptive_only and not old.original.certified
        if not self.frozen.alarmed:
            if old.issued:
                self.issued_original+=1
                return RecoveryDecision(old.original,True,"prealarm_original",None)
            self.abstained_pre_sparse+=1
            return RecoveryDecision(old.original,False,"prealarm_sparse","sparse")
        if self.epoch is None:raise AssertionError("alarm without new epoch")
        post=self.epoch.query(now_ms,task_class,telemetry_age_ms)
        assert post.descriptive_only and not post.certified
        if post.available:
            self.issued_recovered+=1
            key=(post.task_class,post.telemetry_band)
            if key not in self.recovery_times:self.recovery_times[key]=now_ms
            return RecoveryDecision(post,True,"postalarm_recovered_descriptive",None)
        self.abstained_rebuilding+=1
        return RecoveryDecision(post,False,"postalarm_rebuild","post_alarm_rebuild")

    def dispatch(self,index,node,task_class,dispatch_ms,telemetry_age_ms,
                 predicted_wait_ms,predicted_cpu_ms):
        # The original frozen diagnostic always records the dispatch.
        out=self.frozen.dispatch(index,node,task_class,dispatch_ms,telemetry_age_ms,
                                 predicted_wait_ms,predicted_cpu_ms)
        if self.frozen.alarmed:
            assert self.epoch is not None
            assert dispatch_ms>=self.epoch_started_ms
            self.epoch.dispatch(index,node,task_class,dispatch_ms,telemetry_age_ms,
                                predicted_wait_ms,predicted_cpu_ms)
            assert index not in self.epoch_registered_ids
            self.epoch_registered_ids.add(index)
        return out

    def finish(self,index,node,start_ms,finish_ms):
        # Original CPU-finish updates are the ONLY way the alarm can trigger.
        was_alarm=self.frozen.alarmed
        total=self.frozen.finish(index,node,start_ms,finish_ms)
        if not was_alarm and self.frozen.alarmed:
            assert self.epoch is None
            self.epoch=CausalNonnetworkCalibrator()
            self.epoch.last_time=finish_ms
            self.epoch_started_ms=finish_ms
            self.epoch_created_at_finished_count=self.frozen.finished_cpu_labels
            # The triggering job is a prealarm dispatch and MUST NOT enter epoch.
        if index in self.epoch_registered_ids:
            assert self.epoch is not None
            second=self.epoch.finish(index,node,start_ms,finish_ms)
            if not math.isclose(total,second,rel_tol=0,abs_tol=1e-8):
                raise AssertionError("post-alarm nonnetwork q math differs from frozen Stage28")
            self.epoch_finished+=1
            self.epoch_registered_ids.remove(index)
        return total

    def invariant(self):
        self.frozen.base.invariant()
        assert self.issued_original+self.issued_recovered+self.abstained_pre_sparse+self.abstained_rebuilding==self.frozen.base.dispatches
        assert self.epoch_finished<=self.frozen.finished_cpu_labels
        if self.epoch is None:
            assert not self.frozen.alarmed and not self.epoch_registered_ids
            assert self.issued_recovered==self.abstained_rebuilding==0
        else:
            assert self.frozen.alarmed
            assert self.epoch_started_ms==self.frozen.first_alarm_delivery_ms
            self.epoch.invariant()
            assert len(self.epoch_registered_ids)==len(self.epoch.pending)
            assert self.epoch.finishes==self.epoch_finished
            assert self.epoch.dispatches==self.epoch_finished+len(self.epoch_registered_ids)
