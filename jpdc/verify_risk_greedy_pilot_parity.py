#!/usr/bin/env python3
"""Fail-closed paired pilot CSV audit: baseline policy rows must not change."""
import argparse,csv
from pathlib import Path
NEW="UNCERTAINTY_PENALIZED_GREEDY"
SCENARIOS={"S0_STATIONARY","S1_LAMBDA_X2","S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS","S4_COMPOUND"}
def read(path):
    with Path(path).open(newline="") as f:
        reader=csv.DictReader(f)
        cols=reader.fieldnames
        if not cols or not {"seed","scenario","policy","late_dvr","p99_late_latency_ms"} <= set(cols):
            raise ValueError("missing required columns")
        records=list(reader)
    if not records or any(set(row)!=set(cols) for row in records):
        raise ValueError("empty or malformed csv")
    keys=[(r["seed"],r["scenario"],r["policy"]) for r in records]
    if len(keys)!=len(set(keys)):raise ValueError("duplicate keys")
    return cols, {k:r for k,r in zip(keys,records)}
def audit(before,after):
    c0,b=read(before);c1,a=read(after)
    if c0!=c1:raise ValueError("schema changed")
    old=set(b)
    if len(old)!=40 or {k[1] for k in old}!=SCENARIOS or any(k[2]==NEW for k in old):
        raise ValueError("unexpected baseline sample")
    if not old.issubset(set(a)):raise ValueError("missing original baseline policy rows")
    if set(a)-old!={("4202202600",scenario,NEW) for scenario in SCENARIOS}:
        raise ValueError("missing/new unexpected policies")
    if len(a)!=45:raise ValueError("expected 45 output rows")
    for k in old:
        if a[k]!=b[k]:
            changed=[c for c in c0 if a[k][c]!=b[k][c]]
            # mapper wall-clock runtime includes nondeterministic platform timing;
            # do not treat its ordinary variation as science drift.
            if set(changed)!={"mean_mapper_us"} and (set(changed)-{"mean_mapper_us"}):
                raise ValueError(f"scientific drift at {k}, columns={changed}")
    return len(old),len(a)
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--before",required=True);p.add_argument("--after",required=True)
    args=p.parse_args()
    print("RISK_GREEDY_PARITY_PASS",audit(args.before,args.after))
