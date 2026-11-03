# E17 feedback detector replay: why S3 seeds 7 and 18 diverge (2026-11-03)

## Verified execution and provenance
- Final successful GitHub Actions run **41658004816** (two jobs, both SUCCESS), artifacts seed7 **13241260387**, seed18 **13239324890**.
- Generated E45 only: `jpdc/instrument_eta_feedback_generated_e45.py`, commit `6345efd`. Workflow `.github/workflows/jpdc-s3-eta-feedback-2seed-once.yml`, corrected validation commit `0baa782`.
- Earlier runs 41657526057 and 41657636231 failed *after* successful simulation because the trace validator assumed only CASPER_FULL logged feedback; generated E45 properly logs **both** adaptive policies (`CASPER_FULL`, `CASPER_ADAPT_NO_HEALTH`). The validated final run accepts both and checks provenance/record integrity. Original frozen E42 git blob `34256ca7bff46f911cf20e8b94278fbd09175746` verified by workflow; E4.6 also unchanged.
- Formal independent replay from event logs reconstructs `E17DualMemory` detector `deque<50>` for each policy: each score strictly > the per-seed reference q95 counts as an exceedance; alarm goes true on **12 or more exceedances in 50**. Check reported pre/post alarm booleans and transition ages against replay at every mission completion. **ALL event-level checks PASS** for both seeds and both adaptive policies. Replay script: `jpdc/audit_e17_feedback_detector.py`, commit `987ebc9` (same detector semantics); validated local audit table `e17_feedback_replay.csv`.

## S3 mission completion feedback evidence

| Seed | Policy | Pre exceeds / n | Post exceeds / n | Max exceeds per rolling 50 | First alarm task | Final eta |
|---|---|---:|---:|---:|---|---:|
| 7 | CASPER_FULL | 24/510 | 40/980 (4.08%) | 6 | Never | 1.0 |
| 7 | CASPER_ADAPT_NO_HEALTH | 25/510 | 40/980 (4.08%) | 6 | Never | 1.0 |
| 18 | CASPER_FULL | 40/483 | 965/1021 (94.52%) | 50 | 10165 | 3.0 |
| 18 | CASPER_ADAPT_NO_HEALTH | 38/483 | 961/1021 (94.12%) | 50 | 10165 | 3.0 |

Seed7 reference score q95=.386495092143; seed18 reference score q95=.348875647205. These are *within-seed* normalized score thresholds. E17 slow window=200, fast window=50, detector window=50, exceedance threshold=12, fast transition hold=200, eta clipped to [1,3]. Alarm is latched (`alarmEver`) and is never reset. Fast-memory contribution is only during transition hold, but sustained elevated slow-memory scores can maintain eta near 3 much longer, as in seed18.

## Mechanistic conclusion and boundaries
The **immediate difference in alarm activation is fully accounted for by observed score-threshold exceedances**: seed7 never met 12 of the most recent 50, while seed18 crossed the threshold at mission task 10165. This is a strict state-machine replay conclusion, not just a correlation between aggregate FAR and eta. It does **not** yet explain *why the underlying actual network/residual scores differ so much* between random seeds; affected-node selection and realized normalized latency deserve a separate trace-level check. Nor does alarm activation alone prove the cause of all eta changes: slow-memory quantiles can raise eta without an alarm and can keep eta elevated after the fast hold.

Difference in values at DISPATCH vs FEEDBACK time is expected due to asynchronous task completion. These measurements should never be presented as an independent replication study or as statistical confirmation of a deadline-violation benefit.

## Recovery
GitHub Actions: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41658004816
Each artifact contains `eta_feedback.csv` and the official `results.csv`; exact CSV columns are recorded in `jpdc/instrument_eta_feedback_generated_e45.py`. Local package available in generating session as `/mnt/data/jpdc_e17_feedback_mechanism_2026_11_03.zip`; do not assume local files persist across chats.
