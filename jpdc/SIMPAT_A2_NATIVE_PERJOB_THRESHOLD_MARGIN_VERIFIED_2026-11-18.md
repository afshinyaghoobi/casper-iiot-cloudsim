# SIMPAT A2 original-log per-job signed completion and deadline margins — 2026-11-18

**Article locked exact user title:** Queue-Wait and Execution-Time Semantics in CloudSimPlus 8.5.7: Implications for IoT Scheduling Simulation
**Status:** Genuine new **POSTHOC DERIVED** job-level observation of the already finished **original 24-case, 288-job native Java A2** dataset. No new Java execution, independent source sample, physical IoT evidence, or causal result.

## Primary-source acquisition and evidence
- Downloaded **original** workflow artifact ID14387238746 from verified [A2 Java run44215741883](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/44215741883), exact original ZIP SHA256 independently rehashed **1d29943e5e48d27f65eed186df23ff22d3dd7bdab381ebe63fca88dba1e3bb4b**. The original `native.log` SHA256 is **9fb08d07fe9741772b0de59a837046d0152362d3724da04daf02ccbc3d879391**.
- [Full auditable source](audit_simpat_a2_per_job_completion_margins.py) re-parses each `A2_SUBMIT,AFTER` and `A2_FINISH` line using the original observed scheduler submission order, reconstructs the event-independent PE-matched FIFO recurrence using **original requested service**, extracts native and FIFO completion time per job and derives signed completion differences and synthetic threshold margins.
- [SUCCESS CI run44352984149](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/44352984149) independently re-downloads the ORIGINAL archived run into GitHub Actions (no simulated rerun), validates the original native-log SHA, verifies 288 job records, recomputes all24 published maximum wait gaps, all 24 +25/+50 classification totals, full mean absolute wait49.0960972223ms, and exports complete **288-row per-job CSV** plus signed-margin JSON; derived artifact ID **14448254073**, name `simpat-a2-verified-original-perjob-completion-margins`. This artifact can expire; reproducibility script is committed permanently. GitHub Actions result check is a provenance/data consistency audit, not an independent validation with real IoT data.

## Exact threshold semantics
For job j, at artificial threshold offset d∈{25ms,50ms}, define:
`M_native(j,d)=C_native(j)-(a_native_submit(j)+d)`
`M_FIFO(j,d)=C_FIFO(j)-(a_native_submit(j)+d)`
where deadline **miss** in each model uses the exact previously published numerical tolerance `M>1e-8ms`. Disagreement occurs iff Boolean miss flags differ. `M_native-M_FIFO=C_native-C_FIFO` is an algebraic identity, not novel simulation science. The *fraction of threshold disagreements* depends not only on absolute per-job timing differences, but whether the threshold lies between the native/FIFO constructed finish estimates.

## Reproduced totals
| Metric | A2 fixed jobs |
|---|---:|
| Native cases / jobs | 24 / 288 |
| Deadline +25ms model disagreements | **86/288** |
| Among the +25ms disagreements: native finish later than FIFO | **73** |
| Among the +25ms disagreements: native finish earlier than FIFO | **13** |
| Deadline +50ms model disagreements | **107/288** |
| Among the +50ms disagreements: native later than FIFO | **102** |
| Among the +50ms disagreements: native earlier than FIFO | **5** |
| 1PE jobs, deadline+25ms disagreements | 27 / 144 |
| 2PE jobs, deadline+25ms disagreements | 59 / 144 |
| 1PE jobs, deadline+50ms disagreements | 49 / 144 |
| 2PE jobs, deadline+50ms disagreements | 58 / 144 |

These count different **model predictions at chosen synthetic thresholds**, **not physical deadline failures**. PE groups here are selected combinations of fixed workload fixtures, not random samples or isolated causal effects.

## Concrete mechanism at fixed A2 BURSTY_S0_1US
- **One-PE configuration:** largest absolute wait gap **157.018ms** but only **one** +25ms classification disagreement, job ID **1**. Many other jobs finish after the synthetic deadline under **both** models, despite large absolute completion gaps. Both outcomes correspond to the same Boolean class, so they do not increase disagreement count.
- **Two-PE configuration:** largest absolute wait gap shrinks to **25.005ms**, but **five** +25ms classification disagreements, jobs **2,4,5,6,7**. In each flagged job, the native finish is later than its artificial deadline, and FIFO finish is before it. They straddle the threshold despite smaller absolute gaps.
- This **explains the specific observed ranking reversal**: changing the capacity of the tested configurations changes the location of the two estimated finishes relative to the threshold. Worst-case wait disagreement is not a monotonic substitute for thresholded completion disagreement in the original fixed cases. This is a deterministic *observed counterexample* to a possible metric-surrogate assumption, not a causal demonstration that capacity raises physical IoT deadline errors.
- At +25ms, for the entire fixed 288-jobs data, 73/86 model-discordant jobs had later native completion and 13 had earlier native completion relative to FIFO. These are directions of model-completion difference, not observed actual service errors.

## Editorial limits and next scientific decision
The identity that a fixed threshold must lie between two completion-time predictions to cause a classification reversal is algebraic; it is not a new theorem or sufficient novelty for a full SIMPAT article. The specific empirical pattern is **posthoc**, shares original A2 synthetic data, lacks independent or physically grounded validation, and uses completion estimates from knowingly nonequivalent models. It offers a useful *practical diagnostic framing*, not proof of a novel queueing paradigm, unique causal event mechanism, or CloudSim defect.

**Go/no-go:** current first-paper SIMPAT full-length originality gate remains **HOLD**. A stronger claim would require a justified independent, preregistered methodology experiment (not cosmetic extra seeds) or a new generalizable model relationship. Further expansions are not automatic. Keep author approval, FGCS overlap disclosure, AI-assisted Methods/declarations and archive permanence as separate mandatory gates. Original strict30k Java–Python parity FAIL and Stage65 safety FAIL unchanged. Program B separate RESERVED/NOT STARTED.
