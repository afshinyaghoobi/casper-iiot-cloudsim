#!/usr/bin/env python3
"""Stage55 QA-only original independent Python event-vs-analytic reference."""
import argparse
import json
from pathlib import Path
from analytic_fcfs_reference_stage55 import audit
from independent_physical_event_engine import run as run_engine
from independent_workload_generator import tasks

QA_SEEDS=(1201,1202)
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
POLICIES=("CLOUD_ONLY","EDGE_FIRST","PRED_GREEDY")
TASK_COUNT=12000

def run(seed):
    if seed not in QA_SEEDS:
        raise ValueError("seed not in QA plan")
    rows=[]
    for scenario in SCENARIOS:
        original=list(tasks(4202202600+seed,TASK_COUNT,scenario))
        assert len(original)==TASK_COUNT
        for policy in POLICIES:
            result=run_engine(seed,scenario,policy,TASK_COUNT,save_trace=True,stochastic=True)
            assert result["status"]=="PASS" and result["tasks"]==TASK_COUNT
            ref=audit(result["trace"],original)
            assert ref["source_tasks"]==TASK_COUNT
            assert ref["criticality_counts"]==result["by_criticality"]
            assert ref["deadline_misses"]==result["deadline_misses"]
            assert ref["node_counts"]==result["node_dispatch_counts"]
            rows.append(dict(seed=seed,scenario=scenario,policy=policy,
                             task_count=TASK_COUNT,
                             analytical_reference=ref,
                             event_engine_mission_misses=result["deadline_misses"]["MISSION"],
                             mean_event_wait_ms=result["mean_wait_ms"],
                             mean_event_latency_ms=result["mean_latency_ms"]))
            print("JPDC_STAGE55_FROZEN_ROUTE_CROSSCHECK",json.dumps(rows[-1],sort_keys=True),flush=True)
    assert len(rows)==6
    return dict(status="PASS",model="strict FIFO Python event engine vs independent Lindley reference",
                original_java_30k_parity="previous registered FAIL remains",
                no_new_algorithm_or_independent_physics=True,
                source_seed=seed,rows=rows)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--seed",type=int,required=True)
    p.add_argument("--out",required=True)
    args=p.parse_args()
    outcome=run(args.seed)
    dest=Path(args.out)
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(outcome,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print("JPDC_STAGE55_SOURCE_QA_COMPLETE_PASS",args.seed,flush=True)
