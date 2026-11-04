# JPDC manuscript-ready native holdout Results/Discussion addendum — verified 2026-11-04

## Deliverable
The existing original Java CloudSim `jpdc/JPDC_INTEGRATED_RESULTS_DISCUSSION_2026-11-03.md` was **not overwritten**. Instead we drafted an American-English supplemental Results and Discussion `jpdc/JPDC_NATIVE_HOLDOUT_RESULTS_DISCUSSION_ADDENDUM_2026-11-04.md` and programmatic fail-closed manuscript transcription/claims auditor `jpdc/audit_native_holdout_manuscript_addendum.py`.

The addendum covers fully-independent native Python physical simulator scope, original per-seed 80k physical calibration, all 8 policies, 10 seed indices60–69, S2/S3×30k complete 160 deployment runs /4.8million task-policy records, original frozen single PRIMARY matched seed-level GREEDY-minus-FULL postshock MISSION deadline miss benefit, all 10 individual effects, exact two-sided sign p=1.000 (five beneficial, four detrimental, one exact tie), mean benefit +0.3208 percentage points descriptive, fixed bootstrap interval [-0.3060,+0.9882] pp containing zero, original complete scenario S2/S3 6-row descriptive table, independently observed CASPER_FULL rank2 39/rank3 0, native health/E17 activity, and limitations including different physical FCFS vs CloudSimPlus SpaceShared original FAILED queue transfer gate.

All original Java disjoint holdout p=.0625 nonsignificant, factorial exploratory p=.125 nonsignificant preserved. No secondary p-hacking or changing original holdout. The source is the original previously registered run `41920321822` and immutable original artifact `13367565614`, plus original reporting-only run `41920792886`, not any newly generated experiment. Manuscript figures were audited against the original written verified result report, with provenance caveat that this is transcription/claim audit, not a raw-event replay.

## Verified CI
Original draft commit `703e115cf2efb0700e43c6589234c182d46b9e26`, numeric claim auditor original commit `fcc417248ea223209c4819d4ba2681564974d671`. Initial audits 41923093707, 41923200035 and 41923313962 FAILED on *auditor parsing the manuscript markdown emphasis and syntax*, not on numerical contradiction or algorithm/model changes. Fixed parser/formatting assertions, preserving all data and thresholds. **Actual final GitHub Actions run `41923518215` COMPLETED SUCCESS**, artifact **13368600467**; source CI workflow final `b704cff9f08bd9629323d099545fb65897ac7906`, original E42 Git blob unchanged `34256ca7bff46f911cf20e8b94278fbd09175746`.

Actual CI logs confirm:
- `JPDC_NATIVE_HOLDOUT_MANUSCRIPT_NUMERIC_AND_CLAIM_AUDIT_PASS` including all 10 seed signs and effects, all 6 S2/S3 scenario rows, observed rank2 counts, all 3 null-significance statements, queue failure and external validity limits;
- `PASS: manuscript aggregate transcription and arithmetic audit complete` from the prior original Java integrated manuscript audit;
- `JPDC_ALL_MANUSCRIPT_SOURCE_NUMBER_GATES_PASS`.

Final report is a **draft supplement ready for integration**, not a full submission-ready JPDC paper. The first original integrated manuscript still requires merging with supplemental material, coherent title/novelty assessment, methods, all figure/table references, full literature review and final English polish. The current registered native holdout **did not show** supported CASPER_FULL deadline miss improvement. We should not claim otherwise.

## Links
- Addendum: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/blob/jpdc-seed0-repro-20261024/jpdc/JPDC_NATIVE_HOLDOUT_RESULTS_DISCUSSION_ADDENDUM_2026-11-04.md
- Numeric auditor: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/blob/jpdc-seed0-repro-20261024/jpdc/audit_native_holdout_manuscript_addendum.py
- Original 10-seed science: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41920321822
- Final successful manuscript audit: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41923518215
- Audit evidence artifact: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41923518215/artifacts/13368600467
