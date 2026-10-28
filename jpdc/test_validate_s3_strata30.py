#!/usr/bin/env python3
"""Synthetic contract test of the S3 30-seed fail-closed validator."""
import csv,importlib.util,tempfile
from pathlib import Path
spec=importlib.util.spec_from_file_location("s3_validator",Path(__file__).with_name("validate_s3_strata30.py"))
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
def rejects(ref,log,name):
    try: v.parse([str(log)],str(ref))
    except ValueError:
        print("PASS expected reject:",name);return
    raise AssertionError("accepted invalid input: "+name)
with tempfile.TemporaryDirectory() as directory:
    ref=Path(directory)/"reference.csv";log=Path(directory)/"strata.log"
    with ref.open("w",newline="") as f:
        wr=csv.DictWriter(f,fieldnames=["seed","window","count","affected","misses"]);wr.writeheader()
        for seed in range(4202202600,4202202630):
            for w in range(3): wr.writerow(dict(seed=seed,window=w,count=10,affected=4,misses=3))
    with log.open("w") as f:
        for seed in range(4202202600,4202202630):
            for w in range(3):f.write(f"S3_STRATA seed={seed} window={w} unaffectedN=6 unaffectedMiss=1 affectedN=4 affectedMiss=2\n")
    good=v.parse([str(log)],str(ref))
    assert len(good)==90
    report=v.report(good)
    assert report["seeds"]==30
    for w in range(3):
        assert abs(report["windows"][w]["total_rate"]-0.3)<1e-12
        assert abs(report["standardized_rates_at_window0_mix"][w]-0.3)<1e-12
    print("PASS valid fixture, counts and standardization")
    base=log.read_text()
    cases=[
        ("duplicate seed-window",base+base.splitlines(True)[0]),
        ("missing seed-window","".join(base.splitlines(True)[1:])),
        ("miss exceeds candidates",base.replace("unaffectedMiss=1","unaffectedMiss=7",1)),
        ("affected count mismatch",base.replace("affectedN=4","affectedN=3",1)),
        ("miss total mismatch",base.replace("affectedMiss=2","affectedMiss=3",1)),
        ("unexpected window",base.replace("window=0","window=3",1)),
        ("malformed row",base.replace("S3_STRATA seed=","S3_STRATA malformed=",1))
    ]
    for label,mutated in cases:
        log.write_text(mutated);rejects(ref,log,label)
print("VALIDATOR_CONTRACT_TEST_PASS")
