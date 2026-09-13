# CASPER-IIoT E4.6 Frozen Publication Artifact

Release tag: `v1.0.0-casper-iiot-e46`  
Version: `1.0.0-casper-iiot-e46`  
Date: `2026-09-13`

## Scope

This release archives the frozen CASPER-IIoT reproducibility package used by the companion FGCS manuscript. It is an archival/reproducibility release, not a new scientific campaign.

## What is included

Attach these assets to the GitHub release:

1. `e46-publication-results.zip`
   - SHA-256: `d1cf8be940669f9551dec34505ee75784142b5d14eb5f6d7c737e0281bc2c1c9`
   - GitHub Actions artifact name: `e46-publication-results`
   - GitHub Actions artifact ID: `10292758918`
   - Workflow run ID: `34677758057`

2. `E56H_Minor_Revision_Cleanup_Submission_Polish_Package.zip`
   - SHA-256: `439822dae05d727b5e26cd6ee3b32a42fe924d73257b2e3bc3f055d9fa3771b7`
   - Purpose: reviewer-cleaned manuscript support package, including the E5.6H minor-revision cleanup materials.

## Frozen source and workflow anchors

- Frozen scientific source SHA: `ee1600b808a9747bc0373489e8ce531bd6bfb5e0`
- E4.6 orchestration commit: `fb8fab039886a98ba582541d15956bb4a01569ff`
- E4.6 closure/provenance commit: `896d7f01be26f70c9259b938aa1a3f67c2f757c6`
- E4.5 validated preflight SHA: `cd4727bf9125d43bbfe8c48aea61960d5eb3b2de`
- E4.5 preflight run ID: `34677313227`
- CloudSim Plus dependency: `org.cloudsimplus:cloudsimplus:8.5.7`

## Campaign design

- Seeds: 30
- Scenarios: 5
- Policies: 8
- Scenario-policy-seed rows: 1,200
- Deployment tasks per scenario-policy-seed: 30,000
- Calibration tasks per seed: 80,000
- Calibration burn-in: 10,000
- Seed formula: `4_202_202_600 + seed_index`, for `seed_index` in `0..29`

## Important scientific-integrity note

No result-driven retuning was performed. This release does not modify frozen thresholds, workloads, disturbance scenarios, policy logic, conformal quantiles, seed construction, detector windows, or frozen campaign outputs. The E4.6 campaign outcome remains valid-complete with one prelocked scientific gate failure: `S3_HIDDEN_NETWORK_50LOSS` did not meet the observed mean late-FWC threshold of 0.99. This is reported as a robustness boundary, not an execution failure.

## Recommended citation before DOI assignment

Yaghoobi, A. (2026). *CASPER-IIoT: Frozen CloudSim Plus Online-Dispatch Publication Artifact* (Version 1.0.0-casper-iiot-e46). GitHub/Zenodo archival release.

After Zenodo assigns a DOI, replace the temporary citation with the Zenodo version DOI citation.
