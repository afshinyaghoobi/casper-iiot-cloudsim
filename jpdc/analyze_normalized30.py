#!/usr/bin/env python3
"""Matched normalized topology scaling vs immutable E4.6; network capacity remains variable."""
import csv,glob,io,json,zipfile
from pathlib import Path
import numpy as np
from scipy.stats import t,ttest_1samp
root=Path("normalized_analysis")
files=list(root.glob("input/**/norm*_seed*.csv"))
assert len(files)==60, f"expected 60 CSV artifacts, got {len(files)}"
data={}
for f in files:
    n=int(f.name.split("_")[0].replace("norm",""))
    assert n in (14,28)
    with f.open() as handle: rows=list(csv.DictReader(handle))
    assert len(rows)==40, (f,len(rows))
    for row in rows:
        key=(n,int(row["seed"]),row["scenario"],row["policy"])
        assert key not in data,key
        data[key]=row
assert len(data)==2400
with zipfile.ZipFile(root/"e46-publication-results.zip") as z:
    frozen={}
    for i in range(30):
        rows=list(csv.DictReader(io.StringIO(z.read(f"raw/e46_seed_{i}.csv").decode())))
        assert len(rows)==40
        for row in rows:
            key=(int(row["seed"]),row["scenario"],row["policy"])
            assert key not in frozen
            frozen[key]=row
assert len(frozen)==1200
seeds=range(4202202600,4202202630)
scenarios=sorted(set(k[1] for k in frozen))
policies=sorted(set(k[2] for k in frozen))
assert len(scenarios)==5 and len(policies)==8
assert {(n,s,sc,p) for n in (14,28) for s in seeds for sc in scenarios for p in policies}==set(data)
metrics=("late_dvr","late_fwc","p99_late_latency_ms")
results=[]
for sc in scenarios:
 for policy in ("CASPER_FULL","PRED_GREEDY"):
  for metric in metrics:
   base=np.array([float(frozen[s,sc,policy][metric]) for s in seeds])
   for nodes in (14,28):
    scaled=np.array([float(data[nodes,s,sc,policy][metric]) for s in seeds])
    delta=scaled-base
    sd=float(delta.std(ddof=1));avg=float(delta.mean())
    half=float(t.ppf(.975,29)*sd/np.sqrt(30))
    p=float(ttest_1samp(delta,0).pvalue) if sd else (1. if avg==0 else 0.)
    results.append(dict(scenario=sc,policy=policy,metric=metric,nodes=nodes,n=30,scaled_mean=float(scaled.mean()),reference21_mean=float(base.mean()),paired_delta=avg,ci95_low=avg-half,ci95_high=avg+half,p_unadjusted=p))
for metric in metrics:
 family=sorted([x for x in results if x["metric"]==metric],key=lambda x:x["p_unadjusted"])
 latest=0.
 for idx,r in enumerate(family):
  latest=max(latest,min(1.,r["p_unadjusted"]*(len(family)-idx)))
  r["holm_p"]=latest
root.mkdir(exist_ok=True)
(root/"normalized30_results.json").write_text(json.dumps(dict(status="PASS",records=2400,frozen_records=1200,seed_count=30,experimental_caveat="Per-node expected compute scaled by 21/N; bandwidth, topology, stochastic realized capacity and workload-to-network ratio are not normalized.",comparisons=results),indent=2))
with (root/"topology30_results.csv").open("w",newline="") as f:
 w=csv.DictWriter(f,fieldnames=list(results[0]))
 w.writeheader();w.writerows(results)
print("NORMALIZED30_ANALYSIS_PASS rows=2400 frozen=1200 comparisons=",len(results))
for r in results:
 if r["policy"]=="CASPER_FULL" and r["metric"] in ("late_dvr","late_fwc"):
  print("NORMALIZED30_RESULT",r["scenario"],r["metric"],r["nodes"],"mean",round(r["scaled_mean"],6),"base",round(r["reference21_mean"],6),"delta",round(r["paired_delta"],6),"holm",round(r["holm_p"],7))
