# VERIFIED — actual SQLite source resume hardened with atomic exact-identity digests and original source-backed migration (2026-11-16)

## Scientific engineering question
The previous real original Google Borg2011 task_events part375 SQLite prototype (`jpdc/google2011_sqlite_job_inventory.py`) returned `ALREADY_VERIFIED_NOOP` based on only source generation and compressed SHA. Consequently a completed DB could lose or replace a `job_presence`/`task_presence` entry while preserving file_inventory, and the ingest could silently skip rereading the source. The previous 500-file offline preflight identified this **actual safety deficit**, not a scheduler-effect hypothesis. This iteration **changes the real ingest path**, not just a separate validator, and tests an altered same-cardinality real-source DB copy.

## Frozen pre-outcome protocol
`jpdc/GOOGLE2011_SQLITE_RESUME_DIGEST_PREREG_2026-11-16.md` commit **911f2f81920cfd24bf423433b50476a588cc3691** before source modification. Frozen genuine **previously spent** Google Borg2011 v2.1 original gzip `task_events/part-00375-of-00500.csv.gz` source from original GitHub run43928939896 artifact14256968650 SHA256 `0ca3c532707d1a291228d59c75d7831d654cd330579a4dc9e32cfa0685783025`, generation1416266880306000. Previously independently verified old original SQLite from run43936091950 artifact14259594511 SHA256 `692059aca2d6b8621f84693490d71c9243d5a41b37f3c0b826101a34e10f0cb2`; 130812 rows,1838 unique job IDs,44979 unique job/task keys.

- New canonical per-file SHA256 `source-presence-sha256-v1` uses domain-separated, lexicographically SQL-ordered tuple streams with explicitly big-endian signed-64-bit encoding; stores 3 hashes for job IDs, job/task IDs, event types and counts with 3 cardinalities in `file_digests`.
- Source-new ingestion inserts the digest in the **same commit transaction** as original source `file_inventory` COMPLETE and presence/event tables, after gzip EOF/row/event validations. Original ingest's `ALREADY_VERIFIED_NOOP` now invokes `strict_resume` to rehash actual stored IDs/events and reject missing/altered digest, event counts and orphan task keys.
- **Legacy migration is not self-certifying:** before creating digest metadata on an old source DB, reparses authentic full original archived gzip, independently constructs exact source job/task sets in TEMP SQLite, compares both sides with SQL EXCEPT, verifies original source row totals, event histograms, time range, compressed SHA. ONLY then records digest in a transaction on a **copy**. Original historical SQLite artifact remains immutable.
- Synthetic tests include same-cardinality key substitution, job substitution, modified event counts, digest removal, wrong source SHA/generation, and source-backed migration refusal of already-corrupted legacy source copy. Original E42 and frozen rejected Stage64 hash guards unchanged.

## Actual code and original GitHub execution
`jpdc/google2011_sqlite_source_digests.py` source commits **d769460c25c9608026c9df0f1261fc557c7645d6**, bugfix **7bba1df0806f4a87b64c7df3b5736bdd5070ca28** (TEMP SQL implicit-transaction handling); real original ingest path `jpdc/google2011_sqlite_job_inventory.py` fixed in commit **4cd6e5fd0b03eaec5c51aa755c20e981b7aaace9**. New synthetic test `jpdc/test_google2011_sqlite_resume_digest_hardening.py` commit **6831a1da38c60dc894e257aa54b9d612d12f7b27**. Original source-copy migration and adversarial real-source DB test `jpdc/audit_google2011_original_sqlite_resume_migration.py` commit **f632c4cbe00482d66be2dcb30cb6cd86ce66a971**.

[**GitHub Actions run43975777090**](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/43975777090) **COMPLETE SUCCESS**, code SHA **2e394db3de4569e4a86584b521fb510a8e7d4653**, original artifact ID **14280318617** `jpdc-google2011-source-backed-sqlite-resume-hardened-migration`, artifact ZIP sha256 **9a643922a9016dc35f1e1d6f7cf18ce5642c4efe6dea808c6418babe2f0619b3**, downloaded and inspected. Original source-based audit showed:

| Original archived real-source artifact COPY condition | Actual result |
|---|---|
| Old legacy DB contains no versioned per-file digests | Resume **REJECTED** safely, before migration |
| Independently reread exact old genuine publisher gzip; SQL EXCEPT both directions for job/task sets | Verified source-backed migration **PASS** |
| Same original source, migrated SQLite digest stable | Original source resume **ALREADY_VERIFIED_NOOP** |
| Swap one genuine task ID for different valid ID; no change to total 44,979 keys | Resume **REJECTED** |
| Swap one genuine job ID for different valid ID; no change to total 1,838 job IDs | Resume **REJECTED** |
| Restore prior job/task IDs | Original digest strict recheck **PASS** |
| New synthetic same-count corruption, altered events/digest deletion | Negative tests **PASS** |
| Original E42 and rejected Stage64 Git blob guards | PASS, unchanged |

Original migrated source database `migrated_presence.sqlite` SHA256 **ab4851f5fd43f01bbd212a31789b9d88237cfec81db074f921d570ea3d44f5dc**, size **1,986,560 bytes**, `PRAGMA integrity_check=ok`; `file_digests` contains one row with version `source-presence-sha256-v1`, jobs_n1838, tasks_n44979, events_n130812. Derived report audit.json captured source old SHA, original count and both mutation detection flags. Working-container independent read-only inspection of the downloaded archived SQLite and audit JSON confirms **database SHA matches report, actual SQL integrity OK and source digest schema/count row present**, in addition to GitHub Actions success. Source full SHA earlier independently checked in run43929341145; no fresh publisher data were sampled.

## Scope and remaining gaps
**Scientific class:** verified software behavior + independently source-grounded legacy artifact comparison, NOT independent scheduler evaluation or new trace population. Exactly **one previously spent file** was consumed again; full 500-file (~1.513GiB compressed) scan **NOT executed**, full cross-file source job grouping/causal retry history not established. Google Borg2011 is a *datacenter* source, not actual IIoT edge trace. No actual per-task physical CPU work, application deadline or transferred network bytes observed. Original Stage65 prospective candidate safety FAIL and Java↔Python 30k queue parity FAIL remain.

**Security scope:** source identity digests are SHA256 but stored inside the **same mutable SQLite file**. This detects non-coordinated accidental or malicious post-commit row alteration, provided digest metadata is not also rewritten. It is **not an authenticated externally anchored manifest**, cannot prevent coordinated source+digest rewrites or SQLite DB rollback substitution; the old immutable GitHub source artifacts provide additional historical audit provenance only. For complete 500-file ingestion, provide external per-batch digest/checkpoint manifests and staged provenance verification with disk/runner and possible egress costs evaluated.

**Next legitimate action:** implement a source-checkpoint manifest anchored outside SQLite, plus checks that a resumed multi-batch ingest cannot silently accept a replaced entire DB or missing file, before any 500-file GCS acquisition. No new CASPER scheduling method until physical-model fidelity and scientifically credible source assumptions are addressed.
