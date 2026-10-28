# JPDC S3 stratified instrumentation pilot (2026-10-27)

## Purpose
Measure S3 all-candidate misses by affected-node status and test passive instrumentation parity on an identical seed. This is a **new proposed measurement run**, not a reported result.

## Exact files
- `jpdc/s3_stratified_candidate_patch.py` applies only to generated `src/main/java/org/casperiiot/e45/E45Campaign.java` after `tools/e45_generate.py` and `jpdc/s3_all_candidate_patch.py`.
- `.github/workflows/jpdc-s3-stratified-pilot.yml` runs 30,000-task S3 seed index zero, with 80,000 calibration samples, twice (pre and post passive-strata instrumentation).
- The script counts candidates and misses separately for `affected[node]` true/false in each of three task-index windows, using the exact same `actualAudit[ix]>upper[ix]` predicate as the prior all-candidate audit.
- Asserts before/after CSV byte-for-byte equality and equality of legacy `S3_ALL` log lines; verifies for each window `affectedN+unaffectedN=count`, `affectedN=affected`, and `affectedMiss+unaffectedMiss=misses`.

## Verification gate
GitHub commit of workflow and patch **does not prove that a GitHub Actions run succeeded**. At authoring time the new job's execution, output artifact, and baseline parity are **not yet confirmed**. No affected/unaffected miss rates, statistical significance, mechanism or coverage conclusions should be reported until an actual successful run and output inspection.

If pilot passes, expand to all 30 original seeds as a *separate audit run*; retain policy version E4.6 and compare output invariants. Do not call this external validation or claim 99% coverage or novel superiority.
