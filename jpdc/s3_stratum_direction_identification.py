#!/usr/bin/env python3
"""Sharp signs of affected/unaffected miss-rate changes given 90 original marginals."""
import argparse,csv,hashlib,json
from pathlib import Path
SHA="78fd57691aa3fabd7a3d84fddac28903c66b173f7165def809b7ec374685321c"
def analyze(path):
 raw=Path(path).read_bytes()
 if hashlib.sha256(raw).hexdigest()!=SHA:raise ValueError("wrong input SHA256")
 data={}
 for r in csv.DictReader(raw.decode().splitlines()):
  key=int(r["seed"]),int(r["window"])
  if key in data:raise ValueError("duplicate")
  n,a,m=[int(r[k]) for k in ("count","affected","misses")]
  if not(0<=a<=n and 0<=m<=n):raise ValueError("bad marginals")
  data[key]=(n,a,m)
 seeds=range(4202202600,4202202630)
 if set(data)!={(s,w) for s in seeds for w in range(3)}:raise ValueError("missing rows")
 def interval(v,group):
  n,a,m=v;lo=max(0,m-(n-a));hi=min(a,m)
  return (a,lo,hi) if group=="affected" else (n-a,m-hi,m-lo)
 out={"source_run":40517387076,"reference_sha256":SHA,"comparisons":{}}
 for group in ("affected","unaffected"):
  for a,b in ((0,1),(1,2),(0,2)):
   classification=[];left=[];right=[]
   for s in seeds:
    d0,l0,h0=interval(data[s,a],group);d1,l1,h1=interval(data[s,b],group)
    left.append((d0,l0,h0));right.append((d1,l1,h1))
    if not(d0 and d1):classification.append("undefined");continue
    low=l1/d1-h0/d0;high=h1/d1-l0/d0
    classification.append("decrease" if high<0 else "increase" if low>0 else "ambiguous")
   def aggregate(x):
    return tuple(sum(z[k] for z in x) for k in range(3))
   d0,l0,h0=aggregate(left);d1,l1,h1=aggregate(right)
   out["comparisons"][f"{group}_{a}_to_{b}"]={
    "pooled_delta_bounds_pp":[100*(l1/d1-h0/d0),100*(h1/d1-l0/d0)],
    "seed_decreases_identified":classification.count("decrease"),
    "seed_increases_identified":classification.count("increase"),
    "seed_ambiguous":classification.count("ambiguous"),
    "seed_undefined":classification.count("undefined")}
 return out
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("csv");p.add_argument("--out");a=p.parse_args()
 result=analyze(a.csv);doc=json.dumps(result,indent=2,sort_keys=True)+"\n"
 if a.out:Path(a.out).write_text(doc)
 print(doc)
