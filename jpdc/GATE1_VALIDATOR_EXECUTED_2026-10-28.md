# Gate 1: executed validator contract test and provenance (2026-10-28)

## What was actually executed
From the locally available checked-out validator and synthetic test fixture:

```bash
cd /mnt/data/jpdc_validation
python test_strata_validator.py
```

Observed `VALIDATOR_CONTRACT_TEST_PASS`; one valid 90-row fixture, and seven deliberately corrupted fixture cases were correctly rejected (duplicate seed-window, missing seed-window, miss exceeding candidates, affected count mismatch, miss total mismatch, unexpected window, and malformed record).

The input baseline `s3_all30_by_seed.csv`, from successful aggregate GitHub Actions run 40517387076, was independently SHA256 checked locally:

`78fd57691aa3fabd7a3d84fddac28903c66b173f7165def809b7ec374685321c`

This is an executed contract test **on synthetic validator fixtures** and a real-data file integrity check, **not** a successful 30-seed affected/unaffected simulation or parity test.

## Important GitHub Actions status limitation
The available commit-associated workflow query currently filters to pull-request-triggered runs only, and returned no runs for commit `290e8a2df765a08a7a3fe70d5913f76477c18808`. Therefore absence of results does **not** establish that the push/dispatch workflow never ran. We must not report S3 strata 30-seed outputs, or parity, without independently accessing actual Actions status and artifacts.

## Immediate next evidence gate
1. Determine the actual run identifier of `.github/workflows/jpdc-s3-strata30.yml` from GitHub Actions UI / an API capable of listing push-triggered runs.
2. Inspect parity job before/after CSV equality and `S3_ALL` equality.
3. Retrieve all 30 seed logs and run `jpdc/validate_s3_strata30.py`, validating against this SHA-locked reference.
4. Report conditional group-specific miss rates only if all checks pass; then undertake scientific sensitivity analysis.

No E4.6 changes; no claimed 99% coverage, causal improvement, or SOTA superiority.
