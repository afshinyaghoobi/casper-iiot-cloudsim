# S3 seed29 mission-task phase-conditioned reliability audit (2026-11-02)

Source is actual verified task dispatch and outcome trace from Actions run `41504014147`, artifact `13170236795`. This is a descriptive *single-seed* audit; phase comparisons are dependent observations, not independent inferential trials.

The 30,000-task run has 499 mission tasks with task index <10000, and 993 mission tasks at index >=10000. The latter comprise the first 743 post-change mission tasks and final 250 late mission tasks. The exact same mission-task indices are compared between policies.

| Phase, policy | n mission tasks | FWC family covered | Certificates issued | False certificates | Abstentions | Deadline misses |
|---|---:|---:|---:|---:|---:|---:|
| Pre, CASPER_FULL | 499 | 497 | 479 | 0 | 20 | 0 |
| Pre, CASPER_HEALTH_STATIC | 499 | 495 | 484 | 0 | 15 | 0 |
| Post, CASPER_FULL | 993 | 568 | 831 | 37 | 162 | 118 |
| Post, CASPER_HEALTH_STATIC | 993 | 1 | 972 | 96 | 21 | 115 |
| Late 250, CASPER_FULL | 250 | 135 | 216 | 12 | 34 | 31 |
| Late 250, CASPER_HEALTH_STATIC | 250 | 0 | 245 | 25 | 5 | 30 |

FWC = counterfactual *family-wide* coverage of predicted upper bounds. It is not precision of issued certificates. FAR = false certificates / n mission; conditional certificate error = false / issued; AIR = abstentions / n mission.

Important observation: FULL post-change false certificates 37/993 vs STATIC 96/993, accompanied by abstentions 162 vs 21, while deadline misses 118 vs 115. This descriptive effect is consistent with adaptive conservative certification under shift, **not** a demonstrated improvement in deadline scheduling. Pre-shock both policies have zero observed false certifications and deadline violations. No formal before/after causal claim, calibration coverage guarantee under shift, or p-value inference is warranted from this single seed. Frozen E42/E4.6 code unchanged.

Reproducible local audit: `/mnt/data/jpdc_seed29_phase_calibration_audit.py`; output `/mnt/data/jpdc_seed29_phase_calibration_audit_2026_11_02.zip`. In a new conversation, local paths may not persist; original trace can be re-downloaded from artifact 13170236795. For multi-seed confidence, repeat phase-conditioned analysis across independent seeds with task-level traces.
