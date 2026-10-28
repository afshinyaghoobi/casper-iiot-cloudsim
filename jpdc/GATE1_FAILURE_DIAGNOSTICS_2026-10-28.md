# JPDC Gate 1 — failure-diagnostic preservation (2026-10-28)

## Observed limitation and change
The S3 30-seed GitHub Actions workflow previously uploaded per-seed logs only on success and did not upload parity-job logs. A failing parity or seed job could therefore conceal the precise failure in downloadable artifacts.

Changed `.github/workflows/jpdc-s3-strata30.yml`:
- Added an `if: always()` upload of `parity/` (before/after CSV and log when generated) as `s3-strata-parity-diagnostics`.
- Set each seed's log upload to `if: always()` and `if-no-files-found: warn`, so failed jobs can still preserve their partial logs without treating a nonexistent file as a successful experiment.
- Kept the mandatory dependency `seeds: needs: parity` and `aggregate: needs: seeds`. The final validated artifact is only produced after successful upstream jobs and the existing reference SHA/count validation.

## Verification
Read back the changed workflow from GitHub. Static assertions confirmed the parity diagnostics upload, per-seed diagnostic upload, 30-index matrix, strict CSV parity command and unchanged original reference run 40517387076. This is **static source inspection**, not a successful Actions execution.

GitHub Actions push/dispatch run listing is not exposed by the connected GitHub tool presently, and direct external REST access could not retrieve private workflow runs. We do not claim that the new 30-seed run has executed or passed.

## Next empirical gate
Use GitHub Actions workflow page to locate the newest run. Inspect the `parity` job first, and only if it succeeds inspect all 30 seed logs and the aggregate `jpdc-s3-strata30-validated` artifact. If parity fails, retrieve `s3-strata-parity-diagnostics` and investigate mismatched bytes/legacy counters. If a seed job fails, inspect its preserved log. Keep frozen E4.6 unchanged.

No coverage, mechanism, causality, generalization, or superiority claim follows from this change.
