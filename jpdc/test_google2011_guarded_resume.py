#!/usr/bin/env python3
"""Real already-spent original gzip/DB + synthetic checkpoint lineage controls."""
import json
import shutil
import sqlite3
import tempfile
from pathlib import Path

from google2011_guarded_resume import guarded_resume,verify_chain
from google2011_sqlite_detached_checkpoint import (
    canonical,hashfile,issue,SOURCE_SHA,GENERATION,REAL_MIGRATED_DB_SHA)
from google2011_sqlite_source_digests import compute_digests,strict_resume

PIN="e8b134abc3f1f4e656d830ee5906548124daddd4ecbecb1cdcfe24c0bf8a83f5"

def denied(fn):
    try:fn()
    except (ValueError,FileNotFoundError):return
    raise AssertionError("unsafe resume/lineage was admitted")

def run(archived_db,archived_checkpoint,archived_gzip):
    assert hashfile(archived_db)==REAL_MIGRATED_DB_SHA
    assert hashfile(archived_checkpoint)==PIN
    assert hashfile(archived_gzip)==SOURCE_SHA
    with tempfile.TemporaryDirectory() as t:
        root=Path(t)
        db=root/"data.sqlite";checkpoint=root/"checkpoint.json"
        shutil.copyfile(archived_db,db);shutil.copyfile(archived_checkpoint,checkpoint)
        good=guarded_resume(db,checkpoint,archived_gzip,trusted_sha=PIN,latest_ordinal=1)
        assert good["status"]=="PASS" and good["source_state"]=="ALREADY_VERIFIED_NOOP"
        denied(lambda:guarded_resume(db,checkpoint,archived_gzip,trusted_sha=None,latest_ordinal=1))
        denied(lambda:guarded_resume(db,checkpoint,archived_gzip,trusted_sha=PIN,latest_ordinal=None))
        denied(lambda:guarded_resume(db,checkpoint,archived_gzip,trusted_sha="0"*64,latest_ordinal=1))
        denied(lambda:guarded_resume(db,checkpoint,archived_gzip,trusted_sha=PIN,latest_ordinal=2))
        denied(lambda:guarded_resume(db,checkpoint,archived_gzip,trusted_sha=PIN,latest_ordinal=0))
        fake=root/"checkpoint_swapped.json"
        fake.write_bytes(canonical(issue(db,ordinal=2,previous_sha=PIN)))
        denied(lambda:guarded_resume(db,fake,archived_gzip,trusted_sha=PIN,latest_ordinal=1))
        # Actual previously verified archive COPY with same-count key replacement
        # AND deliberately recomputed internal SQL digests: the prior in-DB
        # strict_resume is fooled but our externally pinned wrapper rejects.
        corrupt=root/"corrupt.sqlite"
        shutil.copyfile(db,corrupt)
        con=sqlite3.connect(corrupt)
        job,task=con.execute("SELECT job_id,task_index FROM task_presence WHERE file_index=375 LIMIT 1").fetchone()
        con.execute("UPDATE task_presence SET task_index=? WHERE file_index=375 AND job_id=? AND task_index=?",(task+1000000000,job,task))
        digests=compute_digests(con,375)
        con.execute("""UPDATE file_digests SET jobs_sha256=?,tasks_sha256=?,events_sha256=?,
          jobs_n=?,tasks_n=?,events_n=? WHERE file_index=375""",digests)
        con.commit()
        assert strict_resume(con,375,GENERATION,SOURCE_SHA)==digests
        con.close()
        denied(lambda:guarded_resume(corrupt,checkpoint,archived_gzip,trusted_sha=PIN,latest_ordinal=1))
        # Chain below is synthetic/administrative ONLY, not new original GCS
        # files and not an empirical second batch.
        link2=root/"synthetic_ordinal2.json"
        link2.write_bytes(canonical(issue(db,ordinal=2,previous_sha=PIN)))
        sha2=hashfile(link2)
        link3=root/"synthetic_ordinal3.json"
        link3.write_bytes(canonical(issue(db,ordinal=3,previous_sha=sha2)))
        sha3=hashfile(link3)
        actual=verify_chain([link2,link3],trusted_head_sha=sha3,
            latest_ordinal=3,trusted_predecessor_sha=PIN)
        assert actual["manifest_count"]==2
        assert actual["classification"]=="SYNTHETIC_ADMINISTRATIVE_CHAIN_ONLY"
        denied(lambda:verify_chain([link2],trusted_head_sha=sha3,
            latest_ordinal=3,trusted_predecessor_sha=PIN))
        denied(lambda:verify_chain([link2,link3],trusted_head_sha=PIN,
            latest_ordinal=3,trusted_predecessor_sha=PIN))
        denied(lambda:verify_chain([link3,link2],trusted_head_sha=sha3,
            latest_ordinal=3,trusted_predecessor_sha=PIN))
        denied(lambda:verify_chain([link2,link3],trusted_head_sha=sha3,
            latest_ordinal=4,trusted_predecessor_sha=PIN))
        denied(lambda:verify_chain([link2,link3],trusted_head_sha=sha3,
            latest_ordinal=3,trusted_predecessor_sha="0"*64))
    print("JPDC_GUARDED_SOURCE_RESUME_EXTERNAL_PIN_AND_SYNTHETIC_CHAIN_NEGATIVES_PASS")

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("--old-db",required=True)
    p.add_argument("--old-checkpoint",required=True)
    p.add_argument("--old-gzip",required=True)
    a=p.parse_args()
    run(Path(a.old_db),Path(a.old_checkpoint),Path(a.old_gzip))
