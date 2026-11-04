#!/usr/bin/env python3
"""Fail-closed reconciliation of actual E45 task outcome sidecar vs official CSV.

Usage: python3 jpdc/audit_observed_outcome_sidecar.py --log run.log --results run.csv --tasks 30000
Only observed outcomes are interpreted as actual latency; no counterfactual replay.
"""
import argparse
import csv
import math

POLICIES = ("CASPER_FULL", "CASPER_HEALTH_STATIC")
SCENARIO = "S3_HIDDEN_NETWORK_50LOSS"
FIELDS = ("tag", "seed", "scenario", "policy", "task", "node", "eta", "prediction_ms",
          "network_ms", "queue_wait_ms", "service_ms", "observed_ms", "deadline_ms",
          "certified", "family_covered", "miss", "false_cert")


def close(a, b, eps=1e-6):
    return math.isclose(float(a), float(b), abs_tol=eps, rel_tol=0)


def percentile_99(values):
    ordered = sorted(values)
    return ordered[math.ceil((len(ordered)-1) * .99)]


def audit(log_file, results_file, tasks):
    traced = {policy: {} for policy in POLICIES}
    with open(log_file, encoding="utf-8") as f:
        for line in f:
            if not line.startswith("JPDC_OBSERVED_OUTCOME,"):
                continue
            row = next(csv.reader([line]))
            if len(row) != len(FIELDS):
                raise ValueError(f"bad sidecar column count {len(row)}")
            r = dict(zip(FIELDS, row))
            if r["tag"] != "JPDC_OBSERVED_OUTCOME" or r["scenario"] != SCENARIO or r["policy"] not in POLICIES:
                raise ValueError("sidecar identity invalid")
            task, node = int(r["task"]), int(r["node"])
            if not 0 <= task < tasks or not 0 <= node < 21:
                raise ValueError("invalid task/node")
            if task in traced[r["policy"]]:
                raise ValueError("duplicate task")
            vals = {k: float(r[k]) for k in ("eta", "prediction_ms", "network_ms",
                     "queue_wait_ms", "service_ms", "observed_ms", "deadline_ms")}
            if not all(math.isfinite(x) for x in vals.values()) or any(
                vals[k] < 0 for k in ("network_ms", "queue_wait_ms", "service_ms", "observed_ms")
            ) or vals["deadline_ms"] <= 0 or not 1 <= vals["eta"] <= 3:
                raise ValueError("invalid observed numerical value")
            if not close(vals["network_ms"] + vals["queue_wait_ms"] + vals["service_ms"],
                         vals["observed_ms"], 5e-8):
                raise ValueError("observed latency sum mismatch")
            for flag in ("certified", "family_covered", "miss", "false_cert"):
                if r[flag] not in ("true", "false"):
                    raise ValueError("malformed boolean")
            cert = r["certified"] == "true"
            miss = r["miss"] == "true"
            far = r["false_cert"] == "true"
            # Reported flag is authoritative at decimal rounding equality.
            if miss != (vals["observed_ms"] > vals["deadline_ms"]) and not (
                miss and close(vals["observed_ms"], vals["deadline_ms"], 1e-9)
            ):
                raise ValueError("deadline result mismatch")
            if far != (cert and miss):
                raise ValueError("incorrect false-certificate flag")
            r.update(vals)
            r["task"] = task
            r["certified"] = cert
            r["miss"] = miss
            r["false_cert"] = far
            r["family_covered"] = r["family_covered"] == "true"
            traced[r["policy"]][task] = r

    with open(results_file, encoding="utf-8", newline="") as f:
        official_rows = list(csv.DictReader(f))
    if len(official_rows) != 8 or len({r.get("policy") for r in official_rows}) != 8:
        raise ValueError("official CSV requires eight distinct policy rows")
    if any(r.get("scenario") != SCENARIO or int(r.get("tasks", "-1")) != tasks for r in official_rows):
        raise ValueError("official scenario/task-count metadata mismatch")
    official = {r["policy"]: r for r in official_rows if r.get("policy") in POLICIES}
    if len(official) != 2:
        raise ValueError("missing required official policies")
    seed_expected = {r["seed"] for r in official.values()}
    if len(seed_expected) != 1 or any(row["seed"] not in seed_expected for policy_rows in traced.values() for row in policy_rows.values()):
        raise ValueError("seed identity mismatch")
    # Both policies must evaluate the SAME generated MISSION task cohort.
    # Counts alone cannot detect one missing task replaced with a different one.
    task_sets = {policy: set(traced[policy]) for policy in POLICIES}
    if task_sets[POLICIES[0]] != task_sets[POLICIES[1]]:
        missing_full = sorted(task_sets[POLICIES[1]] - task_sets[POLICIES[0]])[:5]
        missing_static = sorted(task_sets[POLICIES[0]] - task_sets[POLICIES[1]])[:5]
        raise ValueError(f"cross-policy mission task ID mismatch: full missing={missing_full}; static missing={missing_static}")
    for task in task_sets[POLICIES[0]]:
        if not close(traced[POLICIES[0]][task]["deadline_ms"],
                     traced[POLICIES[1]][task]["deadline_ms"], 1e-9):
            raise ValueError(f"cross-policy deadline mismatch task {task}")

    for policy in POLICIES:
        rr = official[policy]
        all_rows = traced[policy]
        if len(all_rows) != int(rr["mission_n"]) or int(rr["tasks"]) != tasks:
            raise ValueError("mission count mismatch")
        post = sorted((r for r in all_rows.values() if r["task"] >= 10000),
                      key=lambda r: r["task"])
        if len(post) != int(rr["post_mission_n"]) or len(post) < 250:
            raise ValueError("post-shock mission count mismatch")
        late = post[-250:]
        mean = lambda seq, key: sum(float(r[key]) for r in seq) / len(seq)
        measures = {
            "post_far": mean(post, "false_cert"),
            "post_air": 1 - mean(post, "certified"),
            "post_dvr": mean(post, "miss"),
            "post_fwc": mean(post, "family_covered"),
            "late_far": mean(late, "false_cert"),
            "late_air": 1 - mean(late, "certified"),
            "late_dvr": mean(late, "miss"),
            "late_fwc": mean(late, "family_covered"),
            "p99_post_latency_ms": percentile_99([r["observed_ms"] for r in post]),
            "p99_late_latency_ms": percentile_99([r["observed_ms"] for r in late]),
            "late_eta": mean(late, "eta"),
        }
        for key, value in measures.items():
            if key.endswith(("far", "air", "fwc")) and (key.startswith("post") or key.startswith("late")):
                if rr[key].lower() == "nan":
                    continue
            if not close(value, rr[key], 2e-6):
                raise ValueError(f"{policy} {key}: trace {value} != official {rr[key]}")
        print(f"PASS {policy}: missions={len(all_rows)} post={len(post)} late=250, official metrics match")
    print("JPDC_OBSERVED_OUTCOME_RECONCILIATION_PASS")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--log", required=True)
    p.add_argument("--results", required=True)
    p.add_argument("--tasks", type=int, default=30000)
    args = p.parse_args()
    audit(args.log, args.results, args.tasks)
