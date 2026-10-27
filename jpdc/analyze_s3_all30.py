#!/usr/bin/env python3
"""Validate and aggregate 30 seed S3 windows across ALL candidates (not only failures)."""
import csv,glob,json,re,math
from pathlib import Path
root=Path("s3_all30_analysis")
files=sorted(root.glob("input/**/seed_*.log"))
assert len(files)==30,f"expected 30 logs, got {len(files)}"
pattern=re.compile(r"^S3_ALL seed=(\d+) window=(\d+) count=(\d+) affected=(\d+) misses=(\d+) networkMs=([0-9.eE+-]+) absQueueMs=([0-9.eE+-]+) absServiceMs=([0-9.eE+-]+) etaSum=([0-9.eE+-]+) etaSqSum=([0-9.eE+-]+)$",re.M)
rows=[]
for f in files:
    matches=pattern.findall(f.read_text())
    assert len(matches)==3,(f,len(matches))
    seed=4202202600+int(f.stem.split("_")[-1])
    assert {int(x[1]) for x in matches}=={0,1,2}
    for m in matches:
        assert int(m[0])==seed,(f,m)
        r=dict(seed=seed,window=int(m[1]),count=int(m[2]),affected=int(m[3]),misses=int(m[4]),networkMs=float(m[5]),absQueueMs=float(m[6]),absServiceMs=float(m[7]),etaSum=float(m[8]),etaSqSum=float(m[9]))
        assert 0<=r["misses"]<=r["count"] and 0<=r["affected"]<=r["count"] and r["count"]>0
        assert all(math.isfinite(v) for k,v in r.items() if k not in ("seed","window"))
        rows.append(r)
assert len(rows)==90 and {r["seed"] for r in rows}==set(range(4202202600,4202202630))
summaries=[]
for window in range(3):
    part=[r for r in rows if r["window"]==window]
    total={key:sum(r[key] for r in part) for key in ("count","affected","misses","networkMs","absQueueMs","absServiceMs","etaSum","etaSqSum")}
    n=total["count"]
    summaries.append(dict(window=window,**total,candidate_miss_rate=total["misses"]/n,affected_share=total["affected"]/n,mean_eta=total["etaSum"]/n,eta_sd=math.sqrt(max(0,total["etaSqSum"]/n-(total["etaSum"]/n)**2)),mean_network_increment_ms=total["networkMs"]/n,mean_abs_queue_error_ms=total["absQueueMs"]/n,mean_abs_service_error_ms=total["absServiceMs"]/n))
root.mkdir(exist_ok=True)
(root/"s3_all30_summary.json").write_text(json.dumps(dict(status="PASS",seeds=30,windows=summaries,notes=["candidate-level measurements, not family-wise coverage","windows are the instrumented program's post-shock partitions","descriptive means not causal contributions"]),indent=2))
with (root/"s3_all30_by_seed.csv").open("w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]))
    w.writeheader();w.writerows(rows)
print("S3_ALL30_PASS",json.dumps(summaries,sort_keys=True))
