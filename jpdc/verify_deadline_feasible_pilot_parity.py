#!/usr/bin/env python3
"""Strict parity audit for standalone deadline-feasible policy pilot."""
import argparse,csv
from pathlib import Path
SCENARIOS={"S0_STATIONARY","S1_LAMBDA_X2","S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS","S4_COMPOUND"}
OLD={"CLOUD_ONLY","EDGE_FIRST","PRED_GREEDY","GLOBAL_CP","RANKED_CP_STATIC","CASPER_ADAPT_NO_HEALTH","CASPER_HEALTH_STATIC","CASPER_FULL"}
NEW="DEADLINE_FEASIBLE_MIN_UNCERTAINTY"
def load(path):
    with Path(path).open(newline="") as f:
        reader=csv.DictReader(f)
        fields=reader.fieldnames
        if not fields or not {"seed","scenario","policy","late_dvr","p99_late_latency_ms","mean_mapper_us"}<=set(fields):
            raise ValueError("missing columns")
        data={}
        for row in reader:
            key=(row["seed"],row["scenario"],row["policy"])
            if key in data:raise ValueError("duplicate "+str(key))
            data[key]=row
    return fields,data
def verify(before,after):
    fields,b=load(before);other,a=load(after)
    if fields!=other:raise ValueError("changed CSV schema")
    expected={("4202202600",scenario,policy) for scenario in SCENARIOS for policy in OLD}
    additions={("4202202600",scenario,NEW) for scenario in SCENARIOS}
    if set(b)!=expected:raise ValueError("wrong original policy grid")
    if set(a)!=expected|additions:raise ValueError("wrong patched policy grid")
    for k in expected:
        for c in fields:
            if c=="mean_mapper_us":continue
            if b[k][c]!=a[k][c]:raise ValueError(f"scientific mismatch {k} {c}")
    return len(b),len(a)
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--before",required=True);p.add_argument("--after",required=True);x=p.parse_args()
    print("DEADLINE_PILOT_PARITY_PASS",verify(x.before,x.after))
