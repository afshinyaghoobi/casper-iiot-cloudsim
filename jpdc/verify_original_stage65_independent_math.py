#!/usr/bin/env python3
"""Independent Stage65 statistics via ORIGINAL audit artifact, not original auditor.

This source never imports jpdc.audit_stage65_holdout_cohort nor reruns a
policy or a simulator. Enumerate the conditional sign-test null directly.
"""
import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path

EXPECTED_SOURCE_COHORT_SHA256 = "b52c5e29a93c4d46ca61ce2fc34cb1eea48f4c9cf270a3f194de4fb8e703e8c7"
EXPECTED_SCENARIOS = ("S2_HIDDEN_COMPUTE_40LOSS", "S3_HIDDEN_NETWORK_50LOSS")
EXPECTED_SEEDS = tuple(range(1811, 1819))


def exact_two_sided_sign_by_enumeration(deltas):
    """Enumerate 2^n equally likely sign labels; drop exact paired ties."""
    nz = [x for x in deltas if x != 0]
    n = len(nz)
    if n == 0:
        return {"n_nonzero": 0, "favorable": 0, "adverse": 0, "two_sided_p": 1.0}
    favorable = sum(x < 0 for x in nz)
    adverse = n - favorable
    observed_extremeness = abs(2 * favorable - n)
    outcomes = list(itertools.product((False, True), repeat=n))
    extreme = sum(abs(2 * sum(bits) - n) >= observed_extremeness for bits in outcomes)
    return dict(n_nonzero=n, favorable=favorable, adverse=adverse,
                two_sided_p=extreme / len(outcomes))


def recompute(path):
    original = path.read_bytes()
    assert hashlib.sha256(original).hexdigest() == EXPECTED_SOURCE_COHORT_SHA256, (
        "Original exact cohort content changed; cannot recompute as original Stage65")
    source = json.loads(original)
    assert source["status"] == "PASS"
    assert source["original_source_n"] == 8
    assert source["dependent_policy_task_observations"] == 576000
    assert source["prereg_acceptance_gate"] == "FAIL"
    cells = source["cells"]
    assert len(cells) == 16

    complete = []
    result = {}
    for scenario in EXPECTED_SCENARIOS:
        group = {int(row["seed"]): row for row in cells if row["scenario"] == scenario}
        assert set(group) == set(EXPECTED_SEEDS)
        deltas = []
        whole_deltas = []
        for seed in EXPECTED_SEEDS:
            row = group[seed]
            assert 0 <= row["full_post_misses"] <= row["post_mission_n"]
            assert 0 <= row["partial_post_misses"] <= row["post_mission_n"]
            p = int(row["partial_post_misses"]) - int(row["full_post_misses"])
            q = int(row["partial_all_mission_misses"]) - int(row["full_all_mission_misses"])
            assert row["partial_minus_full_post"] == p
            assert row["partial_minus_full_all"] == q
            deltas.append(p)
            whole_deltas.append(q)
            complete.append((scenario, seed))
        sign = exact_two_sided_sign_by_enumeration(deltas)
        prior = source["scenarios"][scenario]
        assert math.isclose(sign["two_sided_p"], prior["exact_paired_sign"]["p"], abs_tol=0, rel_tol=0)
        assert prior["paired_seed_deltas"] == deltas
        assert math.isclose(sum(deltas) / 8, prior["mean_delta_misses_per_source"])
        result[scenario] = dict(
            independent_source_seeds=list(EXPECTED_SEEDS), independent_unit="SOURCE_SEED",
            paired_postshock_miss_deltas=deltas,
            paired_whole_mission_deltas=whole_deltas,
            source_postshock_harm=[seed for seed, diff in zip(EXPECTED_SEEDS, deltas) if diff > 0],
            source_whole_mission_harm=[seed for seed, diff in zip(EXPECTED_SEEDS, whole_deltas) if diff > 0],
            observed_full_postshock_misses=sum(group[s]["full_post_misses"] for s in EXPECTED_SEEDS),
            observed_partial_postshock_misses=sum(group[s]["partial_post_misses"] for s in EXPECTED_SEEDS),
            exact_conditional_sign_test=sign,
            sum_paired_delta=sum(deltas),
            mean_paired_delta=sum(deltas) / len(deltas))
    assert len(set(complete)) == 16
    assert result[EXPECTED_SCENARIOS[0]]["source_postshock_harm"] == [1815, 1816]
    assert sum(len(x["source_whole_mission_harm"]) for x in result.values()) == 6
    assert not source["no_harm_both_scopes_all_16_cells"]
    assert not source["statistical_superiority_at_p_005_per_scenario"]
    assert result[EXPECTED_SCENARIOS[0]]["exact_conditional_sign_test"]["two_sided_p"] == 1.0
    assert result[EXPECTED_SCENARIOS[1]]["exact_conditional_sign_test"]["two_sided_p"] == .125
    return dict(status="PASS", verification="RECOMPUTED_FROM_EXACT_ORIGINAL_ARCHIVED_COHORT",
                not_an_independent_physical_replication=True,
                not_new_scientific_source_seeds=True,
                original_stage65_safety="FAIL",
                original_java_python_queue_parity="FAIL",
                original_cohort_sha256=EXPECTED_SOURCE_COHORT_SHA256,
                scenarios=result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--original-cohort", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    report = recompute(Path(args.original_cohort))
    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, sort_keys=True, indent=2, allow_nan=False) + "\n")
    for scenario, summary in report["scenarios"].items():
        print("JPDC_INDEPENDENT_ORIGINAL_HOLDOUT_RECOMPUTE",
              json.dumps({"scenario": scenario, **summary}, sort_keys=True))
    print("JPDC_INDEPENDENT_STAGE65_MATH_FROM_ORIGINAL_ARCHIVE_PASS")
