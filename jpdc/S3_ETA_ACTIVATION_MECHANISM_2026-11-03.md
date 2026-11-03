# JPDC S3 eta activation vs routing — actual task-level traces (2026-11-03)

## Verified provenance
Source: SUCCESS GitHub Actions run `41652750267`; seed 0 artifact `13237917384`, seed 7 artifact `13238761161`, seed 18 artifact `13238521488`. Each has 60,000 JPDC_TASK_DISPATCH and 60,000 JPDC_TASK_OUTCOME rows for two policies, official `results.csv`, and passed `jpdc/audit_phase_mission_trace.py`. Generated E45 instrumented using `jpdc/instrument_seed29_task_dispatch.py`. Original E42 scientific git blob `34256ca7bff46f911cf20e8b94278fbd09175746` and E4.6 are frozen, unmodified.

## What was measured
For all 30,000 task indices, compare actual dispatched node and issued certification between CASPER_FULL and CASPER_HEALTH_STATIC; separately restrict to mission tasks at task indices >=10000 (post perturbation), <10000 (pre), and the last 250 mission tasks. Effective eta is the logged `etaAtDispatch` of CASPER_FULL; static eta=1 by design. `eta > 1` means the adaptive scaling is active at decision time, not necessarily that a routing/certificate decision differs from static.

| Seed | Post mission n | Mean eta | Max eta | Mission eta >=2 | Mission certificate disagreements | Mission node disagreements | Mission miss disagreements |
|---|---:|---:|---:|---:|---:|---:|---:|
| 0 | 1019 | 2.951257 | 3.0 | 992 | 31 | 0 | 0 |
| 7 | 980 | 1.036345 | 1.299635 | 0 | 0 | 0 | 0 |
| 18 | 1021 | 2.988577 | 3.0 | 1014 | 131 | 0 | 0 |

Last 250 mission tasks: eta=3.0 throughout in seeds 0 and 18; eta=1.0 throughout in seed 7. Last-250 certificate disagreements: seed0 11, seed7 0, seed18 36. In these three experimental traces, no differing chosen node for **any** of the 30,000 tasks of each seed, even where certificates differ. This is sample-specific, **not** a general property; prior successful seed29 real trace found 66/30,000 differing node choices.

Among *all* post-shock tasks (20,000 task indices/seed, including NORMAL), count differing certificates: seed0 31, seed7 0, seed18 193. Seed7 had eta>1 for 5,669/20,000 post tasks (so adaptation did activate transiently), but never eta>=2 and did not change any certificate/selected node in that period.

Counterfactual family-wide coverage and actual certificate quality remain conceptually different metrics. The logging only records effective eta and *chosen* node, not complete top-three candidate bounds for every task. Thus it does not establish the exact causal reasons eta trajectories differ by seed; it establishes the observed association between high eta and changed certification decisions. Earlier `eta=1` generated E45 intervention experiments provide separate evidence of causal policy effects.

## Next technical opportunity
A bounded instrumentation run recording eta update events (innovation/errors and trigger) for seed7 vs seed18 could distinguish no distribution-shift alarm from differing severity, and reveal why eta remains at 1 in seed7. Any such trace should avoid changing E42/E4.6, and should have an exact data contract and generated-E45-only changes.

## Local reproducibility and recovery
Standalone analysis script: `/mnt/data/jpdc_s3_eta_activation_audit_2026_11_03/audit.py` and output `phase_activation_metrics.csv`; local ZIP `/mnt/data/jpdc_s3_eta_activation_audit_2026_11_03.zip`. These paths are session-local; recover source traces through Actions artifact IDs above. Scientific rows in `jpdc/S3_PHASE_REPLICATION_3SEED_2026-11-03.md`. Script computes per-mission eta distribution, node/certificate/outcome disagreement counts and phase-specific counts from actual CSV events, but does not claim inferential significance from three seeds.
