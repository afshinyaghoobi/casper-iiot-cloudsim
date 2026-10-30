# Gate 2 — deadline-slack literature screening and policy identifiability (2026-10-30)

## Sources and applicability

1. "A three-stage heuristic task scheduling for optimizing the service level agreement satisfaction in device-edge-cloud cooperative computing," available at https://pmc.ncbi.nlm.nih.gov/articles/PMC8802786/ . The public abstract and contribution describe optimizing numbers of hard-deadline-satisfied tasks in device-edge-cloud and a heuristic drawing on least accumulated slack time first (LASTF) and EDF. **Full implementation mapping has NOT been verified**; this note does not claim to reproduce its three-stage algorithm.
2. "Deadline-Aware Scheduling of Mixed-Criticality Tasks," ICPP 2025, DOI 10.1145/3754598.3754639, https://doi.org/10.1145/3754598.3754639 . Publisher preview describes online-capable methods, a deadline-slack heuristic, and scheduling distinctions. It does not establish source-level compatibility with CASPER.
3. Braun et al., JPDC 2001, DOI 10.1006/jpdc.2000.1714, offers static independent-task heuristic context; static Min-Min/Max-Min must not be relabeled online unchanged.

## Critical degeneracy before adding a baseline

The CASPER dispatcher maps **one task at a time at its arrival**. The task deadline D is the same for each potential node of that task. Thus, for node j and predicted response latency p_j,

    slack_j = D - p_j

and maximizing raw slack_j is **identical** to minimizing p_j. A policy named `MAX_SLACK` that selects argmax_j(D-p_j) duplicates `PRED_GREEDY` under matching eligibility and tie-breaks. Ordering *across different waiting tasks* by EDF or LASTF cannot be implemented fairly by simply swapping a per-task VM mapper's node scoring rule: it requires a specified centralized task queue, batch window and admission/reordering semantics, applied consistently to all compared policies.

A potential non-degenerate, node-selection-only research control is to maximize *standardized* slack `(D-p_j)/sigma_j`, with `sigma_j=(3+0.1*p_j)*sigmaMult_j`, selecting the index with maximum score. This differs from minimum raw latency and from minimum sigma, but is a **new exploratory parametric control**, NOT the paper's LASTF/EDF and NOT an empirical risk guarantee.

Example D=100 ms:
- Node A: p=80, sigmaMult=1.10, sigma=12.1, standardized slack=20/12.1≈1.6529.
- Node B: p=90, sigmaMult=.90, sigma=10.8, standardized slack=10/10.8≈.9259.
The minimum-absolute-sigma policy chooses B; standardized-slack chooses A. Under a shared centered location-scale residual distribution, A has lower miss probability. The empirical model need not satisfy that distributional assumption, particularly under hidden-shock scenarios.

## Next scientifically meaningful implementation gate

1. Obtain full method/pseudocode and code or supplementary methods for a **published online** deadline-aware independent-task comparator; identify what is known to each policy at arrival.
2. If a paper relies on EDF across tasks, introduce a **separate shared scheduling model** (batch or queue) for every policy, without modifying frozen E4.6.
3. Preserve `PRED_GREEDY` as existing estimated-response-minimization baseline, not duplicate `MCT` or raw `MAX_SLACK`.
4. Run only the pre-registered 5-scenario existing pilot first, then a paired multi-seed experiment; no performance numbers inferred from this literature screening.

## Status

No new CloudSim run was verified. E4.6 stays frozen.
