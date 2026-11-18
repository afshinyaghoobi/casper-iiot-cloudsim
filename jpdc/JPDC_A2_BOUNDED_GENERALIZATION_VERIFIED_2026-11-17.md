# VERIFIED — Program A2 native 24-case SpaceShared vs FIFO-capacity-matched semantics

**Date:** 2026-11-17 America/Chicago (CI UTC 2026-11-18)
**Scientific status:** NEW GENUINE JAVA SIMULATION + TWO INDEPENDENT COMPUTATIONAL AUDITS PASS.
**CI run:** https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/44215741883
**Source commit:** 31a4acf167078ccbb255f01034630bca64ce40e8
**Artifact ID:** 14387238746
**Original GitHub artifact ZIP SHA256:** 1d29943e5e48d27f65eed186df23ff22d3dd7bdab381ebe63fca88dba1e3bb4b (also independently rehashed from downloaded original ZIP)
**Original native log SHA256:** 9fb08d07fe9741772b0de59a837046d0152362d3724da04daf02ccbc3d879391
**Primary audit JSON SHA256:** 433035fa66895fa2d47b8e48757e2edbe68849a2947c9ea79474a43e27b06266
**Independent audit JSON SHA256:** 83500b3b3a546fdfd72f409f46735310aaf8b679fad5e748429329a42011b96c
**Protocol prior to actual outcomes:** [A2 prereg](JPDC_A2_BOUNDED_GENERALIZATION_PREREG_2026-11-17.md) commit 5c3160aa5d5f97514048a206eb186f7368f3324e.

## Genuine fresh prospective native input and quality controls

New isolated Java class NativeA2BoundedGeneralization.java runs exact real CloudSimPlus 8.5.7 on Java 17. Two fixed synthetic arrival families (STAGGERED/BURSTY), three predetermined arrival jitter variants (S0–S2), two min-event-gap settings (1us/5ms), one/two-PE VM SpaceShared. **24 native cases and 288/288 actual Cloudlets completed**. Same native trace EXACT repeat; independent Python parser computes FIFO m-server reference from actual native observed submission timestamp/order, not nominal job delays; second separate implementation independently recomputes results. Both PASS. Original FGCS E42 and rejected Stage64 Git blob guards pass. No CASPER policy experiment.

First trial [run44215584921](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/44215584921) compilation failed on Java generic HostSimple List<PeSimple> vs List<Pe>; fixed host declaration without modifying preregistered workloads. Second [run44215672151](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/44215672151) compiled and actually executed all original native cases, then failed on six-column case-header parser unpacking (no impact on simulator inputs/results); corrected parser, did not change workload/Java simulation inputs. Third [run44215741883](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/44215741883) PASS both auditors. Preserve original failed jobs; no silent erasure.

## Predeclared measurements (all 24 native cases included)

Primary case-level statistic: maximum absolute reported native WAIT minus declared ideal deterministic FIFO m-server waiting time using the ACTUAL observed native scheduler submit order and requested service. Over 24 cases: **range 24.0–246.0 ms**, overall maximum **246.0 ms** in BURSTY_S2_5MS_P1. Median of 12 cell-level maxima for STAGGERED = **73.3055 ms** (range 24–171); for BURSTY = **87.0 ms** (range 25.005–246). These are *descriptive fixed synthetic variants*, not independent random source population statistics.

Predeclared deadline classification comparison uses **observed actual native submit timestamp + [25,50] ms**, not actual IIoT app deadlines. Across 288 paired native/reference job classifications, **86/288 disagree at +25ms** and **107/288 disagree at +50ms**. These are pairwise metric discrepancies under defined two models, NOT errors against measured real-world deadlines and NOT independent population samples.

| Native case | Max abs waiting difference (ms) | Deadline +25ms disagreements | Deadline +50ms disagreements |
|---|---:|---:|---:|
| BURSTY_S0_1US_P1 | 157.018 | 1 | 3 |
| BURSTY_S0_1US_P2 | 25.005 | 5 | 3 |
| BURSTY_S0_5MS_P1 | 118 | 1 | 3 |
| BURSTY_S0_5MS_P2 | 51 | 6 | 8 |
| BURSTY_S1_1US_P1 | 157.018 | 1 | 3 |
| BURSTY_S1_1US_P2 | 30.006 | 5 | 3 |
| BURSTY_S1_5MS_P1 | 118 | 1 | 3 |
| BURSTY_S1_5MS_P2 | 51.4 | 6 | 8 |
| BURSTY_S2_1US_P1 | 178.019 | 3 | 5 |
| BURSTY_S2_1US_P2 | 33.004 | 2 | 4 |
| BURSTY_S2_5MS_P1 | 246 | 2 | 5 |
| BURSTY_S2_5MS_P2 | 56 | 5 | 5 |
| STAGGERED_S0_1US_P1 | 87.011 | 4 | 5 |
| STAGGERED_S0_1US_P2 | 24 | 4 | 2 |
| STAGGERED_S0_5MS_P1 | 171 | 2 | 4 |
| STAGGERED_S0_5MS_P2 | 60 | 6 | 7 |
| STAGGERED_S1_1US_P1 | 87.411 | 4 | 5 |
| STAGGERED_S1_1US_P2 | 24 | 4 | 2 |
| STAGGERED_S1_5MS_P1 | 171 | 2 | 4 |
| STAGGERED_S1_5MS_P2 | 60 | 6 | 7 |
| STAGGERED_S2_1US_P1 | 86.611 | 4 | 5 |
| STAGGERED_S2_1US_P2 | 24 | 4 | 2 |
| STAGGERED_S2_5MS_P1 | 171 | 2 | 4 |
| STAGGERED_S2_5MS_P2 | 60 | 6 | 7 |

## Scientific claims permitted / prohibited

**Permitted:** Under the 24 specifically fixed synthetic configurations, the *native scheduler-reported* wait and deadline classifications differ from explicitly constructed same-input capacity-matched event-independent FIFO model; measurement depends on workload timing, event minimum and VM PEs. Trace/back-end inputs and auditor source are reproducible. Results now have broader experimental support than original single fixed three-job illustration.

**NOT permitted:** CloudSimPlus bug proven; native scheduler necessarily violates contract or strict general FIFO fairness; Python vs Java 30k parity passed; user-defined deadlines represent real-world IIoT; policy CASPER beats baseline; data are independent random source samples; 86/288 or 107/288 are independent p-value successes; exact mechanism of each discrepancy determined by event callbacks alone.

**Important methodological consideration:** Native wait/time accounting includes event-processing semantics that abstract FIFO reference intentionally omits. The observed difference is a model comparison and MAY be explained by timing/callback semantics, not faulty native source. Strong physical fidelity remains unresolved. Also do not call fixed deterministic jitter variants statistically independent original source seeds.

## Next paper work

**A2 actual execution and reproducibility DONE**, but before claiming publishable paper novelty, integrate results into full Introduction/Methods/Results/Discussion and compare with FGCS first manuscript plus relevant literature. Identify one or two representative event-transition traces for figures and discuss native service-duration inflation/update cadence; do not keep adding unnecessary factorials. A1 eligibility callback dynamic evidence [here](JPDC_A1_DYNAMIC_ELIGIBILITY_CALLBACK_VERIFIED_2026-11-17.md) is supporting, not central proof. Original 30k Java↔Python queue parity **FAIL** and Stage65 safety **FAIL** unchanged. Program B still reserved.
