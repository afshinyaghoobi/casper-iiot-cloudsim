#!/usr/bin/env python3
"""Pre-specified family tests on 30 paired seeds for queue weighted vs CASPER/greedy."""
import csv,glob,json,math
from pathlib import Path
import numpy as np
from scipy.stats import t,ttest_1samp
root=Path("queue_holdout_analysis")
files=sorted(root.glob("input/**/seed_*.csv"))
assert len(files)==30, f"expected 30 distinct result files, observed {len(files)}"
policies=("CASPER_FULL","PRED_GREEDY","QUEUE_AWARE_WEIGHTED_COMPLETION")
scenarios=("S0_STATIONARY","S1_LAMBDA_X2","S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS","S4_COMPOUND")
records={}
for f in files:
    with f.open() as h: rows=list(csv.DictReader(h))
    assert len(rows)==45,(f,len(rows))
    seed=int(f.stem.split("_")[-1])
    assert 30<=seed<60
    for row in rows:
        assert int(row["seed"])==4202202600+seed
        key=(seed,row["scenario"],row["policy"])
        assert key not in records,key
        records[key]=row
assert len(records)==1350
assert all((seed,sc,policy) in records for seed in range(30,60) for sc in scenarios for policy in policies)
results=[]
for sc in scenarios:
 for baseline in ("CASPER_FULL","PRED_GREEDY"):
  for metric in ("late_dvr","p99_late_latency_ms"):
   challenger=np.array([float(records[i,sc,"QUEUE_AWARE_WEIGHTED_COMPLETION"][metric]) for i in range(30,60)])
   comparator=np.array([float(records[i,sc,baseline][metric]) for i in range(30,60)])
   assert np.all(np.isfinite(challenger)) and np.all(np.isfinite(comparator))
   difference=challenger-comparator
   mean=float(difference.mean())
   sd=float(difference.std(ddof=1))
   half=float(t.ppf(.975,29)*sd/math.sqrt(30))
   p=float(ttest_1samp(difference,0).pvalue) if sd>0 else (0. if mean else 1.)
   results.append(dict(scenario=sc,reference=baseline,metric=metric,n=30,challenger_mean=float(challenger.mean()),reference_mean=float(comparator.mean()),paired_delta=mean,ci95_low=mean-half,ci95_high=mean+half,p_unadjusted=p))
for metric in ("late_dvr","p99_late_latency_ms"):
 family=sorted((r for r in results if r["metric"]==metric),key=lambda r:r["p_unadjusted"])
 running=0
 for i,r in enumerate(family):
  running=max(running,min(1,r["p_unadjusted"]*(len(family)-i)))
  r["holm_p"]=running
root.mkdir(exist_ok=True)
(root/"queue_holdout_statistics.json").write_text(json.dumps(dict(status="PASS",records=1350,seeds=30,comparisons=results,notes=["exploratory queue-weight-2 policy, not established published SOTA", "independent holdout seed indices 30 to 59; preselected S2/S4 confirmation", "no conformal FWC for non-conformal policies; do not compare undefined FWC"]),indent=2))
with (root/"queue_holdout_statistics.csv").open("w",newline="") as f:
 w=csv.DictWriter(f,fieldnames=list(results[0]))
 w.writeheader();w.writerows(results)
print("QUEUE_HOLDOUT_ANALYSIS_PASS records=1350 holdout_seeds=30 comparisons="+str(len(results)))
for r in results:
 if r["metric"]=="late_dvr":
  print("QUEUE_HOLDOUT_RESULT",r["scenario"],r["reference"],"queue",round(r["challenger_mean"],6),"ref",round(r["reference_mean"],6),"delta",round(r["paired_delta"],6),"holm",round(r["holm_p"],7))
