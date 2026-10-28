#!/usr/bin/env python3
"""Sharp two-stratum composition-only sensitivity bound (not causal/statistical)."""
import csv,json,hashlib,sys
from pathlib import Path
raw=Path(sys.argv[1]).read_bytes()
rows=list(csv.DictReader(raw.decode().splitlines()))
d={}
for r in rows:
 s,w=int(r["seed"]),int(r["window"])
 n,a,m=[int(r[k]) for k in ("count","affected","misses")]
 assert n>0 and 0<=a<=n and 0<=m<=n and (s,w) not in d
 d[s,w]=(n,a,m)
seeds=list(range(4202202600,4202202630))
assert len(d)==90 and set(d)=={(s,w) for s in seeds for w in range(3)}
def rates(s,w):
 n,a,m=d[s,w];return a/n,m/n
out={"input_sha256":hashlib.sha256(raw).hexdigest(),"source_run":40517387076,"bounds":{},"assumption":"Within-stratum miss risks are constant between compared windows; for pooled analysis also common across seeds."}
for a,b in [(0,1),(1,2),(0,2)]:
 da=[];dm=[]
 for s in seeds:
  qa,ma=rates(s,a);qb,mb=rates(s,b)
  da.append(qb-qa);dm.append(mb-ma)
 n0,A0,M0=[sum(d[s,a][j] for s in seeds) for j in range(3)]
 n1,A1,M1=[sum(d[s,b][j] for s in seeds) for j in range(3)]
 dq=A1/n1-A0/n0;dr=M1/n1-M0/n0
 out["bounds"][f"{a}_to_{b}"]={"pooled_delta_miss_pp":dr*100,"pooled_delta_affected_share_pp":dq*100,"max_composition_only_magnitude_pp":abs(dq)*100,"excess_magnitude_pp":max(0,abs(dr)-abs(dq))*100,"seed_pairs_exceeding_bound":sum(abs(m)>abs(q)+1e-12 for m,q in zip(dm,da)),"mean_seed_delta_miss_pp":100*sum(dm)/30,"mean_seed_delta_share_pp":100*sum(da)/30}
print(json.dumps(out,indent=2,sort_keys=True))
