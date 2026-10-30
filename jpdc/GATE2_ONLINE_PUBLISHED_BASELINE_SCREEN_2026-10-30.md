# JPDC Gate 2 — verified online-placement shortlist (2026-10-30)

**Source screening, not implementation or simulator evidence.** Objective: select an independent online comparator under E45's irrevocable per-arrival mapper, heterogeneous 24 nodes, hidden compute/network shocks, CPU-only CloudSim execution and algebraic network response time.

## Screened primary publications

### 1. Kaur & Auluck (2022), FiFSA / EFSA
*Scheduling algorithms for truly heterogeneous hierarchical fog networks*, Software: Practice and Experience 52(11), 2411–2438, DOI 10.1002/spe.3132. Publisher abstract: FiFSA assigns an online job to the **first fog device with sufficient spare capacity**. EFSA uses load-aware MinMin / minimum completion time. This is the most promising **mechanistically different** arrival-only placement candidate. Source: https://onlinelibrary.wiley.com/doi/10.1002/spe.3132

**Critical mapping gap:** E45 does not expose a physical per-job spare-CPU-capacity admission gate. Each VM admits queued cloudlets; its queue estimator provides predicted waiting time and a nominal service time. Converting "sufficient spare capacity" into `backlog==0`, `predictedLatency<=deadline`, or a utilization threshold without the source's exact definition would be a **FiFSA-inspired adaptation**, not a paper-faithful reproduction. An order-sensitive "first" rule also requires a specified fixed/priority tier order, not a convenient order tuned after observing seed-zero results.

**Implementation gate:** acquire full paper's eligibility formula, network model, hierarchy search order, spillover/fallback and online/batch distinction. If unavailable, pre-register a transparent `FIRST_IDLE_TIER` control with fixed tier ordering and label it **inspired**, not literal FiFSA.

### 2. Han et al. (2019), OnDisc
*OnDisc: Online Latency-Sensitive Job Dispatching and Scheduling in Heterogeneous Edge-Clouds*, IEEE/ACM Transactions on Networking 27(6), 2472–2485, DOI 10.1109/TNET.2019.2953806. Source: https://hub.hku.hk/handle/10722/294269

Strong arrival-time and heterogeneous-server relevance; includes upload and download delays, arbitrary releases and weighted response time. **Gap:** jointly controls dispatch and server-side scheduling, uses speed augmentation and targets total weighted response time, not mission deadline-window DVR. Abstract does not provide enough pseudocode to implement source-faithfully. Candidate for deeper reading, *not yet approved for direct E45 insertion*.

### 3. Meng et al. (2020), Dedas
*Online Deadline-Aware Task Dispatching and Scheduling in Edge Computing*, IEEE TPDS, DOI 10.1109/TPDS.2019.2961905. Source: https://bip.imsi.athenarc.gr/site/details?id=10.1109%2Ftpds.2019.2961905

Online task arrivals, bandwidth and deadline constraints, but explicitly allows replacement of some **previously scheduled tasks**. E45's irreversible VM mapper does not. Do not label a non-replacing approximation Dedas.

### 4. IEEE TVT (2025), hard-deadline vehicular scheduling
*Task Offloading and Scheduling Under Hard Deadlines in Vehicular Edge Computing Systems*, DOI 10.1109/TVT.2025.3539885. Source: https://ieeexplore.ieee.org/abstract/document/10878130

Tasks arrive randomly and practical server-information acquisition is modeled. Online offloading integrates Moore–Hodgson admission/reordering. Good information-visibility reference, but not directly equivalent to irrevocable E45 placement.

### 5. Azmi, Haque, Murad (2026), GMO / RT-MOMFO
*Comparative analysis of task scheduling in multi-tier fog-cloud computing: from classical approaches to greedy multi-objective optimization*, Journal of King Saud University — Computer and Information Sciences 38, article 258, DOI 10.1007/s44443-026-00649-y. Source: https://link.springer.com/article/10.1007/s44443-026-00649-y

Explicit online adaptation with ready-queue management and tier cycling. A potentially strong contemporary methodological comparison, but its *periodic tier cycling and queue policy* differ from E45. Paper states full pseudocode in Section 4; examine before deciding whether equivalent arrival-only adaptation is feasible.

## Selection decision

**No paper-faithful new policy is yet authorized by the accessible source evidence.** Prioritize obtaining FiFSA's full decision rule. This avoids the earlier documented failures: renaming PRED_GREEDY as MCT, renaming max raw slack as a novel baseline, or importing online EDF/HEFT/TSSLA with incompatible queue/scheduling rights.

A separate **clear exploratory control** based on a fixed tier search and currently empty queue could be valid, but it must not be presented as FiFSA faithful or published SOTA. Evaluate with frozen original E45 and precommitted paired seeds.

No actual CloudSim pilot run or performance numbers have been verified. Frozen E4.6 unchanged.
