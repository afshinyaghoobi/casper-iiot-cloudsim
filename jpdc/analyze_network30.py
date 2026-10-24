#!/usr/bin/env python3
"""Paired network severity robustness, fixed baseline E4.6, prespecified controls."""
import csv,glob,io,json,math,zipfile
from pathlib import Path
import numpy as np
from scipy.stats import ttest_1samp,t
root=Path("jpdc_network_analysis")
files=list(root.glob("input/**/net*_seed*.csv"))
assert len(files)==60,("network archive count",len(files))
data={}
for f in files:
    fraction=int(f.name.split('_')[0][3:])
    with f.open() as z: rows=list(csv.DictReader(z))
    assert len(rows)==40,(f,len(rows))
    for row in rows:
        key=(fraction,int(row['seed']),row['scenario'],row['policy'])
        assert key not in data,key
        data[key]=row
assert len(data)==2400
seeds=list(range(4202202600,4202202630))
scenarios=sorted({x[2] for x in data})
policies=sorted({x[3] for x in data})
assert len(scenarios)==5 and len(policies)==8
with zipfile.ZipFile(root/"e46-publication-results.zip") as z:
    frozen={}
    for idx in range(30):
        for row in csv.DictReader(io.StringIO(z.read(f"raw/e46_seed_{idx}.csv").decode())):
            frozen[int(row['seed']),row['scenario'],row['policy']]=row
assert len(frozen)==1200
# S0-S2 are unchanged by the exploratory severity patch. Probe timing is volatile.
ignored={'mean_mapper_us'}
for retention in (25,75):
    for seed in seeds:
        for scenario in scenarios[:3]:
            for policy in policies:
                key=(seed,scenario,policy)
                original=frozen[key];changed=data[retention,*key]
                for column,v in original.items():
                    if column in ignored:continue
                    new=changed[column]
                    try:
                        a,b=float(v),float(new)
                        if math.isnan(a) and math.isnan(b):continue
                        assert math.isclose(a,b,rel_tol=1e-9,abs_tol=1e-10),(retention,key,column,v,new)
                    except ValueError:assert v==new,(retention,key,column,v,new)
results=[]
for scenario in scenarios[3:]:
 for metric in ('late_dvr','late_fwc','late_air','p99_late_latency_ms'):
  for retention in (25,75):
    x=np.array([float(data[retention,s,scenario,'CASPER_FULL'][metric]) for s in seeds])
    y=np.array([float(frozen[s,scenario,'CASPER_FULL'][metric]) for s in seeds])
    delta=x-y;mean=float(delta.mean());sd=float(delta.std(ddof=1))
    half=float(t.ppf(.975,29))*sd/np.sqrt(30)
    p=float(ttest_1samp(delta,0).pvalue) if sd>0 else (1. if mean==0 else 0.)
    results.append(dict(scenario=scenario,metric=metric,retained_percent=retention,reference_retained_percent=50,n=30,mean_at_retention=float(x.mean()),reference_mean=float(y.mean()),mean_delta=mean,ci95_low=mean-half,ci95_high=mean+half,p_unadjusted=p))
for metric in ('late_dvr','late_fwc','late_air','p99_late_latency_ms'):
 family=sorted((r for r in results if r['metric']==metric),key=lambda r:r['p_unadjusted'])
 latest=0.
 for i,r in enumerate(family):
  latest=max(latest,min(1.,r['p_unadjusted']*(len(family)-i)))
  r['holm_p']=latest
root.mkdir(exist_ok=True)
(root/"network30_results.json").write_text(json.dumps({'status':'PASS','records':2400,'seeds':30,'invariance_non_network_scenarios':'PASS','results':results},indent=2))
with (root/"network30_results.csv").open("w",newline="") as f:
 w=csv.DictWriter(f,fieldnames=list(results[0]));w.writeheader();w.writerows(results)
print("NETWORK30_ANALYSIS_PASS rows=2400 invariant_scenarios=PASS")
for r in results:
 print("NETWORK30_RESULT",r['scenario'],r['metric'],r['retained_percent'],f"mean={r['mean_at_retention']:.6f}",f"reference={r['reference_mean']:.6f}",f"delta={r['mean_delta']:.6f}",f"holm={r['holm_p']:.7g}")
