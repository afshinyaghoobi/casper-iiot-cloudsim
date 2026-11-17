#!/usr/bin/env python3
"""Detached, independently SHA-pinned checkpoint for verified original source SQLite.

Caller MUST supply a trusted sha256 checkpoint pin from outside the candidate
artifact. Self-pinned manifests offer no meaningful anti-rollback protection.
"""
import argparse
import hashlib
import json
import sqlite3
from pathlib import Path

from google2011_sqlite_source_digests import strict_resume

VERSION="jpdc-external-sqlite-checkpoint-v1"
SOURCE_SHA="0ca3c532707d1a291228d59c75d7831d654cd330579a4dc9e32cfa0685783025"
GENERATION="1416266880306000"
REAL_MIGRATED_DB_SHA="ab4851f5fd43f01bbd212a31789b9d88237cfec81db074f921d570ea3d44f5dc"
ORIGINAL_INDEX=375
EXPECTED_ROWS=130812
EXPECTED_JOBS=1838
EXPECTED_TASKS=44979

def canonical(d):
    return (json.dumps(d,sort_keys=True,separators=(",",":"),ensure_ascii=True)+"\n").encode("ascii")

def hashfile(p):
    h=hashlib.sha256()
    with Path(p).open("rb") as f:
        for piece in iter(lambda:f.read(65536),b""):
            h.update(piece)
    return h.hexdigest()

def validate_source_sqlite(db):
    con=sqlite3.connect("file:"+str(Path(db).resolve())+"?mode=ro",uri=True)
    try:
        if con.execute("PRAGMA integrity_check").fetchone()[0]!="ok":
            raise ValueError("EXTERNAL_CHECKPOINT_FAIL SQLite integrity")
        dg=strict_resume(con,ORIGINAL_INDEX,GENERATION,SOURCE_SHA)
        files=con.execute("SELECT file_index FROM file_inventory ORDER BY file_index").fetchall()
        if files!=[(ORIGINAL_INDEX,)]:
            raise ValueError("EXTERNAL_CHECKPOINT_FAIL unrecorded/extra source files")
        rec=con.execute("SELECT row_count,bytes_plain,first_us,last_us FROM file_inventory WHERE file_index=375").fetchone()
        if rec!=(EXPECTED_ROWS,14973713,1879800290193,1884810781196):
            raise ValueError("EXTERNAL_CHECKPOINT_FAIL source rows/clock mismatch")
        if dg[-3:]!=(EXPECTED_JOBS,EXPECTED_TASKS,EXPECTED_ROWS):
            raise ValueError("EXTERNAL_CHECKPOINT_FAIL SQL set cardinalities")
        return dg
    finally:
        con.close()

def issue(db,ordinal=1,previous_sha=None):
    if not isinstance(ordinal,int) or ordinal<1:
        raise ValueError("invalid ordinal")
    if (ordinal==1 and previous_sha is not None) or (
        ordinal>1 and (not isinstance(previous_sha,str) or len(previous_sha)!=64)):
        raise ValueError("missing or unexpected externally pinned previous checkpoint")
    dg=validate_source_sqlite(db)
    return dict(version=VERSION,ordinal=ordinal,previous_checkpoint_sha256=previous_sha,
        original_source_index=ORIGINAL_INDEX,original_source_generation=GENERATION,
        original_source_gzip_sha256=SOURCE_SHA,
        sqlite_sha256=hashfile(db),
        file_digests=dict(jobs_sha256=dg[0],tasks_sha256=dg[1],
                          events_sha256=dg[2],jobs_n=dg[3],
                          tasks_n=dg[4],events_n=dg[5]),
        original_event_rows=EXPECTED_ROWS,
        original_source_independent_holdout_certified=False,
        original_500_file_scan_executed=False,
        stage65_scientific_safety="FAIL",
        java_python_queue_parity="FAIL")

def verify(db,checkpoint,*,trusted_sha,minimum_ordinal=1,
           expected_predecessor=None,expected_latest_ordinal=None):
    if not isinstance(trusted_sha,str) or len(trusted_sha)!=64:
        raise ValueError("EXTERNAL_CHECKPOINT_FAIL external SHA pin REQUIRED")
    checkpoint=Path(checkpoint)
    raw=checkpoint.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=trusted_sha:
        raise ValueError("EXTERNAL_CHECKPOINT_FAIL trusted checkpoint SHA mismatch")
    manifest=json.loads(raw)
    if raw!=canonical(manifest):
        raise ValueError("EXTERNAL_CHECKPOINT_FAIL noncanonical manifest")
    if manifest.get("version")!=VERSION or manifest.get("ordinal",0)<minimum_ordinal:
        raise ValueError("EXTERNAL_CHECKPOINT_FAIL stale manifest ordinal")
    if expected_latest_ordinal is not None and manifest["ordinal"]!=expected_latest_ordinal:
        raise ValueError("EXTERNAL_CHECKPOINT_FAIL checkpoint head was rolled back")
    if expected_predecessor is not None and manifest.get("previous_checkpoint_sha256")!=expected_predecessor:
        raise ValueError("EXTERNAL_CHECKPOINT_FAIL missing trusted predecessor")
    if manifest.get("sqlite_sha256")!=hashfile(db):
        raise ValueError("EXTERNAL_CHECKPOINT_FAIL whole SQLite database differs from externally pinned checkpoint")
    live=issue(db,ordinal=manifest["ordinal"],previous_sha=manifest["previous_checkpoint_sha256"])
    if manifest!=live:
        raise ValueError("EXTERNAL_CHECKPOINT_FAIL original source provenance/digest mismatch")
    return dict(status="PASS",externally_pinned_checkpoint_sha256=trusted_sha,
        verified_original_full_sqlite_sha256=manifest["sqlite_sha256"],
        verified_checkpoint_ordinal=manifest["ordinal"],
        full_source_original_rows=EXPECTED_ROWS,source_jobs=EXPECTED_JOBS,
        source_tasks=EXPECTED_TASKS,independent_source_seed=False,
        actual_full_500_files_scanned=False,stage65="FAIL",java_python_parity="FAIL")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--db",required=True)
    p.add_argument("--checkpoint",required=True)
    p.add_argument("--issue",action="store_true")
    p.add_argument("--trusted-sha")
    p.add_argument("--ordinal",type=int,default=1)
    p.add_argument("--previous-sha")
    p.add_argument("--minimum-ordinal",type=int,default=1)
    p.add_argument("--expected-latest",type=int)
    p.add_argument("--out")
    a=p.parse_args()
    if a.issue:
        c=issue(a.db,a.ordinal,a.previous_sha)
        Path(a.checkpoint).write_bytes(canonical(c))
        print("JPDC_DETACHED_CHECKPOINT_ISSUED_SHA256",hashfile(a.checkpoint))
    else:
        result=verify(a.db,a.checkpoint,trusted_sha=a.trusted_sha,
            minimum_ordinal=a.minimum_ordinal,
            expected_latest_ordinal=a.expected_latest)
        if a.out:Path(a.out).write_bytes(canonical(result))
        print("JPDC_EXTERNAL_CHECKPOINT_STRICT_VERIFICATION_PASS",json.dumps(result,sort_keys=True))
if __name__=="__main__":main()
