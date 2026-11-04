#!/usr/bin/env python3
"""Fail-closed, standard-library audit of JPDC narrative against committed result reports.

Run at repository root:
    python3 jpdc/audit_integrated_manuscript_numbers.py

This validates transcription/arithmetic of committed reported aggregates. It does
NOT independently validate raw CloudSim traces, artifact provenance, or causality.
"""
from __future__ import annotations

import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRAFT = ROOT / "jpdc/JPDC_INTEGRATED_RESULTS_DISCUSSION_2026-11-03.md"
FACT = ROOT / "jpdc/S3_MASK_ETA_FACTORIAL_4SEED_RESULTS_2026-11-03.md"
MASK = ROOT / "jpdc/S3_CONTROLLED_MASK_4SEED_RESULTS_2026-11-03.md"
CONT = ROOT / "jpdc/NEW_CHAT_CONTINUITY_2026-11-02.md"


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)
    print("PASS", label)


def table_rows(text: str, prefix: str) -> list[str]:
    return [line for line in text.splitlines() if line.startswith("| " + prefix)]


def cells(row: str) -> list[str]:
    return [c.strip().replace("**", "") for c in row.strip().strip("|").split("|")]


def p_sign(positive: int, negative: int) -> float:
    """Two-sided exact sign test, discarding ties."""
    n = positive + negative
    if n == 0:
        return 1.0
    k = min(positive, negative)
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2**n)


def main() -> None:
    draft, fact, mask, cont = (p.read_text(encoding="utf-8") for p in
                              (DRAFT, FACT, MASK, CONT))
    require("p = .0625" in draft and "FAILED alpha=.05" in cont,
            "primary disjoint holdout explicitly non-significant in draft/handoff")
    require(p_sign(0, 5) == 0.0625, "holdout exact sign p (5 negative, 5 ties)")
    require(p_sign(0, 4) == 0.125, "factorial 4/4 exact two-sided sign p")
    require(p_sign(1, 0) == 1.0, "factorial deadline sign p (3 ties)")

    # Compare all four four-seed factorial rows, not just narrative highlights.
    labels = {
        "LOW, adaptive eta": ("LOW", "FULL adaptive"),
        "LOW, fixed eta = 1": ("LOW", "FULL eta=1"),
        "HIGH, adaptive eta": ("HIGH", "FULL adaptive"),
        "HIGH, fixed eta = 1": ("HIGH", "FULL eta=1"),
    }
    source_rows = {}
    for name, (mask_name, state) in labels.items():
        matches = [cells(r) for r in table_rows(fact, mask_name)
                   if len(cells(r)) >= 7 and cells(r)[1] == state]
        require(len(matches) == 1, "source factorial unique " + name)
        source_rows[name] = tuple(int(v) for v in matches[0][2:6])
        draft_matches = [cells(r) for r in table_rows(draft, name)]
        require(len(draft_matches) == 1, "draft factorial unique " + name)
        require(tuple(int(v) for v in draft_matches[0][1:5]) ==
                source_rows[name], "draft factorial agrees with report " + name)
    low_a, low_f, high_a, high_f = (source_rows[k] for k in labels)
    # Columns: incorrect certificates, abstentions, FWC, deadline misses.
    expected_pp = (-3.0, +11.1, +83.0, +0.1)
    measured_pp = tuple(
        ((high_a[i] - high_f[i]) - (low_a[i] - low_f[i])) / 10
        for i in range(4)
    )
    require(all(math.isclose(x, y, abs_tol=1e-10)
                for x, y in zip(measured_pp, expected_pp)),
            "four factorial interaction magnitudes computed from counts")
    require((high_f[0] - high_a[0]) / high_f[0] * 100 > 90.9 - 0.01,
            "HIGH false-certificate descriptive relative reduction 90.9%")
    require(("p = .125" in draft or "p=.125" in draft) and
            ("p = .125" in fact or "p=.125" in fact),
            "four-seed inference limited to exploratory p=.125")

    # Disjoint holdout table must use correct rates and certificate denominators.
    holdout = {}
    for label in ("False certifications", "Abstentions",
                  "Deadline misses", "Issued certificates"):
        rr = [cells(r) for r in table_rows(draft, label)]
        require(len(rr) == 1, "holdout row exists exactly once: " + label)
        holdout[label] = rr[0][1:3]
    for label, a, b in (("False certifications", 7, 40),
                        ("Abstentions", 176, 47),
                        ("Deadline misses", 65, 63)):
        require(holdout[label] == [f"{a} ({a/2500:.2%})",
                                   f"{b} ({b/2500:.2%})"],
                "holdout count and denominator: " + label)
    require(holdout["Issued certificates"] == ["2,324", "2,453"],
            "holdout issued certificates reconcile with abstentions")

    # Cross-document physical exposure values are source-reported rounded values.
    for quantity in ("0.051%", "99.656%", "0.0032", "12.8762"):
        require(quantity in draft and quantity in mask,
                "exposure/delay value transcribed: " + quantity)
    # 12.8762 - 0.0032 = 12.8730, so 12.8731 in source is a
    # rounding-from-unrounded-means issue, not independently verifiable here.
    require("12.8731" in mask, "rounded source subtraction discrepancy flagged")
    print("NOTE: source reports HIGH-LOW mean delay 12.8731 ms; displayed"
          " rounded means subtract to 12.8730 ms. Check unrounded artifact"
          " before asserting extra precision.")

    require("not statistically significant" in draft.lower(),
            "no confirmatory-significance claim")
    print("PASS: manuscript aggregate transcription and arithmetic audit complete")
    print("LIMIT: no raw GitHub Actions artifacts were independently replayed.")


if __name__ == "__main__":
    main()
