#!/usr/bin/env python3
"""Fail-closed validator for S3 all-candidate stratified log output.
Validates 30 original seeds, every window, original published counts and
affected/unaffected partitions. No re-evaluation of frozen E4.6.
"""
import argparse,csv,glob,json,re
from pathlib import Path

def parse(logs, reference):
    source={}
    for r in csv.DictReader(Path(reference).open(newline="")):
        key=(int(r["seed"]),int(r["window"]))
        if key in source: raise ValueError("duplicate reference row")
        source[key]=tuple(int(r[k]) for k in ("count","affected","misses"))
    if len(source)!=90 or set(source)!={(4202202600+i,w) for i in range(30) for w in range(3)}:
        raise ValueError("reference seed/window set invalid")
    pat=re.compile(r'^S3_STRATA seed=(\d+) window=(\d+) unaffectedN=(\d+) unaffectedMiss=(\d+) affectedN=(\d+) affectedMiss=(\d+)$')
    records={}
    for filename in logs:
        for line in Path(filename).read_text().splitlines():
            if not line.startswith("S3_STRATA "): continue
            m=pat.fullmatch(line.strip())
            if m is None: raise ValueError(f"invalid stratum row: {filename}: {line}")
            seed,win,u,um,a,am=map(int,m.groups())
            key=(seed,win)
            if key in records: raise ValueError(f"duplicate {key}")
            if key not in source: raise ValueError(f"unexpected {key}")
            n,affected,miss=source[key]
            if not (0<=um<=u and 0<=am<=a and u+a==n and a==affected and um+am==miss):
                raise ValueError(f"mismatch {key}: {(u,um,a,am)} reference={source[key]}")
            records[key]=dict(seed=seed,window=win,unaffectedN=u,unaffectedMiss=um,affectedN=a,affectedMiss=am)
    if set(records)!=set(source):
        raise ValueError(f"missing {sorted(set(source)-set(records))[:8]}")
    return [records[k] for k in sorted(records)]

def report(rows):
    windows={}
    for w in range(3):
        p=[x for x in rows if x["window"]==w]
        a=sum(x["affectedN"] for x in p)
        u=sum(x["unaffectedN"] for x in p)
        am=sum(x["affectedMiss"] for x in p)
        um=sum(x["unaffectedMiss"] for x in p)
        if not(a and u): raise ValueError("empty stratum")
        windows[w]=dict(affectedN=a,affectedMiss=am,unaffectedN=u,unaffectedMiss=um,
                        affected_rate=am/a,unaffected_rate=um/u,total_rate=(am+um)/(a+u))
    # Direct standardization using fixed overall affected share from reference W0.
    weight=windows[0]["affectedN"]/(windows[0]["affectedN"]+windows[0]["unaffectedN"])
    std={w:weight*windows[w]["affected_rate"]+(1-weight)*windows[w]["unaffected_rate"] for w in range(3)}
    return {"status":"PASS","seeds":30,"windows":windows,
            "reference_affected_weight_window0":weight,
            "standardized_rates_at_window0_mix":std,
            "note":"Descriptive standardization only; no causal adjustment, significance or coverage claim."}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--logs",required=True,help="glob of seed logs")
    p.add_argument("--reference",required=True)
    p.add_argument("--out",required=True)
    args=p.parse_args()
    files=sorted(glob.glob(args.logs,recursive=True))
    if not files: raise ValueError("no logs")
    rows=parse(files,args.reference)
    result=report(rows)
    Path(args.out).parent.mkdir(parents=True,exist_ok=True)
    Path(args.out).write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("S3_STRATA30_VALIDATION_PASS",json.dumps(result,sort_keys=True))

if __name__=="__main__": main()
