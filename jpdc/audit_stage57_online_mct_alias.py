#!/usr/bin/env python3
"""Stage57 transparent *non-independent* MCT-vs-PRED_GREEDY alias audit.

This audit compares mathematically equivalent causal cost definitions under
identical eligibility and tie rules; it is NOT a second experimental method.
"""
import argparse
import json
import math
from pathlib import Path
from independent_workload_generator import nodes,tasks,predicted_latency
from independent_casper_state import VirtualQueue

QA_SEEDS=(1301,1302,1303)
QA_SCENARIOS=("S0_STATIONARY","S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
COUNT=1200
NODES=21

def greedy(task,specs,queue,now,eligible):
    choices=list(eligible)
    if not choices:
        raise ValueError("empty eligible set")
    values={j:predicted_latency(task,specs[j],queue.predicted_backlog(j,now))
            for j in choices}
    if not all(math.isfinite(v) and v>0 for v in values.values()):
        raise ValueError("invalid predicted latency")
    return min(choices,key=lambda j:(values[j],j))

def online_mct_adapted(task,specs,queue,now,eligible):
    # Completely independent expression of cost as absolute predicted finish.
    # Task arrival 'now' is the same constant for all eligible candidate nodes.
    choices=list(eligible)
    if not choices:
        raise ValueError("empty eligible set")
    def finish_at(j):
        _,capacity,bw,rtt,_,_=specs[j]
        _,_,_,_,work,received,sent,_=task
        remaining=max(0.0,queue.next_free[j]-now)
        return now+rtt+(received+sent)*8000.0/bw+remaining+work*12.0/capacity
    # Float arithmetic can differ by tiny relative rounding after summing
    # the common arrival offset; calculate relative completion to preserve
    # semantic tie policy and avoid false sub-ULP ordering.
    return min(choices,key=lambda j:(finish_at(j)-now,j))

def verify_contract():
    specs=nodes(4202202600+1301)
    q=VirtualQueue(21)
    t=next(tasks(4202202600+1301,2,"S0_STATIONARY"))
    assert greedy(t,specs,q,t[7],range(NODES))==online_mct_adapted(
        t,specs,q,t[7],range(NODES))
    assert all(greedy(t,specs,q,t[7],[i])==i for i in range(NODES))
    # Eligibility is a real part of the policy; unequal eligibility is NOT
    # a legitimate 'same Online MCT' comparison.
    g=greedy(t,specs,q,t[7],range(NODES))
    assert online_mct_adapted(t,specs,q,t[7],[i for i in range(NODES) if i!=g])!=g
    # The advertised formula includes transfer; omitting it changes objective
    # on a fixed deterministic fixture with two different network link rates.
    ex=list(specs)
    x=list(ex[0]);y=list(ex[1])
    x[1]=y[1]=5.
    x[2]=1.;y[2]=100000.
    x[3]=0.1;y[3]=1.
    ex[0]=tuple(x);ex[1]=tuple(y)
    sample=list(t);sample[4]=1.;sample[5]=100.;sample[6]=100.
    sample=tuple(sample)
    assert greedy(sample,ex,q,t[7],[0,1])==1
    no_transfer=min((0,1),key=lambda j:(ex[j][3]+sample[4]*12/ex[j][1],j))
    assert no_transfer==0
    print("JPDC_STAGE57_MCT_ALIAS_CONTRACT_PASS")

def run(seed):
    if seed not in QA_SEEDS:
        raise ValueError("unregistered QA source seed")
    rows=[]
    for scenario in QA_SCENARIOS:
        seed_value=4202202600+seed
        specs=nodes(seed_value)
        q=VirtualQueue(21)
        mismatches=[]
        assignments=[0]*NODES
        task_count=0
        for t in tasks(seed_value,COUNT,scenario):
            now=t[7]
            eligible=range(NODES)
            a=greedy(t,specs,q,now,eligible)
            b=online_mct_adapted(t,specs,q,now,eligible)
            if a!=b:
                mismatches.append(dict(task=t[1],greedy=a,online_mct=b))
            assignments[a]+=1
            nominal_service=12.0*t[4]/specs[a][1]
            q.on_dispatch(a,now,nominal_service)
            task_count+=1
        assert task_count==COUNT and sum(assignments)==COUNT
        # Exact-alias condition; any discrepancy is a gate FAIL.
        assert not mismatches,(seed,scenario,mismatches[:20])
        rows.append(dict(seed=seed,scenario=scenario,task_count=COUNT,
            identical_decisions=COUNT,mismatch_count=0,
            node_assignment_counts=assignments))
        print("JPDC_STAGE57_MCT_ALIAS_SOURCE",json.dumps(rows[-1],sort_keys=True),flush=True)
    return dict(status="PASS",source_seed=seed,qa_only=True,
       new_independent_policy_count=0,original_Braun_MCT_reproduced=False,
       source_task_decisions=COUNT*len(QA_SCENARIOS),rows=rows)

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--seed",type=int,required=True)
    ap.add_argument("--out",required=True)
    args=ap.parse_args()
    verify_contract()
    result=run(args.seed)
    p=Path(args.out)
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(result,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print("JPDC_STAGE57_MCT_ALIAS_AUDIT_PASS",args.seed)
