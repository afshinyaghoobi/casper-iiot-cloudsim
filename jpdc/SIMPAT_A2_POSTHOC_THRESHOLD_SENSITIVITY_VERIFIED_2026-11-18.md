# SIMPAT — A2 posthoc threshold-sensitivity sweep with original source verification (2026-11-18)

**Author-approved exact title:** Queue-Wait and Execution-Time Semantics in CloudSimPlus 8.5.7: Implications for IoT Scheduling Simulation.
**Study type:** EXPLORATORY POSTHOC analysis of the already frozen original A2 native CloudSimPlus 8.5.7 24-condition × 12-Cloudlet experiment (288 fixed Cloudlet-condition observations). **No new Java simulation, independent sample, causal experiment, field IoT trace, predictive claim or preregistered threshold-sweep hypothesis.**

## Original source and actual execution
- **Original Java experimental run:** [44215741883](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/44215741883); native log exact SHA256 **9fb08d07fe9741772b0de59a837046d0152362d3724da04daf02ccbc3d879391**, original archive ZIP SHA256 **1d29943e5e48d27f65eed186df23ff22d3dd7bdab381ebe63fca88dba1e3bb4b**.
- **New code:** [audit_simpat_a2_threshold_sensitivity_grid.py](audit_simpat_a2_threshold_sensitivity_grid.py); checks original per-job 288-source outputs via [audit_simpat_a2_per_job_completion_margins.py](audit_simpat_a2_per_job_completion_margins.py). **GitHub Actions SUCCESS [run44354321501](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/44354321501)**: re-download original native artifact, verify original native-log hash, reconstruct each of 288 native and analytical FIFO completion time values, recompute all 24 case-level results, and exhaustively recompute a **declared retrospective grid 0,5,10,...,250ms (51 points)**. Derived ZIP **artifact14449682188** contains the full 51-row `a2_disagreement_threshold_sweep_0_250_step5.csv` and `a2_disagreement_threshold_sweep_audit.json`, which may expire; analytic scripts are permanent in GitHub.
- **Independent algebraic audit inside workflow:** each threshold's disagreement count is recomputed using both a strict-miss Boolean classifier and an interval membership test; all 51 totals must match. Numerical tolerance `1e-8ms` exactly matches original audit. This is a mathematical identity and data-integrity check, not independent physical correctness.
- **Grid was chosen during this posthoc continuation**, not in the original preregistered A2 protocol. The original two 25/50ms thresholds *were* specified before the native study, but this 51-point sweep was not. Do not call the sweep preregistered.

## Measured discrepancy totals vs synthetic deadline offsets

The number of job-condition observations whose completion classification disagrees between native CloudSimPlus and the explicit event-independent FIFO comparator:

| Artificial offset after native scheduler submit | One-PE configurations (144 fixed job observations) | Two-PE configurations (144 fixed job observations) | All (288) |
|---:|---:|---:|---:|
| 0ms | 0 | 0 | 0 |
| 15ms | 2 | 48 | 50 |
| **25ms (original A2)** | **27** | **59** | **86** |
| 40ms | 41 | 78 | **119** |
| **50ms (original A2)** | **49** | **58** | **107** |
| 55ms | 51 | 47 | 98 |
| 75ms | 64 | 22 | 86 |
| 100ms | 78 | 1 | 79 |
| 150ms | 57 | 0 | 57 |
| 200ms | 29 | 0 | 29 |
| 250ms | 14 | 0 | 14 |

All values are directly from the source-verified CI audit, not newly simulated outputs. **Within the 51-point fixed exploratory grid**, the largest total disparity occurred at **40ms (119/288)**; this is not a new deployment SLA, global mathematical maximum over continuous thresholds, or externally selected optimum. The sign of (two-PE count minus one-PE count) across the whole grid is **positive in 9**, **negative in 40**, **tie in 2** positions; the positive-versus-negative split is not a probability estimate because points in a grid are correlated and the 0–250ms range was chosen posthoc.

**Central interpretation:** the previously observed larger two-PE disagreement at 25ms (59 vs27) and 50ms (58 vs49) is **threshold-dependent**: at 55ms it reverses (47 vs51), and at 75ms two-PE discrepancy is lower (22 vs64). Thus no monotonic physical “more PE worsens deadline accuracy” or more PE always increases the model difference can be supported. These are completely different simulator/reference models and task sets under fixed artificial deadlines, not observed real service violations.

## Exact algebraic mechanism (not a novel theorem)
For task j and margin d, with native and reference submission time a_j shared:
`L_N(j)=C_N(j)-a_j`, `L_F(j)=C_F(j)-a_j`. Disagreement occurs when `(L_N(j)>d+epsilon) != (L_F(j)>d+epsilon)`, equivalently when `d` lies between the two completion offsets (correct endpoint convention with tolerance). The count at d is the **overlap depth of 288 intervals of completion offset differences**, not an additive score of average/max waiting error. This explains how a maximum waiting gap can decrease while thresholded disagreement count increases in particular configurations. The identity holds for **any pair** of arbitrary completion estimates and is therefore **not a new simulator algorithm, proof of discrepancy causal source, or substantive general simulation theorem by itself**.

## Journal contribution and next scientific gate
This sweep materially strengthens honest interpretation by exposing **threshold choice as an influential reporting dimension** in this synthetic task fixture. A defensible *evaluation recommendation* is to report the actual deadline margin policy and a sensitivity curve or threshold-range robustness analysis, rather than interpreting a single arbitrary deadline threshold as universal. However, this is a sound reporting practice already motivated by general decision theory and model validation, not shown to be newly invented here. The major **SIMPAT originality/significance gate is still HOLD**, with no proof this modest single-VM model-comparison study meets the journal's criteria. Resist increasing test-grid size without a concrete falsifiable contribution.

**Author and publisher gates still open:** verify FGCS CASPER earlier-paper status/overlap; all author identities/CRediT approvals, declared AI involvement, original publication record, conflicts/funding; durable original data archival; target-journal guide. A1/A2/A3 original values unchanged, original strict 30k cross-runtime parity FAIL and Stage65 safety FAIL unchanged, future Program B reserved.
