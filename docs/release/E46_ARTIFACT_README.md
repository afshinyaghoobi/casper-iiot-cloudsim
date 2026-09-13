# E4.6 Artifact README

## Artifact name

`e46-publication-results.zip`

## Purpose

This artifact preserves the frozen E4.6 publication-scale CloudSim Plus campaign results for CASPER-IIoT. It is intended to support reproducibility review and long-term archival through GitHub Releases and Zenodo.

## Integrity anchors

- Artifact SHA-256: `d1cf8be940669f9551dec34505ee75784142b5d14eb5f6d7c737e0281bc2c1c9`
- GitHub Actions workflow: `E4.6 Online-Dispatch Publication Campaign`
- Workflow run ID: `34677758057`
- Aggregation job: `aggregate-publication-results`
- Aggregation job ID: `103510962427`
- GitHub Actions artifact ID: `10292758918`
- Closure commit: `896d7f01be26f70c9259b938aa1a3f67c2f757c6`
- Campaign orchestration commit: `fb8fab039886a98ba582541d15956bb4a01569ff`
- Frozen scientific source SHA: `ee1600b808a9747bc0373489e8ce531bd6bfb5e0`

## Expected contents

The artifact includes:

- `E46_LOCKED_PROTOCOL.json`
- `E46_DECISION.json`
- `E46_PROVENANCE.txt`
- `E46_REPORT.md`
- `E46_RAW_SHA256.txt`
- `e46_all_runs.csv`
- `e46_summary.csv`
- `e46_bootstrap_ci.csv`
- `e46_paired_tests.csv`
- `e46_friedman.csv`
- `e46_full_gates.csv`
- raw per-seed CSVs under `raw/`

## Validation expectations

A valid copy should satisfy:

- exactly 30 raw seed CSV files;
- exactly 1,200 scenario-policy-seed rows;
- 30 seeds, five scenarios, and eight policies;
- `cloudsim_completion = 1.0` for all rows;
- maximum selected-service parity error no greater than 2 ms;
- no result-driven retuning flags set to true.

## Statistical analysis settings

- Bootstrap resamples: 20,000
- Bootstrap RNG seed: `4_202_202_699`
- Paired tests: two-sided Wilcoxon signed-rank tests
- Multiple-comparison correction: Holm correction within scenario/metric families
- Omnibus test: Friedman test on Mission late DVR across eight policies

## Runtime environment used in GitHub Actions

- Runner image: `ubuntu-24.04`, image version `20260907.300.1`
- Python: `3.12.14`
- Python packages installed by the aggregation job:
  - `numpy==2.5.3`
  - `pandas==3.0.5`
  - `scipy==1.18.1`
  - `tabulate==0.10.0`
  - `python-dateutil==2.9.0.post0`
  - `six==1.17.0`
- Java setup: Java 21 in the seed jobs
- Maven compiler release: 17
- CloudSim Plus dependency: `org.cloudsimplus:cloudsimplus:8.5.7`

## Reproduction command pattern

The aggregation job used the following command pattern after downloading all 30 E4.6 seed artifacts:

```bash
python scripts/e46_aggregate.py --input e46_raw --out e46_publication
```

The publication campaign itself was executed through the locked GitHub Actions workflow `.github/workflows/e46-online-dispatch-publication.yml` at run ID `34677758057`.

## Known result boundary

The E4.6 execution completed validly. One prelocked scientific gate failed: in `S3_HIDDEN_NETWORK_50LOSS`, CASPER_FULL did not meet the observed mean late-FWC gate of 0.99. This is a robustness boundary under hidden network degradation, not a CloudSim runtime failure.
