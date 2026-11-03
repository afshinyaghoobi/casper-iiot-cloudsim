# Controlled mask placement experiment: preregistered protocol
Date: 2026-11-03. This is a **new exploratory mechanism intervention**, not a second confirmatory attempt on the failed holdout hypothesis.

## Independent seed indices and experimental construction
Fix unused seed indices **40, 41, 42, 43** before execution; no replacement by observed results. The existing 0–39 results are excluded from this new experiment. Each seed's S3_HIDDEN_NETWORK_50LOSS simulation has 21 nodes, 6 degraded, bandwidth retained 50%, cal 80000 and 30000 deployments. First run original unaltered generated-E45 campaign with mission task routing instrumentation to measure the **pre-shock** (task index <10000) node frequency for CASPER_FULL. Construct two predeclared 6-node damage masks:
- LOW: six nodes with *fewest* pre-shock mission assignments; tie-break numeric node ID ascending.
- HIGH: six nodes with *most* pre-shock mission assignments; tie-break numeric node ID **descending**, by taking the last six elements of the common list sorted on (count, node ID). This guarantees no LOW/HIGH overlap even with many zero-count nodes.
No decisions are based on post-shock outcomes, quality of certificates, or eta. Because only six selected from 21, LOW and HIGH are disjoint by sorting (low=first six, high=last six of the same sorted list). No mask retuning based on results.

Then run the identical frozen scientific seed with the LOW and HIGH masks (two separate full CloudSim simulator runs) by a strict, generated-E45-only intervention to `affectedMask` applied **identically to all eight policies**. Verify all masks exactly 6/21 and correct 2x network delay postshock only on affected nodes; pre-shock zero additional delay. Maintain original E42 hash `34256ca7bff46f911cf20e8b94278fbd09175746` and do not modify E4.6. Only 12 simulator runs (4 baseline + 4 LOW + 4 HIGH). All planned runs are to be reported, including failures.

## Primary descriptive checks and outcomes
1. Manipulation check: HIGH *pre-shock overlap* > LOW pre-shock overlap, and HIGH *realized post-shock mission exposure* > LOW. Report numerical differences including failures/violations. This tests the experimental manipulation, NOT a hypothesis about scientific significance.
2. Mechanism: HIGH minus LOW late_eta, FAR, AIR, DVR, FWC, and mean added network delay in CASPER_FULL; keep all four seed pairs (seed independent unit).
3. Compare LOW/HIGH with original random mask but do not use it as a confirmatory benchmark. Report per-seed masks and full official CSV.
4. Check that original pre-shock mission node counts from the LOW/HIGH runs equal baseline at least for FULL (unless queue/order effects legitimately differ); if they do not, explicitly report and investigate, without silently omitting any seed.
5. Any sign tests are exploratory, two-sided and marked low-power; do not claim confirmatory inference or treat individual tasks as independent replicates.

Distinguish pre-shock placement criterion (set before applying the shock) from post-shock realized exposure (policy-dependent mediator). Design cannot be interpreted as random sampling of masks, and uses the same seed across mask variants to compare controlled exposure contrast, not estimate unbiased population-average random-mask efficacy.
