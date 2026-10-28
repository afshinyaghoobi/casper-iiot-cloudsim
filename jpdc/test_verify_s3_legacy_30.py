#!/usr/bin/env python3
"""Synthetic acceptance + negative fixtures for cross-run legacy parity."""
import csv,tempfile
from pathlib import Path
from verify_s3_legacy_30 import validate
with tempfile.TemporaryDirectory() as d:
    p=Path(d); ref=p/"source.csv";log=p/"run.log"
    with ref.open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=["seed","window","count","affected","misses"])
        w.writeheader()
        for seed in range(4202202600,4202202630):
            for win in range(3):
                w.writerow(dict(seed=seed,window=win,count=15,affected=4,misses=2))
    good="".join(f"S3_ALL seed={s} window={w} count=15 affected=4 misses=2 networkMs=0.0\n" for s in range(4202202600,4202202630) for w in range(3))
    log.write_text(good)
    assert validate(ref,str(log))==90
    print("VALID_PARITY_FIXTURE_PASS")
    for label,bad in (
        ("mutated count",good.replace("count=15","count=16",1)),
        ("missing row","".join(good.splitlines(True)[1:])),
        ("duplicate row",good+good.splitlines(True)[0]),
        ("wrong miss",good.replace("misses=2","misses=3",1)),
        ("malformed row",good.replace("count=15","count=no",1))):
        log.write_text(bad)
        try:validate(ref,str(log))
        except (ValueError,AssertionError):print("REJECT_PASS",label)
        else:raise AssertionError("failed to reject "+label)
print("LEGACY_PARITY_TESTS_PASS")
