#!/usr/bin/env python3
"""Independent deterministic single-server FCFS event simulator; not CloudSim equivalence.

Routes three original baseline node families using independently generated
Python source workloads and node specifications, not observed Java outcomes.
"""
from collections import deque
import heapq
import math
from independent_workload_generator import nodes, tasks, predicted_latency
from independent_casper_state import VirtualQueue
from independent_stochastic_physics import affected_nodes, physical_durations, SCENARIOS

POLICIES = ('CLOUD_ONLY', 'EDGE_FIRST', 'PRED_GREEDY')

def choose(task, node_specs, vq, now, policy):
    if policy == 'CLOUD_ONLY': candidates = range(18, 21)
    elif policy == 'EDGE_FIRST': candidates = range(12)
    elif policy == 'PRED_GREEDY': candidates = range(21)
    else: raise ValueError('invalid baseline')
    return min(candidates, key=lambda j: (predicted_latency(task, node_specs[j],
                                      vq.predicted_backlog(j, now)), j))

def simulate(task_stream, node_specs, policy, save_trace=False, stochastic_seed=None, scenario=None):
    if len(node_specs)!=21 or [n[0] for n in node_specs]!=list(range(21)):
        raise ValueError('require 21 ordered, unique nodes')
    if policy not in POLICIES: raise ValueError('invalid policy')
    if (stochastic_seed is None)!=(scenario is None):
        raise ValueError('stochastic seed and scenario must be specified together')
    if scenario is not None and scenario not in SCENARIOS:
        raise ValueError('unrecognized physical scenario')
    affected=affected_nodes(stochastic_seed,scenario) if scenario is not None else frozenset()
    postshock_exposed=0
    events = []
    prev = -math.inf
    count = 0
    for t in task_stream:
        if t[1]!=count or not math.isfinite(t[7]) or t[7]<prev:
            raise ValueError('bad task order or arrival')
        if t[2] not in ('NORMAL','HIGH','MISSION') or not all(math.isfinite(x) and x>0 for x in t[3:7]):
            raise ValueError('invalid task')
        heapq.heappush(events,(t[7],1,t[1],t))
        prev=t[7];count+=1
    if count==0: raise ValueError('empty workload')
    # Completions precede arrivals at identical timestamps.
    waiting=[deque() for _ in node_specs]
    running=[None]*21
    next_free=[0.0]*21
    previous_finish=[0.0]*21
    assigned=[[] for _ in node_specs]
    started=[[] for _ in node_specs]
    vq=VirtualQueue(21)
    next_telemetry=1000.0
    telemetry_updates=0
    arrival_seen=set();finish_seen=set()
    count_by_type={k:0 for k in ('NORMAL','HIGH','MISSION')}
    late_by_type={k:0 for k in ('NORMAL','HIGH','MISSION')}
    latency_sum=wait_sum=0.0
    trace=[] if save_trace else None

    def start(node,item,now):
        task,network,cpu=item
        if running[node] is not None or now+1e-8<previous_finish[node]:
            raise AssertionError('overlapping execution')
        if now+1e-8<task[7]:raise AssertionError('start before task arrival')
        running[node]=(task[1],now)
        started[node].append(task[1])
        heapq.heappush(events,(now+cpu,0,task[1],(node,item,now)))

    while events:
        timestamp,kind,task_id,payload=heapq.heappop(events)
        if kind==1:
            t=payload
            if task_id in arrival_seen:raise AssertionError('duplicate arrival')
            arrival_seen.add(task_id)
            if timestamp>=next_telemetry:
                vq.reset_from_telemetry(next_free)
                next_telemetry=timestamp+50.0
                telemetry_updates+=1
            node=choose(t,node_specs,vq,timestamp,policy)
            spec=node_specs[node]
            nominal_cpu=t[4]/spec[1]*12.0
            if scenario is not None:
                cpu,network=physical_durations(stochastic_seed,t,spec,scenario,affected)
                if t[1]>=10000 and node in affected:
                    postshock_exposed+=1
            else:
                cpu=nominal_cpu
                network=spec[3]+(t[5]+t[6])*8000.0/spec[2]
            if not all(math.isfinite(v) and v>0 for v in (cpu,network)):
                raise ValueError('invalid service/network physics')
            assigned[node].append(task_id)
            next_free[node]=max(next_free[node],timestamp)+cpu
            vq.on_dispatch(node,timestamp,nominal_cpu)
            item=(t,network,cpu)
            if running[node] is None:
                if waiting[node]:raise AssertionError('bypassed older waiting task')
                start(node,item,timestamp)
            else:waiting[node].append(item)
        else:
            node,item,started_at=payload
            t,network,cpu=item
            if running[node]!=(task_id,started_at):raise AssertionError('stale completion')
            if task_id in finish_seen:raise AssertionError('duplicate completion')
            wait=max(0.0,started_at-t[7])
            latency=network+wait+cpu
            if abs(timestamp-(started_at+cpu))>1e-8 or abs(latency-(timestamp-t[7]+network))>1e-8:
                raise AssertionError('physical timing decomposition mismatch')
            finish_seen.add(task_id)
            count_by_type[t[2]]+=1
            if latency>t[3]:late_by_type[t[2]]+=1
            latency_sum+=latency;wait_sum+=wait
            if save_trace:
                trace.append({'task':task_id,'node':node,'arrival_ms':t[7],
                              'start_ms':started_at,'finish_ms':timestamp,
                              'wait_ms':wait,'network_ms':network,'cpu_ms':cpu,
                              'latency_ms':latency})
            running[node]=None
            previous_finish[node]=timestamp
            if waiting[node]:start(node,waiting[node].popleft(),timestamp)
    if arrival_seen!=set(range(count)) or finish_seen!=arrival_seen:
        raise AssertionError('task conservation violated')
    for node in range(21):
        if running[node] is not None or waiting[node] or assigned[node]!=started[node]:
            raise AssertionError('node did not preserve FIFO')
    out={'status':'PASS','engine':'independent_strict_FCFS_nominal_Python',
         'policy':policy,'tasks':count,'by_criticality':count_by_type,
         'deadline_misses':late_by_type,'mean_latency_ms':latency_sum/count,
         'mean_wait_ms':wait_sum/count,'telemetry_resets':telemetry_updates,
         'node_dispatch_counts':[len(x) for x in assigned]}
    if scenario is not None:
        out.update(stochastic_physics=True,postshock_affected_dispatches=postshock_exposed,
                   affected_nodes=sorted(affected))
    if save_trace:out['trace']=sorted(trace,key=lambda e:e['task'])
    return out

def run(seed_index,scenario,policy,count=12000,save_trace=False,stochastic=False):
    seed=4202202600+seed_index
    out=simulate(tasks(seed,count,scenario),nodes(seed),policy,save_trace,
                 stochastic_seed=seed if stochastic else None,
                 scenario=scenario if stochastic else None)
    out.update(seed_index=seed_index,scenario=scenario,scientific_seed=seed)
    return out
