#!/usr/bin/env python3
"""Audit JPDC novelty claim boundary against frozen evidence; no new simulations.

Checks explicit negative and external-validity disclosures in novelty decision.
"""
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT/"jpdc/JPDC_NOVELTY_ORIGINALITY_GATE_2026-11-04.md"
NATIVE=ROOT/"jpdc/NATIVE_TEN_SEED_ALL_EIGHT_HOLDOUT_VERIFIED_2026-11-04.md"
JAVA=ROOT/"jpdc/JPDC_INTEGRATED_RESULTS_DISCUSSION_2026-11-03.md"
DRAFT=ROOT/"jpdc/JPDC_NATIVE_HOLDOUT_RESULTS_DISCUSSION_ADDENDUM_2026-11-04.md"

def check(condition,message):
    if not condition:raise AssertionError(message)
    print("PASS",message)

def main():
    a=AUDIT.read_text(encoding="utf-8")
    n=NATIVE.read_text(encoding="utf-8")
    j=JAVA.read_text(encoding="utf-8")
    d=DRAFT.read_text(encoding="utf-8")
    require=("NO-GO","CONDITIONAL","CASPER_FULL","PRED_GREEDY","rank2","rank3",
             "strict-FCFS","YAFS","full side-by-side","FGCS")
    for token in require:check(token.lower() in a.lower(),f"novelty gate declares {token}")
    check(re.search(r"p\\s*=\\s*1\\.000",a) is not None and re.search(r"p\\s*=\\s*1\\.000",n) is not None,
          "negative ten-seed independent result unchanged")
    check("p=.0625" in a and "p = .0625" in j,
          "original nonsignificant Java confirmatory result preserved")
    check("p=.125" in a and "p = .125" in j,
          "original nonsignificant factorial inference preserved")
    check("9.1214ms" in a and "5ms" in a and "9.1214 ms" in d,
          "failed exact Java-to-Python physical queue parity disclosed")
    check("rank2=39" in a and "rank3=0" in a and
          "rank1, 39 rank2, zero rank3" in n,
          "independent observed rank2 and absent rank3 not overclaimed")
    check("a full side-by-side" in a.lower() and "not" in a.lower(),
          "explicitly acknowledges missing full FGCS-vs-JPDC manuscript comparison")
    check("not yet an invention validated" in a.lower(),
          "future exposure-aware algorithm is labeled hypothetical, not established")
    forbidden=[
       r"casper_full (?:significantly|statistically) (?:improves|outperforms)",
       r"validated (?:in|with) yafs",
       r"rank3 was (?:observed|selected) in the native holdout",
       r"guarantees deadline success under arbitrary drift",
    ]
    for term in forbidden:
        check(re.search(term,a,re.I) is None,f"no unsupported novelty/performance claim: {term}")
    check("p-value was 1.000" in d and "rank 3 was never selected" in d.lower(),
          "existing native manuscript keeps negative outcome and mechanism limits")
    print("JPDC_NOVELTY_CLAIM_BOUNDARY_AUDIT_PASS")

if __name__=="__main__":main()
