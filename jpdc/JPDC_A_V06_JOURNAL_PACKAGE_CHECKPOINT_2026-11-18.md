# JPDC Program A — working submission package v0.6 and remaining decision gates (2026-11-18)

## Actual new deliverables completed this continuation

- [Journal-facing manuscript v0.6](JPDC_A_JOURNAL_FACING_MANUSCRIPT_V06_2026-11-18.md): Abstract, full numbered scientific sections, observed-submit-order analytical FIFO model, exact Java 8.5.7 Cloudlet native waiting definition, 24-case Table 1 embedded, source-committed Figure 1, A1/A2/A3 outcomes, service-duration posthoc confound, bounded discussion, validity threats, references and GitHub reproducibility. **This is a working submission-format copy, not a paper accepted for review or an actual journal submission.**
- [Permanent all-24 primary data](manuscript_a2_primary_24_cases_2026-11-18.csv) and [source-referenced vector Figure 1](figure_a2_24_case_native_vs_fifo_2026-11-18.svg), rather than solely expiring GitHub Actions artifacts.
- Original source archive `jpdc_a2_24_case.zip` original GitHub artifact ID14387238746 was independently verified against SHA256 **1d29943e5e48d27f65eed186df23ff22d3dd7bdab381ebe63fca88dba1e3bb4b** in the active analytical container. On original archived primary audit JSON, 24 cases, all288 fixed jobs and overall mean abs wait difference **49.0960972223 ms**; source row mean signed average44.1877638889ms. These are fixed synthetic job-condition means, NOT independent sampling estimates. For the 24 case-level maxima: range24–246ms; all-cases median73.3055ms. Source author input unchanged.
- New reproducible [static package QA](audit_a2_manuscript_v06_package.py) and [successful GitHub Actions run44324159517](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/44324159517), all24 table rows cross-matched to permanent CSV, all24 labels appear in SVG, totals 86(+25ms)/107(+50ms), max246ms, source references present, internal TODO labels stripped. GitHub artifact14434874439; uploaded artifact ZIP SHA256 reported **04ac5180d4d571f4819168fcfd97b29e29249b728ffd231330dce497c9352a67**. Static QA does **not** certify external scientific novelty or content validity.

## Invariants and important negative findings

- A1 genuine CloudSimPlus 8.5.7 6-case native callback audit and 54 callbacks PASS; A2 24-case 288 Cloudlets real Java and independent auditors PASS; A2 posthoc native-service mismatch250/288 with worst native-vs-hindsight FIFO154ms, still residual>1ms in all24; A3 288 native jobs show datacenter arrival and scheduler-submit times identical at logged precision with exact original A2 control log.
- Original earlier 30k Java↔Python strict FCFS fidelity max9.12140093294972ms >5ms **FAIL**; Stage65 safety **FAIL**. Do not change these conclusions. No new CASPER policy, no real-world IIoT deployments, no CloudSimPlus bug proof.
- Old FGCS CASPER submitted draft already contains original algorithm, queue approximation and feedback limitations; no new published status inferred; proper differentiation remains mandatory.
- Evidence-tiered related-work screen: Vondra2017 publication summary (not accessed full text), Zakarya/Gillam2019 abstract/institutional metadata (full text not audited), Sallo/Kecskemeti2023 open publisher full article directly read. Prior literature clearly covers CloudSim service-duration inaccuracies, model comparison and submit-time sensitivity; claim of generic novelty prohibited.

## Actual readiness and next minimal tasks

| Gate | Result | What is still needed |
|---|---|---|
| A1/A2/A3 source numeric experiments | PASS | No additional trial unless scientific critical check fails |
| 24-case table and permanent vector figure | PASS static QA + original source archive verified | Journal column-width visual review and final PDF/doc packaging only after venue choice |
| Journal-facing paper text | v0.6 assembled | Bibliography styling and final copyedit; author verification of statements |
| Nearest-paper originality and full-text comparison | **INCOMPLETE** | Read legitimate full texts of closest Vondra2017 and Zakarya/Gillam2019 when accessible; otherwise disclose access limits and avoid priority claims |
| JPDC suitability | **NOT ESTABLISHED** | Current study single VM CPU-only; choose if sufficient substantial independent distributed-systems evidence vs a simulation-oriented journal |
| Authors and editorial declarations | **NOT APPROVED** | Author list/affiliations, earlier FGCS manuscript disclosure, funding/conflicts, generative AI declaration according to eventual publisher, licensing/data availability |
| Journal submission | **NOT DONE** | Author decision, guide compliance, final source or PDF and cover letter |

**Non-perfectionist decision:** stop unnecessary expansion, not scientific caution. Working manuscript now serves as a durable base for final editorial review. Conditional internal target Dec20, 2026; do not force inappropriate JPDC submission. An alternative journal with more direct simulation verification scope may be better, but no venue has been selected yet.

**Future Program B:** independent policy paper remains RESERVED and NOT STARTED under [original roadmap](NEXT_PAPER_RISK_AWARE_SCHEDULING_RESEARCH_ROADMAP_2026-11-17.md).

## Next continuation

Prefer an actual bounded **author-oriented editorial review** of v0.6: check reference metadata and full texts where possible; use target journal guide; produce a venue-specific submission package only once author/venue decision is justified. No new simulation campaigns without critical methodological need.
