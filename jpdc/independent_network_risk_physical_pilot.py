"""Exploratory original-style native physical system plus new nonconformal network-risk policy.

NOT a validated novel algorithm or original CloudSim queue equivalence.
All network risk observations become policy-visible at end-to-end feedback,
never on dispatch or CPU-finish. The original comparator policy E17 feedback
still follows the prior Stage4 CPU-finish timing; this is an identified
comparability/physical feedback limitation, not a claim of causal parity.
"""
#!/usr/bin/env python3
"""Native independent CASPER deployment on a strict FCFS Python physical engine.

Inputs: independent Stage3 physical calibration, original-model RNG task/node
generation, native hashed physical noise. Does NOT use Java events/results.
This is explicitly not CloudSim SpaceShared queue-equivalent or YAFS.
"""
from collections import deque,Counter
import heapq,math
from independent_workload_generator import nodes,tasks,predicted_latency
from independent_stochastic_physics import physical_durations,affected_nodes
from independent_casper_state import DualMemory,NodeHealth,VirtualQueue
from network_residual_risk_policy import NetworkResidualRisk

POLICY_FLAGS={
    "CLOUD_ONLY":dict(cp=False,ranked=False,adaptive=False,health=False),
    "EDGE_FIRST":dict(cp=False,ranked=False,adaptive=False,health=False),
    "PRED_GREEDY":dict(cp=False,ranked=False,adaptive=False,health=False),
    "GLOBAL_CP":dict(cp=True,ranked=False,adaptive=False,health=False),
    "RANKED_CP_STATIC":dict(cp=True,ranked=True,adaptive=False,health=False),
    "CASPER_ADAPT_NO_HEALTH":dict(cp=True,ranked=True,adaptive=True,health=False),
    "CASPER_HEALTH_STATIC":dict(cp=True,ranked=True,adaptive=False,health=True),
    "CASPER_FULL":dict(cp=True,ranked=True,adaptive=True,health=True),
}
POLICIES=tuple(POLICY_FLAGS)
NODES=21

def route(task,pred,alarmed,sigma,qrank,qglobal,eta,policy):
    """Exact original E42 eight-mode routing, conditional on native simulator state."""
    if policy not in POLICY_FLAGS:raise ValueError("unrecognized policy")
    if len(pred)!=NODES or len(alarmed)!=NODES or len(sigma)!=NODES:
        raise ValueError("21-node policy state required")
    if not all(math.isfinite(x) and x>0 for x in [*pred,*sigma,eta]):
        raise ValueError("invalid predicted state")
    flags=POLICY_FLAGS[policy]
    if flags["cp"] and (len(qrank)!=3 or
        not all(math.isfinite(q) and q>=0 for q in qrank) or
        not math.isfinite(qglobal) or qglobal<0):
        raise ValueError("invalid conformal quantiles")
    base=(range(18,21) if policy=="CLOUD_ONLY" else
          range(12) if policy=="EDGE_FIRST" else range(NODES))
    eligible=[j for j in base if not (flags["health"] and alarmed[j])]
    if not flags["cp"]:
        options=eligible if eligible else list(base)
        return min(options,key=lambda j:(pred[j],j)),1,False,()
    family=tuple(sorted(eligible,key=lambda j:(pred[j],j))[:3])
    if not family:
        return min(base,key=lambda j:(pred[j],j)),1,False,()
    safe=None
    for p,j in enumerate(family):
        q=qrank[p] if flags["ranked"] else qglobal
        upper=pred[j]+eta*q*sigma[j]
        if upper<=task[3]:
            safe=p;break
    rank=(safe+1) if safe is not None else 1
    return family[safe if safe is not None else 0],rank,safe is not None,family

NEW_POLICY="NEW_NETWORK_RESIDUAL"

def simulate(seed_index,scenario,policy,calibration,count=12000):
    if policy not in (*POLICIES,NEW_POLICY):raise ValueError("invalid pilot policy")
    flags=(POLICY_FLAGS["PRED_GREEDY"] if policy==NEW_POLICY else POLICY_FLAGS[policy])
    risk_state=NetworkResidualRisk()
    if scenario not in ("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS"):
        raise ValueError("Stage4 frozen scenario constraint")
    seed=4202202600+seed_index
    if calibration.get("scientific_seed")!=seed or calibration.get("calibration_tasks")!=80000:
        raise ValueError("native calibration seed/n mismatch")
    qrank=calibration["q_rank"]
    thresholds=calibration["tier_thresholds"]
    raw_reference=calibration.get("reference_scores")
    if raw_reference is None or len(raw_reference)!=calibration["mission_score_count"]:
        raise ValueError("native calibration raw mission references required")
    if min(calibration["rank_counts"])<=200 or len(thresholds)!=3:
        raise ValueError("insufficient calibration")
    e17=DualMemory(raw_reference) if flags["adaptive"] else None
    health=[NodeHealth(thresholds[0 if j<12 else 1 if j<18 else 2]) for j in range(NODES)]
    specs=nodes(seed);affected=affected_nodes(seed,scenario)
    generated=list(tasks(seed,count,scenario))
    # CPU service end kind0, observed end-to-end feedback kind1,
    # arrival kind2. Same-time feedback is processed BEFORE next arrival.
    events=[(t[7],2,t[1],t) for t in generated];heapq.heapify(events)
    physical_next=[0.0]*NODES
    last_finish=[0.0]*NODES
    running=[None]*NODES;queues=[deque() for _ in range(NODES)]
    assigned=[[] for _ in range(NODES)]
    started=[[] for _ in range(NODES)]
    vq=VirtualQueue(NODES)
    last_observed=[-1]*NODES;finish_ordinal=0
    next_telemetry=1000.0
    arrived=set();completed=set();mission_results=[]
    normal=0;probe_budget=0;probes=0;probe_violations=0
    alarm_transitions=0;feedback_count=0;feedback_alarm_transitions=0
    exposed=0;telemetry=0
    rank_counts=Counter();miss_by_type=Counter();by_type=Counter()
    latency_sum=0.0;wait_sum=0.0;false_alarm_nodes=set()
    eta_above_one=0
    risk_positive_arrivals=0
    risk_reroutes=0
    risk_penalty_sum=0.0
    risk_updated_postshock=0
    def start(j,job,now):
        t,net,cpu,nominal,predj,sigmaj,eta,cert,family_covered,probe,rank=job
        if running[j] is not None or now+1e-8<t[7] or now+1e-8<last_finish[j]:
            raise AssertionError("FIFO start overlap or premature service")
        running[j]=(t[1],now)
        started[j].append(t[1])
        heapq.heappush(events,(now+cpu,0,t[1],(j,job,now)))
    while events:
        now,kind,i,payload=heapq.heappop(events)
        if kind==2:
            t=payload
            if i in arrived:raise AssertionError("duplicate dispatch")
            arrived.add(i)
            if now>=next_telemetry:
                vq.reset_from_telemetry(physical_next)
                next_telemetry=now+50.0;telemetry+=1
            pred=[predicted_latency(t,specs[j],vq.predicted_backlog(j,now)) for j in range(NODES)]
            sigma=[(3.0+.1*pred[j])*specs[j][4] for j in range(NODES)]
            alarm=[h.alarmed for h in health] if flags["health"] else [False]*NODES
            eta=e17.eta_before_outcome() if e17 is not None else 1.0
            if eta>1:eta_above_one+=1
            if policy==NEW_POLICY:
                j,penalty,active=risk_state.choose(pred)
                rank,cert,family=1,False,()
                risk_positive_arrivals+=int(active)
                risk_reroutes+=int(j!=min(range(NODES),key=lambda k:(pred[k],k)))
                risk_penalty_sum+=penalty
            else:
                j,rank,cert,family=route(t,pred,alarm,sigma,qrank,calibration["q_global"],eta,policy)
            # Family coverage is a diagnostic of actual independent counterfactual
            # instantaneous queue predictions; not the routed task's result.
            family_covered=True
            for k in family:
                svc,net_candidate=physical_durations(seed,t,specs[k],scenario,affected)
                audit_latency=net_candidate+max(0.0,physical_next[k]-now)+svc
                family_q=qrank[family.index(k)] if flags["ranked"] else calibration["q_global"]
                if audit_latency>pred[k]+eta*family_q*sigma[k]:
                    family_covered=False
            probe=False
            if t[2]=="NORMAL":
                normal+=1
                if flags["health"] and normal%100==0 and probe_budget<math.ceil(.01*normal):
                    probe_budget+=1
                    candidates=[k for k in range(NODES) if not alarm[k] and pred[k]<=t[3]]
                    if candidates:
                        j=min(candidates,key=lambda k:(last_observed[k],pred[k],k))
                        probe=True;probes+=1
            cpu,net=physical_durations(seed,t,specs[j],scenario,affected)
            if i>=10000 and j in affected:exposed+=1
            nominal=t[4]/specs[j][1]*12.0
            if min(cpu,net,nominal)<=0 or not all(math.isfinite(x) for x in (cpu,net,nominal)):
                raise AssertionError("invalid native physical duration")
            physical_next[j]=max(now,physical_next[j])+cpu
            vq.on_dispatch(j,now,nominal)
            assigned[j].append(i)
            job=(t,net,cpu,nominal,pred[j],sigma[j],eta,cert,family_covered,probe,rank)
            if running[j] is None:
                if queues[j]:raise AssertionError("waiting job bypass")
                start(j,job,now)
            else:queues[j].append(job)
        elif kind==0:
            j,job,started_at=payload
            t,net,cpu,nominal,predj,sigmaj,eta,cert,family_covered,probe,rank=job
            if running[j]!=(i,started_at) or i in completed:
                raise AssertionError("missing running job or duplicate finish")
            if abs(now-(started_at+cpu))>1e-8:
                raise AssertionError("service timing mismatch")
            wait=max(0.0,started_at-t[7])
            latency=net+wait+cpu
            if abs(latency-(now-t[7]+net))>1e-8:
                raise AssertionError("physical latency decomposition mismatch")
            completed.add(i);by_type[t[2]]+=1
            # The network observable is deliberately delayed until actual
            # CPU finish PLUS full network time; not fed to new policy here.
            heapq.heappush(events,(now+net,1,i,(j,net,t[5],t[6])))
            if latency>t[3]:miss_by_type[t[2]]+=1
            latency_sum+=latency;wait_sum+=wait
            last_observed[j]=finish_ordinal;finish_ordinal+=1
            if flags["health"]:
                was=health[j].alarmed
                health[j].observe(cpu,nominal)
                if not was and health[j].alarmed:alarm_transitions+=1
                if health[j].alarmed and j not in affected:false_alarm_nodes.add(j)
            if e17 is not None and t[2]=="MISSION":
                score=max(0.0,(latency-predj)/(sigmaj+1e-12))
                before=e17.alarm_ever
                e17.observe(score)
                feedback_count+=1
                if not before and e17.alarm_ever:feedback_alarm_transitions+=1
            if probe and latency>t[3]:probe_violations+=1
            if t[2]=="MISSION":
                rank_counts[rank]+=1
                mission_results.append((i,i>=10000,cert,latency>t[3],family_covered,latency,eta,rank))
            running[j]=None
            last_finish[j]=now
            if queues[j]:start(j,queues[j].popleft(),now)
        else:
            # Only completed end-to-end observations may enter the risk state.
            j,actual_net,inmb,outmb=payload
            nominal_net=specs[j][3]+(inmb+outmb)*8000.0/specs[j][2]
            excess=risk_state.observe_e2e(j,actual_net,nominal_net,now)
            risk_updated_postshock+=int(i>=10000 and excess>0)
    if risk_state.total_feedback!=count:
        raise AssertionError("missing independently delayed network feedback")
    if arrived!=set(range(count)) or completed!=arrived or any(r is not None for r in running):
        raise AssertionError("native deployment task conservation")
    if any(queues) or assigned!=started:
        raise AssertionError("native strict FIFO order violated")
    mission_results.sort(key=lambda v:v[0])
    post=[r for r in mission_results if r[1]]
    if len(mission_results)!=by_type["MISSION"]:
        raise AssertionError("mission outcome count")
    if e17 is not None and feedback_count!=len(mission_results):
        raise AssertionError("incomplete independent adaptive feedback")
    if not flags["adaptive"] and feedback_count!=0:
        raise AssertionError("adaptive feedback in nonadaptive policy")
    if not flags["cp"] and any(r[2] for r in mission_results):
        raise AssertionError("baseline issued certificate")
    def rate(items,pred_fn):
        return sum(pred_fn(v) for v in items)/len(items) if items else None
    return {"status":"PASS","engine":"native_Python_stochastic_strict_FCFS",
            "seed_index":seed_index,"scientific_seed":seed,"scenario":scenario,
            "policy":policy,"policy_flags":flags,"deployment_tasks":count,
            "mission_tasks":len(mission_results),"post_mission_tasks":len(post),
            "rank_counts":{str(k):rank_counts[k] for k in (1,2,3)},
            "post_cert_rate":rate(post,lambda r:r[2]),
            "post_abstention_rate":rate(post,lambda r:not r[2]) if flags["cp"] else None,
            "post_false_cert_rate":rate(post,lambda r:r[2] and r[3]) if flags["cp"] else None,
            "post_deadline_miss_rate":rate(post,lambda r:r[3]),
            "post_family_covered_rate":rate(post,lambda r:r[4]) if flags["cp"] else None,
            "mission_deadline_misses":sum(r[3] for r in mission_results),
            "mean_latency_ms":latency_sum/count,"mean_wait_ms":wait_sum/count,
            "normal_arrivals":normal,"probes":probes,"probe_violations":probe_violations,
            "health_alarm_transitions":alarm_transitions,
            "health_alarmed_nodes":sum(h.alarmed for h in health),
            "healthy_false_alarm_nodes":len(false_alarm_nodes),
            "adaptive_feedback_events":feedback_count,
            "adaptive_feedback_alarm_transitions":feedback_alarm_transitions,
            "eta_gt_one_dispatches":eta_above_one,
            "postshock_affected_dispatches":exposed,
            "telemetry_resets":telemetry,
            "node_dispatch_counts":[len(x) for x in assigned],
            "calibration_q_rank":qrank,
            "calibration_q_global":calibration["q_global"],
            "not_cloudsim_queue_equivalent":True,
            "network_feedback_events":risk_state.total_feedback,
            "network_positive_excess_feedback":risk_state.positive_feedback,
            "postshock_positive_network_feedback":risk_updated_postshock,
            "risk_positive_penalty_arrivals":risk_positive_arrivals,
            "risk_changed_node_selections":risk_reroutes,
            "risk_selected_penalty_sum_ms":risk_penalty_sum,
            "network_feedback_strictly_delayed":True}
