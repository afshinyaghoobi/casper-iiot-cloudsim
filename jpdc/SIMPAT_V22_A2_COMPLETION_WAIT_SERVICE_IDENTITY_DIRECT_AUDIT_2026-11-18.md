# SIMPAT v2.2 — directly rechecked completion/wait/service accounting identity

**Immutable article title:** Queue-Wait and Execution-Time Semantics in CloudSimPlus 8.5.7: Implications for IoT Scheduling Simulation

**Date:** 2026-11-18. **Type:** new independent *static arithmetic audit* of previously archived A2 per-job data; **not** new simulation, independent empirical sampling, physical IoT validation, prospective hypothesis, mechanistic attribution, or new theorem. Main manuscript v2.2 intentionally unchanged.

## Grounded original data and calculation

Source: `jpdc/evidence/simpat_v857_original_2026-11-18/a2_derived_original_288_job_margins.csv`, 288 rows, 24 cases, generated from original A2 native Java log via `jpdc/audit_simpat_a2_per_job_completion_margins.py`, original A2 run [44215741883](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/44215741883). The CSV is part of the 14-file archived evidence mirror with SHA manifest in `jpdc/evidence/simpat_v857_original_2026-11-18/SHA256SUMS.txt`. This independent arithmetic pass directly read the complete committed CSV through the GitHub connector; it did not rerun Java and does not claim a fresh byte-level SHA verification or CI run.

For each matched job j, the *same native submission time* a_j is used by native wait clock (A3 checked matching source origins at logged resolution) and analytical FIFO. Let W^N, W^F denote measured and reference waits; let S^N be *native-reported total execution time*, and S^F be the requested CPU service used by FIFO. Provided the native logged identity C^N-a=W^N+S^N and the reference definition C^F-a=W^F+S^F hold, subtracting gives the exact **accounting identity**:

`(C_native - C_fifo) = (W_native - W_fifo) + (S_native_reported - S_requested)`.

This equation describes **reported model clocks** and **does not decompose causal mechanisms**. The original primary A2 auditor checked native completion = native wait + native reported execution time at logged precision. The current audit checked the three independent CSV difference columns using a JavaScript computation performed over every original row.

## Actual results of the current direct arithmetic check

- **288 rows / 24 unique cases**; maximum absolute residual `|(completion_delta_ms - wait_delta_ms) - (native_reported_execution_ms - requested_service_ms)|` = **2.4868995751603507e-14 ms** (CSV decimal-precision arithmetic).
- **Zero** residual violations at `1e-5 ms`.
- Native-reported minus requested service: **250 positive**, **0 negative**, **38 zero** with `1e-6 ms` matching tolerance. Mean **+3.821881944444444 ms**, median **+2.5995 ms**, maximum **+15 ms**.
- Per-job waiting difference: mean signed **+44.187763888888924 ms**, mean absolute **49.096097222222255 ms**; range **-79.4 ms to +246 ms**.
- Per-job completion difference: mean signed **+48.00964583333339 ms**, mean absolute **51.956597222222236 ms**; range **-76.998 ms to +252 ms**.
- In **39** cases wait and service accounting components have opposing signs (product below `-1e-8`); therefore component magnitudes cannot be added as if they were independent nonnegative 'causes'.
- By job-level absolute component magnitude: **243** had |wait delta| > |service delta|, **25** had |service delta| > |wait delta|, **20** tied within `1e-6 ms`. This is descriptive within the fixed synthetic dataset, not causal dominance.
- By 1PE/2PE: 144 observations each; service-report mismatch positive in **119** 1PE and **131** 2PE observations.

## Interpretation and publication integrity

1. The identity is analytically mandatory given the recorded clock definitions: **it is not a new discovery, theorem, novel scheduling method, or independent model validation**. It is valuable as a *measurement-consistency diagnostic*, and exposes that both wait and service-accounting differences contribute to observed completion-model differences at the bookkeeping level.
2. Zero residual proves internal numerical closure of these archived derived columns, **not** that the native runtime adheres to a physical service-time model, nor that one particular callback causes the discrepancy.
3. In particular `getTotalExecutionTime` is a **postcompletion reported simulator quantity**; it must not be used as future job service information available to an online scheduler. Claiming 250 Cloudlets physically executed more CPU work is unwarranted.
4. The sign distribution is a fixed deterministic-data observation, not a population frequency. No inferential p values or confidence intervals.
5. A strong method-level novelty argument **cannot be based on this identity**. Its role is quality assurance and precise interpretation; a transferable, non-tautological semantic-validity method remains unestablished.

## Current gate

- Existing exact-title v2.2 remains frozen and archived; primary A1/A2/A3 native results preserved; predeclared failed input-only 5ms>1us H (1/4 vs 1/4) and historical 30k Java/Python parity FAIL and Stage65 safety FAIL preserved.
- **Scientific originality for full SIMPAT original research = HOLD**. No DOI minted, no authorship approval, no publisher submission, no changes to Program B.
- Recommended next action: audit if the paper currently *implies* that native-reported service is requested CPU work or that waiting-gap magnitude explains deadline-model disagreement. Tighten only genuinely misleading claims, with author sign-off. Avoid running additional near-duplicate synthetic grids.
