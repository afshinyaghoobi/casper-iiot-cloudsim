#!/usr/bin/env python3
"""Exploratory exhaustive threshold sensitivity for frozen ORIGINAL A2 job-level data.

Input: immutable-source-verified 288-row original A2 per-job completion CSV,
reconstructed from native Java original log by audit_simpat_a2_per_job_completion_margins.py.
NOT a new simulator experiment, new preregistered hypothesis, model improvement,
statistical sample or physical IoT validation. 0..250ms/5ms defined for this
retrospective sweep before the GitHub workflow that computes final results.
"""
import argparse, csv, hashlib, json
from pathlib import Path
from collections import Counter

GRID=list(range(0,251,5))
TOL=1e-8
def main(data_path,outdir):
    with data_path.open(newline="") as f:rows=list(csv.DictReader(f))
    assert len(rows)==288 and len({r["case"] for r in rows})==24
    assert all(r["case"].endswith(("_P1","_P2")) for r in rows)
    groups={p:[r for r in rows if r["case"].endswith(f"_P{p}")] for p in (1,2)}
    assert len(groups[1])==144 and len(groups[2])==144
    assert all(len([r for r in rows if r["case"]==n])==12 for n in {r["case"] for r in rows})
    def signed_end_to_end(r):
        a=float(r["submit_ms"]);n=float(r["native_finish_ms"])-a;f=float(r["fifo_finish_ms"])-a
        return n,f
    def miss(t,finish_rel):
        return finish_rel>t+TOL
    def discord(rows,t):
        return sum(miss(t,n)!=miss(t,f) for r in rows for n,f in [signed_end_to_end(r)])
    out=[]
    for t in GRID:
        c1=discord(groups[1],t);c2=discord(groups[2],t)
        out.append({"threshold_ms":t,"one_pe_disagreements":c1,
                    "two_pe_disagreements":c2,"total_disagreements":c1+c2,
                    "two_minus_one":c2-c1})
    assert [x for x in out if x["threshold_ms"]==25][0]["total_disagreements"]==86
    assert [x for x in out if x["threshold_ms"]==50][0]["total_disagreements"]==107
    assert discord(groups[1],25)==27 and discord(groups[2],25)==59
    assert discord(groups[1],50)==49 and discord(groups[2],50)==58
    # Independent geometry: for each job, threshold is inside the interval
    # between both completion-offset values, with a consistent > tolerance.
    for t in GRID:
        via_intervals=0
        for r in rows:
            n,f=signed_end_to_end(r)
            via_intervals+=int(min(n,f)-TOL<=t<max(n,f)-TOL)
        assert via_intervals==next(x["total_disagreements"] for x in out if x["threshold_ms"]==t)
    sign=Counter(("positive" if x["two_minus_one"]>0 else
                  "negative" if x["two_minus_one"]<0 else "tie") for x in out)
    peak=max(x["total_disagreements"] for x in out)
    peak_t=[x["threshold_ms"] for x in out if x["total_disagreements"]==peak]
    examples=[next(x for x in out if x["threshold_ms"]==t) for t in (0,25,50,55,75,100,250)]
    outdir.mkdir(parents=True,exist_ok=True)
    with (outdir/"a2_disagreement_threshold_sweep_0_250_step5.csv").open("w",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=list(out[0]));writer.writeheader();writer.writerows(out)
    result={
      "status":"PASS_ORIGINAL_SOURCE_VERIFIED_POSTHOC_THRESHOLD_SWEEP",
      "analysis_design":"EXPLORATORY_POSTHOC_FIXED_0_TO_250_MS_STEP_5",
      "threshold_grid_n":len(GRID),"threshold_min_ms":0,"threshold_max_ms":250,"step_ms":5,
      "jobs":288,"cases":24,"one_pe_jobs":144,"two_pe_jobs":144,
      "two_pe_minus_one_pe_sign_counts":dict(sign),
      "peak_total_disagreement_count":peak,"peak_thresholds_ms":peak_t,
      "illustrative_fixed_thresholds":examples,
      "input_per_job_csv_sha256":hashlib.sha256(data_path.read_bytes()).hexdigest(),
      "strict_miss_tol_ms":TOL,
      "model_comparison_not_observed_iot_error":True,
      "not_preregistered":True,"new_java_simulations":False,
      "general_causal_significance_claim":False,
      "original_30k_parity":"FAIL","stage65_safety":"FAIL"}
    (outdir/"a2_disagreement_threshold_sweep_audit.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--input",type=Path,required=True)
    p.add_argument("--outdir",type=Path,required=True)
    a=p.parse_args();main(a.input,a.outdir)
