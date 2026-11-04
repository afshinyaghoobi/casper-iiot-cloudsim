#!/usr/bin/env python3
"""Native Python physical event-driven calibration with NO CloudSim outcome input.

Original-model S0 task/node RNG, source-style ranked mission calibration and
sparse probes; original hashed physical service noise and strictly FIFO queues.
The physical engine differs from CloudSimPlus SpaceShared admissions.
"""
from collections import deque
import heapq
import math
from independent_workload_generator import (
    nodes,tasks,calibration_mission_ranks,conformal_qhat,predicted_latency)
from independent_stochastic_physics import physical_durations
from independent_casper_state import VirtualQueue

BURN_IN=10000
CAL_SIZE=80000
NODES=21

def calibrate(seed_index,cal_size=CAL_SIZE):
    if cal_size<=BURN_IN:raise ValueError("calibration must exceed burn-in")
    seed=4202202600+seed_index
    specs=nodes(seed)
    ranks=calibration_mission_ranks(seed,cal_size,BURN_IN)
    generated=list(tasks(seed,cal_size,"S0_STATIONARY",seed_salt=0xCA11B4A7))
    events=[(t[7],1,t[1],t) for t in generated]
    heapq.heapify(events)
    waiting=[deque() for _ in range(NODES)]
    running=[None]*NODES
    physical_next=[0.0]*NODES
    prior_finish=[0.0]*NODES
    assigned=[[] for _ in range(NODES)]
    started=[[] for _ in range(NODES)]
    observed_ordinal=[-1]*NODES
    ordinal=0
    vq=VirtualQueue(NODES)
    next_telemetry=1000.0
    telemetry=0
    normal_arrivals=0
    probe_budget_consumed=0
    actual_probes=0
    service_by_tier=[[] for _ in range(3)]
    scores_by_rank=[[] for _ in range(3)]
    reference_scores=[]
    dispatched=set()
    completed=set()
    mission_dispatched=set()
    service_completed=set()
    total_wait=0.0

    def start(j,job,when):
        t,net,cpu,rank,nominal,pred,sigma,probe=job
        if running[j] is not None or when+1e-8<t[7] or when+1e-8<prior_finish[j]:
            raise AssertionError("physical FIFO service overlap / time inversion")
        running[j]=(t[1],when)
        started[j].append(t[1])
        heapq.heappush(events,(when+cpu,0,t[1],(j,job,when)))

    while events:
        now,kind,i,payload=heapq.heappop(events)
        if kind==1:
            t=payload
            if i in dispatched:raise AssertionError("duplicate physical dispatch")
            dispatched.add(i)
            if now>=next_telemetry:
                vq.reset_from_telemetry(physical_next)
                next_telemetry=now+50.0
                telemetry+=1
            pred=[predicted_latency(t,specs[j],vq.predicted_backlog(j,now))
                  for j in range(NODES)]
            order=sorted(range(NODES),key=lambda j:(pred[j],j))
            rank=1
            probe=False
            if t[2]=="MISSION" and i>=BURN_IN:
                rank=ranks[i]
                j=order[rank-1]
                mission_dispatched.add(i)
            else:
                j=order[0]
                if t[2]=="NORMAL":
                    normal_arrivals+=1
                    if normal_arrivals%100==0 and probe_budget_consumed<math.ceil(.01*normal_arrivals):
                        probe_budget_consumed+=1
                        eligible=[k for k in range(NODES) if pred[k]<=t[3]]
                        if eligible:
                            # Java tie behavior: lowest age, then latency, then first encountered ID.
                            j=min(eligible,key=lambda k:(observed_ordinal[k],pred[k],k))
                            probe=True
                            actual_probes+=1
            nominal=t[4]/specs[j][1]*12.0
            cpu,net=physical_durations(seed,t,specs[j],"S0_STATIONARY",frozenset())
            sigma=(3+.1*pred[j])*specs[j][4]
            if not all(math.isfinite(v) and v>0 for v in (cpu,net,nominal,sigma,pred[j])):
                raise AssertionError("nonfinite physical input")
            physical_next[j]=max(physical_next[j],now)+cpu
            vq.on_dispatch(j,now,nominal)
            assigned[j].append(i)
            job=(t,net,cpu,rank,nominal,pred[j],sigma,probe)
            if running[j] is None:
                if waiting[j]:raise AssertionError("pre-existing waiting task bypassed")
                start(j,job,now)
            else:
                waiting[j].append(job)
        else:
            j,job,started_at=payload
            t,net,cpu,rank,nominal,pred,sigma,probe=job
            if running[j]!=(i,started_at) or i in completed:
                raise AssertionError("stale/duplicate physical completion")
            if abs(now-started_at-cpu)>1e-8 or started_at+1e-8<t[7]:
                raise AssertionError("physical service timing mismatch")
            wait=max(0.0,started_at-t[7])
            actual_latency=net+wait+cpu
            total_wait+=wait
            completed.add(i)
            observed_ordinal[j]=ordinal
            ordinal+=1
            if i>=BURN_IN:
                ratio=cpu/max(nominal,1e-12)
                if not math.isfinite(ratio) or ratio<=0:raise AssertionError("invalid health ratio")
                tier=0 if j<12 else 1 if j<18 else 2
                service_by_tier[tier].append(ratio)
                service_completed.add(i)
                if t[2]=="MISSION":
                    if ranks[i]!=rank:raise AssertionError("mission rank was not honored")
                    score=max(0.0,(actual_latency-pred)/(sigma+1e-12))
                    if not math.isfinite(score) or score<0:raise AssertionError("bad native score")
                    scores_by_rank[rank-1].append(score)
                    reference_scores.append(score)
            running[j]=None
            prior_finish[j]=now
            if waiting[j]:start(j,waiting[j].popleft(),now)

    if dispatched!=set(range(cal_size)) or completed!=dispatched:
        raise AssertionError("incomplete independent physical calibration")
    if service_completed!=set(range(BURN_IN,cal_size)):
        raise AssertionError("missing post-burnin service ratio")
    if mission_dispatched!=set(ranks) or len(reference_scores)!=len(ranks):
        raise AssertionError("incomplete independently generated mission score cohort")
    if any(x is not None for x in running) or any(waiting) or assigned!=started:
        raise AssertionError("FCFS physical queue admission/conservation failure")
    rank_n=[len(x) for x in scores_by_rank]
    tier_n=[len(x) for x in service_by_tier]
    if sum(rank_n)!=len(ranks) or sum(tier_n)!=cal_size-BURN_IN:
        raise AssertionError("score or service tier conservation failure")
    if cal_size==CAL_SIZE and (min(rank_n)<=200 or min(tier_n)==0):
        raise AssertionError("insufficient full scientific calibration groups")
    rank_alpha=(.006,.003,.001)
    q_rank=[conformal_qhat(group,alpha) for group,alpha in zip(scores_by_rank,rank_alpha)]
    q_global=conformal_qhat(reference_scores,.01)
    tier_thresholds=[conformal_qhat(group,.01) for group in service_by_tier]
    if cal_size==CAL_SIZE and not all(math.isfinite(v) and v>0 for v in
                                      [*q_rank,q_global,*tier_thresholds]):
        raise AssertionError("nonfinite/zero scientific calibration quantile")
    return {"status":"PASS","engine":"independent_strict_FCFS_stochastic_calibration",
            "scientific_seed":seed,"seed_index":seed_index,
            "calibration_tasks":cal_size,"burn_in":BURN_IN,
            "postburnin_service_ratio_count":len(service_completed),
            "mission_score_count":len(reference_scores),
            "rank_counts":rank_n,"tier_counts":tier_n,
            "q_rank":q_rank,"q_global":q_global,
            "tier_thresholds":tier_thresholds,
            "normal_arrivals":normal_arrivals,
            "probe_budget_consumed":probe_budget_consumed,
            "actual_probes":actual_probes,
            "telemetry_resets":telemetry,
            "mean_physical_wait_ms":total_wait/cal_size,
            "source":"native_Python_completion_latency_and_service_not_Java",
            "not_cloudsim_queue_equivalent":True}
