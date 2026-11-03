# Verified S3 pre/post-shock mission-task trace replication: seeds 0,7,18

Date 2026-11-03. Actual GitHub Actions run **41652750267**; all three jobs successful with source hash guard. Artifacts: seed0 **13237917384**, seed7 **13238761161**, seed18 **13238521488**. Generated E45 task-level instrumentation only; original frozen E42 and E4.6 unchanged.

Tool: `jpdc/audit_phase_mission_trace.py`; validates each policy's 30,000 dispatch and 30,000 outcome rows per seed, task-index alignment, and exact agreement of mission post/late FWC, AIR, FAR, DVR rates with official CloudSim CSV. Each seed contains two policies in trace; total 360,000 task records across 3 seeds.

| Phase | Policy | Mission tasks | FWC covered | False certs (FAR count) | Abstentions | Deadline misses |
|---|---|---:|---:|---:|---:|---:|
| Pre (<10000 index) | FULL | 1529 | 1516 | 0 | 35 | 11 |
| Pre | HEALTH_STATIC | 1529 | 1512 | 0 | 28 | 11 |
| Post (>=10000) | FULL | 3020 | 2439 | 21 | 216 | 163 |
| Post | HEALTH_STATIC | 3020 | 1033 | 115 | 54 | 163 |
| Late (250/seed) | FULL | 750 | 622 | 5 | 59 | 40 |
| Late | HEALTH_STATIC | 750 | 266 | 30 | 12 | 40 |

Seed-level post FAR difference FULL − STATIC = -13,-81,0 for seed indices 0,18,7 respectively. Exact two-sided sign p=0.5 (two nonzero seed differences); no statistically confirmed effect from this small trace study. Seed7 is a strict negative-control example: both policies identical on the displayed metrics. Post AIR changes similarly 31,131,0; FWC +658,+748,0; DVR 0,0,0. This illustrates heterogeneity and the need to report seed-level replication instead of pooling tasks as independent.

FWC is *counterfactual family-wide bound coverage*, distinct from issued certificate correctness. FAR denominator is all mission tasks, not certified subset. Postshock adaptation decreases false certificates while abstaining more; aggregate postshock deadline miss counts are identical. Observational paired simulations, not a causal pre/post intervention.

Local analysis archive may be available at `/mnt/data/jpdc_phase_s3_multi_seed_2026_11_03.zip`; GitHub Actions artifacts are the durable recoverable originals. Do not modify E42/E4.6.
