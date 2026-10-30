#!/usr/bin/env python3
"""Cross-check 45-row CloudSim CSV and 24-node dispatch log, fail closed."""
import argparse
import csv
from pathlib import Path
from verify_first_idle_assignment_log import audit

def check(csv_path,log_path):
    placements=audit(Path(log_path).read_text())
    with Path(csv_path).open(newline="") as file:
        reader=csv.DictReader(file)
        if not reader.fieldnames or not {"seed","scenario","policy","tasks","cloudsim_completion"}<=set(reader.fieldnames):
            raise ValueError("missing required CSV fields")
        rows=list(reader)
    if len(rows)!=len(placements):raise ValueError("CSV/log row count mismatch")
    observed=set()
    for row in rows:
        key=(row["scenario"],row["policy"])
        if key in observed or key not in placements:raise ValueError(f"duplicate or unknown CSV key {key}")
        observed.add(key)
        if row["seed"]!="4202202600":raise ValueError("CSV seed mismatch")
        if int(row["tasks"])!=sum(placements[key]):raise ValueError(f"assignment total mismatch {key}")
        if float(row["cloudsim_completion"])!=1.0:raise ValueError(f"incomplete CloudSim {key}")
    if observed!=set(placements):raise ValueError("unmatched assignment lines")
    return len(rows)
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--csv",required=True);p.add_argument("--log",required=True);a=p.parse_args()
    print("FIRST_IDLE_CROSS_ARTIFACT_PASS",check(a.csv,a.log))
