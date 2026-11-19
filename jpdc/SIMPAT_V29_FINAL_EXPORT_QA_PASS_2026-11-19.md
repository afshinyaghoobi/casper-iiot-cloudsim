# SIMPAT v2.9 — clean package QA passed

**Date:** 2026-11-19. **Status:** reproducible Word/PDF export completed successfully; professor and coauthor final approval and actual submission pending.

## Final validated build

- [Final clean cover-letter export — GitHub Actions run 44542306844](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/44542306844)
- **Conclusion:** success; source commit `38e6df2e4b7de8da1b74bcec7b6b1d7ff76147f4`.
- **Artifact:** `simpat-v29-author-review-word-and-pdfs` (ID `14538148312`, ZIP size 810,571 bytes; 30-day workflow artifact retention).
- Main `SIMPAT_Manuscript_v29_AUTHOR_REVIEW.docx`: **180,962 bytes**, 115 body paragraphs, **two Word tables**, **one embedded A2 Figure 1**, **15 rendered PDF pages**.
- `SIMPAT_Supplementary_AUTHOR_REVIEW.docx`: 33,196 bytes, 5 rendered PDF pages.
- `SIMPAT_Highlights_AUTHOR_REVIEW.docx`: 23,497 bytes, 1 rendered PDF page.
- `SIMPAT_Cover_Letter_AUTHOR_REVIEW.docx`: **24,375 bytes**, 11 body paragraphs, 1 rendered PDF page. This is the **clean, author-addressed cover letter**, not the old internal placeholder-laden draft.
- Original Figure 1 SVG and PNG also exported.

## Checks passed in final build

- Primary main-text table contains exactly 24 distinct cases; recomputed sums 86 and 107, maximum absolute wait discrepancy 246 ms.
- Sequential bibliography references [1] through [12] intact.
- Required declarations (funding, author contributions, competing interests, data availability) retained.
- Exact title, both named authors and ORCIDs, corresponding email, key outcome/negative-result anchors present in exported Word.
- Non-empty Word files, primary embedded figure/two tables, PDF render to nonempty pages with valid page dimensions.
- No original Java simulation, source data, negatives, numerical outcome, approved title or authorship changed to fix the export.

## Remaining steps

1. Manual author/faculty visual proof of the main 15-page PDF plus supplementary, checking math, page breaks, wide Table 1, link accessibility and Figure 1 legibility. Automated rendering is not equivalent to full visual review.
2. Professor to resolve publisher-specific AI assistance declarations in final version using truthful research/manuscript preparation history, as requested by the authors. This task was **not** marked complete or silently omitted.
3. Confirm all author approvals and the current SIMPAT submission form required fields and files; upload only after authorization. An earlier separate FGCS paper was rejected and is not under concurrent consideration. No manuscript submission or publication claim.

**Latest manuscript source:** `SIMPAT_MANUSCRIPT_V29_CLEAN_PROFESSOR_REVIEW_2026-11-19.md`. 
**Latest matching clean cover letter:** `SIMPAT_V29_CLEAN_COVER_LETTER_FOR_PROFESSOR_2026-11-19.md`.
