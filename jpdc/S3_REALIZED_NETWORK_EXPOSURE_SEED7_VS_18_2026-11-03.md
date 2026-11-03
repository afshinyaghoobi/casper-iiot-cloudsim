# S3 realized network exposure explains seed7 versus seed18 E17 response

Date 2026-11-03. This is a two-seed **mechanism diagnosis**, not population-level statistical inference.

## Source and scientific controls
- E42 frozen source git blob `34256ca7bff46f911cf20e8b94278fbd09175746` and E4.6 were unmodified. Generated E45 is instrumented only.
- Real CloudSim run `41685432122` completed both simulations with Maven BUILD SUCCESS, original output produced, but validation FAILED because an incorrect assumption of 24 nodes was coded (actual `FrozenConfig.TOTAL_NODES=21`). The raw artifact files are valid and independently analyzed: seed7 artifact `13255495133`, seed18 artifact `13253273742`.
- Validation corrected in workflow at commit `9cf1215`, triggering repeat run `41685852046`. Both corrected rerun jobs subsequently **completed SUCCESS** with artifacts seed7 `13255386941` and seed18 `13253124265`.
- Mechanism instrumentation: `jpdc/instrument_s3_network_exposure_generated_e45.py`, commit `a692056`; trace columns: scientific seed, scenario, policy, task index, chosen node, affected node flag, nominal network ms, actual network ms, network multiplier, predicted latency.
- The S3 shock mask chooses 6 of 21 nodes via `affectedMask(seed,scenario)`; the network multiplier for a task dispatched to an affected node after task index 10000 is 2.0.

## Findings from actual instrumented FULL task-level trace
| Statistic | Seed 7 | Seed 18 |
|---|---:|---:|
| Six affected nodes | 2,5,7,11,14,19 | 3,8,12,13,15,17 |
| Number of mission tasks postshock (task index >= 10000) | 980 | 1021 |
| Mission tasks assigned an affected node postshock | 0 | 960 |
| Realized affected-node exposure rate | **0.0%** | **94.0%** |
| Mean network delay postshock | 10.640 ms | 29.788 ms |
| Mean *additional* network delay attributable to shock, all postshock mission | **0 ms** | **14.665 ms** |
| E17 normalized scores exceeding calibration reference postshock | 40/980 (4.08%) | 965/1021 (94.52%) |
| E17 first observed alarm (FULL) | None | mission task 10165 |
| FULL late mission eta | 1 | 3 |

Before shock, seed18 sent 455/483 mission tasks to nodes that would later be affected, but the network multiplier was still 1; no pre-shock added network latency. Seed7 pre-shock assigned zero mission tasks to its six would-be affected nodes. Thus the large difference in realized exposure is **not** entirely explained by post-shock adaptation. The mask intersects different naturally preferred execution nodes between seeds.

## Scientific interpretation
This is a concrete explanation of why the same nominal S3 configuration yielded drastically different E17 alarm trajectories. The affected subset's **overlap with the actual workload placement** (realized treatment) matters more than the fixed count of six damaged nodes. In this two-seed diagnostic, seed7 mission tasks never traverse the degraded nodes, whereas seed18 mission tasks overwhelmingly do; consequent network delay differs by ~14.7 ms averaged across all postshock mission tasks. The result supports an exposure-mediated explanation for E17 error/alarm differences, though it does not prove a causal mediation model or establish how frequently this occurs over the seed population.

Future experimental design should stratify or report realized task-level exposure, network-delay increments, and policy-specific route changes, but beware conditioning on a variable affected by the policy (selection/collider bias). If designing a causal exposure intervention, predefine affected nodes based on baseline route distribution and evaluate with separate randomized confirmation seeds. Do not post-hoc exclude zero exposure seeds to obtain significance.

## Reproducibility
- Original source run `41685432122`, artifact IDs 13255495133, 13253273742
- Corrected workflow `.github/workflows/jpdc-s3-network-exposure-2seed-once.yml` at commit 9cf1215, rerun `41685852046`.
- Previous independent E17 detector trace: run `41658004816`; artifact seed7 13241260387; seed18 13239324890.
