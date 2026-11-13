# Stage57 preregistration — baseline fidelity, exact Online-MCT alias audit (2026-11-13)

## Motivation, literature and pre-outcome decision
Stage56 original nine-case CloudSimPlus completion gate FAILED; Stage56B retrospective evidence of queue timing discrepancy is preserved. Stage52 modern queue-pressure-inspired comparator failed its S2 no-harm gate. More heuristic variants are not valuable without credible externally grounded and **distinct** baseline implementation. This stage is a *methodology and software identity audit*, not a fresh algorithm, independent workload, or efficacy study.

Grounded 2026 journal methods:
- Wu et al. (2026) **DFAQ-LB**, Future Generation Computer Systems 182, 108460, DOI 10.1016/j.future.2026.108460: elastic queue capacity regulation, multidimensional VM health (CPU/MIPS/memory/bandwidth), adaptive congestion response and possible migration. Our `QUEUE_PRESSURE_05` and `QUEUE_PRESSURE_E2E_05` do **not** implement its complete method; call them simple queue/feedback-inspired controls, never 'reproduced DFAQ-LB'.
- Lei et al. (2026) **AUHS**, Journal of Parallel and Distributed Computing 216, 105308, DOI 10.1016/j.jpdc.2026.105308: stochastic arriving *serverless workflows* with DAG/function hierarchy, container state, cross-workflow iterative ordering, user satisfaction objective. Original full method is **not** a faithful online independent cloudlet dispatcher on CASPER synthetic workload.
- Braun et al. (2001) classic MCT: original class of *static independent meta-task* scheduling, not the same as our online assignment; an 'online MCT-style arrival adaptation' must be labeled an adaptation.
- Topcuoglu et al. (2002) HEFT includes DAG upward ranking and insertion; one-step EFT is NOT HEFT.

## Fixed test: non-independent Online MCT alias
CASPER's existing online PRED_GREEDY scores each eligible node using
`predicted_latency(task,node,virtual_queue.predicted_backlog(node,now))`:
`RTT_j+(inputMB+outputMB)*8000/BW_j+max(0,next_free_j-now)+12*work/cap_j`.
Its argmin is deterministic lowest-node-ID tie. The naive online MCT variant proposed in earlier Gate2, when given **exactly the same predictor, eligibility and tie rule**, also minimizes predicted end-to-end completion latency relative to the task arrival; since arrival is shared across all nodes, minimizing absolute predicted completion time `now+pred[j]` is algebraically identical to minimizing `pred[j]`. **Hypothesis: it is an exact policy alias, not an independent control.**

Before outcomes, choose fixed QA seed indexes [1301,1302,1303] and scenarios S0_STATIONARY, S2_HIDDEN_COMPUTE_40LOSS, S3_HIDDEN_NETWORK_50LOSS, first 1200 synthetic tasks each. Build the same node list and task stream and an independent causal virtual queue updated per dispatch. For each task compute the 21 native predictor scores and compare (a) PRED_GREEDY argmin, (b) online-MCT absolute-completion argmin. Assert equal node **at every decision**, including tie. Track node assignment and source task conservation, no future outcomes and no oracle fault mask. Perform exact repeat and byte-identical JSON. Negative fixture: changed node eligibility, one-task future queue oracle, and missing transfer term can cause non-equivalence and **must be rejected as the same baseline definition**.

If all 10,800 decisions match: no separate baseline performance run or independent method claim. If they diverge, report failure and diagnose actual source formula or tie semantics; do NOT force 'alias' by changes to CASPER source. In either case, results are 3 QA seeds ×3 scenarios, not independent method efficacy data.

## Fair baseline decision matrix, fixed now
| Candidate | Causal information equivalence | Scope compatibility | Original-author-fidelity | Decision |
|---|---|---|---|---|
| PRED_GREEDY original | yes, arrival-time task + predictor state | exact native model | native CASPER original | retain control |
| Online MCT arrival-only same cost function | yes, same data | exact independent-task placement | MCT *adaptation*, not Braun original | alias audit; do not double-count if identical |
| Original DFAQ-LB Wu2026 | needs queue trends/health/migration & live VM metrics | cloud load balancing broadly relevant; state/migration model differ | cannot claim authors' implementation | method-gap matrix; full faithful implementation requires complete source/formulas/state |
| Queue pressure simple Stage52 | yes under simulator assumptions | exact synthetic tasks | explicitly NOT DFAQ-LB | retain negative published comparison, not promote |
| Original AUHS Lei2026 | requires multi-level workflow, function dependencies and containers | mismatched independent cloudlet setting | cannot claim authors' implementation | literature comparison only, or separate DAG/FaaS study |
| HEFT original | needs entire DAG and insertion planning | mismatched independent task arrivals | not faithful if one-step EFT | exclude as 'HEFT' baseline |
| Deadline-first EDF/TC-first batch heuristic | requires nonzero observation window / batching, arrivals through window | plausible online scheduler but changes timing and task-admission model | not author reproduction | only separate prospective design with same allowed delay and overhead |

No additional simulator performance seeds or code changes to E42/E4.6/Stage52. Original 30k Java/Python wait parity remains FAIL 9.12140093294972ms>5ms; original Stage56 9/9 completion gate FAIL. This Stage57 is limited to rigorous baseline deduplication and research-method fidelity.
