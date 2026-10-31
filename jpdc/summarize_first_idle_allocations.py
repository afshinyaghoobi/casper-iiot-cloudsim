#!/usr/bin/env python3
"""Descriptive allocation summary from verified seed-zero CloudSim artifacts.

This is NOT inferential evidence of ordering bias: heterogeneity and policy
routing can also produce unequal counts. Always retain the original log/CSV.
"""
import argparse
import csv
import json
import math
from pathlib import Path
from verify_first_idle_assignment_log import audit
from crosscheck_first_idle_artifacts import check

COMPARE=("FIRST_IDLE_TIER","PRED_GREEDY","CASPER_FULL")
def summarize(csv_path,log_path):
    check(csv_path,log_path)  # validates all 45 scientific/placement records
    allocations=audit(Path(log_path).read_text())
    with Path(csv_path).open(newline="") as f:
        rows={(r["scenario"],r["policy"]):r for r in csv.DictReader(f)}
    result=[]
    for (scenario,policy),counts in sorted(allocations.items()):
        if policy not in COMPARE: continue
        n=sum(counts)
        if n!=30000: raise ValueError("unexpected task count")
        layer={"edge":sum(counts[:12]),"fog":sum(counts[12:18]),"cloud":sum(counts[18:])}
        hhi=sum((c/n)**2 for c in counts)
        # Normalized node-level concentration (0 uniform; 1 single-node).
        norm=(hhi-1/24)/(1-1/24)
        row=rows[(scenario,policy)]
        dvr=float(row["late_dvr"])
        latency=float(row["p99_late_latency_ms"])
        if not math.isfinite(dvr) or not 0.0<=dvr<=1.0:
            raise ValueError(f"invalid deadline violation rate {scenario} {policy}")
        if not math.isfinite(latency) or latency<0.0:
            raise ValueError(f"invalid tail latency {scenario} {policy}")
        if not 0.0<=norm<=1.0+1e-12:
            raise ValueError(f"invalid normalized HHI {scenario} {policy}")
        result.append({
            "scenario":scenario, "policy":policy,
            "edge_count":layer["edge"], "fog_count":layer["fog"],"cloud_count":layer["cloud"],
            "edge_share":layer["edge"]/n,"fog_share":layer["fog"]/n,"cloud_share":layer["cloud"]/n,
            "node_hhi":hhi,"node_hhi_normalized":norm,
            "top_node":max(range(24),key=lambda i:counts[i]),
            "top_node_count":max(counts),
            "late_dvr":dvr,
            "p99_late_latency_ms":latency
        })
    if len(result)!=15: raise ValueError("expected 3 policies x 5 scenarios")
    return result

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--csv",required=True);p.add_argument("--log",required=True);p.add_argument("--out",required=True)
    a=p.parse_args()
    data=summarize(a.csv,a.log)
    Path(a.out).write_text(json.dumps({"evidence":"descriptive_seed_zero_only",
      "warning":"Unequal placement counts do not establish causal index bias.",
      "rows":data},indent=2)+"\n")
    print("FIRST_IDLE_ALLOCATION_SUMMARY_PASS",len(data))
