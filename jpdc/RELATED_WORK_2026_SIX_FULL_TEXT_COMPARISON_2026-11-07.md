# JPDC/FGCS 2026 six-user-PDF related-work position and evidence standards (2026-11-07)

All six records reside in `jpdc/references_2026_six_uploaded.bib`. The original full-text PDFs were supplied by the user. Citation != executable baseline; no claim that AUHS/DFAQ-LB/PriorityDRL was reproduced on CASPER source.

## Exact method and evaluation distinctions
| Bib key | 2026 source and full-text observations | Relation to CASPER and caveat |
|---|---|---|
| `Wu2026DFAQLB` | FGCS 182 108460; queues, elastic thresholds and node health; CloudSim 3.0.3; 10 repeats; ACO/PSO/CDLB/DDLB and makespan, wait, completion | **Closest feedback/queue problem**, but does not directly validate delayed CPU-finish + E2E network feedback; not implemented on our original physical workload |
| `Abdellatief2026NSGA3WS` | FGCS 183 108527; NSGA-III + novel fitness under workflow deadline/budget/energy constraints; BDD/SOSGOA/EIS, Friedman/Wilcoxon, sensitivity | Shows engineering adaptation and tradeoff can be accepted. Its paper explicitly has worse mean energy than BDD (707.92 vs 612.89); no blanket superiority |
| `Farabegoli2026IDHGQL` | FGCS 183 108539; HeteroGNN + DQL + collective computing density information; Alchemist; ablates collective observations | Related edge learning and observation design, not an equivalent 21-node IIoT deadline scheduling baseline |
| `Lei2026AUHS` | JPDC 216 105308; serverless container scheduling via iterative ranking, subdeadlines and offloading planning; EdgeCloudSim, 1280 scenario configurations, seven policies; DSR 77.43% vs SKIPPY 67.25%, HEFT 60.83%, PPO 51.15%; parameter ANOVA/HSD | **Closest scheduling experiment/reporting template**. FaaS hierarchy and container cache not identical to native CASPER IIoT tasks. The numerical improvement cannot be transferred directly |
| `TaoLiu2026Colocated` | JPDC 215 105307; latency-sensitive co-located Hadoop YARN resource allocation, contention avoidance, reclaimed idle capacity, Alibaba-inspired workload | Useful interference/latency resource-systems context. Not cloud-edge network-fault routing |
| `Ayadi2026PriorityDRL` | JPDC 217 105322; dual-agent deadline-aware GPU assignment with preemption; Microsoft GPU trace, EDF/SJF/Tetris/Chronus/DRL baselines, multiple reward/preemption ablations | Deadline reporting and ablation template; GPU-specific. In small-job table EDF JCT68.19 vs PriorityDRL70.15, showing no need for every metric to dominate; not an apples-to-apples IIoT baseline |

## Contribution hypothesis and falsifiability
Candidate empirical contribution: a **causal, lightweight, deadline-oriented feedback scheduler** that incorporates CPU-service errors only when CPUs finish, and network excess only when END-TO-END feedback is delivered. Unlike historical conformal coverage, its primary target is *actual deadline misses*, with fixed bounded nominal deviation from PRED_GREEDY. CPU-only, E2E-only, combined policies must be isolated in ablation alongside original PRED_GREEDY and CASPER_FULL. This is proposed incrementally, NOT a verified novel framework or theorem. Closest work DFAQ-LB and AUHS require a precise distinct mechanism comparison in manuscript.

Primary per-source-seed task outcome: **POST-shock MISSION deadline miss integer count / total MISSION**; secondary all MISSION misses, latency, queue wait, switching, E2E feedback and CPU feedback, nominal route overhead. A result is scientifically adverse if S2 CPU and S3 network tradeoffs cause more mission misses than both primary baselines. Mixed, null or adverse results must remain and motivate a documented redesign, not be hidden behind aggregate mean. No 90% confidence language for historical q intervals.

## Experimental quality gaps to close for JPDC
- Repeat paired across new independent source seeds **only after policy freeze**, report per-seed differences, confidence intervals with source seeds (not treating tasks as independent), and exact statistical method. Do not cherry-pick seeds.
- Fair executable modern comparator: if AUHS/DFAQ-LB cannot be faithfully transplanted, explicitly state incompatibilities and implement conceptually comparable simplified baselines with different names, plus source availability/code reproducibility. Do not misname them as original author algorithms.
- Real uncertainty: hold hidden CPU/network states away from routing; no CPU truth at dispatch or network E2E truth before completion; verify code with independent causality tests.
- Abrupt fault phase, false alarming, scenario diversity, class fairness and overdue work tail metrics. Ablate CPU-only and E2E-only update, sample thresholds, search budget and network-delay.
- Preserve original queue model limitations. Strict Python FCFS vs original Java CloudSimPlus8.5.7 SpaceShared registered queue wait fidelity **FAIL** at9.1214ms>5ms; cannot claim engine equivalence; consider building an independent host/runtime or alternative queue discipline.
- No unjustified acceptance prediction, novelty priority, or claim six sources are all exact scheduler baselines.
