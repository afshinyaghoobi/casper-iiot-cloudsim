# SIMPAT 8.5.7 original native evidence: persistent Git mirror and provenance — 2026-11-18

**Exact author-approved article title**: Queue-Wait and Execution-Time Semantics in CloudSimPlus 8.5.7: Implications for IoT Scheduling Simulation

This directory permanently tracks the **original run bytes** and source-derived measurements that were previously accessible mainly as **time-limited GitHub Actions artifacts**. The original native Java experiments were **NOT rerun for this archival step**. A separate workflow fetched original run artifacts, checked **predeclared exact SHA-256 hashes**, checked duplicate native runs byte-for-byte, checked source-derived counts including an **unsuccessful preregistered hypothesis**, and committed canonical primary files to Git. The successful archive workflow is [run44406625844](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/44406625844); verified Git archive commit **95424c68d8e3824c76c0a249cec6b0c5e3491184**.

## Frozen experiments and primary run provenance

| Experiment | Original genuine Java / source audit run | Persisted primary file | SHA256 |
|---|---|---|---|
| A2 original 24 cases / 288 jobs | [44215741883](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/44215741883) | `a2_original_native_288jobs.log` | `9fb08d07fe9741772b0de59a837046d0152362d3724da04daf02ccbc3d879391` |
| A3 actual native datacenter arrival clock audit | [44228414078](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/44228414078) | `a3_original_arrival_clock_288jobs.log` | `c3a978e3e19ec577e752ca31e32da3226ddb05c1fa435577ad8f48d3244e6022` |
| A1 passive actual waiting-promotion method | [44359114031](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/44359114031) | `a1_original_sixcase_wait_promotion.log` | `18b39fb536ae863ea665067f0318a285252ea2c5199792cb3362aa4a5a989abf` |
| A1 source-controlled end-of-update rescan TREATMENT | [44381766155](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/44381766155) | `a1_original_sixcase_rescan_treatment.log` | `af80c4a83caf8542cc6467493252be0d38c1c42f48a313fa4e45fcc52f0f2f55` |
| A1 new 8-case source-predicate run (all 24 tasks) | [44391376042](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/44391376042) | `a1_new_eightcase_original_native.log` | `c4bd49c77c488626fb027831bc8704b34db53f0d34845e1f01fc278ca3438c02` |

Source/audit JSON files for those five experiments are preserved alongside logs. The 6-case rescan CONTROL trace is exactly byte-identical to the A1 passive waiting-promotion log; it was independently validated at archival time. A2 native repeats, A3 native repeats, A1 passive repeats, A1 treatment repeats, and eight-case native repeats were checked with bytewise comparisons, **not simply matching summary totals**. The original A2 native log and A3 original-control log are also byte-identical.

## Canonical derived result files (NOT new experiments)
- `a2_derived_original_288_job_margins.csv`: per-Cloudlet native/FIFO requested-service completion and artificial threshold margins, reconstructed from immutable A2 native Java log via [Python auditor](../../audit_simpat_a2_per_job_completion_margins.py) at [run44352984149](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/44352984149). Exactly **288** job rows; source-derived, retrospective, not physical ground truth.
- `a2_derived_51_threshold_sweep.csv`: 51-point **posthoc** artificial submit-offset threshold sensitivity from 0–250ms step 5 via [auditor](../../audit_simpat_a2_threshold_sensitivity_grid.py) at [run44354321501](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/44354321501). Two-original-threshold outputs 86/288 and 107/288 disagreements are **differences of model classifications**, not real IoT missed deadlines.
- `SHA256SUMS.txt` in this folder: SHA256 for **all fourteen** canonical tracked .log/.json/.csv files; from repository root verify with `cd jpdc/evidence/simpat_v857_original_2026-11-18 && sha256sum --check SHA256SUMS.txt`. The manifest was generated in successful GitHub CI from exact downloaded bytes and verified after commit.

## Preserve negative scientific results
The eight-case source-predicate matches two true positive and six true negative events **within a hand-designed set**. A separate frozen input-only claim **FAILED**: the number of anomalies for 5ms minimum-event interval was **1/4**, identical to **1/4** for 1μs. The predicate uses before-submit native state that may directly reflect documented native admission logic. This is **NOT 100% general predictive accuracy, not proof of new scheduling algorithm and not independent IoT validation**. Original historical 30k strict Java/Python cross-runtime parity **FAIL**, Stage65 safety **FAIL**, explicitly retained.

## Important distinctions: Git archival is not a journal archive DOI
Git tracking and commit hashing make these exact bytes available even after normal GitHub Actions artifact expiration as long as the branch and Git history remain accessible. **The repository is mutable and can be deleted or history-rewritten**, so this is a *persisted source-controlled evidence mirror*, not a guaranteed perpetual archive or independently minted DOI. For publication permanence consider a locked GitHub release and external archival repository (e.g. Zenodo) **only after the author explicitly authorizes repository publishing and a DOI is actually created**. No DOI or external institutional deposit is claimed. The article remains scientifically under SIMPAT full-submission **HOLD** for substantive novel modelling contribution and coauthor/publisher approvals.

**Future CASPER Program B remains separately RESERVED/NOT STARTED**; none of these source logs establish policy improvements, physical performance or real IIoT outcomes.
