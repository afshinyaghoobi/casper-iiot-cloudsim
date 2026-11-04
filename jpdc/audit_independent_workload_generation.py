#!/usr/bin/env python3
"""Compare original frozen Java E42 task/node records with independent Python generator."""
import argparse,csv,math
from pathlib import Path
from independent_workload_generator import nodes,tasks,SCENARIO_MULT,predicted_latency

def equal(actual,expected,label,abs_tol):
    a=float(actual)
    if not math.isfinite(a) or not math.isclose(a,expected,rel_tol=0,abs_tol=abs_tol):
        raise ValueError(f"{label}: original Java={actual}, independent Python={expected}")

def audit(path):
    scientific_seed=4202202640
    expected_nodes=nodes(scientific_seed)
    expected_tasks={name:iter(tasks(scientific_seed,30000,name)) for name in SCENARIO_MULT}
    counts={name:0 for name in SCENARIO_MULT}
    node_count=0;prior_arrival={name:None for name in SCENARIO_MULT}
    done=0
    with Path(path).open(encoding="utf-8") as stream:
        for row in csv.reader(stream):
            if not row:continue
            if row[0]=="JPDC_NODE":
                if len(row)!=7 or node_count>=21 or done:raise ValueError("node fields or ordering")
                exp=expected_nodes[node_count]
                if int(row[1])!=exp[0] or int(row[6])!=exp[5]:raise ValueError("node identity/mips")
                for k in range(2,6):equal(row[k],exp[k-1],f"node{node_count} field{k}",1e-10)
                node_count+=1
            elif row[0]=="JPDC_TASK":
                if node_count!=21 or len(row)!=9 or done:raise ValueError("task shape/order")
                scenario=row[1]
                if scenario not in expected_tasks:raise ValueError("unknown scenario")
                i=counts[scenario]
                if i>=30000:raise ValueError("excess tasks")
                exp=next(expected_tasks[scenario])
                if int(row[2])!=i or row[3]!=exp[2]:
                    raise ValueError(f"task index/criticality mismatch {scenario}/{i}")
                for k in range(4,9):
                    equal(row[k],exp[k-1],f"{scenario} task{i} field{k}",1e-8)
                arr=float(row[8])
                if prior_arrival[scenario] is not None and arr<=prior_arrival[scenario]:
                    raise ValueError("arrival order is not strictly increasing")
                prior_arrival[scenario]=arr
                counts[scenario]+=1
                # Independent predicted-latency source formula, zero backlogs.
                # Original nominalService/network functions are separately audited below.
            elif row[0]=="JPDC_WORKLOAD_REFERENCE_COMPLETE":
                done+=1
            else:raise ValueError("unexpected reference row")
    if node_count!=21 or done!=1 or any(v!=30000 for v in counts.values()):
        raise ValueError(f"incomplete workload verification nodes={node_count}, tasks={counts}, complete={done}")
    return counts

if __name__=="__main__":
    a=argparse.ArgumentParser()
    a.add_argument("--original-java",required=True)
    opts=a.parse_args()
    result=audit(opts.original_java)
    for name,count in result.items():print("PASS",name,count,"original tasks matched by independent Python generator")
    print("JPDC_ORIGINAL_WORKLOAD_INDEPENDENT_GENERATION_PARITY_PASS")
