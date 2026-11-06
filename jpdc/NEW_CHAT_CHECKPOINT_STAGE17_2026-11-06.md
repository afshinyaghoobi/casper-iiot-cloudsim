# JPDC continuation checkpoint — Stage17 complete and Stage18 priorities (2026-11-06)

## Scientific status: no JPDC-level superiority yet
- Stage12 causal diagnosis: five affected nodes no alarm because >12s measurement-generation separation under assumed L=.0001/ms gives a >1 normalized-drift envelope for synthetic 0→1 shock; node17 has ~25ms gap and alarms. No model guarantee or real trace.
- Stage13 controller unit fixtures successful; initial algorithm not yet overall effective.
- Stage14 single development seed84 native physical run: baseline exact parity, negative total misses for freshness-active (S2 17 vs FULL8, S3 15 vs FULL5); old results frozen.
- Stage15 development seed85 2ms nominal detour guard improves prototype over unguarded; S2 22 vs FULL20, S3 5 vs FULL8; not independent validation.
- Stage16 paired seed indices 301–308 frozen, eight success + byte-repeat, primary S3 guarded-FULL mean -1 MISS per seed, sign p=.375 and bootstrap 95% [-2.625,.375]. S2 mean +1.375 MISSES per seed, sign p=.125. No claimed improvement over FULL.
- Stage17 NO_PROBE ablation prereg at commit cc1de0b0a0842d182ca25ade03fd28733f567667, development seed86 and87, full two-seed physical run [42187795512](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42187795512) 2/2 success and byte-repeat; independent immutable artifact audit [42188302693](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42188302693) PASS. All four scenario/seed comparisons yield **zero change in ALL/PRE/POST MISSION miss count when active NORMAL probing is deleted**. PROBE attempts 95 per arm, but only 12-17 changed node assignments. Small mean latency/wait differences exist. n=2 and low miss counts cannot prove generalized zero value. Full immutable result document `STAGE17_PROBING_ABLATION_VERIFIED_NULL_2026-11-06.md`.
- Relevant 2026 literature warns that fresh/load observations are not universally beneficial; reviewed in `STAGE17_RELATED_WORK_NOVELTY_GUARDRAIL_2026-11-06.md`. Do not call age, +2ms detour or E2E probing inherently novel.

## Unresolved simulator fidelity and actual original forensics
- Original CloudSim Plus 8.5.7 SpaceShared native scheduling queue ordered differently from strict Python FCFS under one observed case: node14 tasks 10900/10901 swapped, while 10900 waiting and new 10901 directly admitted after PE became free. Actual Java instrumented [41777312914](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41777312914), root event timing not yet established. Registered Python replay max wait error 9.1214009ms failed <=5ms gate [41773297282](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41773297282). Preserving these exact failures is essential. Existing independent strict-FCFS study remains one *different simulator domain*, not Java equivalent.
- Frozen FGCS E42 Git blob 34256ca7bff46f911cf20e8b94278fbd09175746; no original FGCS/E4.6 modification.

## Focus Stage18 — only if scientifically new
First investigate mechanical event scheduling and admission *in generated E45 only*, trying to reproduce 10900 older waiting vs 10901 new direct admission with auditable simulation event timestamps and controlled multi-event microfixture. Freeze acceptance checks, keep original queue FAIL, and classify whether timing/VM update policy (not algorithm) caused bypass. In parallel, revisit a principled hard-deadline/queue-aware objective with proof/counterexample and a genuine literature differential, rather than another threshold tweak or seed hunt. Need independent new model/source validation and realistic traces before a positive JPDC performance claim. Preserve source-level unit tests and any negative findings. No promises of journal acceptance or publishability.

## Strategy
User explicitly chose **JPDC only**, no CCGrid contribution split. No deadline-driven rush. Favor scientific defensibility, readable honest reporting, and proper related-work comparison.
