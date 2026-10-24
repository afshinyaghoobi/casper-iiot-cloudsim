#!/usr/bin/env python3
import csv, glob, io, json, math, zipfile
from pathlib import Path
from scipy.stats import ttest_1samp,t

root=Path("jpdc_k_analysis")
files=sorted(root.glob("input/**/seed_*.csv"))
assert len(files)==30, f"30 files required, got {len(files)}"
with zipfile.ZipFile(root/"e46-publication-results.zip") as z:
    frozen={}
    for i in range(30):
        data=list(csv.DictReader(io.StringIO(z.read(f"raw/e46_seed_{i}.csv").decode())))
        assert len(data)==40,(i,len(data))
        for row in data:frozen[(int(row["seed"]),row["scenario"],row["policy"])]=row
new={}
for path in files:
    with path.open() as f: data=list(csv.DictReader(f))
    assert len(data)==40,(path,len(data))
    for row in data:
        key=(int(row["seed"]),row["scenario"],row["policy"])
        assert key not in new,key
        new[key]=row
assert len(new)==1200 and set(new)==set(frozen)
metrics=["late_dvr","late_fwc","late_air","p99_late_latency_ms"]
results=[]
for scenario in sorted({x[1] for x in new}):
    for metric in metrics:
        diff=[]
        for seed in range(4202202600,4202202630):
            key=(seed,scenario,"CASPER_FULL")
            diff.append(float(new[key][metric])-float(frozen[key][metric]))
        mean=sum(diff)/len(diff)
        sd=(sum((x-mean)**2 for x in diff)/(len(diff)-1))**.5
        half=float(t.ppf(.975,29))*sd/(30**.5)
        p=1.0 if sd==0 and mean==0 else (0.0 if sd==0 else float(ttest_1samp(diff,0).pvalue))
        results.append(dict(scenario=scenario,metric=metric,n=30,mean_k1_minus_k3=mean,ci95_low=mean-half,ci95_high=mean+half,p_unadjusted=p,changed_seeds=sum(abs(x)>1e-10 for x in diff)))
# Adjust within DVR comparisons across 5 scenarios
subset=[r for r in results if r["metric"]=="late_dvr"]
ordering=sorted(subset,key=lambda x:x["p_unadjusted"])
running=0.0
for i,r in enumerate(ordering):
    running=max(running,min(1.,r["p_unadjusted"]*(len(ordering)-i)))
    r["p_holm_within_dvr"]=running
root.mkdir(exist_ok=True)
(root/"topk30_summary.json").write_text(json.dumps(dict(
    gate="PASS",verified_rows=1200,n_seeds=30,reference="E4.6 frozen K=3",
    comparison="deployment-only K=1 versus K=3; calibration unchanged",
    warning="FWC families differ by K and must not be interpreted as like-for-like coverage",results=results),indent=2))
print("TOPK30_ANALYSIS_PASS rows=1200 seeds=30")
for r in results:
    print("TOPK30_RESULT",r["scenario"],r["metric"],f"delta={r['mean_k1_minus_k3']:.9f}",f"CI=[{r['ci95_low']:.9f},{r['ci95_high']:.9f}]",f"changed={r['changed_seeds']}",f"p={r.get('p_holm_within_dvr','descriptive')}")
