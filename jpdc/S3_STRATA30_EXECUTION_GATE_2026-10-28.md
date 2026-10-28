# S3 affected/unaffected stratified 30-seed study — execution gate

Date: 2026-10-28. Branch: jpdc-seed0-repro-20261024.
Immutable E4.6 tag and prior experiment artifacts remain unchanged.

## New concrete implementation
- `jpdc/validate_s3_strata30.py`: checks **every** seed 4202202600..4202202629 and windows 0,1,2; refuses duplicates, omissions, extra indices, impossible counts and sums inconsistent with the original successful run 40517387076. Computes descriptive group rates and reweights both groups to W0's pooled affected share.
- `.github/workflows/jpdc-s3-strata30.yml`: seed-zero before/after instrumentation parity gate (byte-equal outputs and equal legacy S3_ALL diagnostics); if successful, executes 30 original seeds as an explicitly instrumented rerun in a matrix and validates 90 stratum records against the original `s3_all30_by_seed.csv`.

## Status
Code and workflow committed. The 30-seed job's execution and artifact have NOT been verified. Do not report any stratified miss rates, significance, or parity success before inspecting the actual Actions run and artifacts. A code commit alone is not experimental evidence.

## Important limitation
A reweighted rate using the W0 affected share adjusts only this binary affected classification. It does not control workload difficulty, within-stratum covariate differences, candidate/family dependencies, or seed-specific selection. These descriptive rates are not causal, do not establish 99% conformal coverage, and are not superiority evidence.

## Workflow provenance
Source baseline aggregation run: 40517387076; original generation campaign run: 40517282086. Old frozen E4.6 unaffected.
