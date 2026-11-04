# JPDC S3 original Actions artifact audit — 2026-11-03

## Purpose and scope
This is the next technical step after the processed-ZIP cross-bundle audit: check **original archived GitHub Actions outputs** (not only derived analysis CSVs) for the preselected four independent seed indices 40–43. No new simulation was run in this step. No E42/E4.6 change.

## Original sources independently retrieved
- Physical controlled masks: Actions run 41719553340, seed 40 artifact 13272215535; 41:13271273184; 42:13270784276; 43:13272485400.
- Factorial mask×eta: Actions run 41724362605, seed 40 artifact 13273915636; 41:13273755094; 42:13271869726; 43:13272339554.
- All eight GitHub jobs were observed completed **success**. Artifacts were available, not expired (as of retrieval).
- Original scientific source checkout SHAs recorded in artifacts: physical `254c25f13b12ddb7e2b35e019c05a75d7d4dfa48`; factorial `24262794948949a0c838300d20e51e0c985072d1`.

## Independent verification executed
A fail-closed Python standard-library audit run on downloaded original ZIPs passed **2,100 assertions** across seeds 40–43. Checks include:
1. All four paired seed identifiers and 21-node, six-affected-node mask definitions; deterministic LOW/HIGH selection from pre-shock mission routing counts, with disjoint masks; the HIGH tie-break among remaining equally-used nodes selects **higher** node IDs (important for seeds 41–43).
2. Original per-mission `mission_network.csv`: unique task indices; pre/post task counts; pre-shock node-selection parity across baseline/LOW/HIGH; physical multiplier exactly 2 for selected nodes postshock and 1 otherwise; network delays match nominal × multiplier (CSV stores nominal first, realized second); actual task exposure and mean incremental delay independently reconstructed.
3. Physical run official 8-policy `results.csv` equals paired-results JSON and matching factorial adaptive FULL official CSV across all nine reported post/late metrics, within CSV rounding.
4. Factorial adaptive vs clamped official eight-policy CSVs match the factorial JSON; science columns for non-FULL policies match across arms (excluding mapper timing); integer late mission counts per seed; calculated factorial interaction matches original paired JSON.
5. Four-seed official CSV pooled late counts reproduce every row in the committed four-arm report.

| Condition (n=1000 late mission tasks per row) | False certificates | Abstentions | Deadline misses | Family-wide bound coverage |
|---|---:|---:|---:|---:|
| LOW adaptive | 0 | 14 | 1 | 992 |
| LOW clamped eta1 | 0 | 11 | 1 | 990 |
| HIGH adaptive | 3 | 125 | 45 | 835 |
| HIGH clamped eta1 | 33 | 11 | 44 | 3 |

## Reproducibility
- Committed executable: `jpdc/audit_s3_original_actions_artifacts.py`, commit `f4f13d63d9a6d6c604bc68048ea91093493b8d31`.
- Download the eight original GitHub Actions artifact ZIPs by the IDs above into one directory, keeping names `github-actions-artifact-<id>.zip`. Then run `python3 jpdc/audit_s3_original_actions_artifacts.py DIRECTORY`.
- The local audit yielding 2100 checks includes extra verbose count-level assertions; the committed source is a compact and independently rerunnable core audit covering the same categories. Do not claim it emits precisely the same check count without testing it separately.

## Interpretation and limits
These original archive reconciliations materially strengthen *data lineage and arithmetic reproducibility*. They are not fresh CloudSim execution, proof of cross-simulator validity, or proof of a population-level improvement. Under HIGH, fewer false certs come with substantially more abstentions, without a clear reduction in deadline misses. The four-seed factorial seed-level exploratory two-sided sign p=.125; preregistered disjoint S2/S3 holdout p=.0625, so **no confirmatory significance**. Task counts do not create independent inferential sample units.

## Next technical step
Validate the committed compact audit against original artifacts (and CI), run seed-level raw scientific trace reconstruction of individual certificate events if original instrumentation permits, then design a genuinely independent trace-replay environment. No further opportunistic tests aimed at p<.05.
