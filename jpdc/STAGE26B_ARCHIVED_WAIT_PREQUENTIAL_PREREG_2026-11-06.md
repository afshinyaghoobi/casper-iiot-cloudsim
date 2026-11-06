# JPDC Stage26b — original Stage25 immutable artifact causal prequential replay prereg (2026-11-06)

## Scope and already-known data
Original successful Stage25 artifact [42254782412](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42254782412) contains exact 48k WAIT-only signed residual source labels from **ONE already-examined development seed89**. Stage26 controller unit success [42268358913](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42268358913). This is a **post hoc exploratory replay of archived data**, not independent test, not statistical coverage guarantee, not Stage24 total nonnetwork-error calibration.

## Frozen replay before running
Each one of the four immutable policy/scenario traces is individually reconstructed into exactly 24k dispatch/CPU-finish timestamped events (12k of each). At same timestamp CPU finish event priority 0 and dispatch priority 2, matching the physical source event-loop. For each dispatch:
1. Query `CausalWaitCalibrator` at its dispatch timestamp, task class and actual telemetry-age available at dispatch; archive prediction and whether a central signed WAIT error interval is available; **do not access actual_wait or signed residual** while issuing query.
2. Add the immutable task dispatch record, with dispatch-time backlog only.
For each CPU finish, after its dispatch has occurred:
3. Pass actual service start, CPU finish and actual wait to the calibrator; require identical signed error with original stored trace. No network feedback or future CPU finish information may enter the calibration.
After full replay, compare issued predictions against saved true future labels offline only, recording sample count, availability, conditional **prequential empirical interval inclusion rate** per policy/scenario and task class/telemetry-age bucket. Record number and sign of under/over-coverage and max violation. Never convert these empirical counts into a `certified=True` Stage24 error bound.

## Integrity and expected limits
Complete 12k labels/arm, exactly causal event ordering, chronological replay, full original Stage25 task ID and residual parity, no new source simulation, no false independent n=48k; all archived work dependent on one seed. Rerun byte-identical. Absence of samples leads to abstention; lack of exchangeability, variable queue contexts and rolling calibration mean no 90% guarantee. If achieved rate is poor or uneven, preserve that negative result. Use seed89 forever as DEVELOPMENT only.
