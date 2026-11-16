#!/usr/bin/env python3
"""Original archived source and legacy SQLite copy migration; no new GCS data."""
import argparse
import hashlib
import json
import shutil
import sqlite3
from pathlib import Path
from google2011_sqlite_source_digests import migrate_legacy_verified_source,strict_resume
from google2011_sqlite_job_inventory import ingest,ORIGINAL_PART375_EVENTS

ORIG_DB="692059aca2d6b8621f84693490d71c9243d5a41b37f3c0b826101a34e10f0cb2"
ORIG_SRC="0ca3c532707d1a291228d59c75d7831d654cd330579a4dc9e32cfa0685783025"
GEN="1416266880306000"

def refuses(action):
    try:action()
    except (ValueError,sqlite3.DatabaseError) as err:
        if "UNSAFE_RESUME_INTEGRITY_FAIL" not in str(err):
            raise AssertionError("wrong failure reason: "+str(err)) from err
        return str(err)
    raise AssertionError("unsafe SQLite was accepted")

def execute(old_sqlite,old_source,out):
    src=old_source/"original_full.gz"
    db=old_sqlite/"presence.sqlite"
    if hashlib.sha256(src.read_bytes()).hexdigest()!=ORIG_SRC:raise ValueError("original archived source altered")
    if hashlib.sha256(db.read_bytes()).hexdigest()!=ORIG_DB:raise ValueError("original archived SQLite altered")
    out.mkdir(parents=True,exist_ok=True)
    copy=out/"migrated_presence.sqlite"
    shutil.copyfile(db,copy)
    c=sqlite3.connect(copy)
    try:
        # First demonstrate old data are NOT accepted automatically.
        legacy_result=refuses(lambda:ingest(c,src,375,GEN,ORIG_SRC,
            expected_events=ORIGINAL_PART375_EVENTS,max_compressed=1502643))
        migrated=migrate_legacy_verified_source(c,src,375,GEN,ORIG_SRC,
            expected_events=ORIGINAL_PART375_EVENTS,max_compressed=1502643)
        assert migrated[-3:]==(1838,44979,130812)
        assert ingest(c,src,375,GEN,ORIG_SRC,
            expected_events=ORIGINAL_PART375_EVENTS,max_compressed=1502643)=="ALREADY_VERIFIED_NOOP"
        baseline=tuple(migrated)
        # Same-cardinality task identity substitution on real DB COPY.
        job,task=c.execute("SELECT job_id,task_index FROM task_presence WHERE file_index=375 ORDER BY job_id,task_index LIMIT 1").fetchone()
        newtask=task+1000000000
        assert c.execute("SELECT COUNT(*) FROM task_presence WHERE file_index=375").fetchone()[0]==44979
        c.execute("UPDATE task_presence SET task_index=? WHERE file_index=375 AND job_id=? AND task_index=?",(newtask,job,task))
        c.commit()
        assert c.execute("SELECT COUNT(*) FROM task_presence WHERE file_index=375").fetchone()[0]==44979
        tamper_result=refuses(lambda:ingest(c,src,375,GEN,ORIG_SRC,
            expected_events=ORIGINAL_PART375_EVENTS,max_compressed=1502643))
        c.execute("UPDATE task_presence SET task_index=? WHERE file_index=375 AND job_id=? AND task_index=?",(task,job,newtask))
        c.commit()
        assert strict_resume(c,375,GEN,ORIG_SRC)==baseline
        # Same-cardinality JOB identity substitution on genuine source COPY.
        oldjob=c.execute("SELECT job_id FROM job_presence WHERE file_index=375 ORDER BY job_id LIMIT 1").fetchone()[0]
        c.execute("UPDATE job_presence SET job_id=? WHERE file_index=375 AND job_id=?",(oldjob+1000000000,oldjob))
        c.commit()
        job_tamper_result=refuses(lambda:ingest(c,src,375,GEN,ORIG_SRC,
            expected_events=ORIGINAL_PART375_EVENTS,max_compressed=1502643))
        c.execute("UPDATE job_presence SET job_id=? WHERE file_index=375 AND job_id=?",(oldjob,oldjob+1000000000))
        c.commit()
        assert strict_resume(c,375,GEN,ORIG_SRC)==baseline
        assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
        c.close()
        final_digest=hashlib.sha256(copy.read_bytes()).hexdigest()
        result=dict(status="PASS",
            archived_old_source_sha256=ORIG_SRC,archived_old_sqlite_sha256=ORIG_DB,
            safe_migrated_database_sha256=final_digest,
            archived_original_rows=130812,archived_original_jobs=1838,
            archived_original_job_task_keys=44979,
            source_verified_migration_digest_rows=[1838,44979,130812],
            old_database_rejected_on_resume_before_source_backed_migration=True,
            same_cardinality_real_source_task_key_tampering_rejected=True,
            same_cardinality_real_source_job_id_tampering_rejected=True,
            identical_archived_original_source_resume_after_safe_migration="ALREADY_VERIFIED_NOOP",
            no_new_gcs_source_download=True,no_500_file_ingestion=True,
            no_independent_source_cohort=True,no_algorithm_efficacy=True,
            stage65_safety="FAIL",java_python_parity="FAIL")
        (out/"audit.json").write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
        print("JPDC_ORIGINAL_SQLITE_RESUME_TAMPER_MIGRATION",json.dumps(result,sort_keys=True))
        print("JPDC_ORIGINAL_SQLITE_SAFE_MIGRATION_AND_SAME_CARDINALITY_TAMPER_PASS")
        return result
    finally:
        try:c.close()
        except Exception:pass

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--old-sqlite",required=True)
    p.add_argument("--old-source",required=True)
    p.add_argument("--out",required=True)
    a=p.parse_args()
    execute(Path(a.old_sqlite),Path(a.old_source),Path(a.out))
