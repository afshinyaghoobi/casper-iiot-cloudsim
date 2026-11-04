#!/usr/bin/env python3
"""Strict independent source-physics parity on 5040 source-reflected Java pairs."""
import argparse,csv,math
from pathlib import Path
from independent_workload_generator import nodes,tasks
from independent_stochastic_physics import affected_nodes,physical_durations,SCENARIOS

INDICES=(0,1,2,9980,9999,10000,10001,10002,10004,11000,11999,13000,
         15000,17000,19999,20000,21000,22000,23000,24000,25000,27000,29000,29999)

def audit(path):
    masks=set();pairs=set();end=0
    node_specs={k:nodes(4202202600+k) for k in (50,51)}
    # Consume only internally generated original source input streams.
    task_inputs={(k,scenario):dict((t[1],t) for t in tasks(4202202600+k,30000,scenario) if t[1] in INDICES)
                 for k in (50,51) for scenario in SCENARIOS}
    for line in Path(path).open(encoding="utf-8"):
        if not line.startswith(("STOCH_MASK,","STOCH_PAIR,","STOCH_REFERENCE_COMPLETE")):continue
        row=next(csv.reader([line]))
        if row[0]=="STOCH_MASK":
            if len(row)!=4:raise ValueError("malformed original mask")
            k=int(row[1]);sc=row[2];key=(k,sc);bitstring=row[3]
            if k not in (50,51) or sc not in SCENARIOS or key in masks:
                raise ValueError("unexpected or duplicate scientific mask")
            expected=affected_nodes(4202202600+k,sc)
            if bitstring!="".join("1" if j in expected else "0" for j in range(21)):
                raise ValueError(f"original mask mismatch at {key}")
            masks.add(key)
        elif row[0]=="STOCH_PAIR":
            if len(row)!=7:raise ValueError("malformed source physical pair")
            k=int(row[1]);sc=row[2];task_id=int(row[3]);node=int(row[4])
            key=(k,sc,task_id,node)
            if (k not in (50,51) or sc not in SCENARIOS or
                task_id not in INDICES or not 0<=node<21 or key in pairs):
                raise ValueError("unknown or duplicate physical pair")
            if (k,sc) not in masks:raise ValueError("pair before mask")
            pairs.add(key)
            cpu,net=physical_durations(4202202600+k,task_inputs[(k,sc)][task_id],
                                       node_specs[k][node],sc,affected_nodes(4202202600+k,sc))
            for label,observed,expected in (("cpu",float(row[5]),cpu),("network",float(row[6]),net)):
                if not math.isfinite(observed) or not math.isclose(observed,expected,rel_tol=0,abs_tol=1e-8):
                    raise ValueError(f"independent {label} physics mismatch at {key}: Java={observed}, Python={expected}")
        else:
            if row!=["STOCH_REFERENCE_COMPLETE"]:raise ValueError("bad completion marker")
            end+=1
    if len(masks)!=10 or len(pairs)!=5040 or end!=1:
        raise ValueError(f"incomplete physics coverage masks={len(masks)} pairs={len(pairs)} end={end}")
    return {"masks":len(masks),"pairs":len(pairs),"status":"PASS"}

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--original",required=True)
    r=audit(p.parse_args().original)
    print("PASS original affected masks:",r["masks"])
    print("PASS independently generated CPU and network physics pairs:",r["pairs"])
    print("JPDC_INDEPENDENT_STOCHASTIC_PHYSICS_PARITY_PASS")
