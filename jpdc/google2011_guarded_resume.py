#!/usr/bin/env python3
"""Mandatory external-trust gate before any original source resume write access.

Narrow scope: ONE already spent original Google Borg2011 v2.1 part375.
Synthetic chain verification is separate and is never a new source cohort.
"""
import argparse
import hashlib
import json
import re
import sqlite3
from pathlib import Path

from google2011_sqlite_detached_checkpoint import verify, canonical, hashfile
from google2011_sqlite_job_inventory import (
    ingest, ORIGINAL_PART375_SHA, ORIGINAL_PART375_GENERATION,
    ORIGINAL_PART375_SIZE, ORIGINAL_PART375_EVENTS)

HEX=re.compile(r"[0-9a-f]{64}\Z")
MAX_CHAIN=32

def trusted_arguments(sha,ordinal):
    if not isinstance(sha,str) or HEX.fullmatch(sha) is None:
        raise ValueError("GUARDED_RESUME_DENIED missing independently trusted checkpoint SHA256")
    if type(ordinal) is not int or ordinal<1:
        raise ValueError("GUARDED_RESUME_DENIED missing trusted latest ordinal")

def guarded_resume(db,checkpoint,source,*,trusted_sha,latest_ordinal):
    # Crucial: all trust checks run BEFORE opening a write-capable DB.
    trusted_arguments(trusted_sha,latest_ordinal)
    db=Path(db);checkpoint=Path(checkpoint);source=Path(source)
    start=verify(db,checkpoint,trusted_sha=trusted_sha,
                 minimum_ordinal=latest_ordinal,
                 expected_latest_ordinal=latest_ordinal)
    if source.stat().st_size!=ORIGINAL_PART375_SIZE or hashfile(source)!=ORIGINAL_PART375_SHA:
        raise ValueError("GUARDED_RESUME_DENIED original archived gzip identity mismatch")
    con=sqlite3.connect(str(db))
    try:
        state=ingest(con,source,375,ORIGINAL_PART375_GENERATION,
                     ORIGINAL_PART375_SHA,
                     expected_events=ORIGINAL_PART375_EVENTS,
                     max_compressed=ORIGINAL_PART375_SIZE)
        if state!="ALREADY_VERIFIED_NOOP":
            raise ValueError("GUARDED_RESUME_DENIED new source ingestion not allowed in resume-only path")
    finally:
        con.close()
    after=verify(db,checkpoint,trusted_sha=trusted_sha,
                 minimum_ordinal=latest_ordinal,
                 expected_latest_ordinal=latest_ordinal)
    if start!=after:
        raise ValueError("GUARDED_RESUME_DENIED trusted checkpoint changed during resume")
    return dict(status="PASS",entrypoint="MANDATORY_EXTERNAL_TRUST_GUARDED_SOURCE_RESUME",
        source_state=state,external_checkpoint_sha256=trusted_sha,
        trusted_latest_ordinal=latest_ordinal,original_db_sha256=start[
            "verified_original_full_sqlite_sha256"],
        original_full_source_gzip_sha256=ORIGINAL_PART375_SHA,
        source_event_rows=130812,source_job_ids=1838,source_job_task_keys=44979,
        all_500_original_files_ingested=False,independent_holdout=False,
        external_ledger_signed_or_immutable=False,stage65_safety="FAIL",
        original_java_python_parity="FAIL")


def verify_chain(paths,*,trusted_head_sha,latest_ordinal,trusted_predecessor_sha):
    """Verify synthetic administrative checkpoint HASH chain against caller head.

    All records are passed by caller; no file/manifest self-pin is accepted.
    This only checks lineage integrity, not authentic GCS data content.
    """
    trusted_arguments(trusted_head_sha,latest_ordinal)
    if (not isinstance(trusted_predecessor_sha,str) or
        HEX.fullmatch(trusted_predecessor_sha) is None):
        raise ValueError("GUARDED_CHAIN_DENIED missing trusted first predecessor")
    if not paths or len(paths)>MAX_CHAIN:
        raise ValueError("GUARDED_CHAIN_DENIED missing or oversized input")
    if len(paths)>latest_ordinal:
        raise ValueError("GUARDED_CHAIN_DENIED impossible chain length")
    expected_start=latest_ordinal-len(paths)+1
    previous=trusted_predecessor_sha
    evidence=[]
    for offset,path in enumerate(paths):
        raw=Path(path).read_bytes()
        obj=json.loads(raw)
        if raw!=canonical(obj):
            raise ValueError("GUARDED_CHAIN_DENIED noncanonical record")
        if obj.get("version")!="jpdc-external-sqlite-checkpoint-v1":
            raise ValueError("GUARDED_CHAIN_DENIED wrong checkpoint version")
        if obj.get("ordinal")!=expected_start+offset:
            raise ValueError("GUARDED_CHAIN_DENIED stale or discontinuous ordinal")
        if obj.get("previous_checkpoint_sha256")!=previous:
            raise ValueError("GUARDED_CHAIN_DENIED incorrect predecessor")
        current=hashlib.sha256(raw).hexdigest()
        evidence.append(current)
        previous=current
    if previous!=trusted_head_sha:
        raise ValueError("GUARDED_CHAIN_DENIED latest externally trusted head mismatch")
    return dict(status="PASS",classification="SYNTHETIC_ADMINISTRATIVE_CHAIN_ONLY",
        manifest_count=len(evidence),first_ordinal=expected_start,
        latest_ordinal=latest_ordinal,externally_pinned_head_sha256=trusted_head_sha,
        external_source_independent_data=False,authenticated_remote_ledger=False)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--db",required=True)
    ap.add_argument("--checkpoint",required=True)
    ap.add_argument("--source",required=True)
    ap.add_argument("--trusted-checkpoint-sha",required=True)
    ap.add_argument("--trusted-latest-ordinal",required=True,type=int)
    ap.add_argument("--out",required=True)
    a=ap.parse_args()
    result=guarded_resume(a.db,a.checkpoint,a.source,
        trusted_sha=a.trusted_checkpoint_sha,latest_ordinal=a.trusted_latest_ordinal)
    Path(a.out).write_bytes(canonical(result))
    print("JPDC_GUARDED_ORIGINAL_SOURCE_RESUME_PASS",json.dumps(result,sort_keys=True))
if __name__=="__main__":main()
