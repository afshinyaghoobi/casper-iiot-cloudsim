#!/usr/bin/env python3
"""Fail-closed paired audit for CASPER_FULL eta=1 intervention; no effect claims."""
import argparse
import math
from verify_first_idle_tier_pilot_parity import load, SCENARIOS, ORIGINAL

def verify(before,after):
    cols,b=load(before); other,a=load(after)
    if cols!=other: raise ValueError("schema mismatch")
    expected={("4202202600",s,p) for s in SCENARIOS for p in ORIGINAL}
    if set(b)!=expected or set(a)!=expected: raise ValueError("incomplete or duplicate grid")
    for key in expected:
        if key[2]=="CASPER_FULL": continue
        for col in cols:
            if col=="mean_mapper_us": continue
            if b[key][col]!=a[key][col]:
                raise ValueError(f"non-intervened science changed: {key} {col}")
    for key,row in a.items():
        if float(row["cloudsim_completion"])!=1.0 or int(row["tasks"])!=30000:
            raise ValueError(f"incomplete run {key}")
    # Positive control: with dispatch eta clamped to 1, CASPER_FULL must
    # reproduce the pre-existing CASPER_HEALTH_STATIC scientific outputs.
    # Different policy labels and wall-clock mapper timing are excluded.
    for scenario in SCENARIOS:
        static_key=("4202202600",scenario,"CASPER_HEALTH_STATIC")
        clamp_key=("4202202600",scenario,"CASPER_FULL")
        eta=float(a[clamp_key]["late_eta"])
        if not math.isfinite(eta) or abs(eta-1.0)>1e-9:
            raise ValueError(f"eta clamp not reflected in output: {scenario} eta={eta}")
        for col in cols:
            if col in ("policy","mean_mapper_us"): continue
            if a[static_key][col]!=a[clamp_key][col]:
                raise ValueError(f"eta-clamp positive-control mismatch: {scenario} {col}")
    result=[]
    for s in sorted(SCENARIOS):
        k=("4202202600",s,"CASPER_FULL")
        base=b[k]; intervention=a[k]
        result.append((s,float(base["late_dvr"]),float(intervention["late_dvr"]),
                       float(intervention["late_dvr"])-float(base["late_dvr"])))
    return result

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--before",required=True);p.add_argument("--after",required=True)
    args=p.parse_args()
    for scenario,b,a,d in verify(args.before,args.after):
        print(f"ETA_CLAMP_PARITY_PASS {scenario} original={b:.9f} clamp={a:.9f} delta={d:+.9f}")
