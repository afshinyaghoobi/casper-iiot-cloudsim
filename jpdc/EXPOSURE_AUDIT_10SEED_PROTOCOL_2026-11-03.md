# Prespecified descriptive exposure audit — existing exploratory ten seeds
Date: 2026-11-03. Protocol recorded BEFORE running missing seed traces.

Population is fixed by the already established original ten-seed exploratory cohort: 0,1,5,7,9,13,18,21,27,29; pre-existing real exposure traces exist for 7 and 18. Run missing eight seed indices 0,1,5,9,13,21,27,29 regardless of outcomes.

S3 hidden network 50% retained bandwidth; frozen E42 scientific blob 34256ca7bff46f911cf20e8b94278fbd09175746; generated E45 instrumentation only. 30,000 tasks/seed with 80,000 calibration; mission-task trace from FULL and official aggregate CSV.

Definitions:
- **Pre-shock overlap**: fraction of MISSION tasks indexed <10000 assigned a node in the seed-specific, predetermined six-node affected mask (before the shock is applied).
- **Realized post-shock exposure**: fraction of MISSION tasks indexed >=10000 routed to affected nodes under CASPER_FULL, a policy-dependent descriptive quantity.
- **Added mean network latency**: sum(actual_network_ms - nominal_network_ms) / count(post-shock mission tasks); calculate exactly from traces.
- **S3 FULL late_eta**: official results.csv late_eta.
- **S3 FULL late_far and late_air**: official output rates; no independent-task inference.
Compute seed-level Pearson and Spearman correlation (pre overlap vs post exposure, pre overlap vs late_eta, post exposure vs late_eta) as exploratory mechanism diagnostics ONLY. Include every seed; never filter or stratify post-hoc to produce favorable significance. Report all ten per-seed values, masks, counts, rates, and raw artifacts. Fail closed if any baseline or shock masks inconsistent or outputs diverge from official metrics; no causality claim about naturally differing seeds.
