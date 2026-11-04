#!/usr/bin/env python3
"""Synthetic regression tests for observed E45 outcome validator (no CloudSim dependency)."""
import csv
import pathlib
import tempfile
from audit_observed_outcome_sidecar import audit

POLICIES = ("CASPER_FULL", "CASPER_HEALTH_STATIC")
SEED = "4202202640"
SCENARIO = "S3_HIDDEN_NETWORK_50LOSS"


def expect_reject(log, official, needle):
    try:
        audit(log, official, 30000)
    except (ValueError, AssertionError) as error:
        assert needle in str(error), (needle, error)
    else:
        raise AssertionError("incorrectly accepted invalid record: " + needle)


with tempfile.TemporaryDirectory() as dirname:
    folder = pathlib.Path(dirname)
    log = folder / "events.log"
    results = folder / "results.csv"
    data = []
    for policy in POLICIES:
        for task in list(range(250)) + list(range(10000, 10250)):
            after = task >= 10000
            miss = after and task % 25 == 0
            cert = not (after and task % 10 == 0)
            latency = 60 if miss else 30
            data.append([
                "JPDC_OBSERVED_OUTCOME", SEED, SCENARIO, policy, task, 1,
                1.0, 25, 5, 5, latency - 10, latency, 50,
                str(cert).lower(), "true", str(miss).lower(),
                str(cert and miss).lower()
            ])
    original = [",".join(map(str, row)) for row in data]
    log.write_text("\n".join(original) + "\n", encoding="utf-8")

    fields = ["seed", "scenario", "policy", "tasks", "mission_n",
              "post_mission_n", "post_far", "post_air", "post_dvr",
              "post_fwc", "late_far", "late_air", "late_dvr", "late_fwc",
              "p99_post_latency_ms", "p99_late_latency_ms", "late_eta"]
    with results.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for policy in POLICIES:
            subset = [row for row in data if row[3] == policy and row[4] >= 10000]
            fraction = lambda position: sum(row[position] == "true" for row in subset) / 250
            writer.writerow(dict(
                seed=SEED, scenario=SCENARIO, policy=policy, tasks=30000,
                mission_n=500, post_mission_n=250,
                post_far=fraction(16), post_air=1 - fraction(13),
                post_dvr=fraction(15), post_fwc=fraction(14),
                late_far=fraction(16), late_air=1 - fraction(13),
                late_dvr=fraction(15), late_fwc=fraction(14),
                p99_post_latency_ms=60, p99_late_latency_ms=60, late_eta=1
            ))
    audit(log, results, 30000)
    print("PASS valid 1000 mission-outcome events")

    bad = folder / "bad.log"

    def change_line(index, column, value):
        lines = original.copy()
        record = next(csv.reader([lines[index]]))
        record[column] = value
        lines[index] = ",".join(record)
        bad.write_text("\n".join(lines) + "\n", encoding="utf-8")

    bad.write_text("\n".join(original + [original[0]]) + "\n", encoding="utf-8")
    expect_reject(bad, results, "duplicate task")
    change_line(0, 11, "31.0")
    expect_reject(bad, results, "observed latency sum mismatch")
    change_line(250, 16, "true")
    expect_reject(bad, results, "incorrect false-certificate flag")
    bad.write_text("\n".join(original[:-1]) + "\n", encoding="utf-8")
    expect_reject(bad, results, "mission count mismatch")
    change_line(0, 1, "4202202641")
    expect_reject(bad, results, "seed identity mismatch")
    change_line(0, 13, "invalid")
    expect_reject(bad, results, "malformed boolean")
    # Preserve total counts but silently replace one task ID in only one policy.
    change_line(0, 4, "251")
    expect_reject(bad, results, "cross-policy mission task ID mismatch")
    # A deadline perturbation can leave miss labels/rates unchanged.
    change_line(0, 12, "51")
    expect_reject(bad, results, "cross-policy deadline mismatch")
    wrong = folder / "wrong.csv"
    wrong.write_text(results.read_text().replace(",0.04,", ",0.08,", 1), encoding="utf-8")
    bad.write_text("\n".join(original) + "\n", encoding="utf-8")
    assert wrong.read_text() != results.read_text()
    expect_reject(bad, wrong, "trace")
print("JPDC_OBSERVED_OUTCOME_CONTRACT_TEST_PASS")
