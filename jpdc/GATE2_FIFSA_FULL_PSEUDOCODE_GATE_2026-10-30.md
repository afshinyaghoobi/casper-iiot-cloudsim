# JPDC Gate 2 — FiFSA full-pseudocode reproducibility gate (2026-10-30)

## Verified primary source
Kaur & Auluck, *Scheduling Algorithms for Hierarchical Fog Networks*, preprint arXiv:2112.04715 (2021), p. 5–6, Sections III–IV, Algorithms 1–4. Published related version: *Scheduling algorithms for truly heterogeneous hierarchical fog networks*, Software: Practice and Experience 52 (2022), DOI 10.1002/spe.3132. Cite the actual checked preprint pseudocode instead of assuming every detail is identical in the journal version.

- PDF: https://arxiv.org/pdf/2112.04715
- Published record: https://doi.org/10.1002/spe.3132

## Concrete observed algorithm
Algorithm 1 FiFSA input is a **queue of jobs J**, not just the job arriving now. For the queue it sorts jobs in increasing CPU requirement `Delta(job)` and scans tier-1 devices sequentially, then tier-2, and so forth; a job is assigned to the first device judged to have sufficient capacity; otherwise it goes to cloud. Section III specifies M/M/1 service model (`mu`, `lambda`) and introduces a spare-capacity variable `delta`; the short pseudocode tests `mu_i >= Delta_job`. The exact translation of "spare" as an instantaneous E45 VM slot is **not** justified: E45 queues CPU-only Cloudlets and tracks next-free-time, not a literal CPU-reservation/instantaneous `mu-lambda` admission budget.

Additional incompatibility: Algorithm 1's job sorting presumes a queue/batch of more than one task; E45 makes irrevocable decisions at single-task arrivals and has no shared queue of unscheduled tasks to reorder. In singleton windows the sort disappears, turning it into a *FiFSA-inspired online first-fit tier scan* rather than the full published FiFSA.

Algorithm 2 EFSA queues by tier and Algorithm 4 MinMin repeatedly selects across queued unscheduled jobs: also not a drop-in online mapper.

## Explicit decision
**Original FiFSA and EFSA are not certified paper-faithful same-information E45 baselines.** A defensible method must either:
(A) reproduce original queue-based method in a separately defined common batch/online-window scheduling harness and rerun CASPER on the same modified harness, including equivalent information, queues, network and CPU accounting; or
(B) pre-register a clearly named **FiFSA-inspired arrival-only first-fit tier** heuristic, with specified tier order, exact eligibility threshold, stable deterministic ties and cloud overflow. Do not call this the original algorithm.

For (B) the threshold is a design choice and must not be tuned using seed-zero outcomes. Require an independent baseline study and paired-seed run before citing performance.

No algorithm implemented, no CloudSim result verified, frozen E4.6 unchanged.
