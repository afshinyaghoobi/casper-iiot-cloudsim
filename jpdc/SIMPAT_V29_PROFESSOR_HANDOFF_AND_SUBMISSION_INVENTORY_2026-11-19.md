# SIMPAT — faculty handoff and final submission inventory

**Updated:** November 19, 2026. **Status:** author-facing materials prepared; final faculty review and publisher submission not yet done.

## Manuscript identification

- **Title:** Queue-Wait and Execution-Time Semantics in CloudSimPlus 8.5.7: Implications for IoT Scheduling Simulation
- **Authors:** Afshin Yaghoobi¹,*; Mahsa Nazemi Harandi¹
- **¹ Affiliation (both):** Department of Business Analytics, W. Frank Barton School of Business, Wichita State University, Wichita, KS, USA
- **Corresponding:** Afshin Yaghoobi, axyaghoobi@shockers.wichita.edu
- **ORCID Afshin:** 0009-0006-4695-6018
- **ORCID Mahsa:** 0009-0000-5395-5394

## Files for review and upload

| Role | Git-controlled source | Exported filename |
|---|---|---|
| Main manuscript | `SIMPAT_MANUSCRIPT_V29_CLEAN_PROFESSOR_REVIEW_2026-11-19.md` | `SIMPAT_Manuscript_v29_AUTHOR_REVIEW.docx` |
| Supplementary | `SIMPAT_V24_SUPPLEMENTARY_EXTENDED_RESULTS_2026-11-18.md` | `SIMPAT_Supplementary_AUTHOR_REVIEW.docx` |
| Highlights | `SIMPAT_V25_SUBMISSION_HIGHLIGHTS_2026-11-18.md` | `SIMPAT_Highlights_AUTHOR_REVIEW.docx` |
| Cover letter | `SIMPAT_V29_CLEAN_COVER_LETTER_FOR_PROFESSOR_2026-11-19.md` | `SIMPAT_Cover_Letter_AUTHOR_REVIEW.docx` |
| Figure 1 | `figure_a2_24_case_native_vs_fifo_2026-11-18.svg` | `Figure_1_A2_full_factorial.png`, plus SVG |

- The latest successful *previous* Word export, run 44475108479, contains a 15-page main PDF, five-page supplement, one-page cover letter, one-page highlights, two primary Word tables and one embedded figure.
- An *updated* workflow additionally uses the professor-facing clean cover letter and checks A2 24 rows / 86 / 107 / 246 against manuscript source before Word output. Download the **newest successful** run's artifact on the [workflow page](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/workflows/simpat-v25-word-export.yml), not the older run when the new one finishes.

## Evidence checks preserved

- Primary experiment: 24 conditions × 12 Cloudlets = 288; +25 ms mismatch 86/288; +50 ms mismatch 107/288; maximum within-case wait gap 246 ms.
- 250/288 requested/native execution duration discrepancies; A3 native timestamp origins equal at logged precision 288/288.
- Six A1 known microfixtures, event-level controls, eight additional predefined fixtures and negative input-only directional hypothesis (1/4 versus 1/4).
- Source/raw evidence frozen at Git commit `95424c68d8e3824c76c0a249cec6b0c5e3491184` with checksum manifest. No new experiment or claim made during packaging.

## Author-provided declarations already included

- Funding: no specific grant from public, commercial or nonprofit sectors.
- Competing interest: none known as declared by the authors.
- CRediT: full roles for Afshin and Mahsa, supplied by corresponding author.
- Data: upon reasonable request from corresponding author; substantial original code/logs already publicly linked in the repository.

## Remaining human action before submission

1. **Professor/corresponding author review** of the main Word and PDF, including equation rendering, 24-row table, figure labels, source links, typo/layout issues and confirmation of both authors' approval.
2. **Publisher-policy/compliance review:** professor to take responsibility for truthful and complete disclosure of generative-AI assistance under the applicable Elsevier journal policy, including assistance in research methods and manuscript preparation. Do not present omission as a factual statement that no tool was used. Historical FGCS CASPER submission was rejected; avoid treating it as simultaneously pending, but confirm no inappropriate duplicated content.
3. **Final journal portal check** of accepted category, format, figure and supplemental uploads, competing interests declaration fields, and corresponding author data. Journal editor decides suitability. The actual journal portal has **not** been used by this workflow.

## Explicit limitations of QA

- Github Actions conversion and successful PDF generation demonstrate basic file integrity, **not a manual page-by-page print proof**.
- No article acceptance, editorial communication, DOI deposit, live portal submission or coauthor consent is asserted here.
- Generated Word/PDF names retain `AUTHOR_REVIEW` so the professor does not accidentally upload unapproved drafts.
