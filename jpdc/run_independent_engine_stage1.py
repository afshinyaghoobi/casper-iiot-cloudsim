#!/usr/bin/env python3
"""Frozen Stage-1 clean-room physical engine baseline matrix, descriptive only."""
import argparse,json
from pathlib import Path
from independent_physical_event_engine import run,POLICIES

SEEDS=(50,51)
SCENARIOS=("S0_STATIONARY","S1_LAMBDA_X2")
TASKS=12000

def main(out):
    rows=[]
    for seed in SEEDS:
        for scenario in SCENARIOS:
            for policy in POLICIES:
                r=run(seed,scenario,policy,TASKS)
                if r["status"]!="PASS" or r["tasks"]!=TASKS:
                    raise AssertionError("missing event records")
                if sum(r["by_criticality"].values())!=TASKS or sum(r["node_dispatch_counts"])!=TASKS:
                    raise AssertionError("broken task conservation")
                print("ENGINE_RESULT",seed,scenario,policy,
                      "mean_latency_ms",round(r["mean_latency_ms"],6),
                      "mean_wait_ms",round(r["mean_wait_ms"],6),
                      "mission_misses",r["deadline_misses"]["MISSION"])
                rows.append(r)
    if len(rows)!=12 or sum(r["tasks"] for r in rows)!=144000:
        raise AssertionError("incomplete original fixed matrix")
    payload={"status":"PASS","stage":"baseline-only clean-room deterministic physical FCFS",
             "comparison_scope":"exploratory mechanical test, NOT independent CASPER policy efficacy",
             "seeds":list(SEEDS),"scenarios":list(SCENARIOS),
             "total_task_policy_evaluations":144000,
             "models":list(POLICIES),"rows":rows}
    p=Path(out);p.parent.mkdir(parents=True,exist_ok=True)
    serialized=json.dumps(payload,indent=2,sort_keys=True,allow_nan=False)+"\n"
    p.write_text(serialized,encoding="utf-8")
    assert p.read_text(encoding="utf-8")==serialized
    print("JPDC_INDEPENDENT_ENGINE_FROZEN_MATRIX_PASS")

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--out",required=True)
    main(p.parse_args().out)
