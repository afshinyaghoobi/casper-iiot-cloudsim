#!/usr/bin/env python3
"""Stage30 causal CPU-finish shift alarm with immutable interval revocation.

EXPLORATORY diagnostic only: no safety certificate and no claim of calibrated
sequential false-alarm/detection power. Underlying Stage28 model is UNCHANGED.
"""
from collections import deque
from dataclasses import dataclass
from causal_nonnetwork_calibration_stage28 import CausalNonnetworkCalibrator,QEstimate

WINDOW=8
HITS=3
POSITIVE_CPU_ERROR_THRESHOLD_MS=10.0
MIN_FINISHED=40

@dataclass(frozen=True)
class IssuedWithGuard:
    original: QEstimate
    issued:bool
    abstention_reason:str | None
    cpu_shift_alarm_active:bool
    certified:bool=False

class CausalCpuShiftGuard:
    def __init__(self):
        self.base=CausalNonnetworkCalibrator()
        self.last_window=deque(maxlen=WINDOW)
        self.finished_cpu_labels=0
        self.alarmed=False
        self.first_alarm_delivery_ms=None
        self.first_alarm_task_index=None
        self.alarm_positive_evidence=()
        self.alarm_count=0
        self.issued=0
        self.sparse_abstentions=0
        self.alarm_abstentions=0

    def query(self,now_ms,task_class,telemetry_age_ms):
        original=self.base.query(now_ms,task_class,telemetry_age_ms)
        assert original.descriptive_only and not original.certified
        if not original.available:
            reason="sparse"
        elif self.alarmed:
            reason="cpu_shift_alarm"
        else:
            reason=None
        self.issued+=int(reason is None)
        self.sparse_abstentions+=int(reason=="sparse")
        self.alarm_abstentions+=int(reason=="cpu_shift_alarm")
        return IssuedWithGuard(original,reason is None,reason,self.alarmed)

    def dispatch(self,*args):
        return self.base.dispatch(*args)

    def finish(self,index,node,start_ms,finish_ms):
        # Do not touch detector state until original source validates completion.
        item=self.base.pending.get(index)
        if item is None:raise ValueError("unknown task")
        cpu_error=(finish_ms-start_ms)-item.predicted_cpu_ms
        full_nonnetwork=self.base.finish(index,node,start_ms,finish_ms)
        self.finished_cpu_labels+=1
        self.last_window.append((index,cpu_error>POSITIVE_CPU_ERROR_THRESHOLD_MS))
        if (not self.alarmed and self.finished_cpu_labels>=MIN_FINISHED
                and sum(int(flag) for _,flag in self.last_window)>=HITS):
            self.alarmed=True
            self.alarm_count=1
            self.first_alarm_delivery_ms=finish_ms
            self.first_alarm_task_index=index
            self.alarm_positive_evidence=tuple(
                job_id for job_id,flag in self.last_window if flag)
        return full_nonnetwork

    def invariant(self):
        self.base.invariant()
        assert self.base.finishes==self.finished_cpu_labels
        assert self.alarm_count==int(self.alarmed)
        assert 0<=len(self.last_window)<=WINDOW
        if self.alarmed:
            assert self.first_alarm_delivery_ms is not None
            assert self.first_alarm_task_index is not None
            assert len(self.alarm_positive_evidence)>=HITS
        else:
            assert self.first_alarm_delivery_ms is None
        assert self.issued+self.sparse_abstentions+self.alarm_abstentions==self.base.dispatches
