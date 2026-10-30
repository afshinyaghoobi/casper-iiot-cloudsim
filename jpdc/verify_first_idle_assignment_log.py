#!/usr/bin/env python3
"""Strict audit of deployment node-assignment logs; no simulator claims."""
import argparse
import re
from pathlib import Path
SCENARIOS={"S0_STATIONARY","S1_LAMBDA_X2","S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS","S4_COMPOUND"}
POLICIES={"CLOUD_ONLY","EDGE_FIRST","PRED_GREEDY","GLOBAL_CP","RANKED_CP_STATIC",
"CASPER_ADAPT_NO_HEALTH","CASPER_HEALTH_STATIC","CASPER_FULL","FIRST_IDLE_TIER"}
PATTERN=re.compile(r"^JPDC_NODE_ASSIGNMENTS scenario=(\w+) policy=(\w+) seed=(\d+) counts=\[([\d, ]+)\]$", re.M)
def audit(text, tasks=30000, seed=4202202600):
    found={}
    for line in text.splitlines():
        if not line.startswith("JPDC_NODE_ASSIGNMENTS"):
            continue
        match=PATTERN.fullmatch(line)
        if match is None:
            raise ValueError(f"malformed assignment record: {line[:200]}")
        scenario,policy,seed_text,numbers=match.groups()
        key=(scenario,policy)
        if key in found: raise ValueError(f"duplicate assignment line {key}")
        if scenario not in SCENARIOS or policy not in POLICIES or int(seed_text)!=seed:
            raise ValueError(f"unexpected scenario/policy/seed {match.group(0)}")
        counts=[int(v.strip()) for v in numbers.split(",")]
        if len(counts)!=24 or sum(counts)!=tasks: raise ValueError(f"invalid assignment counts {key}")
        found[key]=counts
    expected={(s,p) for s in SCENARIOS for p in POLICIES}
    if set(found)!=expected: raise ValueError(f"missing {len(expected-set(found))} or unexpected {len(set(found)-expected)} records")
    return found
if __name__=="__main__":
    a=argparse.ArgumentParser();a.add_argument("--log",required=True);a.add_argument("--tasks",type=int,default=30000);args=a.parse_args()
    rows=audit(Path(args.log).read_text(),args.tasks)
    print("FIRST_IDLE_ASSIGNMENT_AUDIT_PASS",len(rows),"rows")
