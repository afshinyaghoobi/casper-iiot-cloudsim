# Externally pinned original Google2011 part375 checkpoint (2026-11-17)

- **Trusted separately committed checkpoint SHA256**: `e8b134abc3f1f4e656d830ee5906548124daddd4ecbecb1cdcfe24c0bf8a83f5`.
- Original, previously archived **migrated** SQLite file SHA256: `ab4851f5fd43f01bbd212a31789b9d88237cfec81db074f921d570ea3d44f5dc`.
- Frozen Google GCS original part375 full gzip SHA256: `0ca3c532707d1a291228d59c75d7831d654cd330579a4dc9e32cfa0685783025`, generation `1416266880306000`.
- Canonical deterministic JSON checkpoint `jpdc-external-sqlite-checkpoint-v1`, ordinal **1** and no predecessor, includes source event rows **130812**, exact job count **1838**, task key count **44979**, and all three checked original SQL key/event SHA256 values.
- The original SQLite checkpoint hash above is **not** derived from the presented candidate artifact at verification time; verifier CI must supply this exact separately committed checkpoint SHA.
- Source data originate only from previously verified actual Google2011 part375 `jpdc-google2011-source-backed-sqlite-resume-hardened-migration` GitHub run43975777090 artifact14280318617. No new publisher source calls.
- This text/CI pin relies on the trust and immutability of the exact Git commit/repository history and CI setup; it does not defend against repository authorization compromise or rollback of the trusted pin itself. There is no off-platform signed timestamp/append-only ledger in this experiment. The test only establishes detection of DB replacement relative to this immutable caller-selected checkpoint.
