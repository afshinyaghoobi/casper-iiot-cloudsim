# CASPER-IIoT CloudSim Plus Reproducibility Package

This repository contains the frozen implementation and provenance records for CASPER, a conformal adaptive scheduling framework for robust online dispatch in cloud-edge Industrial Internet of Things (IIoT) settings.

## Archival release

The intended archival release tag is `v1.0.0-casper-iiot-e46`. The release is designed for GitHub-Zenodo archiving and DOI assignment.

Recommended release title:

```text
CASPER-IIoT E4.6 Frozen Publication Artifact
```

## Frozen anchors

- Frozen scientific source SHA: `ee1600b808a9747bc0373489e8ce531bd6bfb5e0`
- E4.6 orchestration SHA: `fb8fab039886a98ba582541d15956bb4a01569ff`
- E4.6 closure/provenance SHA: `896d7f01be26f70c9259b938aa1a3f67c2f757c6`
- E4.6 workflow run ID: `34677758057`
- E4.6 publication artifact ID: `10292758918`
- E4.6 publication artifact ZIP SHA-256: `d1cf8be940669f9551dec34505ee75784142b5d14eb5f6d7c737e0281bc2c1c9`
- CloudSim Plus dependency: `org.cloudsimplus:cloudsimplus:8.5.7`

## Scientific integrity statement

The E4.6 results are frozen. Metadata, citation, and release-preparation files do not change workloads, thresholds, seeds, policies, scenarios, statistical logic, or scientific outcomes. The `S3_HIDDEN_NETWORK_50LOSS` result is preserved as a transparent robustness boundary rather than treated as an execution failure.

## Reproduction overview

The E4.6 campaign contains 30 seed replications, five scenarios, eight policies, and 1,200 scenario-policy-seed runs. The seed formula is:

```text
scientific_seed = 4_202_202_600 + seed_index
seed_index ∈ {0, ..., 29}
```

The aggregation job validates all 1,200 rows, verifies 30 raw seed CSVs, checks CloudSim completion, and enforces the 2 ms selected-service parity gate.

See `docs/release/E46_ARTIFACT_README.md` and `docs/release/RELEASE_NOTES_v1.0.0-casper-iiot-e46.md` for release-specific details.
