# JPDC Stage22–23 verified — conditional dominance algorithm and first physical one-seed improvement only (2026-11-06)

## Provenance and exact workflow outcomes
- Stage22 theoretical and implementation preregistration `STAGE22_ROBUST_INTERVAL_DOMINANCE_PROTOCOL_2026-11-06.md` committed before tests. It explicitly includes falsifying **queue prediction error** counterexample, uncalibrated drift assumptions, and no JPDC performance/novelty guarantee.
- New controller `jpdc/robust_interval_dominance_stage22.py` with E2E-delivered-only network bounds: only switch from queue-aware nominal greedy g when candidate j has fresh accepted measurements, is not post-alarm unverified, and `p_j + Uextra_j + 1e-9 < p_g + Lextra_g`; MISSION additionally needs candidate upper latency <= deadline. No active probing. This yields conditional **T_j<T_g** only if network interval assumption is valid and nominal queue predictions have **zero error**; one easy queue error counterexample defeats an unconditional claim.
- Stage22 actual CI [42236837502](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42236837502) SUCCESS, all unit contracts, old Stage13/15/10 regressions and byte-identical rerun.
- Stage23 physical development protocol `STAGE23_ROBUST_INTERVAL_PHYSICAL_DEV_PREREG_2026-11-06.md` committed before any physical outcomes: original source-generated strict FCFS Python, 21 nodes, **one exploratory development seed88**, 80k calibration, S2/S3 x four arms PRED_GREEDY/CASPER_FULL/Stage15 guarded/Stage22 robust, 12k tasks per arm = 96k dependent task-policy records; do not infer as n96000. Exact frozen Stage6/Stage15 parity and twice identical full experiment demanded.
- Two Stage23 early runs failed **engineering gates**: [42237319307](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42237319307) incorrectly counted HIGH switches as MISSION in a diagnostic counter; [42237991721](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42237991721) passed new unit tests but incorrectly passed the new task-type argument to frozen Stage15 controller. Both patched **without changing decision objective, seeded workload, physical physics or preregistered protocol**. Preserve failures.
- Real fully successful [Stage23 physical run 42238156427](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42238156427), artifact `13515360049`, 8/8 arms, exact Stage6 and Stage15 policy parity, CPU/E2E preservation, zero explicit new-policy probes, exact native source rerun bit-identical `JPDC_STAGE23_NATIVE_PHYSICAL_REPRODUCIBILITY_PASS`, original E42 Git blob `34256ca7bff46f911cf20e8b94278fbd09175746` unchanged. Stage23 archival analysis first run [42239114961](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42239114961) failed due to local `argparse` variable shadowing **after printing all eight frozen results**, then successful after report-only fix in immutable-artifact-only [42239231025](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42239231025). None of these audit changes ran new physics or modified measured outcomes.

## Full original seed88 physical evidence — NOT statistical generalization

Every arm exactly 630 MISSION jobs of which 105 post task-index shock:

| Scenario | Policy | PRE miss /525 | POST miss /105 | TOTAL MISSION miss /630 | Mean E2E ms | Mean WAIT ms |
|---|---|---:|---:|---:|---:|---:|
| S2 compute | PRED_GREEDY |4|10|14|48.836933|2.736121|
| S2 compute | CASPER_FULL |5|4|**9**|49.177520|2.803352|
| S2 compute | Stage15 GUARDED |5|8|13|48.877856|2.840627|
| S2 compute | Stage22 ROBUST |4|10|**14**|48.836933|2.736121|
| S3 network | PRED_GREEDY |4|28|32|53.354531|2.715327|
| S3 network | CASPER_FULL |5|28|**33**|53.756916|2.683828|
| S3 network | Stage15 GUARDED |5|20|25|53.066888|2.721057|
| S3 network | Stage22 ROBUST |4|12|**16**|51.639658|**3.247831**|

New-policy network S3 vs CASPER_FULL **17 fewer total miss jobs (16 vs33), a descriptive 51.5% fewer in exactly one source seed**; vs Stage15 guarded **9 fewer misses (16 vs25)**, lower mean E2E latency but **higher mean queue wait**. S3 source damaged-node assignments after shock 317 robust vs1531 CASPER_FULL, but source mask only used for *offline diagnostic* and cannot be called oracle-free performance proof without independent threat/trace models. S3 robust controller switched from greedy **1681 of 12,000 dispatches**, including **73 MISSION**; 10,319 decisions had no valid robust-dominance verification. S2 robust switched **0/12000**, all 12000 unverified, exactly reproduces PRED_GREEDY miss and mean latency, **worse than CASPER_FULL by 5 MISSION misses**. Do not omit this S2 weakness or misdescribe all dispatches as certified.

## Scientific interpretation and remaining blockers
Promising **network-fault-specific developmental feasibility** in S3, but one seed is not independently reliable evidence. Under normal/compute fault S2 the strict rule abstains entirely and loses CASPER_FULL's advantages. The simple bounded residual comparison is known-type robust interval logic, so its scientific **novelty is not established**. The inequality is assumption-conditioned on exact queue predicted time (q=0) and valid artificial `L=.0001/ms`, `eps=0`, `max age=10000ms`; neither carries empirical uncertainty coverage. The physical simulator here is independent Python strict FCFS, while original Java CloudSimPlus v8.5.7 SpaceShared queue parity **FAILED** registered maximum wait threshold 9.1214009ms>5ms; Stage18–21 explained a source-specific event timing mechanism but did not turn it to PASS.

Targeted related work is documented `STAGE22_23_LITERATURE_NOVELTY_RISKS_2026-11-06.md`: IEEE TVT 2025 hard-deadline online acquisition, IEEE TSC 2025 cloud-edge asynchronous delayed feedback, Applied Soft Computing 2026 uncertain edge-cloud workflows, etc. Do not claim delayed feedback or trivial robust dominance alone as novelty. Original FGCS E42/E4.6 fully frozen.

## Next go/no-go approach
1. **Do not retune based on seed88 or add opportunistic seeds to chase significance.** Treat it as development seed forever; Stage16 seed301–308 not fresh again.
2. More principled next algorithm may augment intervals with **independently bounded/estimated queue prediction error**, treating unknown queue error as unverified rather than promising hard deadline guarantee. Need formal robust comparison `p_j + Uextra_j + Uqueue_j < p_g + Lextra_g + Lqueue_g` if bounds valid, plus abstention/fallback policy in compute regimes.
3. Check novel methodology against the strongest relevant prior baselines, not just greedy and old CASPER.
4. **Before new confirmatory results** lock algorithms, fault/queue models, external traces if available, independent paired validation seeds, metrics, sample size and statistical tests; inspect failure cases and S2/S3 equally.
5. No JPDC submission-ready claim, no forced p-value or guaranteed acceptance probability. A technically defensible manuscript remains possible but needs independent validation and novelty.
