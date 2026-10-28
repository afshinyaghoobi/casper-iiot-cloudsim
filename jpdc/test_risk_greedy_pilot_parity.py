#!/usr/bin/env python3
"""Positive and mutation-negative fixtures for risk greedy scientific parity."""
import csv, tempfile
from pathlib import Path
from verify_risk_greedy_pilot_parity import audit, SCENARIOS, NEW
P=["CLOUD_ONLY","EDGE_FIRST","PRED_GREEDY","GLOBAL_CP","RANKED_CP_STATIC","CASPER_ADAPT_NO_HEALTH","CASPER_HEALTH_STATIC","CASPER_FULL"]
def write(path,rows):
    with path.open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=["seed","scenario","policy","late_dvr","p99_late_latency_ms","mean_mapper_us"])
        w.writeheader();w.writerows(rows)
with tempfile.TemporaryDirectory() as tmp:
    before=Path(tmp)/"before.csv";after=Path(tmp)/"after.csv"
    base=[dict(seed="4202202600",scenario=sc,policy=p,late_dvr="0.01",p99_late_latency_ms="22",mean_mapper_us="4") for sc in sorted(SCENARIOS) for p in P]
    extra=[dict(seed="4202202600",scenario=sc,policy=NEW,late_dvr="0.02",p99_late_latency_ms="23",mean_mapper_us="5") for sc in sorted(SCENARIOS)]
    write(before,base)
    write(after,base+extra)
    assert audit(before,after)==(40,45)
    print("PASS valid 40-to-45 fixture")
    changed=[dict(x) for x in base+extra]
    changed[0]["mean_mapper_us"]="99"
    write(after,changed)
    assert audit(before,after)==(40,45)
    print("PASS ignores non-deterministic timing only")
    for label,records in [
        ("scientific drift",[dict(x) for x in base+extra]),
        ("missing old row",base[1:]+extra),
        ("duplicate new row",base+extra+extra[:1]),
        ("missing new row",base+extra[:-1])
    ]:
        if label=="scientific drift":records[0]["late_dvr"]="0.5"
        write(after,records)
        try:audit(before,after)
        except ValueError:print("PASS rejected",label)
        else:raise AssertionError("accepted "+label)
print("RISK_GREEDY_PARITY_MUTATIONS_PASS")
