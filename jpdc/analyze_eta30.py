#!/usr/bin/env python3
"""Predeclared eta sensitivity analysis; fails on missing or mismatched archives."""
from collections import defaultdict
from pathlib import Path
import csv,glob,io,json,math,zipfile
import numpy as np
from scipy.stats import ttest_1samp,t
base=Path("jpdc_eta_analysis")
files=list(base.glob("input/**/cap*_seed*.csv"))
assert len(files)==90, f"Expected 90 CSVs, found {len(files)}"
new={}
for f in files:
    cap=int(f.name.split('_')[0][3:])
    with f.open(newline='') as stream:
        rows=list(csv.DictReader(stream))
    assert len(rows)==40,(str(f),len(rows))
    for row in rows:
        key=(cap,int(row['seed']),row['scenario'],row['policy'])
        assert key not in new,key
        new[key]=row
assert len(new)==3600
seeds=set(range(4202202600,4202202630))
scenarios={key[2] for key in new}
policies={key[3] for key in new}
assert {k[1] for k in new}==seeds
assert len(scenarios)==5 and len(policies)==8
for cap in (1,2,3):
    assert sum(k[0]==cap for k in new)==1200
with zipfile.ZipFile(base/"e46-publication-results.zip") as z:
    frozen={}
    for idx in range(30):
        for row in csv.DictReader(io.StringIO(z.read(f"raw/e46_seed_{idx}.csv").decode())):
            frozen[(int(row['seed']),row['scenario'],row['policy'])]=row
# timing and wall-clock performance measurement are non-deterministic.
ignored={"mean_mapper_us"}
mismatch=[]
for (seed,scenario,policy),ref in frozen.items():
    row=new[3,seed,scenario,policy]
    for metric in ref:
        if metric in ignored:continue
        a,b=ref[metric].strip(),row[metric].strip()
        if a==b:continue
        try:
            fa,fb=float(a),float(b)
            if math.isnan(fa) and math.isnan(fb):continue
            if math.isclose(fa,fb,abs_tol=1e-10,rel_tol=1e-9):continue
        except ValueError:pass
        mismatch.append((seed,scenario,policy,metric,a,b))
assert not mismatch, f"Cap3 frozen reproducibility mismatch, first mismatches={mismatch[:5]}"
results=[]
for scenario in sorted(scenarios):
 for metric in ["late_dvr","late_fwc","late_eta"]:
    for cap in (1,2):
        a=np.array([float(new[cap,seed,scenario,"CASPER_FULL"][metric]) for seed in sorted(seeds)])
        b=np.array([float(new[3,seed,scenario,"CASPER_FULL"][metric]) for seed in sorted(seeds)])
        diff=a-b
        mean=float(diff.mean());sd=float(diff.std(ddof=1))
        half=float(t.ppf(.975,29))*sd/math.sqrt(30)
        p=float(ttest_1samp(diff,0).pvalue) if sd>0 else (1.0 if mean==0 else 0.0)
        results.append(dict(scenario=scenario,metric=metric,contrast=f"cap{cap}-cap3",n=30,
          mean_cap=float(a.mean()),mean_cap3=float(b.mean()),mean_diff=mean,
          ci95_low=mean-half,ci95_high=mean+half,p_unadjusted=p))
# Holm within each prespecified family of 10 comparisons per endpoint
for metric in ["late_dvr","late_fwc","late_eta"]:
    family=sorted((x for x in results if x["metric"]==metric),key=lambda x:x["p_unadjusted"])
    adj=0.
    for i,item in enumerate(family):
        adj=max(adj,min(1.,item["p_unadjusted"]*(len(family)-i)))
        item["holm_p"]=adj
report={"status":"PASS","rows":3600,"frozen_cap3_parity":"PASS","scientific_seed_count":30,
 "interpretation":"FWC is not sufficient to establish time-uniform or conditional coverage.",
 "statistics":"paired t confidence intervals, Holm correction across 10 comparisons within each endpoint; exploratory",
 "results":results}
base.mkdir(exist_ok=True)
(base/"eta30_report.json").write_text(json.dumps(report,indent=2))
with (base/"eta30_comparisons.csv").open("w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(results[0]))
    w.writeheader();w.writerows(results)
print("ETA30_VALIDATED_PASS rows=3600 cap3_parity=PASS comparisons=30")
for x in results:
 print("ETA30_RESULT",x["scenario"],x["metric"],x["contrast"],
       "delta",round(x["mean_diff"],8),"holm",round(x["holm_p"],8))
