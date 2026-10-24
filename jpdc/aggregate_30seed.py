#!/usr/bin/env python3
"""Analysis of frozen 30-seed JPDC comparative experiment; no retuning."""
import csv, glob, json, math
from collections import defaultdict
from pathlib import Path
import numpy as np
from scipy.stats import t as student_t

paths=sorted(glob.glob('jpdc_aggregate/input/**/seed_*.csv',recursive=True))
assert len(paths)==30, f"Expected 30 per-seed files, got {len(paths)}"
rows=[]
for p in paths:
    with open(p,newline='') as f: r=list(csv.DictReader(f))
    assert len(r)==45,(p,len(r))
    seeds={int(x['seed']) for x in r}
    assert len(seeds)==1,(p,seeds)
    assert len({(x['scenario'],x['policy']) for x in r})==45,p
    rows.extend(r)
assert len(rows)==1350
assert {int(x['seed']) for x in rows}==set(range(4_202_202_600,4_202_202_630)), sorted({int(x['seed']) for x in rows})
idx={(int(r['seed'])-4_202_202_600,r['scenario'],r['policy']):r for r in rows}
out=[]
for scenario in sorted({r['scenario'] for r in rows}):
  for competitor in ('PRED_GREEDY','DEADLINE_CAPACITY_PRESERVING'):
    diffs=[]
    for seed in range(30):
      a=float(idx[seed,scenario,'CASPER_FULL']['late_dvr'])
      b=float(idx[seed,scenario,competitor]['late_dvr'])
      diffs.append(a-b)
    vals=np.array(diffs);mean=float(vals.mean());se=float(vals.std(ddof=1)/np.sqrt(len(vals)))
    ci=float(student_t.ppf(.975,29))*se
    tt=student_t.ttest_1samp(vals,0)
    p=float(tt.pvalue) if np.isfinite(tt.pvalue) else (1.0 if np.all(vals==0) else 0.0)
    out.append(dict(scenario=scenario,comparison='CASPER_FULL minus '+competitor,n=30,
      mean_difference=mean,ci95_low=mean-ci,ci95_high=mean+ci,p_value=p,
      casper_better=int((vals<0).sum()),casper_worse=int((vals>0).sum()),
      ties=int((vals==0).sum())))
# Holm familywise across 10 comparisons
ordering=sorted(range(len(out)),key=lambda i:out[i]['p_value'])
running=0.
for k,i in enumerate(ordering):
    running=max(running,min(1.,out[i]['p_value']*(len(out)-k)))
    out[i]['holm_adjusted_p']=running
Path('jpdc_aggregate').mkdir(exist_ok=True)
with open('jpdc_aggregate/paired_results.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
Path('jpdc_aggregate/summary.json').write_text(json.dumps(dict(rows=len(rows),seeds=30,scenarios=5,policies=9,results=out),indent=2))
print('JPDC_AGGREGATION_PASS rows=1350 seeds=30 policies=9')
for x in out:
 print('JPDC_RESULT',x['scenario'],x['comparison'],f"delta={x['mean_difference']:.7f}",f"CI=[{x['ci95_low']:.7f},{x['ci95_high']:.7f}]",f"p_holm={x['holm_adjusted_p']:.6g}",'wins=',x['casper_better'],'losses=',x['casper_worse'])
