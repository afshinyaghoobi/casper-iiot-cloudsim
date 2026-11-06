# JPDC Stage16 — eight-seed frozen paired physical evaluation VERIFIED, 2026-11-06

## Provenance
- Scientific protocol frozen before outcomes: `STAGE16_PAIRED_EIGHT_SEED_PROTOCOL_PREREG_2026-11-06.md`, commit 015583975f376cfe6bee1a888a039c99e0bb851c.
- Original physical run [42186301148](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42186301148), **8/8 success**, each shard repeated with byte-identical JSON and exact original Stage6 parity for CASPER_FULL/PRED_GREEDY. 8 seeds 301..308, S2/S3, 3 policies, 12k tasks each =576,000 dependent task-policy outcomes; scientific n=8.
- Independent **immutable-artifact-only** statistical audit [42186584939](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42186584939), PASS `JPDC_STAGE16_EIGHT_INDEPENDENT_SEEDS_PAIRED_AGGREGATE_PASS`. No extra physical rerun or retroactive tuning.

## Mandatory paired outcomes vs CASPER_FULL
Per-seed total MISSION misses, identical workloads across each policy in each scenario:

| Seed | S2 FULL | S2 GUARDED | S2 delta | S3 FULL | S3 GUARDED | S3 delta |
|---|---:|---:|---:|---:|---:|---:|
|301|4|4|0|5|4|-1|
|302|12|14|+2|12|14|+2|
|303|0|1|+1|7|7|0|
|304|17|16|-1|4|4|0|
|305|11|15|+4|16|10|-6|
|306|22|24|+2|35|35|0|
|307|10|11|+1|14|12|-2|
|308|8|10|+2|6|5|-1|

S2 delta mean +1.375 misses/seed, two-sided exact sign p=.125, 95% seed-bootstrap percentile interval [+0.375,+2.375], 6 worse /1 better /1 tie. S3 **preregistered primary** delta mean -1.000 miss/seed, two-sided exact sign p=.375, 95% seed-bootstrap percentile interval [-2.625,+0.375], 4 better /1 worse /3 ties. At n8 these CIs are fragile; no claim of significant improvement against FULL. S2 tendency toward harm is important; the bootstrap CI excludes zero descriptively, although the prespecified exact sign test is non-significant and the metrics/tests differ.

## Mandatory paired outcomes vs PRED_GREEDY
S2 mean guarded minus greedy +0.250, two-sided sign p=1.0, bootstrap percentile [-0.375,+0.875]. S3 mean guarded minus greedy -1.250, sign p=.0625, bootstrap percentile [-2.75,-0.25]. The paired S3 differences against greedy are [-1,0,-1,0,-6,0,-1,-1]: five wins, no losses, three ties, exact two-sided p=.0625. The seed-level bootstrap interval excluding zero does not override the nonsignificant prespecified sign test, and n=8 limits inference.

## Interpretation / go-no-go
Stage16 passes engineering and reproduction gates. **It does NOT pass the criterion of demonstrated robust superiority over CASPER_FULL**, since the S3 primary sign test is not significant and S2 tends adverse. The Stage15 policy is a prototype, not a validated CASPER extension, not a conformal guarantee; original FGCS CASPER/E42 remains untouched. Do not seed-hunt or retroactively tune frozen validation evidence. Future method improvement must be labelled a new distinct design requiring its own prospective validation cohort (no reuse of 301..308 as an untouched holdout), with novelty relative to real published algorithms audited and cross-engine queue fidelity addressed (Python FCFS versus Java CloudSimPlus SpaceShared remains unvalidated).
