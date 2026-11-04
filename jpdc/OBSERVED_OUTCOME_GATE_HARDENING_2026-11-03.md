# JPDC observed-outcome sidecar gate hardening — 2026-11-03

## Context and verified source
This checkpoint extends the registered actual-outcome validation, without modifying the frozen scientific E42 Git blob `34256ca7bff46f911cf20e8b94278fbd09175746` or E4.6. Source inspection reconfirmed that the official E42 `summarize` orders MISSION task outcomes by `taskIndex`, filters `taskIndex>=10000`, takes the **last 250 postshock** tasks, and computes P99 as ordered element `ceil((n-1)*.99)`; the existing sidecar validator follows this selection. Outcome definition still uses realized network + CloudSim wait + service and distinguishes it from `pred[j]`.

## New fail-closed invariants added
1. Both `CASPER_FULL` and `CASPER_HEALTH_STATIC` sidecar traces must contain **exactly the same MISSION task-index set**, not just the same counts. For every shared task, their recorded deadline must agree. These block an unobserved missing/replaced task or drifted task metadata while totals remain unchanged.
2. Official CloudSim CSV must have exactly eight distinct policy rows, each with the required S3 scenario and total deployment task count. Earlier validator only required the two targeted policies and could silently ignore missing unrelated policy rows or duplicate entries.
3. Synthetic regression fixture now mirrors the official full eight-policy E42 CSV contract. It deliberately tests a swapped task ID and a perturbed deadline, in addition to the prior positive test and seven negative corruptions.

## Recorded commits
- `jpdc/audit_observed_outcome_sidecar.py`: stricter task-cohort/deadline invariant at `6006db6bcc9c4c0ba9860d992fa5a90f58968e2a`; eight-row official scientific result gate at `c697d418c8a977137a362e7d2b40ed7922100bdd`.
- `jpdc/test_observed_outcome_sidecar_contract.py`: new two negative regression scenarios at `a6eb1fdf41b938d8cd615b2dbfeeeb6f307dfc11`; eight-policy synthetic fixture corrected at `0f7b6647e3e51aa42765d745d6d27056f580c602`.
- The existing `.github/workflows/jpdc-observed-outcome-validator-tests.yml` triggers automatically for these two paths, and may run the updated regression test.

## Honest execution status and scientific interpretation
This step **source-verified** the frozen generator's quantile/late selection contract and **committed** stronger checks and tests. There is NOT yet an independently observed GitHub Actions conclusion for either lightweight regression CI or the full seed40 generated-E45 observed-outcome smoke workflow. Previously executed local synthetic test (before these stricter changes) accepted one valid fixture and rejected seven corruptions. Therefore **do not claim the expanded nine-fault regression has passed** without fetching its CI result or independently running exact updated files. No new CloudSim simulation results or independent trace replay were generated here.

The original preregistered disjoint holdout p=.0625 is non-significant; exploratory factorial sign p=.125 is non-significant. Do not interpret within-task count as independent seeds.

## Next action
Obtain Actions run IDs/CI outcome or run `python3 jpdc/test_observed_outcome_sidecar_contract.py` in a checked-out repository. Then inspect paired seed40 HIGH observed logger run, artifact and scientific equality gate, followed by a separately specified independent replay experiment.
