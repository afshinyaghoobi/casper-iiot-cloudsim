# Gate 1 — original-counter parity hardening (2026-10-28)

## Work completed
Added `jpdc/verify_s3_legacy_30.py` to cross-check every new `S3_ALL` run-log row against the unmodified original 90-row `s3_all30_by_seed.csv` from successful GitHub Actions run 40517387076. Required keys are 30 frozen scientific seeds × 3 task-index windows; rejects duplicate, missing, malformed, or contradictory legacy rows.

Updated `.github/workflows/jpdc-s3-strata30.yml` so the aggregation job must pass this additional check *before* accepting the newly instrumented affected/unaffected count validation. A separate synthetic positive/negative fixture test `jpdc/test_verify_s3_legacy_30.py` was added to `.github/workflows/jpdc-s3-validator-tests.yml`.

## Evidence classification
- Source code and workflow wiring: committed.
- The new tests are **specified in CI**, not asserted to have passed GitHub Actions.
- The new 30-seed experiment is **not yet verified as successfully executed**. The GitHub commit-to-workflow lookup available in this environment is limited to PR-triggered runs; absence of results for a push commit is inconclusive.
- Original S3 aggregate reference: run 40517387076, SHA256 of CSV `78fd57691aa3fabd7a3d84fddac28903c66b173f7165def809b7ec374685321c`.
- No novelty, causality, significance, 99% coverage, or cross-generator validity claim.

## Reproduction after workflow produces real artifacts
```bash
python3 jpdc/test_verify_s3_legacy_30.py
python3 jpdc/verify_s3_legacy_30.py --reference source/s3_all30_by_seed.csv --logs 'strata/**/*.log'
python3 jpdc/validate_s3_strata30.py --reference source/s3_all30_by_seed.csv --logs 'strata/**/*.log' --out strata30_report.json
```

## Decision gate
Only interpret stratified rates if the seed-zero policy parity, original-counter parity across 90 rows, and stratified-count validator **all** pass on actual downloaded artifacts. Frozen E4.6 remains unchanged.
