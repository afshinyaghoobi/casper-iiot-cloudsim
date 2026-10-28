#!/usr/bin/env python3
"""Fail-closed compare legacy S3_ALL counters against original 30-seed CSV."""
import argparse,csv,glob,re
from pathlib import Path
def validate(reference,pattern):
    original={}
    for row in csv.DictReader(Path(reference).open(newline="")):
        k=(int(row["seed"]),int(row["window"]))
        if k in original: raise ValueError("duplicate original")
        original[k]=tuple(int(row[c]) for c in ("count","affected","misses"))
    assert len(original)==90
    logs=glob.glob(pattern,recursive=True)
    if not logs: raise ValueError("missing logs")
    observed={}
    regex=re.compile(r'^S3_ALL seed=(\d+) window=(\d+) count=(\d+) affected=(\d+) misses=(\d+)\b')
    for f in logs:
        for line in Path(f).read_text().splitlines():
            if not line.startswith("S3_ALL "):continue
            m=regex.match(line)
            if not m:raise ValueError(f"malformed legacy {f}")
            nums=list(map(int,m.groups()));key=tuple(nums[:2])
            if key in observed:raise ValueError(f"duplicate legacy {key}")
            observed[key]=tuple(nums[2:])
    if observed!=original:
        missing=set(original)-set(observed)
        bad=[k for k in observed.keys()&original.keys() if observed[k]!=original[k]]
        raise ValueError(f"legacy mismatch missing={sorted(missing)[:5]} mismatched={sorted(bad)[:5]}")
    return len(observed)
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--reference",required=True);p.add_argument("--logs",required=True)
    a=p.parse_args()
    print("LEGACY_S3_ALL_30_PARITY_PASS",validate(a.reference,a.logs))
