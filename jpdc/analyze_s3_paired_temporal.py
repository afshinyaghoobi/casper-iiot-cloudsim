#!/usr/bin/env python3
"""Exploratory paired seed-level temporal audit of S3 candidate misses.

Input: the *unchanged* by-seed CSV artifact of Actions run 40517387076.
No policy execution, E4.6 mutation, or candidate-level independence assumption.
"""
import argparse
import csv
import json
import math
import random
from pathlib import Path

SEEDS = tuple(range(4202202600, 4202202630))
WINDOWS = (0, 1, 2)

def quantile(xs, p):
    a = sorted(xs)
    k = (len(a) - 1) * p
    lo = int(k)
    hi = min(lo + 1, len(a) - 1)
    return a[lo] * (hi - k) + a[hi] * (k - lo)

def analyze(path, nboot=20000, seed=20261027):
    with path.open(newline="") as fp:
        reader = csv.DictReader(fp)
        required = {"seed", "window", "count", "misses", "affected", "etaSum", "networkMs"}
        assert required <= set(reader.fieldnames or ()), reader.fieldnames
        records = list(reader)
    assert len(records) == 90, f"expected 90 rows, received {len(records)}"
    index = {}
    for r in records:
        s, w = int(r["seed"]), int(r["window"])
        assert s in SEEDS and w in WINDOWS and (s, w) not in index
        n, miss, affect = (int(r[k]) for k in ("count", "misses", "affected"))
        assert n > 0 and 0 <= miss <= n and 0 <= affect <= n
        for k in ("etaSum", "networkMs"):
            assert math.isfinite(float(r[k]))
        index[s, w] = {"count": n, "misses": miss, "affected": affect,
                       "etaSum": float(r["etaSum"]), "networkMs": float(r["networkMs"])}
    assert set(index) == {(s, w) for s in SEEDS for w in WINDOWS}
    rates = {s: [index[s, w]["misses"] / index[s, w]["count"] for w in WINDOWS] for s in SEEDS}
    rng = random.Random(seed)
    out = {"status": "PASS", "source_run": 40517387076,
           "source_file": path.name, "unit_of_resampling": "seed",
           "bootstrap_replicates": nboot, "rng_seed": seed,
           "descriptive": {}, "paired": {},
           "limitations": [
               "Exploratory temporal comparisons; windows are not randomized intervention arms.",
               "Each window has different numbers/compositions of candidates.",
               "Within-seed time correlation is retained; across-seed independence is assumed.",
               "Candidate miss is not family-wise coverage and cannot establish nominal 99% coverage.",
               "No inference of causality or superiority over external baselines."]}
    for w in WINDOWS:
        N = sum(index[s, w]["count"] for s in SEEDS)
        M = sum(index[s, w]["misses"] for s in SEEDS)
        out["descriptive"][str(w)] = {"candidates": N, "misses": M,
            "pooled_miss_rate": M/N,
            "mean_seed_miss_rate": sum(rates[s][w] for s in SEEDS)/30}
    for a, b in ((0, 1), (1, 2), (0, 2)):
        differences = [rates[s][b] - rates[s][a] for s in SEEDS]
        obs = sum(differences)/30
        boot = []
        for _ in range(nboot):
            boot.append(sum(differences[rng.randrange(30)] for _ in range(30))/30)
        neg, pos, ties = sum(d < 0 for d in differences), sum(d > 0 for d in differences), sum(d == 0 for d in differences)
        # Two-sided exact sign test, ignoring ties. This tests the median sign, not pooled event rate.
        m = neg + pos
        if m:
            k = min(neg, pos)
            p = min(1.0, 2 * sum(math.comb(m, i) for i in range(k+1)) / 2**m)
        else:
            p = 1.0
        out["paired"][f"{a}_to_{b}"] = {
            "mean_seed_rate_change_pp": obs*100,
            "bootstrap_95pct_CI_pp": [quantile(boot, .025)*100, quantile(boot, .975)*100],
            "seeds_decreased": neg, "seeds_increased": pos, "seeds_tied": ties,
            "two_sided_sign_test_p_exploratory": p}
    return out

def main():
    p = argparse.ArgumentParser()
    p.add_argument("csv", type=Path)
    p.add_argument("--out", type=Path, default=Path("s3_all30_analysis/s3_paired_temporal_audit.json"))
    args = p.parse_args()
    result = analyze(args.csv)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("S3_PAIRED_TEMPORAL_PASS", json.dumps(result, sort_keys=True))

if __name__ == "__main__":
    main()
