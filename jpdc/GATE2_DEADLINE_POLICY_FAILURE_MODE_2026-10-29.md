# Gate 2 policy audit: nominal feasibility is not deadline-risk optimal (2026-10-29)

**Scope:** `DEADLINE_FEASIBLE_MIN_UNCERTAINTY` in the generated E45 campaign, not frozen E4.6. This is an analytic counterexample, not a CloudSim performance result.

The policy checks `pred[node] <= D` and chooses the node with the minimum `fixedSigma(pred[node], sigmaMult)` among nominally feasible nodes. A smaller absolute uncertainty proxy does **not** imply a smaller probability of missing deadline because remaining slack differs.

## Concrete counterexample under the implemented fixedSigma formula

Given a task with deadline `D=100 ms`, compare two eligible nodes:

| Node | `pred` (ms) | `sigmaMult` | `fixedSigma=(3+0.1*pred)*sigmaMult` (ms) | Slack `D-pred` (ms) | Normalized slack |
| --- | ---: | ---: | ---: | ---: | ---: |
| A (edge tier) | 10 | 1.10 | 4.40 | 90 | 20.45 |
| B (cloud tier) | 99 | 0.90 | 11.61 | 1 | 0.086 |

**Correction to a tempting intuition:** the implemented formula does *not* pick B here; A has the smaller absolute sigma. A valid inversion requires both a close prediction and sufficiently different tier multipliers. Because the tier multipliers range from 0.9 to 1.1, such inversions can occur only for modestly separated predicted latencies.

Valid counterexample:

| Node | `pred` (ms) | `sigmaMult` | `fixedSigma` (ms) | Slack (ms) | Normalized slack |
| --- | ---: | ---: | ---: | ---: | ---: |
| A (edge tier) | 80 | 1.10 | 12.10 | 20 | 1.653 |
| B (cloud tier) | 90 | 0.90 | 10.80 | 10 | 0.926 |

Both are nominally feasible at D=100. The implemented policy chooses **B** (sigma 10.8 < 12.1); greedy prediction chooses **A**. If standardized prediction errors are independent and follow the same centered distribution whose upper-tail exceedance probability decreases with normalized slack, B has a **higher** deadline miss probability than A. In particular under standard normal residuals, the approximate miss risks are `1-Phi(1.653)≈0.049` (A) versus `1-Phi(0.926)≈0.177` (B). These are **illustrative assumptions**, NOT empirically calibrated CASPER rates or simulation results.

This establishes that nominal feasibility + minimum absolute sigma alone cannot justify deadline-risk dominance. Conversely, it does not prove poorer empirical performance for the existing workloads.

## Interpretation rules

1. Treat the policy as an exploratory mechanistic control, not a validated deadline-reliability algorithm or SOTA comparator.
2. Interpret higher and lower deadline misses jointly with latency, scope (mission tasks), workload and complete paired-seed analysis.
3. Do not tune a new normalized-slack policy using the single-seed pilot; if developed, separately pre-register and benchmark it using disjoint seeds.
4. No claim is made about simulator outcomes until Actions artifacts and scientific parity are verified.

**Frozen E4.6 is unchanged.**
