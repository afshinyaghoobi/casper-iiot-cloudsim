# LATEST EDITORIAL PRIOR-ART GATE — 2026-11-17

[Working manuscript v0.3](JPDC_A_COMPLETE_WORKING_MANUSCRIPT_V03_2026-11-17.md) added explicit observed-native-submit FIFO m-server recurrence and direct nearest prior work. [Closest-prior-work comparison](JPDC_A_CLOSEST_PRIOR_ART_AND_NOVELTY_RISK_2026-11-17.md) confirms **HIGH** generic-method overlap: Vondra et al. 2017 documented CloudSim job-duration computation inaccuracies; Zakarya/Gillam 2019 compared CloudSim accuracy with simplified models; Sallo/Kecskemeti 2023 documented arrival-time handling disparities in simulator comparisons. Exact CloudSimPlus 8.5.7 Javadoc does not guarantee equivalence to our analytically defined FIFO m-server queue. Thus a JPDC article based only on “simulator outcomes differ” has real novelty risk. **Decision is still CONDITIONAL / NOT SUBMIT-READY.** Next limited tasks: manuscript mathematical and raw trace checks, direct full-text nearest-paper review, journal-appropriate article suitability and final coauthor approval. No more unmotivated simulation campaigns. Original negative parity and Stage65 safety remain failed. B research reserved.

---

# Program A — JPDC bounded submission-readiness checkpoint (2026-11-17)

**Decision:** ADVANCE TO MANUSCRIPT QUALITY / EDITORIAL ORIGINALITY CHECK. No need to run larger native simulation grid merely because existing tests returned a negative or simulator-dependent outcome. Submission target around Dec 20, 2026 remains a conditional **internal planning milestone**, NOT forecast of acceptance or proof of sufficient novelty.

## Completed source-verified tasks

| Gate | Current verified evidence | Status |
|---|---|---|
| A1 native mechanism | [Real Java run44214864810](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/44214864810), 6 cases, 18 finished, 54 eligibility callbacks and log-equivalent old harness | SUPPORTING COMPLETE, waiting-promotion branch not dynamically instrumented |
| A2 generalization | [Real Java run44215741883](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/44215741883), preregistered 24 synthetic cases 288 finished, two independent audit implementations, native log repeat | COMPLETE FOR FIXED SCIENTIFIC SCOPE |
| A2 confound | [Posthoc source reanalysis run44216958536](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/44216958536), 250/288 service durations differ; requested FIFO worst246ms, hindsight-service FIFO worst154ms, residual >1ms all24 cases | COMPLETE AS RETROSPECTIVE SENSITIVITY, NOT PROSPECTIVE HOLDOUT |
| Numbers and figures | [Original-data-derived all-24 CSV + vector SVG run44217510468](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/44217510468) including byte-identical figure/table rerun | GENERATED; manuscript visual quality and final format to confirm |
| Writing | [Full working manuscript v0.2](JPDC_A_COMPLETE_WORKING_MANUSCRIPT_V02_2026-11-17.md) has initial Abstract through Conclusion, partial references, A1/A2/retrospective results, threats | DRAFT COMPLETE, NOT SUBMISSION-READY |
| Literature | [Targeted primary-reference and FGCS overlap screen](JPDC_A_RELATED_WORK_ORIGINALITY_SCREEN_2026-11-17.md): verified CloudSimPlus, CloudSim, simulation validation, SimGrid JPDC precedent | INITIAL SCREEN ONLY; nearest-specific prior methods and originality unresolved |

## Scientific go/no-go rule (non-perfectionist, non-negotiable)
**GO only if** the final manuscript answers a distinct empirical systems-evaluation question *not already resolved or claimed in the earlier FGCS CASPER submitted manuscript or nearest CloudSim/SimGrid literature*, with a precise comparison model and raw source-backed values. No obligation to make a new CASPER algorithm, obtain 500 real Google files, reproduce hardware, remedy unrelated Stage65, or prove a CloudSimPlus bug. Two independent scientific components already exist; avoid expanding scope unless a critical defect is found.

**NO-GO / PIVOT if** novelty collapses to just “two different simulators/models have different outputs”, if the m-server FIFO reference is mischaracterized as CloudSim equivalence, if exact scheduler method semantics materially contradict the claims, or if journal scope requires a broader distributed-system contribution than this fixed CPU-only micro-study provides. Options: specialize to reproducibility/model-validation venue, reduce claims and present a technical note if venue supports, or return to Program B distinct algorithm paper. Do not retitle an unoriginal result and submit anyway.

## Remaining focused editorial tasks
- **Literature:** Read nearest primary queue/event-granularity/model-fidelity papers (not just abstracts), cite exact bibliographic records, compare methods and claims; distinguish well-known simulation-validation principle from our v8.5.7 quantitative observation.
- **Science/method:** Check formula for observed-order m-server FIFO and what CloudSimPlus `getStartWaitTime` measures; label native reported service as measured *by simulator*, not hardware. Ensure requested vs oracle posthoc results properly separated in abstract/table and no causal claim made from difference between 246 and154.
- **Figures/table:** Check vector SVG readability at journal column width and prepare appropriately formatted export; verify all-24 raw-cell CSV and totals.
- **Manuscript:** Clean placeholders, finalize author-approved title/abstract, statements of originality/limitations, citations, computational reproducibility, author order, competing interests, funding, data/code availability and journal-specific requirements.
- **Editorial:** Review official JPDC Guide for Authors, verify AI use disclosure requirements current at actual submission time; final approval by all authors before submission. No journal submission has been initiated or completed.

## Preserve separation and negative findings
FGCS original E42/E4.6 unchanged and should be properly cited. Original Java↔Python 30k strict FCFS fidelity max9.12140093294972ms >5ms **FAIL**; original Stage65 prospective policy safety **FAIL**. These are NOT corrected by A2 success. Program B next risk-aware policy paper remains RESERVED/NOT STARTED; see [two-paper master index](TWO_PAPER_RESEARCH_PROGRAM_INDEX_2026-11-17.md).
