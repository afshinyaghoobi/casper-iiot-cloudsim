# Zenodo and GitHub Release Steps

Use these steps after this metadata branch is merged.

## 1. Confirm metadata and license

Before publishing the release, review these files:

- `CITATION.cff`
- `.zenodo.json`
- `LICENSE`
- `docs/release/RELEASE_NOTES_v1.0.0-casper-iiot-e46.md`
- `docs/release/E46_ARTIFACT_README.md`

This preparation uses the MIT license for the software/release metadata. If you prefer a different license, change `LICENSE`, `CITATION.cff`, and `.zenodo.json` before publishing the GitHub release.

## 2. Enable the repository in Zenodo

1. Log in to Zenodo using the account you want associated with the DOI.
2. Open the Zenodo GitHub integration page.
3. Sync repositories if needed.
4. Enable `afshinyaghoobi/casper-iiot-cloudsim`.

## 3. Create a GitHub release

In GitHub, open the repository and go to **Releases** > **Draft a new release**.

Use:

- Tag: `v1.0.0-casper-iiot-e46`
- Target: the merged metadata commit on `main`
- Release title: `CASPER-IIoT E4.6 Frozen Publication Artifact`
- Release notes: paste the content of `docs/release/RELEASE_NOTES_v1.0.0-casper-iiot-e46.md`

Attach these binary assets:

- `e46-publication-results.zip`
- `E56H_Minor_Revision_Cleanup_Submission_Polish_Package.zip`

Do not mark this as a pre-release unless you intentionally want it treated as non-final.

## 4. Wait for Zenodo

After GitHub publishes the release, Zenodo should process the release and create an archival record. When Zenodo displays the DOI, use the **version DOI** for the exact release in the manuscript Data and Code Availability statement.

## 5. Update manuscript metadata

After DOI assignment, update the manuscript, cover letter, and declarations with:

```text
Code and data availability: The frozen CASPER-IIoT E4.6 source and artifacts are archived at Zenodo: [VERSION DOI TO INSERT]. The GitHub release tag is v1.0.0-casper-iiot-e46.
```
