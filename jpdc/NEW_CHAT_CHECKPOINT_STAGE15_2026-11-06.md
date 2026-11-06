# JPDC handoff checkpoint after Stage15, 2026-11-06

## Last verified
1. Original Stage14 native dev seed84 negative total MISSION result: [successful Stage14 run](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42184744223), archived pre/post audit [42184993467](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42184993467), documented in `STAGE14_NATIVE_PHYSICAL_PILOT_VERIFIED_NEGATIVE_2026-11-06.md`. Former run with variable alias bug failed; corrected, evidence preserved.
2. Stage15 frozen congestion guard 2ms nominal detour, source dev seed85, S2/S3 x5 arms, 120,000 dependent task-policy records in one seed, exact duplicate, successful [42185326575](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42185326575). [Detailed negative+positive report](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/blob/jpdc-seed0-repro-20261024/jpdc/STAGE15_GUARDED_PHYSICAL_DEV_SEED85_VERIFIED_2026-11-06.md): S2 guarded total22 vs FULL20, S3 guarded5 vs FULL8. This does not establish expected superiority, novelty or cross-simulator validity.
3. Separate Stage15 nominal-detour/probe unit gate [42185883795](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42185883795) SUCCESS marker `JPDC_STAGE15_GUARD_UNIT_CONTRACT_PASS`, also Stage13 baseline fixtures pass.

## Frozen assets
- `jpdc/congestion_guarded_freshness_stage15.py` prototype; guard predicts task-dependent nominal queue-aware latency and restricts fresh choices within +2.0ms of greedy. E2E-only feedback, <=1% NORMAL probe, no probe MISSION. Neither conformal certificate nor externally calibrated network assumption.
- `jpdc/independent_physical_guarded_freshness_stage15.py` clone, which leaves original E42/Stage6/Stage11/Stage14 files alone.
- `jpdc/STAGE15_CONGESTION_GUARDED_FRESHNESS_PREREG_2026-11-06.md` registered before data.
- E42 frozen Git blob `34256ca7bff46f911cf20e8b94278fbd09175746`; E4.6 untouched.

## Scientifically necessary next work
A. Independent related-work novelty audit (active probing, delayed feedback, freshness-aware scheduling, nonstationary cloud-edge IIoT; do not rename standard methods novelty).
B. Preregister a confirmatory disjoint paired multi-seed cohort with seed values not previously used anywhere in project, without seed hunting; lock frozen Stage15 policy, thresholds, scenarios, primary TOTAL MISSION miss endpoint, statistical plan and interval presentation. Need multiple source-level replications, not task-level fake n.
C. Add independent policy/physical simulator fidelity work. Existing Python strict-FCFS vs Java CloudSimPlus SpaceShared mismatch (9.1214ms >5ms gate) means no engine parity claim. External traces or validated independent simulator necessary to strengthen JPDC prospects.
D. Evaluate S2 weakness and S3 strengths, probe cost and congestion at node level; do not discard S2 or only show postshock positives. No JPDC submission or acceptance probabilities yet.
E. Verify reproducibility, software-release/data protocol and research-paper ethics, explicitly distinguish FGCS CASPER vs JPDC independent algorithm.

## Scope and strategy
User explicitly chose **JPDC only**, no CCGrid submission or splitting contribution. No deadline-driven rush; prioritize a defensible journal paper. Current Stage15 is developmental and promising only conditionally under S3. Don't claim success without independent multi-seed external validation.
