"""Exploratory original-style native physical system plus new nonconformal network-risk policy.

NOT a validated novel algorithm or original CloudSim queue equivalence.
All network risk observations become policy-visible at end-to-end feedback,
never on dispatch or CPU-finish. Both E17 MISSION and new risk network outcome feedback are now observed
at separately scheduled E2E feedback events. NodeHealth retains the earlier
CPU-service finish time, as that partial outcome is then available.
"""
#!/usr/bin/env python3
"""Native independent CASPER deployment on a strict FCFS Python physical engine.

Inputs: independent Stage3 physical calibration, original-model RNG task/node
generation, native hashed physical noise. Does NOT use Java events/results.
This is explicitly not CloudSim SpaceShared queue-equivalent or YAFS.
"""
from collections import deque,Counter
from feedback_deadline_scheduler import CausalFeedbackDeadlineScheduler
from causal_regime_selector_stage42 import CausalRegimeSelector
from causal_node_regime_selector_stage44 import CausalNodeRegimeSelector
from queue_pressure_baseline_stage51 import choose as choose_stage51, QUEUE_ONLY, QUEUE_E2E
import heapq,math
from independent_workload_generator import nodes,tasks,predicted_latency
from independent_stochastic_physics import physical_durations,affected_nodes
from independent_casper_state import DualMemory,NodeHealth,VirtualQueue
from network_residual_risk_policy import NetworkResidualRisk
from normal_network_probe_stage6 import NormalNetworkProbe
from normalized_network_shock_epochs_stage10 import NormalizedObservedNetworkEpochs
from freshness_active_observation_stage13 import FreshnessAwareController
from congestion_guarded_freshness_stage15 import BoundedFreshnessController
from robust_interval_dominance_stage22 import RobustDominanceController

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
PROBE_POLICY="NEW_NETWORK_RESIDUAL_PROBE"
ACTIVE_POLICY="NEW_FRESHNESS_ACTIVE"
GUARDED_POLICY="NEW_FRESHNESS_GUARDED"
ROBUST_POLICY="NEW_ROBUST_INTERVAL_DOMINANCE"
CPU_POLICY="NEW_CPU_FEEDBACK_ONLY"
E2E_POLICY="NEW_E2E_FEEDBACK_ONLY"
COMBINED_POLICY="NEW_CPU_E2E_FEEDBACK"
FEEDBACK_POLICIES=(CPU_POLICY,E2E_POLICY,COMBINED_POLICY)
MISSION_CPU_POLICY="NEW_MISSION_ONLY_CPU_FEEDBACK"
MISSION_COMBINED_POLICY="NEW_MISSION_ONLY_CPU_E2E_FEEDBACK"
MISSION_FEEDBACK_POLICIES=(MISSION_CPU_POLICY,MISSION_COMBINED_POLICY)
ALL_FEEDBACK_POLICIES=(*FEEDBACK_POLICIES,*MISSION_FEEDBACK_POLICIES)
REGIME_COMBINED="NEW_REGIME_GATED_MISSION_COMBINED"
REGIME_E2E="NEW_REGIME_GATED_MISSION_E2E"
REGIME_POLICIES=(REGIME_COMBINED,REGIME_E2E)
FEEDBACK_AND_REGIME=(*ALL_FEEDBACK_POLICIES,*REGIME_POLICIES)
NODE_E2E_POLICY="NEW_NODE_REGIME_MISSION_E2E"
NODE_COMBINED_POLICY="NEW_NODE_REGIME_MISSION_COMBINED"
NODE_REGIME_POLICIES=(NODE_E2E_POLICY,NODE_COMBINED_POLICY)
ALL_REGIME_POLICIES=(*REGIME_POLICIES,*NODE_REGIME_POLICIES)
STAGE51_POLICIES=(QUEUE_ONLY,QUEUE_E2E)

def simulate(seed_index,scenario,policy,calibration,count=12000,trace_hook=None,mission_audit_hook=None):
    if policy not in (*POLICIES,NEW_POLICY,PROBE_POLICY,ACTIVE_POLICY,GUARDED_POLICY,ROBUST_POLICY,*FEEDBACK_AND_REGIME,*NODE_REGIME_POLICIES,*STAGE51_POLICIES):raise ValueError("invalid pilot policy")
    flags=(POLICY_FLAGS["CASPER_FULL"] if policy in ALL_REGIME_POLICIES else
           POLICY_FLAGS["PRED_GREEDY"] if policy in (NEW_POLICY,PROBE_POLICY,ACTIVE_POLICY,GUARDED_POLICY,ROBUST_POLICY,*ALL_FEEDBACK_POLICIES,*STAGE51_POLICIES)
           else POLICY_FLAGS[policy])
    regime=CausalRegimeSelector() if policy in REGIME_POLICIES else None
    node_regime=CausalNodeRegimeSelector() if policy in NODE_REGIME_POLICIES else None
    mission_network_selected=0
    mission_mode_full=0
    feedback_scheduler=CausalFeedbackDeadlineScheduler() if policy in (*FEEDBACK_AND_REGIME,*NODE_REGIME_POLICIES) else None
    net_probe=NormalNetworkProbe()
    risk_state=NetworkResidualRisk()
    shadow=NormalizedObservedNetworkEpochs([.0001]*NODES,[0.0]*NODES)
    fresh_controller=(FreshnessAwareController() if policy==ACTIVE_POLICY else
                      BoundedFreshnessController() if policy==GUARDED_POLICY else
                      RobustDominanceController() if policy==ROBUST_POLICY else None)
    shadow_alerts=[]
    shadow_first_arrival=None
    shadow_first_e2e=None
    shadow_affected_feedback=0
    shadow_seen_nodes=set()
    shadow_alarmed_nodes=set()
    shadow_false_alarms=0
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
    mission_dispatch_audit={}
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
    stage51_decisions=stage51_switches=stage51_mission_switches=0
    stage51_qpen_sum=stage51_e2epen_sum=0.0
    active_arrival_changes=0
    active_mission_changes=0
    active_probe_deadline_misses=0
    active_probe_latency_sum_ms=0.0
    active_probe_nominal_extra_ms=0.0
    cpu_finish_events=0
    e2e_feedback_events=0
    e17_observed_at_e2e=0
    probe_normal_deadline_misses=0
    probe_positive_network_excess_feedback=0
    probe_actual_latency_sum_ms=0.0
    probe_predicted_nominal_extra_ms=0.0
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
            active_selection=None
            if policy in ALL_REGIME_POLICIES:
                observed_regime=(regime.select(now) if regime is not None
                                 else node_regime.select(now,pred,t[2]=="MISSION"))
                baseline_node,rank,cert,family=route(
                    t,pred,alarm,sigma,qrank,calibration["q_global"],eta,"CASPER_FULL")
                if t[2]=="MISSION" and observed_regime.regime=="NETWORK":
                    mode=("BOTH" if policy in (REGIME_COMBINED,NODE_COMBINED_POLICY)
                          else "E2E")
                    d=feedback_scheduler.select(pred,t[3],t[2],risk_state.penalties(),mode)
                    j=d.node
                    rank,cert,family=1,False,()
                    mission_network_selected+=1
                else:
                    # Count dispatches in the feedback observer, but make the
                    # original CASPER_FULL decision, with its rank and screen.
                    feedback_scheduler.select(pred,t[3],t[2],(0.,)*NODES,"E2E")
                    j=baseline_node
                    if t[2]=="MISSION":mission_mode_full+=1
            elif policy in ALL_FEEDBACK_POLICIES:
                if policy in MISSION_FEEDBACK_POLICIES and t[2]!="MISSION":
                    # Source-greedy background: no node change or future feedback.
                    mode="E2E"
                    available_network=(0.,)*NODES
                else:
                    mode=("CPU" if policy in (CPU_POLICY,MISSION_CPU_POLICY) else
                          "E2E" if policy==E2E_POLICY else "BOTH")
                    available_network=risk_state.penalties()
                decision=feedback_scheduler.select(
                    pred,t[3],t[2],available_network,mode)
                j=decision.node
                rank,cert,family=1,False,()
            elif policy in (ACTIVE_POLICY,GUARDED_POLICY,ROBUST_POLICY):
                nominal_net_vector=[
                    specs[k][3]+(t[5]+t[6])*8000.0/specs[k][2]
                    for k in range(NODES)]
                if policy==ROBUST_POLICY:
                    active_selection=fresh_controller.select(
                        now,pred,nominal_net_vector,t[3],
                        t[2]=="NORMAL",t[2]=="MISSION")
                else:
                    active_selection=fresh_controller.select(
                        now,pred,nominal_net_vector,t[3],t[2]=="NORMAL")
                j=active_selection.node
                rank,cert,family=1,False,()
                active_arrival_changes+=int(j!=min(range(NODES),
                                                  key=lambda k:(pred[k],k)))
                active_mission_changes+=int(t[2]=="MISSION" and
                    j!=min(range(NODES),key=lambda k:(pred[k],k)))
                if active_selection.probe:
                    # Controller internally enforces deadline eligibility and
                    # <=2ms incremental NOMINAL route prediction.
                    active_probe_nominal_extra_ms+=(
                        pred[j]-pred[min(range(NODES),key=lambda k:(pred[k],k))])
            elif policy in STAGE51_POLICIES:
                # Only currently observable virtual queue and delivered E2E evidence.
                causal_backlog=[vq.predicted_backlog(k,now) for k in range(NODES)]
                j,qpen,epen=choose_stage51(pred,causal_backlog,risk_state.penalties(),policy)
                rank,cert,family=1,False,()
                stage51_decisions+=1
                stage51_qpen_sum+=qpen
                stage51_e2epen_sum+=epen
                greedy=min(range(NODES),key=lambda k:(pred[k],k))
                stage51_switches+=int(j!=greedy)
                stage51_mission_switches+=int(t[2]=="MISSION" and j!=greedy)
            elif policy in (NEW_POLICY,PROBE_POLICY):
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
            probe=active_selection.probe if active_selection is not None else False
            if policy==PROBE_POLICY:
                normal_risk_node=j
                j,probe,probe_changed=net_probe.pick(pred,t[3],normal_risk_node,t[2]=="NORMAL")
                if probe:
                    probe_predicted_nominal_extra_ms+=pred[j]-pred[normal_risk_node]
            if t[2]=="NORMAL":
                normal+=1
                if flags["health"] and normal%100==0 and probe_budget<math.ceil(.01*normal):
                    probe_budget+=1
                    candidates=[k for k in range(NODES) if not alarm[k] and pred[k]<=t[3]]
                    if candidates:
                        j=min(candidates,key=lambda k:(last_observed[k],pred[k],k))
                        probe=True;probes+=1
            if mission_audit_hook is not None and t[2]=="MISSION":
                original_greedy=min(range(NODES),key=lambda k:(pred[k],k))
                mission_dispatch_audit[i]=dict(
                    task_index=i,task_class=t[2],arrival_ms=now,
                    deadline_ms=t[3],chosen_node=j,
                    original_greedy_node=original_greedy,
                    nominal_chosen_latency_ms=pred[j],
                    nominal_greedy_latency_ms=pred[original_greedy],
                    differs_from_nominal_greedy=j!=original_greedy)
            cpu,net=physical_durations(seed,t,specs[j],scenario,affected)
            if i>=10000 and j in affected:
                exposed+=1
                if shadow_first_arrival is None:shadow_first_arrival=now
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
            cpu_finish_events+=1
            if feedback_scheduler is not None:
                feedback_scheduler.observe_cpu(j,cpu,nominal,now)
            if regime is not None:
                regime.observe_cpu_finish(cpu,nominal,now)
            if node_regime is not None:
                node_regime.observe_cpu_finish(j,cpu,nominal,now)
            # No future network or E17 outcome visible at physical CPU finish.
            outcome_score=(max(0.0,(latency-predj)/(sigmaj+1e-12))
                           if t[2]=="MISSION" and e17 is not None else None)
            heapq.heappush(events,(now+net,1,i,(j,net,t[5],t[6],outcome_score,now,probe)))
            if latency>t[3]:miss_by_type[t[2]]+=1
            latency_sum+=latency;wait_sum+=wait
            last_observed[j]=finish_ordinal;finish_ordinal+=1
            if flags["health"]:
                was=health[j].alarmed
                health[j].observe(cpu,nominal)
                if not was and health[j].alarmed:alarm_transitions+=1
                if health[j].alarmed and j not in affected:false_alarm_nodes.add(j)
            if policy in (ACTIVE_POLICY,GUARDED_POLICY) and probe:
                active_probe_latency_sum_ms+=latency
                active_probe_deadline_misses+=int(latency>t[3])
            if probe:
                probe_actual_latency_sum_ms+=latency
                if latency>t[3]:
                    probe_violations+=1
                    if policy==PROBE_POLICY:probe_normal_deadline_misses+=1
            if t[2]=="MISSION" and mission_audit_hook is not None:
                audit=mission_dispatch_audit.pop(i)
                mission_audit_hook(dict(**audit,
                    actual_cpu_ms=cpu,actual_wait_ms=wait,
                    actual_network_ms=net,actual_total_latency_ms=latency,
                    actual_deadline_miss=bool(latency>t[3]),
                    cpu_finished_ms=now))
            if t[2]=="MISSION":
                rank_counts[rank]+=1
                mission_results.append((i,i>=10000,cert,latency>t[3],family_covered,latency,eta,rank))
            running[j]=None
            last_finish[j]=now
            if queues[j]:start(j,queues[j].popleft(),now)
        else:
            # Only completed end-to-end observations may enter the risk state.
            j,actual_net,inmb,outmb,outcome_score,cpu_finish_time,was_probe=payload
            if now+1e-8 < cpu_finish_time+actual_net:
                raise AssertionError("premature end-to-end observation")
            e2e_feedback_events+=1
            nominal_net=specs[j][3]+(inmb+outmb)*8000.0/specs[j][2]
            excess=risk_state.observe_e2e(j,actual_net,nominal_net,now)
            if regime is not None:
                regime.observe_network_e2e(actual_net,nominal_net,now)
            if node_regime is not None:
                node_regime.observe_network_e2e(j,actual_net,nominal_net,now)
            # Shadow state sees ONLY delivered observations, not hidden truth.
            # Optional E2E-only scientific audit hook: never consulted by routing.
            # Capture state strictly before this report enters the observer.
            prior_history=tuple(shadow.history[j]) if trace_hook is not None else ()
            prior_measurement=shadow.last_measurement[j] if trace_hook is not None else None
            observation=shadow.deliver(j,actual_net,nominal_net,cpu_finish_time,now)
            if fresh_controller is not None:
                fresh_controller.deliver_e2e(j,actual_net,nominal_net,cpu_finish_time,now)
            if trace_hook is not None:
                trace_hook(dict(task_index=i,node=j,cpu_finish_ms=cpu_finish_time,
                    delivered_ms=now,actual_network_ms=actual_net,
                    nominal_network_ms=nominal_net,
                    normalized_excess=max(0.0,actual_net/nominal_net-1.0),
                    prior_accepted_count=len(prior_history),
                    prior_latest_measurement_ms=(
                        prior_measurement if math.isfinite(prior_measurement) else None),
                    kind=observation.kind,epoch=observation.epoch))

            if i>=10000 and j in affected:
                shadow_affected_feedback+=1
                shadow_seen_nodes.add(j)
                if shadow_first_e2e is None:shadow_first_e2e=now
            if observation.kind=="observed_incompatible_change_alarm":
                affected_post=(i>=10000 and j in affected)
                if affected_post:shadow_alarmed_nodes.add(j)
                else:shadow_false_alarms+=1
                shadow_alerts.append(dict(node=j,time_ms=now,
                                          task_index=i,affected_postshock=affected_post))
            net_probe.observe_completed_e2e(j)
            if policy==PROBE_POLICY and was_probe and excess>0:
                probe_positive_network_excess_feedback+=1
            risk_updated_postshock+=int(i>=10000 and excess>0)
            if outcome_score is not None:
                if e17 is None:raise AssertionError("adaptive outcome delivered to nonadaptive policy")
                previous=e17.alarm_ever
                e17.observe(outcome_score)
                feedback_count+=1
                e17_observed_at_e2e+=1
                if not previous and e17.alarm_ever:feedback_alarm_transitions+=1
    net_probe.assert_valid()
    if fresh_controller is not None:
        if policy==ROBUST_POLICY:
            fresh_controller.invariant()
        else:
            fresh_controller.assert_budget()
        if fresh_controller.observer.total_delivered!=count:
            raise AssertionError("active network feedback conservation")
    if feedback_scheduler is not None:
        feedback_scheduler.invariant(count)
    if regime is not None:
        regime.invariant(count)
    if node_regime is not None:
        node_regime.invariant(count,by_type["MISSION"])
    if net_probe.global_ordinal!=count:
        raise AssertionError("network probe E2E feedback conservation failed")
    if risk_state.total_feedback!=count or cpu_finish_events!=count or e2e_feedback_events!=count:
        raise AssertionError("missing or duplicated CPU/E2E feedback")
    if arrived!=set(range(count)) or completed!=arrived or any(r is not None for r in running):
        raise AssertionError("native deployment task conservation")
    if any(queues) or assigned!=started:
        raise AssertionError("native strict FIFO order violated")
    if mission_audit_hook is not None and mission_dispatch_audit:
        raise AssertionError("missing MISSION CPU-finish forensic labels")
    mission_results.sort(key=lambda v:v[0])
    post=[r for r in mission_results if r[1]]
    if len(mission_results)!=by_type["MISSION"]:
        raise AssertionError("mission outcome count")
    if e17 is not None and feedback_count!=len(mission_results):
        raise AssertionError("incomplete independent adaptive feedback")
    if not flags["adaptive"] and feedback_count!=0:
        raise AssertionError("adaptive feedback in nonadaptive policy")
    if feedback_count!=e17_observed_at_e2e:
        raise AssertionError("E17 feedback arrived before physical E2E event")
    if not flags["cp"] and any(r[2] for r in mission_results):
        raise AssertionError("baseline issued certificate")
    def rate(items,pred_fn):
        return sum(pred_fn(v) for v in items)/len(items) if items else None
    result={"status":"PASS","engine":"native_Python_stochastic_strict_FCFS",
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
            "network_feedback_strictly_delayed":True,
            "e17_feedback_strictly_delayed":True,
            "cpu_finish_events":cpu_finish_events,
            "e2e_feedback_events":e2e_feedback_events,
            "e17_observed_at_e2e":e17_observed_at_e2e,
            "network_probe_opportunities":net_probe.opportunities if policy==PROBE_POLICY else 0,
            "network_probe_attempts":net_probe.attempts if policy==PROBE_POLICY else 0,
            "network_probe_skipped_empty":net_probe.skipped_empty if policy==PROBE_POLICY else 0,
            "network_probe_changed_choices":net_probe.changed_decisions if policy==PROBE_POLICY else 0,
            "network_probe_positive_feedback":probe_positive_network_excess_feedback,
            "network_probe_normal_deadline_misses":probe_normal_deadline_misses,
            "network_probe_actual_latency_sum_ms":probe_actual_latency_sum_ms if policy==PROBE_POLICY else 0.0,
            "network_probe_predicted_nominal_extra_ms":probe_predicted_nominal_extra_ms,
            "network_node_feedback_counts":net_probe.completed_feedback if policy in (NEW_POLICY,PROBE_POLICY) else None,
            "shadow_network_epoch":{
                "shadow_only_no_routing_control":True,
                "drift_L_per_ms":.0001,
                "measurement_epsilon":0.0,
                "feedback_events":shadow.total_delivered,
                "alarms_by_node":list(shadow.alarms),
                "quarantined_reports_by_node":list(shadow.late_quarantined),
                "alarms":shadow_alerts,
                "alarm_count":len(shadow_alerts),
                "affected_postshock_dispatches":exposed,
                "affected_postshock_feedback":shadow_affected_feedback,
                "affected_nodes_observed_postshock":len(shadow_seen_nodes),
                "affected_nodes_alarmed":len(shadow_alarmed_nodes),
                "false_alarms":shadow_false_alarms,
                "distinct_affected_unobserved_nodes":len(affected-shadow_seen_nodes),
                "affected_unobserved_ids_offline_only":sorted(affected-shadow_seen_nodes),
                "affected_no_alarm_ids_offline_only":sorted(shadow_seen_nodes-shadow_alarmed_nodes),
                "first_exposed_task_arrival_ms":shadow_first_arrival,
                "first_exposed_task_e2e_delivery_ms":shadow_first_e2e,
                "first_observed_affected_alarm_e2e_ms":min(
                    (a["time_ms"] for a in shadow_alerts if a["affected_postshock"]),default=None),
                "detector_delay_from_first_affected_arrival_ms":(
                    min(a["time_ms"] for a in shadow_alerts if a["affected_postshock"])-shadow_first_arrival
                    if shadow_alarmed_nodes and shadow_first_arrival is not None else None),
                "detector_delay_from_first_affected_feedback_ms":(
                    min(a["time_ms"] for a in shadow_alerts if a["affected_postshock"])-shadow_first_e2e
                    if shadow_alarmed_nodes and shadow_first_e2e is not None else None)
            }}
    if fresh_controller is not None and policy!=ROBUST_POLICY:
        result["stage14_active"]={
            "nonconformal_unverified_policy":True,
            "causal_e2e_delivered":fresh_controller.observer.total_delivered,
            "normal_arrivals":fresh_controller.normal_arrivals,
            "probe_opportunities":fresh_controller.probe_opportunities,
            "probe_attempts":fresh_controller.probe_attempts,
            "probe_skipped":fresh_controller.probe_skipped,
            "probe_changed_choices":fresh_controller.probe_changed,
            "probe_nominal_extra_ms_vs_greedy":active_probe_nominal_extra_ms,
            "probe_actual_latency_sum_ms":active_probe_latency_sum_ms,
            "probe_normal_deadline_misses":active_probe_deadline_misses,
            "mission_unverified_decisions":fresh_controller.mission_unverified,
            "arrivals_changed_from_nominal_greedy":active_arrival_changes,
            "mission_changed_from_nominal_greedy":active_mission_changes,
            "alarms_by_node":list(fresh_controller.observer.alarms),
            "late_quarantine_by_node":list(fresh_controller.observer.late_quarantined)
        }
    if regime is not None:
        assert mission_network_selected+mission_mode_full==len(mission_results)
        result["stage42_regime"]={
            "cpu_finish_observations":regime.cpu_observations,
            "network_e2e_deliveries":regime.network_observations,
            "regime_decisions":regime.dispatches,
            "network_regime_dispatches":regime.network_dispatches,
            "ambiguous_cpu_and_network_dispatches":regime.ambiguous_dispatches,
            "first_network_regime_dispatch_ms":regime.first_network_dispatch_clock,
            "mission_network_regime_dispatches":mission_network_selected,
            "mission_full_regime_dispatches":mission_mode_full,
            "uses_hidden_fault_mask_or_actual_scenario_at_dispatch":False,
            "conditional_safety_certificate":False,
            "post_mission_deadline_misses":sum(int(r[3]) for r in post)
        }
    if node_regime is not None:
        assert mission_network_selected+mission_mode_full==len(mission_results)
        result["stage44_node_regime"]={
            "cpu_finish_observations":node_regime.cpu_observations,
            "network_e2e_deliveries":node_regime.network_observations,
            "decisions":node_regime.decisions,
            "network_regime_dispatches":node_regime.network_mode_decisions,
            "ambiguous_cpu_and_network_dispatches":node_regime.ambiguous_decisions,
            "first_network_regime_dispatch_ms":node_regime.first_network_mode_clock,
            "mission_network_regime_dispatches":node_regime.mission_network_decisions,
            "mission_full_regime_dispatches":node_regime.mission_full_decisions,
            "network_node_evidence_counts":node_regime.network_node_observation_counts,
            "cpu_node_evidence_counts":node_regime.cpu_node_observation_counts,
            "hidden_scenario_or_true_fault_mask_used_at_dispatch":False,
            "no_hard_deadline_or_conformal_certificate":True,
            "post_mission_deadline_misses":sum(int(r[3]) for r in post)
        }
    if feedback_scheduler is not None:
        if policy in MISSION_FEEDBACK_POLICIES and feedback_scheduler.changed!=feedback_scheduler.mission_changed:
            raise AssertionError("MISSION-only feedback rerouted a non-MISSION job")
        result["stage37_feedback"]={
            "causal_cpu_finishes":feedback_scheduler.cpu_finishes,
            "delayed_network_observations":risk_state.total_feedback,
            "decisions":feedback_scheduler.decisions,
            "changed_from_greedy":feedback_scheduler.changed,
            "mission_changed_from_greedy":feedback_scheduler.mission_changed,
            "background_changes_from_greedy":(
                feedback_scheduler.changed-feedback_scheduler.mission_changed),
            "mission_only_feedback":policy in MISSION_FEEDBACK_POLICIES,
            "predicted_feasible_selections":feedback_scheduler.predicted_feasible,
            "budget_violations":feedback_scheduler.budget_violations,
            "post_mission_deadline_misses":sum(int(r[3]) for r in post),
            "deadline_misses_by_class":dict(miss_by_type),
            "uses_hidden_fault_map_at_dispatch":False,
            "risk_certificate":False,
            "simulation_backend":"native_Python_stochastic_strict_FCFS"
        }
    if policy in STAGE51_POLICIES:
        assert stage51_decisions==count and 0<=stage51_mission_switches<=stage51_switches<=count
        result["stage51_comparator"]={
            "label":policy,"authors_original_DFAQ_LB_implementation":False,
            "simulation_engine":"Python strict FCFS only",
            "source_oracle_at_dispatch":False,
            "issue_time_queue_only":policy==QUEUE_ONLY,
            "delayed_network_e2e_only_after_delivery":True,
            "decisions":stage51_decisions,
            "switches_vs_pred_greedy":stage51_switches,
            "mission_switches_vs_pred_greedy":stage51_mission_switches,
            "selected_queue_pressure_sum_ms":stage51_qpen_sum,
            "selected_delivered_e2e_penalty_sum_ms":stage51_e2epen_sum,
            "post_mission_deadline_misses":sum(int(r[3]) for r in post)
        }
    if policy==ROBUST_POLICY:
        assert fresh_controller is not None
        result["stage23_robust"]={
            "nonconformal_assumption_conditioned":True,
            "causal_e2e_delivered":fresh_controller.observer.total_delivered,
            "decisions":fresh_controller.decisions,
            "switches":fresh_controller.switches,
            "mission_switches":fresh_controller.mission_switches,
            "unverified_decisions":fresh_controller.unverified_decisions,
            "arrivals_changed_from_greedy":active_arrival_changes,
            "mission_changed_from_greedy":active_mission_changes,
            "probe_attempts":0,
            "alarms_by_node":list(fresh_controller.observer.alarms),
            "late_quarantine_by_node":list(fresh_controller.observer.late_quarantined),
            "all_physics_in_strict_fcfs_python_only":True
        }
        if fresh_controller.decisions!=count or fresh_controller.switches!=active_arrival_changes:
            raise AssertionError("robust source routing decision conservation")
        if fresh_controller.mission_switches!=active_mission_changes:
            raise AssertionError("robust mission switch conservation")
    return result
