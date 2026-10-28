# CASPER -> JPDC: evidence-gated research roadmap (2026-10-28)

## Decision principle
Aim for a defensible JPDC submission, not an arbitrary version number. No submission deadline. Estimated planning horizon: 8–12 weeks for main evidence gates, optionally 4–8 weeks more if experiments reveal substantial gaps. These are planning ranges, not experiment runtimes or promises.

## Current confirmed evidence
- Frozen E4.6 reference: v1.0.0-casper-iiot-e46. Do not modify.
- Queue-weighted challenger: 30-seed run 40280807901 and paired 40280910310; disjoint holdout 40281748580 and 40281798985, positive late DVR evidence in S2 and S4 under the **same** synthetic generator.
- S3 family attribution: 40350526730 / 40350683076.
- S3 all-candidate temporal run 40517282086 and aggregate 40517387076; descriptive decrease in candidate miss rate by task-index window, not a causal adaptation demonstration.
- Paired and composition-only analyses committed in jpdc/; they do not prove nominal 99% coverage, generalization or novelty.
- Stratified 30-seed workflow and synthetic validation tests are committed; their real GitHub Actions successes are not established by this checkpoint. Query and inspect actual run artifacts before asserting completion.

## Gate 1: correctness and S3 (suggested weeks 1–2)
- Confirm github Actions pilot parity and 30-seed strata artifacts; if failed, fix code and rerun.
- Validate affected/unaffected counts and misses against reference CSV for all 90 seed-window rows.
- Compare candidate error dynamics with eta; retain honest undercoverage.
Exit: complete reproducible evidence, verified parity, precise candidate/family-level definitions.

## Gate 2: strong baselines (weeks 3–5)
- Predefine fair comparator selection, hyperparameter budgets, workloads, seeds and outcome metrics.
- Implement/reproduce at least two literature-grounded scheduling comparators.
- Report paired effect sizes and multiplicity considerations; publish negative findings.
Exit: auditably fair comparison, no unqualified SOTA claims.

## Gate 3: generalization (weeks 5–8)
- Evaluate an independently specified workload generator or defensible external trace.
- Vary scale, arrival rate, heterogeneity, network shock, prediction bias/error and distribution shift.
Exit: clear regions of strength and failure, not only within-generator holdout.

## Gate 4: ablation and systems cost (weeks 8–10)
- Remove one mechanism at a time with matched evaluation.
- Quantify computational/runtime and decision overhead, inspect tail-risk outcomes.
Exit: evidence about component contributions and costs.

## Gate 5: writing and independent audit (weeks 10–12)
- Align each manuscript claim with reproducible plots/tables and exact code/data identifiers.
- Audit statistical analyses, limitations, references, format and statements about conformal guarantees.
Exit: no unsupported coverage, novelty, generalization or superiority claims.

## Stop / pivot triggers
- If a baseline consistently outperforms CASPER, characterize failure and redesign only with clear hypothesis and holdout.
- If cross-generator results degrade, report limited scope and revisit mechanism rather than tuning indefinitely on test data.
- If novel contribution remains too weak for JPDC, reconsider outlet/scope rather than accumulating V-number increments.

## Next immediate execution target
Inspect status of .github/workflows/jpdc-s3-strata30.yml. Only on successful parity and new 30-seed validated artifact, publish per-stratum analyses. No simulated results in lieu of actual run.
