# JPDC Stage9 verified — exact two-intercept envelope and false-drift shock detection (2026-11-05)

## Outcome and scope
This stage provides **mathematically exact compression of age-aware Lipschitz residual interval evaluation**, plus a deliberately adversarial test that **falsifies a gentle temporal-drift assumption under a sudden network shock**. It does not show a new scheduling algorithm's deadline benefit, and no scientific seeds or native physical policy workloads were run. We maintain three **distinct validation contracts**, so a compact arithmetic summary cannot silently be promoted to a historical-model guarantee.

- Prior complete first CASPER FGCS E42 Git blob SHA **`34256ca7bff46f911cf20e8b94278fbd09175746`** and E4.6 unchanged.
- The pure Stage8 full-ledger age-aware model stays unchanged.
- Prior independent scientific full original 10seed Python FULL-vs-GREEDY sign p=1.000 NONsignificant; Java original 10seed E17 sign p=.0625 NONsignificant; selected four-seed ETA factorial p=.125 NONsignificant; original Java→Python strict-FCFS physical queue equivalence test FAILED max waiting-time difference9.1214ms>preregistered5ms. None changed.

## Registration and exact algebra
Before the first Stage9 test, the design was registered in `jpdc/STAGE9_INTERVAL_COMPRESSION_AND_SHOCK_PREREG_2026-11-05.md`, commit **`3c485a1f0c32f09c4b7f6a847addcb0881beb677`**.

For previously DELIVERED node-specific reports `(measurement-generation m_i, E2E delivery d_i, observed excess y_i)`, fixed externally justified drift rate L and measurement error epsilon, the Stage8 numerical interval at decision t>=all delivered times is:
`LOW(t)=max(0, max_i[y_i-epsilon-L(t-m_i)])=max(0,A-Lt)`;
`HIGH(t)=min_i[y_i+epsilon+L(t-m_i)]=B+Lt`,
where `A=max_i[y_i-epsilon+L m_i]`, `B=min_i[y_i+epsilon-L m_i]`. Hence interval **evaluation** from delivered reports is exact from two extremal intercepts per node (O(1) per node query, O(21) for all nodes), along with count/newest generation diagnostic fields. This mathematical reduction is basic algebra, **not original theoretical novelty**.

Three implementations in new separate pure Python source `jpdc/two_intercept_network_envelope_stage9.py`, commit **`10c95a8962b28827a41c08f8ec90f65d49454e9b`**:
1. `audited`: delegate incoming reports to original Stage8 full history pairwise compatibility checker, then maintain exact A/B summary. O(1) interval query, but report history still O(n) memory and every new report can cost O(n); **do not claim bounded total memory**.
2. `chronological`: require each newly delivered measurement's **generation timestamp** is >= previous maximum generation timestamp on that node. For this restricted order, historical pairwise compatibility can be checked against existing two extrema alone:
    `y-Lm <= B+epsilon` and `y+Lm >= A-epsilon`. The implementation rejects any future delivered older-generated node measurement, rather than falsely treating it as recent. Under this restricted model, memory O(21) and each node's report update and query O(1), notwithstanding Python arithmetic/computation and 21-node selection. Real E2E delivery order does NOT generally guarantee monotone measurement generation, so this cannot be deployed as if it held automatically.
3. `unaudited`: accepts generation-order permutations and maintains exact numerical interval after ingestion from O(21) extremal summary memory, **but cannot certify that historical data all obey fixed drift/error assumptions**. Returns explicitly `historical_consistency_audited=False`. An empty numerical interval may still be detected, but a seemingly nonempty interval at a late time is not proof there was no contradictory source-time pair.

### Shock and task-size falsification
A toy latent network risk jump `r(0)=0` to `r(10)=20ms` with fixed drift L=.1 ms/ms and epsilon=0 violates the assumption by **19ms** (observed 20ms vs maximum admitted 1ms). Both full-ledger audited and chronological modes reject the second report **without altering prior accepted model state**. By contrast, unaudited arithmetic mode can retain both and at sufficiently late decision time return a widened nonempty interval, which is explicitly **not** historical evidence of model validity. A second fixture uses different task sizes at the exact same node and generation timestamp, with 3ms and 18ms observed network excess at epsilon=0; a single node-time latent excess cannot explain both. This is relevant to IIoT task-size and network-transfer heterogeneity and underscores why the Stage8 abstraction must be validated against task-specific physical network behavior.

### Executable CI evidence
`jpdc/test_two_intercept_network_envelope_stage9.py`, commit **`47199acec5093af3653709a966bd83f6c718e33b`**, validates:
- 21-node empty reports unknown (HIGH=infinity), no fraudulent zero-risk certification.
- Exact A/B vs Stage8 full ledger interval parity across all 21 nodes with multiple valid reports.
- Audited support for late-delivered older-generation data and explicit chronological restriction.
- Abrupt shock/unknown historical compatibility detection and task-size inconsistency rejection.
- **1001 independently constructed, mutually consistent synthetic E2E feedback reports**: original Stage8 full audit stores1001 reports, compact chronological and unaudited summary store zero raw ledger reports with identical age intervals at the query time. State has a constant 105 slot (5 fields×21 nodes); does not mean all runtime computational or historical verification costs vanish for unrestricted delivery.
- No future E2E reports are used, selection explicitly marks unaudited estimates as unverified.

`.github/workflows/jpdc-stage9-interval-compression-shock-gate.yml` commit **`abef813023a849e0fec09bdaa3436bbff642c0f0`** ran the Stage9 new fixtures and the original Stage8/7 validation tests.

**REAL GitHub Actions run `42073466009` COMPLETED SUCCESS**, job **`127407320072`**, original artifact **`13436613856`**. Markers from original logs:
- `PASS all-node exact O(1)-query age interval parity versus full Stage8 ledger`
- `PASS out-of-order measurement supported with audit; chronological compact contract rejects`
- `PASS abrupt-shift contradiction detected in audited modes; unaudited future interval cannot certify history`
- `PASS incompatible task-specific excess requires broader physical model/error budget`
- `PASS 1001-feedback all-node envelope parity; audited ledger grows, chronological summary constant`
- `JPDC_STAGE9_EXACT_COMPRESSION_AND_SHOCK_FALSIFICATION_PASS`
- `JPDC_STAGE9_FROZEN_INTERVAL_SHOCK_AND_PRIOR_CONTRACTS_PASS`

## Scientific decision
This stage **improves auditability and theoretical/engineering separation**, but does not validate a new algorithm for JPDC and demonstrates a genuine weakness in the proposed global time-Lipschitz latent network excess assumption under sudden shocks. Do not retune drift L after observing a shock and claim the original model verified; model a piecewise-stationary change-point or explicit fault process and task-size-specific network dynamics first, then preregister a distinct model/test. A future physically meaningful dispatch scheme must (i) identify whether node-time excess r_j(t) is even a useful observable across different task sizes and upstream/downstream network timing, (ii) establish a principled externally available drift/noise bound, (iii) support delayed out-of-order generation times without inventing historical audit guarantees, and (iv) compare with first FGCS CASPER and relevant delayed-bandit/network-aware schedulers on independent workload/traces. Original native source strict FIFO remains different from Java CloudSimPlus SpaceShared and has no YAFS validation.

## Repo links
- Protocol: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/blob/jpdc-seed0-repro-20261024/jpdc/STAGE9_INTERVAL_COMPRESSION_AND_SHOCK_PREREG_2026-11-05.md
- Source: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/blob/jpdc-seed0-repro-20261024/jpdc/two_intercept_network_envelope_stage9.py
- Fixed tests: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/blob/jpdc-seed0-repro-20261024/jpdc/test_two_intercept_network_envelope_stage9.py
- Original CI: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42073466009
- Artifact: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42073466009/artifacts/13436613856
