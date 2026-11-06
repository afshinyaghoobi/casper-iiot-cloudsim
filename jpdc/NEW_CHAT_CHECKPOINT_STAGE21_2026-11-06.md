# JPDC continuation checkpoint — Stage20–21 successful, 2026-11-06

## User goal
Only JPDC journal, no CCGrid conference paper, preserve original FGCS CASPER contribution, rigorous science; don't chase only paper quantity or acceptance guarantees.

## New exact evidence
Stage20 real CloudSimPlus v8.5.7 on unchanged Stage19 original microfixture: [CI 42234742284](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42234742284) **SUCCESS**, original frozen Stage19 submit snapshots and native original wait/runtime outcomes exact parity; repeated native event trace byte identical. First cloudlet intended MI/MIPS service8.099623ms, native reported18.100623ms, first finish callback clock1018.101623ms, added10.001ms. Actual VM update timestamps 1008.100623, 1018.101623 and every10.001ms afterward, in both cases. Original Stage19 first still RUNNING at all third submissions, so original 3-job fixture never reached free-PE+older-waiter event.

Stage21 exact original CloudSimPlus Maven sources 8.5.7 archive SHA256 `8d3efcacfc661b2f1e018e279761fc4ae1e5584a770b2022d20930568688966c`, [scan 42235135939](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42235135939) SUCCESS twice identical, [archived-source path verification 42235350835](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42235350835) SUCCESS. `DatacenterSimple.java` lines749,754–755,782–783 show host update then nonzero delay floor `getSimulation().getMinTimeBetweenEvents()+0.01` seconds, then schedule VM_UPDATE_CLOUDLET_PROCESSING. In original setup minTimeBetweenEvents=1e-6 sec, exact resulting minimum10.001ms. Source-level **credible explanation** for observed VM processing update cadence and tiny microfixture reporting artifact; not universal extra task latency. Preserve source audit `jpdc/STAGE21_CLOUDSIM_857_EVENT_CADENCE_EXPLAINED_VERIFIED_2026-11-06.md`.

## Unchanged negatives and validity boundaries
Original Python strict chronological FCFS vs Java SpaceShared independent queue parity registered max wait <=5ms FAILED with observed max9.12140093294972ms, run41773297282. Source-generated Java E45 30k tasks actual older 10900 waiting/newer 10901 directly admitted in execution was observed run41777312914. Its event admission paths separated from queued-list update (Stage18). This is not full policy portability / independent validation.
Original frozen E42 blob `34256ca7bff46f911cf20e8b94278fbd09175746`; original E4.6 unchanged.
Stage16 8 seed 301–308 native Python evaluation: guarded vs CASPER_FULL S3 mean difference -1 MISSION miss per seed, exact sign p=.375 (not significant); S2 +1.375 misses per seed (adverse). Stage17 development seeds86–87 no active-probe ablation: zero ALL/PRE/POST MISSION miss count changes in four matched comparisons. Neither novelty nor robust superiority established. FGCS original CASPER submitted/planned separate paper cannot be repackaged as JPDC same contribution.

## Next work priority (do not merely extend forensic numbered stages)
Stop repetitive queue experiments unless required for essential falsifiable validation. **Real JPDC bottleneck is independent novel scheduling method** addressing availability of delayed network measurements, uncertainty interval identifiability and queue-aware deadline risk beyond simplistic +2ms detour. Literature review must seriously benchmark published cloud-edge delayed feedback, hard deadlines and staleness-aware load schemes. Need a specified objective, rigorous algorithm plus theorem/counterexample/safety invariant, new well-specified baselines and pre-registered external-seed and cross-model evaluation. One simulator's synthetic network doubling only insufficient for JPDC. Do not tune Stage16 seeds or Stage17 results to make p-values look better. Record negative experiments as evidence.

## Latest real GitHub commit
f671c00a84f521fe03706734c74f9bcd7b1bf898 (Stage21 report). All files on `jpdc-seed0-repro-20261024`.
