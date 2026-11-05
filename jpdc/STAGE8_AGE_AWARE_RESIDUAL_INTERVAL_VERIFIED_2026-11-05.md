# JPDC Stage8 age-aware residual intervals — conditional math and tests VERIFIED 2026-11-05

## Summary and research status
A standalone **assumption-conditional age-aware network-risk interval prototype** is now implemented and verified through actual GitHub Actions. It is not an empirically demonstrated new scheduler with superior deadlines, not a novel uncertainty-bound theorem, not a statistical guarantee under arbitrary drift and **not yet integrated into full physical Stage6/7 independent simulator**. No seed-based scientific experiment was run. The original frozen Java E42 source git blob `34256ca7bff46f911cf20e8b94278fbd09175746`, E4.6, original independent Stage1–7, original holdout results and failed physical equivalence test remain unchanged.

The protocol `jpdc/STAGE8_AGE_AWARE_RESIDUAL_INTERVAL_PREREG_2026-11-05.md` committed BEFORE tests at **`979aa2a9629d12105d75caed7de4dff4692fe2e5`**. Core pure Python module `jpdc/age_aware_network_interval_stage8.py` commit **`4c11abb20a7328f15868287b7c060fcfe5b8576c`**; adversarial unit `jpdc/test_age_aware_network_interval_stage8.py` commit **`70b3238175411686a87817351937d2869dc41a88`**; CI `.github/workflows/jpdc-stage8-age-aware-interval-gate.yml` commit **`dc98632095f95dd85f9a730dcf405b4e3e25af1b`**.

## Definition and proof boundary
Assume each node has unknown nonnegative network excess `r_j(t)`, bounded drift `|r_j(t)-r_j(s)| <= L_j |t-s|` and measurement error `|y_i-r_j(m_i)| <= epsilon_j` at measurement **generation timestamp** `m_i`. A report is not visible until end-to-end delivery time `d_i >= m_i`. The externally justified numbers `L_j, epsilon_j` are required; the real workload and original generator have **not** been shown to satisfy them. For each already delivered observation at decision t:
- `lower_ij(t)=max(0,y_i-epsilon_j-L_j(t-m_i))`;
- `upper_ij(t)=y_i+epsilon_j+L_j(t-m_i)`.

Intersect all available reports for the node: `LOW_j=max_i lower_ij`, `HIGH_j=min_i upper_ij`. Triangle inequality proves conditionally `LOW_j<=r_j(t)<=HIGH_j`. If no delivered report, LOW=0 and HIGH=infinity, **not** zero risk. If two observations cannot be mutually explained under the fixed drift/noise assumptions, the code raises **AssumptionViolation**, without committing the contradictory report. Out-of-order **measurement generation** reports delivered later are valid, but cannot be treated as newer measurements. Future deliveries never enter a prior decision.

The pilot policy chooses `argmin_j(pred_j+HIGH_j)` over nodes with finite HIGH, lowest-node ID tie; when all nodes are unknown it nominally falls back to greedy with identifiable=False, infinite network margin and NO credible total-latency certificate. It provides informational coverage and a **conditional one-step exogenous** regret ceiling `(pred_chosen+HIGH_chosen)-min_j(pred_j+LOW_j)`, requiring exact nominal pred and `true_latency_j=pred_j+r_j`, and **not** a result for endogenous 21-node queue interactions or actual deadline miss. A finite selected interval when other nodes unknown does **not** establish best-node identification.

The source currently stores *all* delivered reports and scans them, so state memory is O(number of reports) and each 21-node decision is O(total prior reports). This is deliberately transparent for the proof fixture, not a production scheduler. The synthetic Stage6 32-entry rolling quantile is a **different policy**; no source-compatible new Stage8 physical dynamics are claimed.

## Real GitHub Actions verification
**Run `42043084906` COMPLETED SUCCESS**, job **`127298723959`**, artifact **`13421598365`**. The original E42 SHA passed, and tests passed:
- `PASS zero delivered reports => unknown high=inf, explicit uncertified fallback`.
- `PASS age measured from generation m=10, not feedback delivery d=20`; report y=8, m=10, d=20, now=30, L=.1, epsilon=1 => original predicted interval **[5,11] ms**.
- `PASS multi-report intersection, delayed out-of-order generation never looks fresh`.
- `PASS violated drift/noise assumptions fail closed without changing state`.
- `PASS conditional 21-node latent state covered; one-step exogenous regret bounded`.
- `JPDC_STAGE8_CONDITIONAL_AGE_AWARE_INTERVAL_UNIT_PASS`.
- Original Stage7 two-world finite regret counterexample and Stage6 probing unit regressions PASS.
- `JPDC_STAGE8_CONDITIONAL_MATHEMATICAL_AND_PRIOR_SOURCE_QA_PASS`.

### Major scientific caveats
1. **The assumption is strong**: within-node drift rates and bounded sample measurement error must be **externally substantiated**. Synthetic original Stage6 network shocks may be abrupt and violate modest Lipschitz rates. If the bound has no empirical grounding, the interval is formal arithmetic only.
2. Current observations are `observed network excess` rather than source-verifiable node latent risk; real task sizes/network RTT, contention and task class may vary, so per-node latent `r_j(t)` may not exist in this form.
3. This is a standard deterministic Lipschitz uncertainty propagation idea, **not an original theoretical novelty** without additional real innovation and literature clearance.
4. When no node has observed feedback, the fallback is **uncertified nominal greedy**. When some nodes have feedback, the controller conservatively excludes unknown upper-bound nodes and may starve them of evidence without a separate, realistic probing contract.
5. A one-step regret ceiling under exact exogenous nominal latency does not provide bound on future queue-coupled regret, realizable E2E latency, MISSION deadline miss probability, conformal coverage or safety.
6. Report storage unbounded; no efficient data structure, bounded-memory guarantee or online scheduler runtime benchmark yet.
7. No independent YAFS, real traffic dataset or even a physical native Stage8 deployment experiment; this stage validates a conditional decision primitive only.

## Historical unchanged science
- Original Java E17 10-seed disjoint exact two-sided p=.0625 nonsignificant.
- Original 4seed mask×eta factorial p=.125 nonsignificant.
- Native independent seed60..69 10seed CASPER_FULL vs PRED_GREEDY exact two-sided p=1.000 nonsignificant.
- Original physical strict-FCFS versus CloudSimPlus SpaceShared cross-engine equality gate FAILED max wait9.1214ms>preregistered5ms.
- Original FGCS paper already presents ranked CP, E17, health and probing, S3 network blind spot; no redundant CASPER algorithm novelty claim.
- Stage6 seed82 NEW + 1percent probing broadened S3 node feedback coverage 13/21→21/21 but MISSION misses increased 5→6; Stage8 has not reversed or rerun these results.

## Next justified technical work (not performed)
Validate **the model assumptions** against an independent measurable network environment, design time-stamped upstream/CPU/downstream events, and analyze bounded-memory implementations that preserve the confidence envelope and distinguish missingness from low risk. If a demonstrably distinct algorithmic contribution emerges, preregister new development and disjoint holdout studies before scientific efficacy claims. A broader prior-art review of Lipschitz bandits, nonstationary delayed feedback, and online conservative exploration is mandatory before journal originality claims.

## References within repo and GitHub
- Preregistered assumptions: `jpdc/STAGE8_AGE_AWARE_RESIDUAL_INTERVAL_PREREG_2026-11-05.md`.
- Real successful CI https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42043084906
- Original QA artifact https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42043084906/artifacts/13421598365
