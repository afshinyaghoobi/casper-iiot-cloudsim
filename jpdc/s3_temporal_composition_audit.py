#!/usr/bin/env python3
"""S3 seed-window composition diagnostics; ecological, not causal."""
import csv, json, math, hashlib, sys
from pathlib import Path
p=Path(sys.argv[1]); raw=p.read_bytes()
rows=list(csv.DictReader(raw.decode().splitlines()))
assert len(rows)==90
x={}
for r in rows:
 s,w=int(r['seed']),int(r['window'])
 assert (s,w) not in x and 0<=w<=2
 n=int(r['count']);assert n>0
 x[s,w]={'miss':int(r['misses'])/n,'affected':int(r['affected'])/n,'eta':float(r['etaSum'])/n,'network':float(r['networkMs'])/n,'queue':float(r['absQueueMs'])/n,'service':float(r['absServiceMs'])/n}
seeds=sorted({s for s,w in x})
assert seeds==list(range(4202202600,4202202630)) and len(x)==90
out={'input_sha256':hashlib.sha256(raw).hexdigest(),'source_run':40517387076,'n_seeds':30,'windows_task_index':['[10000,16667)','[16667,23334)','[23334,30000)'],'comparison':{}}
for a,b in [(0,1),(1,2),(0,2)]:
 ds={k:[x[s,b][k]-x[s,a][k] for s in seeds] for k in ['miss','affected','eta','network','queue','service']}
 def pearson(v,z):
  mv=sum(v)/len(v);mz=sum(z)/len(z)
  cov=sum((aa-mv)*(bb-mz) for aa,bb in zip(v,z))
  den=math.sqrt(sum((aa-mv)**2 for aa in v)*sum((bb-mz)**2 for bb in z))
  return cov/den if den else None
 out['comparison'][f'{a}_to_{b}']={'mean_delta':{k:sum(v)/30 for k,v in ds.items()},'pearson_delta_miss_vs':{k:pearson(ds['miss'],ds[k]) for k in ds if k!='miss'},'eta_increase_seeds':sum(v>1e-10 for v in ds['eta']),'eta_decrease_seeds':sum(v< -1e-10 for v in ds['eta']),'eta_same_seeds':sum(abs(v)<=1e-10 for v in ds['eta']),'miss_decrease_while_eta_nonincrease':sum(ds['miss'][i]<0 and ds['eta'][i]<=1e-10 for i in range(30))}
for w in range(3):
 vals=[x[s,w] for s in seeds]
 out.setdefault('window',{})[str(w)]={'mean_eta_across_seeds':sum(v['eta'] for v in vals)/30,'seeds_eta_exactly_3':sum(abs(v['eta']-3)<1e-10 for v in vals),'mean_affected_share':sum(v['affected'] for v in vals)/30,'mean_miss_rate':sum(v['miss'] for v in vals)/30}
out['limitations']=['Aggregated seed-window ecological correlations do not identify candidate-level causal relationships.','Chronological boundaries are task-index partitions, not equal candidate-size windows.','Candidate families and composition can change between windows.']
print(json.dumps(out,indent=2,sort_keys=True))
