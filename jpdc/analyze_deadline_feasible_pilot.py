#!/usr/bin/env python3
"""Single-seed descriptive comparison only: NOT a statistical result."""
import argparse,csv,json,math
from pathlib import Path
P=("DEADLINE_FEASIBLE_MIN_UNCERTAINTY","PRED_GREEDY","CASPER_FULL")
M=("late_dvr","p99_late_latency_ms","mean_mapper_us")
def analyze(path):
    with Path(path).open(newline="") as f: rows=list(csv.DictReader(f))
    if len(rows)!=45 or len({(x["seed"],x["scenario"],x["policy"]) for x in rows})!=45:raise ValueError("invalid 45-row grid")
    if {x["seed"] for x in rows}!={"4202202600"}:raise ValueError("seed zero required")
    scenarios=sorted({x["scenario"] for x in rows})
    if len(scenarios)!=5:raise ValueError("five scenarios required")
    lookup={(x["scenario"],x["policy"]):x for x in rows}
    out=[]
    for sc in scenarios:
        if len([k for k in lookup if k[0]==sc])!=9:raise ValueError("nine policies per scenario required")
        values={}
        for p in P:
            row=lookup.get((sc,p))
            if row is None:raise ValueError("missing comparator")
            values[p]={}
            for k in M:
                v=float(row[k])
                if not math.isfinite(v) or v<0:raise ValueError("invalid metric")
                values[p][k]=v
            if values[p]["late_dvr"]>1:raise ValueError("DVR above unity")
        diffs={k:{"new_minus_pred_greedy":values[P[0]][k]-values[P[1]][k],
                  "new_minus_casper_full":values[P[0]][k]-values[P[2]][k]} for k in M}
        out.append({"scenario":sc,"values":values,"descriptive_deltas":diffs})
    return {"status":"DESCRIPTIVE_ONLY","n_independent_seeds":1,
            "statistical_inference_permitted":False,"generalization_claim_permitted":False,
            "note":"Pilot is descriptive; mapper timing is machine-specific. No p-values or confidence intervals.","scenarios":out}
if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("--csv",required=True);ap.add_argument("--out",required=True);a=ap.parse_args()
    report=analyze(a.csv);Path(a.out).write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
    print("DEADLINE_PILOT_DESCRIPTIVE_PASS",len(report["scenarios"]))
