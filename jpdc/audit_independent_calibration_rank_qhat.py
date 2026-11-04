#!/usr/bin/env python3
"""Strict cross-language original calibration rank / quantile parity.

Python generates its own 80k calibration workload and Java shuffle allocations.
"""
import argparse,csv,math
from pathlib import Path
from independent_workload_generator import calibration_mission_ranks,conformal_qhat

SIZES=(0,1,2,10,99,199,200,997)
ALPHAS=(.006,.003,.001,.01,.10)
SEED=4202202640

def validate(path):
    expected=calibration_mission_ranks(SEED,n=80000,burnin=10000)
    observed=set();quantiles=set();count_line=None;complete=0
    for raw in Path(path).open(encoding="utf-8"):
        if not raw.startswith(("JPDC_CAL_","JPDC_CALIBRATION_REFERENCE_COMPLETE")):continue
        r=next(csv.reader([raw]))
        tag=r[0]
        if tag=="JPDC_CAL_RANK":
            if len(r)!=3:raise ValueError("rank arity")
            task=int(r[1]);rank=int(r[2])
            if task not in expected or task in observed or expected[task]!=rank:
                raise ValueError(f"calibration rank mismatch/duplicate at task {task}")
            observed.add(task)
        elif tag=="JPDC_CAL_RANK_COUNT":
            if len(r)!=2 or count_line is not None:raise ValueError("bad rank count")
            count_line=int(r[1])
        elif tag=="JPDC_CAL_QHAT":
            if len(r)!=4:raise ValueError("qhat arity")
            size=int(r[1]);k=int(r[2])
            if size not in SIZES or k not in range(len(ALPHAS)) or (size,k) in quantiles:
                raise ValueError("unknown or repeated qhat fixture")
            samples=[.5+((i*37+11)%113)/100.0+(i%7)*1e-6 for i in range(size)]
            expected_value=conformal_qhat(samples,ALPHAS[k])
            got=float(r[3])
            if math.isinf(expected_value):
                if not math.isinf(got) or got<0:raise ValueError(f"infinity qhat mismatch {size,k}")
            elif not math.isfinite(got) or not math.isclose(got,expected_value,abs_tol=1e-12,rel_tol=0):
                raise ValueError(f"qhat mismatch at {size,k}: got {got} expected {expected_value}")
            quantiles.add((size,k))
        elif tag=="JPDC_CALIBRATION_REFERENCE_COMPLETE":
            if len(r)!=1:raise ValueError("end marker malformed")
            complete+=1
        else:raise ValueError("unexpected calibration reference record")
    if observed!=set(expected) or len(expected)<200:
        raise ValueError(f"missing calibration ranks: observed {len(observed)}, expected {len(expected)}")
    if count_line!=len(expected) or quantiles!={(n,k) for n in SIZES for k in range(len(ALPHAS))} or complete!=1:
        raise ValueError(f"reference incomplete: count {count_line}, qhat {len(quantiles)}, end {complete}")
    return len(expected),len(quantiles)

if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("--java-reference",required=True)
    args=ap.parse_args()
    n,m=validate(args.java_reference)
    print(f"PASS original 80000-calibration-task cohort, {n} independent rank labels, zero differences")
    print(f"PASS {m} original frozen conformal qhat fixtures including infinity edge cases")
    print("JPDC_INDEPENDENT_CALIBRATION_RANK_QHAT_PARITY_PASS")
