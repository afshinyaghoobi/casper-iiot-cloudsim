#!/usr/bin/env python3
"""Stage61 passive original-source observer; NEVER controls a routing decision."""
from collections import Counter
from causal_ambiguity_builder_stage60 import CausalAmbiguityBuilder,NODES
from finite_ambiguity_deadline_stage59 import select

class ShadowFeasibility:
    def __init__(self):
        self.builder=CausalAmbiguityBuilder()
        self.all_arrivals=0
        self.all_mission=0
        self.post_mission=0
        self.ready_mission=0
        self.ready_post_mission=0
        self.ready_all=0
        self.shadow_different=0
        self.mission_reasons=Counter()
        self.post_mission_reasons=Counter()
        self.node_cpu_missing=Counter()
        self.node_e2e_missing=Counter()
        self.events_cpu=0
        self.events_e2e=0
        self.telemetry_count=0

    def telemetry(self,now,vq):
        values=[vq.predicted_backlog(j,now) for j in range(NODES)]
        self.builder.observe_telemetry(now,values)
        self.telemetry_count+=1

    def cpu_finish(self,i,j,nominal,actual,now):
        self.builder.cpu_complete(i,j,nominal,actual,now,now)
        self.events_cpu+=1

    def e2e_finish(self,i,j,nominal,actual,cpu_finish,now):
        self.builder.e2e_delivered(i,j,nominal,actual,cpu_finish,now)
        self.events_e2e+=1

    def arrived(self,now,task,pred,nominal_net):
        i=task[1]
        result=self.builder.construct(now,pred,nominal_net)
        self.all_arrivals+=1
        ready=result.status=="READY_UNCALIBRATED"
        self.ready_all+=int(ready)
        if task[2]!="MISSION":
            return
        self.all_mission+=1
        post=i>=10000
        self.post_mission+=int(post)
        if ready:
            self.ready_mission+=1
            self.ready_post_mission+=int(post)
            # This is a shadow-only hypothetical decision, NOT an actual assignment.
            choice=select(pred,result.worlds,task[3])
            self.shadow_different+=int(choice.switched_from_nominal)
            return
        for reason in result.unavailable:
            self.mission_reasons[reason]+=1
            if post:self.post_mission_reasons[reason]+=1
            if reason.startswith("CPU_NODE_"):
                self.node_cpu_missing[int(reason.split("_")[2])]+=1
            elif reason.startswith("E2E_NODE_"):
                self.node_e2e_missing[int(reason.split("_")[2])]+=1

    def finalize(self,count,mission_count,post_mission_count):
        if self.events_cpu!=count or self.events_e2e!=count or self.all_arrivals!=count:
            raise AssertionError("shadow feedback or arrivals not conserved")
        if self.all_mission!=mission_count or self.post_mission!=post_mission_count:
            raise AssertionError("shadow MISSION count does not match original source")
        if not 0<=self.ready_post_mission<=self.ready_mission<=mission_count:
            raise AssertionError("shadow availability accounting")
        b=self.builder
        if b.accepted_cpu+b.quarantined<count:
            # late quarantines could originate in both channels, and the sum is
            # a lower bound on all received data, never exceed source events.
            raise AssertionError("missing CPU shadow feedback")
        if b.accepted_cpu+b.accepted_e2e+b.quarantined!=2*count:
            raise AssertionError("shadow feedback acceptance/quarantine lost")
        return dict(shadow_only_no_routing_effect=True,
            original_source_task_count=count,
            all_arrivals=count,mission_arrivals=self.all_mission,
            post_mission_arrivals=self.post_mission,
            ready_all_arrivals=self.ready_all,
            ready_mission_arrivals=self.ready_mission,
            ready_post_mission_arrivals=self.ready_post_mission,
            ready_mission_rate=self.ready_mission/self.all_mission if self.all_mission else None,
            ready_post_mission_rate=self.ready_post_mission/self.post_mission if self.post_mission else None,
            shadow_mission_different_from_greedy=self.shadow_different,
            telemetry_reports=self.telemetry_count,
            CPU_completion_deliveries=self.events_cpu,
            E2E_delivered_feedback=self.events_e2e,
            CPU_accepted=b.accepted_cpu,E2E_accepted=b.accepted_e2e,
            late_generated_quarantined=b.quarantined,
            missing_reasons_at_mission=dict(sorted(self.mission_reasons.items())),
            missing_reasons_at_post_mission=dict(sorted(self.post_mission_reasons.items())),
            CPU_node_missing_counts=[self.node_cpu_missing[j] for j in range(NODES)],
            E2E_node_missing_counts=[self.node_e2e_missing[j] for j in range(NODES)],
            parameters_frozen=True,coverage_empirically_calibrated=False,
            true_future_coverage_guarantee=False)
