#!/usr/bin/env python3
"""Fail-closed 5-scenario seed-zero parity for FIRST_IDLE_TIER."""
import argparse, csv
from pathlib import Path

SCENARIOS={"S0_STATIONARY","S1_LAMBDA_X2","S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS","S4_COMPOUND"}
ORIGINAL={"CLOUD_ONLY","EDGE_FIRST","PRED_GREEDY","GLOBAL_CP","RANKED_CP_STATIC",
          "CASPER_ADAPT_NO_HEALTH","CASPER_HEALTH_STATIC","CASPER_FULL"}
ADDED="FIRST_IDLE_TIER"
FIELDS={"seed","scenario","policy","late_dvr","p99_late_latency_ms","mean_mapper_us"}
def load(p):
    with Path(p).open(newline="") as f:
        reader=csv.DictReader(f)
        fields=reader.fieldnames
        if not fields or not FIELDS.issubset(fields): raise ValueError("CSV schema missing fields")
        rows={}
        for row in reader:
            key=(row["seed"],row["scenario"],row["policy"])
            if key in rows: raise ValueError("duplicate "+repr(key))
            rows[key]=row
    return fields,rows
def verify(before,after):
    fields,b=load(before)
    other,a=load(after)
    if fields!=other: raise ValueError("schema mismatch")
    old={("4202202600",s,p) for s in SCENARIOS for p in ORIGINAL}
    add={("4202202600",s,ADDED) for s in SCENARIOS}
    if set(b)!=old: raise ValueError("original policy grid incorrect")
    if set(a)!=old|add: raise ValueError("patched policy grid incorrect")
    for k in old:
        for col in fields:
            if col=="mean_mapper_us": continue
            if a[k][col]!=b[k][col]:
                raise ValueError("original scientific row changed: "+repr((k,col)))
    return len(b),len(a)
if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--before",required=True)
    ap.add_argument("--after",required=True)
    args=ap.parse_args()
    print("FIRST_IDLE_TIER_PARITY_PASS",verify(args.before,args.after))
