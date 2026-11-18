# JPDC Program A — CLOSEST-PRIOR-ART DIFFERENTIATION AND GO/NO-GO (2026-11-17)

**Status:** Targeted externally checked publisher/official-documentation screen and project-specific overlap audit; NOT a systematic exhaustive literature search. No submission-ready novelty claim yet. Research Program A remains a **conditional** venue candidate. Source was searched on 2026-11-17; sources are current publisher abstracts/API text unless otherwise noted. No full paper reprinting.

## Highest-risk specific related works

| Source (publisher metadata) | Actually established in source | Relation to our current A1/A2 result | Overlap risk / wording guard |
|---|---|---|---|
| **T. Vondra, J. Šedivý, J. M. Castro (2017)**, *Modifying CloudSim to accurately simulate interactive services for cloud autoscaling*, Concurrency Computation: Practice and Experience, 29(10), e3983, DOI **10.1002/cpe.3983**; https://onlinelibrary.wiley.com/doi/10.1002/cpe.3983 | Authors explicitly describe issues with *CloudSim job-duration computation* and introduce improved CloudAnalyst/CloudSim/autoscaling simulation, reporting large original relative-duration errors | Direct overlapping *category of concern*: reported service/duration mismatches; a new JPDC paper must not claim discovery that CloudSim-family job duration accounting can be problematic | **HIGH** for the generic premise; their 2017 CloudAnalyst-modified CloudSim is not the identical CloudSimPlus **8.5.7 SpaceShared** runtime nor our exact native timestamps and 24-case m-server comparison. Distinguish models/software/claims explicitly |
| **[Authors to complete from publisher record] (2019)**, *Modelling resource heterogeneities in cloud simulations and quantifying their accuracy*, Simulation Modelling Practice and Theory, 94, 43–65, DOI **10.1016/j.simpat.2019.02.003**; https://doi.org/10.1016/j.simpat.2019.02.003 | Published evaluation explicitly discusses validating extended CloudSim by **comparison with simplified analytical models** and accuracy of predicted quantities under heterogeneous resources | A2's comparison against simple analytical reference is **not methodologically first-of-kind** | **HIGH** for analytical reference comparison as novelty. Their CPU/platform heterogeneity and CloudSim accuracy questions are not necessarily same native queue-admission and deadline classification protocol; exact full-text comparative table still required before submission |
| **H. Casanova, A. Giersch, A. Legrand, M. Quinson, F. Suter (2014)**, *Versatile, scalable, and accurate simulation of distributed applications and platforms*, JPDC 74(10) 2899–2917, DOI **10.1016/j.jpdc.2014.06.008**; https://doi.org/10.1016/j.jpdc.2014.06.008 | SimGrid accuracy/scalability/model fidelity in the **target journal** | Model fidelity is known important distributed-systems research | **MEDIUM/HIGH** for broad framing, not exact CloudSimPlus 8.5.7 diagnosis |
| **D. Alshammari, J. Singer, T. Storer (2018)**, *Performance Evaluation of Cloud Computing Simulation Tools*, IEEE ICCCBDA, pp 522–526, DOI **10.1109/ICCCBDA.2018.8386571**; https://eprints.gla.ac.uk/180854/ | Simulator comparisons against micro-datacenter measurements; real vs simulated sensitivity | Field/hardware validity is harder than our fixed synthetic test; prior art already uses validation contrasts | **MEDIUM**. Our study does not claim comparable physical accuracy or hardware validation |
| **D. H. Sallo, G. Kecskemeti (2023)**, *Enriching computing simulators by generating realistic serverless traces*, Journal of Cloud Computing, DOI **10.1186/s13677-023-00397-8**; https://link.springer.com/article/10.1186/s13677-023-00397-8 | Evaluates workload trace conversion and cross-simulator behaviors, including a reported arrival-time handling discrepancy in tested CloudSim configurations | Explicitly precedes our message that submission/event-time semantics can make simulator outputs different | **MEDIUM/HIGH** for generic arrival timing claims; distinct serverless trace conversion/CloudSim version and tasks, not this exact SpaceShared callback study |
| **CloudSimPlus 8.5.7 SpaceShared API** https://javadoc.io/static/org.cloudsimplus/cloudsimplus/8.5.7/org/cloudsimplus/schedulers/cloudlet/CloudletSchedulerSpaceShared.html | Describes PE exclusivity, waiting list, and *no task priority* guarantee. *Neither equal-server FCFS ordering nor event-independent dispatch is guaranteed as identical behavior in published API docs.* | Strong reason to call reference FIFO a **deliberately different comparator**, not a failed CloudSim contract | **CRITICAL**. Avoid claims of proven FIFO violation, bug or broken official contract |
| **CloudSimPlus official FAQ** https://github.com/cloudsimplus/cloudsimplus/blob/master/docs/FAQ.rst | Distinguishes broker-level cloudlet ordering from VM-level PE scheduling; this is current project documentation and may not be exact 8.5.7 historical docs | Even if broker and scheduler scheduling layers differ, analytical FIFO is NOT by default exact native model | **CRITICAL**. Label as current project documentation and not exact archived source. Native binary/source v8.5.7 plus our logs remain primary software evidence |
| **M. C. Silva Filho et al. (2017)**, original CloudSim Plus framework, DOI **10.23919/INM.2017.7987304** | CloudSimPlus software architecture | Cited tooling; NOT novel simulator |
| **R. G. Sargent (2013)**, verification and validation, DOI **10.1057/jos.2012.20** | V&V are distinct from model fidelity | Establishes rigorous vocabulary; reproducible logs do not demonstrate operational validity |

## Comparison with own FGCS submitted CASPER work

First FGCS submitted manuscript **already covers** original algorithm, uncertainty certificates, limitations of event/queue counterfactual use, selected-node feedback, stochastic synthetic IIoT assumptions and original E42/E4.6 experiments. Detailed full-text comparison: [FGCS_FULL_MANUSCRIPT_VS_JPDC_OVERLAP_AUDIT_2026-11-04.md](FGCS_FULL_MANUSCRIPT_VS_JPDC_OVERLAP_AUDIT_2026-11-04.md). Program A does not present algorithmic CASPER improvement and cannot re-claim previously stated caveats as novel.

## Narrow factual contribution that survives *this* screen (not publication guarantee)

1. Method-level **CloudSimPlus version 8.5.7 native execution** of eligibility callbacks and submit-side WAIT/EXEC snapshots, with byte-for-byte nonintrusive observation comparison in six controlled arrivals (A1).
2. **Prespecified 24-condition same-input m-server FIFO-model contrast** over arrival families, deterministic jitter, native min-event intervals, VM PE capacity, with 288 real Java Cloudlets and two independent numerical auditors (A2).
3. A **separately identified posthoc sensitivity diagnostic** quantifying differences when service times are replaced with native-reported after-completion execution durations, not a real-time oracle: max gap 246ms requested vs154ms hindsight, residual >1ms in every fixed case, 250/288 job lengths differ. This limits overly broad queue-violation claims.

The observation “models differ” and “CloudSim duration calculation matters” are **ALREADY KNOWN**. Our incremental evidence is *version- and setting-specific* quantitative characterization, NOT a novel generic validation principle or complete causal identification.

## Unresolved before recommending JPDC as first choice

- Closest prior-art papers (Vondra 2017, heterogeneous CloudSim analytical comparator 2019, Sallo/Kecskemeti 2023) need direct **full-text** comparison where legal/readily available, not just metadata abstracts; if already exact same per-event diagnostics, pivot or add genuinely distinct contribution.
- Current A2 workload is only one VM, CPU-only, 12 jobs/case and fixed deterministic scenarios; weak distributed-systems breadth. It does NOT directly demonstrate any *actual online scheduling policy rank reversal* or real-world deadline effect, only synthetic threshold classification model disagreement.
- No direct native waiting-promotion method callback, no unique causal partition of service/update/admission. Avoid labels “exact cause solved” or “native execution start measurement.”
- Need define formal FIFO recurrence explicitly, including tie-breaking by actual observed submit callback sequence, not nominal arrival order.
- Need inspect whether original A2 native startWait-time definition has same time origin as reference measured wait; information from versioned API is necessary but not sufficient to assert equivalence.

## Decision and stopping rule

**Conditional GO to prepare manuscript**, not unconditional GO to JPDC submission. If accepted original contribution remains simply an illustrative comparison already treated by previous CloudSim accuracy studies, recommend a more specialized simulation-validation or computing software venue, or mark project as reproducible technical report, instead of salami-slicing/overclaiming. No more expansive unrelated native simulations without an actual identified validation-critical question. Program B distinct new risk-aware scheduling algorithm remains RESERVED.

## Sources and inspection provenance

Wiley original 2017 publisher full summary and author metadata: https://onlinelibrary.wiley.com/doi/10.1002/cpe.3983 ;
Elsevier 2019 publisher abstract / full-text status restricted: https://doi.org/10.1016/j.simpat.2019.02.003 ;
JPDC SimGrid source: https://doi.org/10.1016/j.jpdc.2014.06.008 ;
University of Glasgow institutional research record: https://eprints.gla.ac.uk/180854/ ;
Springer 2023 full article: https://link.springer.com/article/10.1186/s13677-023-00397-8 ;
Exact v8.5.7 API: https://javadoc.io/static/org.cloudsimplus/cloudsimplus/8.5.7/org/cloudsimplus/schedulers/cloudlet/CloudletSchedulerSpaceShared.html .
