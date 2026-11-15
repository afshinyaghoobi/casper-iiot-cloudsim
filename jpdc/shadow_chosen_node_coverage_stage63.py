#!/usr/bin/env python3
"""Stage63 passively freeze chosen-node historical bounds BEFORE service draw.

CPU and network outcome checks occur at their actual finish/delivery.
No hidden fault mask, future duration input or counterfactual node oracle.
"""
from shadow_partial_feasibility_stage62 import ShadowPartialFeasibility
from causal_ambiguity_builder_stage60 import CPU_MIN,NETWORK_MIN,MAX_AGE_MS,TELEMETRY_MAX_AGE_MS,num,nodeid,taskid
from collections import Counter
import math

class ChosenNodeTemporalAudit(ShadowPartialFeasibility):
    def __init__(self):
        super().__init__()
        self.records={}
        self.feedback_cpu=set()
        self.feedback_e2e=set()
        self.total_chosen=0
        self.by_phase={phase:Counter() for phase in ("ALL_MISSION","POST_MISSION")}
        self.max_cpu_overrun={phase:0.0 for phase in self.by_phase}
        self.max_net_overrun={phase:0.0 for phase in self.by_phase}

    def capture_selected(self,now,task,j,nominal_cpu,nominal_net):
        """Called after original policy's final assignment but BEFORE actual service."""
        taskid(task[1]);nodeid(j)
        now=num(now)
        if now<self.builder.last_event:raise ValueError("retroactive dispatch")
        nominal_cpu=num(nominal_cpu,positive=True)
        nominal_net=num(nominal_net,positive=True)
        self.total_chosen+=1
        if task[2]!="MISSION":
            return
        i=task[1]
        if i in self.records:raise AssertionError("duplicate MISSION dispatch")
        cpu_eligible=(len(self.builder.cpu[j])>=CPU_MIN and
            self.builder.last_cpu_measurement[j] is not None and
            now-self.builder.last_cpu_measurement[j]<=MAX_AGE_MS)
        net_eligible=(len(self.builder.net[j])>=NETWORK_MIN and
            self.builder.last_net_measurement[j] is not None and
            now-self.builder.last_net_measurement[j]<=MAX_AGE_MS)
        telemetry=(self.builder.telemetry_time is not None and
            now-self.builder.telemetry_time<=TELEMETRY_MAX_AGE_MS)
        cpu_eligible=bool(cpu_eligible and telemetry)
        net_eligible=bool(net_eligible and telemetry)
        rec=dict(node=j,arrival=now,cpu_eligible=cpu_eligible,
            net_eligible=net_eligible,nominal_cpu=nominal_cpu,
            nominal_net=nominal_net,cpu_bound=max(self.builder.cpu[j]) if cpu_eligible else None,
            net_bound=max(self.builder.net[j]) if net_eligible else None,
            post=i>=10000,cpu_hit=None,net_hit=None,cpu_overrun=None,net_overrun=None,
            actual_cpu_excess=None,actual_net_excess=None)
        self.records[i]=rec
        for phase in ("ALL_MISSION", "POST_MISSION") if rec["post"] else ("ALL_MISSION",):
            c=self.by_phase[phase]
            c["mission"]+=1
            c["cpu_eligible"]+=int(cpu_eligible)
            c["net_eligible"]+=int(net_eligible)
            c["joint_eligible"]+=int(cpu_eligible and net_eligible)

    def cpu_finish(self,i,j,nominal,actual,now):
        # Report real observed outcome against frozen dispatch-time bound BEFORE
        # allowing CPU feedback to enter the history for subsequent arrivals.
        if i in self.records:
            rec=self.records[i]
            if rec["node"]!=j or rec["cpu_hit"] is not None:
                raise AssertionError("wrong or duplicate CPU outcome")
            if not math.isclose(rec["nominal_cpu"],nominal,rel_tol=1e-12,abs_tol=1e-9):
                raise AssertionError("CPU nominal changed since dispatch")
            excess=max(0.0,actual-nominal)
            rec["actual_cpu_excess"]=excess
            if rec["cpu_eligible"]:
                rec["cpu_hit"]=excess<=rec["cpu_bound"]+1e-10
                rec["cpu_overrun"]=max(0.,excess-rec["cpu_bound"])
            self.feedback_cpu.add(i)
        super().cpu_finish(i,j,nominal,actual,now)

    def e2e_finish(self,i,j,nominal,actual,cpu_finish,now):
        if i in self.records:
            rec=self.records[i]
            if rec["node"]!=j or rec["net_hit"] is not None:
                raise AssertionError("wrong or duplicate E2E outcome")
            if not math.isclose(rec["nominal_net"],nominal,rel_tol=1e-12,abs_tol=1e-9):
                raise AssertionError("network nominal changed since dispatch")
            excess=max(0.0,actual-nominal)
            rec["actual_net_excess"]=excess
            if rec["net_eligible"]:
                rec["net_hit"]=excess<=rec["net_bound"]+1e-10
                rec["net_overrun"]=max(0.,excess-rec["net_bound"])
            self.feedback_e2e.add(i)
        super().e2e_finish(i,j,nominal,actual,cpu_finish,now)

    def finalize(self,count,mission_count,post_mission_count):
        base=super().finalize(count,mission_count,post_mission_count)
        assert self.total_chosen==count and len(self.records)==mission_count
        assert len(self.feedback_cpu)==len(self.feedback_e2e)==mission_count
        for rec in self.records.values():
            assert rec["actual_cpu_excess"] is not None and rec["actual_net_excess"] is not None
            for phase in ("ALL_MISSION", "POST_MISSION") if rec["post"] else ("ALL_MISSION",):
                c=self.by_phase[phase]
                if rec["cpu_eligible"]:
                    c["cpu_hit"]+=int(rec["cpu_hit"])
                    c["cpu_violation"]+=int(not rec["cpu_hit"])
                    self.max_cpu_overrun[phase]=max(self.max_cpu_overrun[phase],rec["cpu_overrun"])
                if rec["net_eligible"]:
                    c["net_hit"]+=int(rec["net_hit"])
                    c["net_violation"]+=int(not rec["net_hit"])
                    self.max_net_overrun[phase]=max(self.max_net_overrun[phase],rec["net_overrun"])
                if rec["cpu_eligible"] and rec["net_eligible"]:
                    c["joint_both_hit"]+=int(rec["cpu_hit"] and rec["net_hit"])
                    c["joint_both_violation"]+=int(not(rec["cpu_hit"] and rec["net_hit"]))
                    total=rec["actual_cpu_excess"]+rec["actual_net_excess"]
                    cap=rec["cpu_bound"]+rec["net_bound"]
                    c["joint_total_excess_hit"]+=int(total<=cap+1e-10)
                    c["joint_total_excess_violation"]+=int(total>cap+1e-10)
        out={}
        for phase in ("ALL_MISSION","POST_MISSION"):
            v=self.by_phase[phase]
            # Materialize missing zero counters so zero-rate cases remain visible.
            keys=("mission","cpu_eligible","net_eligible","joint_eligible",
                  "cpu_hit","cpu_violation","net_hit","net_violation",
                  "joint_both_hit","joint_both_violation",
                  "joint_total_excess_hit","joint_total_excess_violation")
            c={k:v[k] for k in keys}
            assert c["cpu_hit"]+c["cpu_violation"]==c["cpu_eligible"]
            assert c["net_hit"]+c["net_violation"]==c["net_eligible"]
            assert c["joint_both_hit"]+c["joint_both_violation"]==c["joint_eligible"]
            assert c["joint_total_excess_hit"]+c["joint_total_excess_violation"]==c["joint_eligible"]
            c["joint_both_coverage"]=c["joint_both_hit"]/c["joint_eligible"] if c["joint_eligible"] else None
            c["max_cpu_overrun_ms"]=self.max_cpu_overrun[phase]
            c["max_net_overrun_ms"]=self.max_net_overrun[phase]
            out[phase]=c
        base["stage63_chosen_node_temporal_coverage"]=out
        base["stage63_no_counterfactual_unselected_nodes"]=True
        base["stage63_no_coverage_calibration_claim"]=True
        return base
