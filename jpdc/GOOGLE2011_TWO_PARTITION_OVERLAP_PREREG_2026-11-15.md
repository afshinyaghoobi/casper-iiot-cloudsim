# Prospective two-partition Google Borg 2011 source-overlap audit — 2026-11-15

## Pre-outcome objective
Test whether **two separately selected original GCS event files** have overlapping observed source timestamp intervals, `job_id` and `(job_id,task_index)` identifiers and whether first-1024-row event-history censoring differs. This provides evidence on the **feasibility of creating genuinely disjoint data source units**, not independent random population sampling and not deadline-aware scheduler validation.

**Frozen original source objects, chosen before examining their original rows:** `gs://clusterdata-2011-2/task_events/part-00125-of-00500.csv.gz` and `gs://clusterdata-2011-2/task_events/part-00425-of-00500.csv.gz`. Exactly those two, no candidate substitution. The earlier explored parts 00000, 00250, 00375 are spent for unbiased discovery; compare descriptively only, not independent holdout.

For **each original file separately**: obtain publisher GCS generation, object size, CRC32C/MD5, complete exact key, then fetch exactly first 262144 bytes using GCS HTTP206 Range bytes0-262143. Inflate at most1048576 original gzip bytes; parse first1024 complete original, headerless 13-field Google Borg 2011 version2.1 `task_events` rows. If fewer than1024, fail original strict gate; do not adapt thresholds. Record raw compressed sha256, original HTTP content range, row count, timestamp range, missing requested CPU and machine ID, event-code counts. Original Google v2.1 SUBMIT0/SCHEDULE1/EVICT2/FAIL3/FINISH4/KILL5/LOST6/UPDATE_PENDING7/UPDATE_RUNNING8. Reject v3 mixing. The selected 1024 records are **contiguous early source-file prefixes** and may be highly nonrepresentative.

## Prespecified provenance/overlap and independence test
For each source row retain in-memory original `job_id`, `(job_id,task_index)`, `time_us`; emit only aggregate or SHA-backed checks, not unnecessary raw IDs. Cross-file compare:
1. number of source `job_id` identifiers appearing in both 1024-row cohorts;
2. number of source `(job_id,task_index)` identifiers appearing in both cohorts;
3. overlap of the **inclusive timestamp intervals** `[first_time,last_time]`, plus signed temporal gap if disjoint, minimum0;
4. event histograms and source-job grouping in each cohort;
5. classify source overlap: `OBSERVED_KEY_OVERLAP` when any same source job/task, `TIMESTAMP_WINDOWS_OVERLAP_NO_OBSERVED_KEY_OVERLAP` when time windows overlap without visible keys, or `NO_OBSERVED_KEY_OR_TIME_OVERLAP_IN_SELECTED_PREFIXES` when neither overlaps.

Scientific caveat: absence of overlap in limited 1024-row prefixes **does not establish full-partition or full-job source independence**; jobs can recur outside observed prefixes and dataset partition files are not guaranteed time-independent source units. A real independent statistical holdout requires whole-job isolation and prospective time/cluster splits with supported sampling frame. No causal / p-value / system performance claim follows.

## Prespecified experimental gates
- **Technical PASS** if the two exact official source objects yield source SHA-verified valid rows, all 13 column/event/chronological and deterministic offline rerun and immutable original guards.
- **Independence gate**: intentionally **NOT CERTIFIABLE** by this design; it remains `UNRESOLVED_FULL_SOURCE_INDEPENDENCE` regardless of observed sampled overlap. If overlap is observed, explicitly recommend rejecting naive file-as-independent-seed inference. If no sampled overlap, do NOT promote the files to independent cohorts.
- Preserve original Stage65 source-n8 safety FAIL, Java↔Python original queue waiting parity FAIL; no raw `network_bytes` nor `deadline`, CPU request only resource allocation, not task execution. Original FGCS E42/E4.6 and rejected Stage64 method immutable.
- Independent artifact-only check must reconstruct key/time overlap from archived original compressed bytes **without invoking the source parser**, and compare source results/byte-repeat, preserving any failures.

This is a cross-domain **Google Borg datacenter trace**, not actual industrial IIoT; not a full 29-day population sample or a workload-driven CASPER evaluation. Record exact source run, artifacts, hashes and limitations in both permanent handoffs after independent verification.
