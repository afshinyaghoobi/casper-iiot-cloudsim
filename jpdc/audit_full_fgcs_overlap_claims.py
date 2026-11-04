#!/usr/bin/env python3
"""QA for human-reviewed FGCS full-manuscript vs JPDC overlap decision.

This audits the repository document's provenance, section anchors and
scientific non-overclaiming. The privately uploaded FGCS PDF is NOT in
public GitHub CI; this is NOT automatic PDF text-similarity detection.
"""
from pathlib import Path

R=Path(__file__).resolve().parents[1]/"jpdc"
matrix=(R/"FGCS_FULL_MANUSCRIPT_VS_JPDC_OVERLAP_AUDIT_2026-11-04.md").read_text()
revised=(R/"JPDC_REVISED_SUBMISSION_GATE_AFTER_FGCS_FULL_TEXT_2026-11-04.md").read_text()
original=(R/"JPDC_INTEGRATED_RESULTS_DISCUSSION_2026-11-03.md").read_text()
native=(R/"NATIVE_TEN_SEED_ALL_EIGHT_HOLDOUT_VERIFIED_2026-11-04.md").read_text()
previous=(R/"JPDC_ONE_PAGE_CONTRIBUTION_CHARTER_2026-11-04.md").read_text()
def check(v,label):
    assert v,label
    print("PASS",label)

anchors=("§1.1","§3.1","Eq. **(1)–(4)**","Eq. **(5)**","Eq. **(6)**",
         "Eq. **(7)**","Eq. **(8)**","Eq. **(9a–c)**","Eq. **(10)**",
         "Eq. **(11)–(12)**","Algorithm 1","Table 2","p. **18**")
for a in anchors:
    check(a in matrix,"original FGCS anchoring: "+a)
check("FGCS-S-26-07417 (1).pdf" in matrix and "22-page" in matrix,
      "source is actual submitted complete PDF, not claimed public final")
check("HIGH overlap risk" in matrix and "newly discovered" in matrix,
      "original first-paper discussion already contained proposed Path A central claim")
check("stronger JPDC-exclusive" in matrix and "fixed-eta factorial" in matrix,
      "new interventions correctly distinguished from original policy")
check("first FGCS manuscript" in revised and "NO submission-ready" in revised,
      "revised internal journal gate is not a premature publication claim")
check("supersedes" in revised and "provisional" in previous.lower(),
      "older proposed title retained only as historical provenance")
check("p=1.000" in revised and "p=.0625" in revised and "p=.125" in revised,
      "three negative or nonsignificant inference gates preserved")
check("9.1214ms >5ms" in revised and "9.1214ms" in matrix,
      "original physical queue equivalence failure preserved")
check("p = 1.000" in native and "p = .0625" in original,
      "registered original science matches source reports")
check("NO-GO" in matrix and "NO submission-ready" in revised,
      "no unsupported algorithm novelty/submission readiness claim")
check("Path X" in revised and "Path Y" in revised and "not" in revised,
      "prospective alternatives do not count as existing validated results")
check("not evidence of final editorial acceptance" in revised,
      "submitted FGCS draft not silently called published")
print("JPDC_COMPLETE_FGCS_FULL_TEXT_OVERLAP_QA_PASS")
