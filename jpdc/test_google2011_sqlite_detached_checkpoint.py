#!/usr/bin/env python3
"""Explicit adversarial synthetic mutation on COPY of authentic old source DB.

The original Google2011 rows are already spent; same-cardinality mutations
are adversarial/synthetic, NOT external experimental data.
"""
import hashlib
import shutil
import sqlite3
import tempfile
from pathlib import Path

from google2011_sqlite_detached_checkpoint import (
    issue,verify,canonical,hashfile,REAL_MIGRATED_DB_SHA,SOURCE_SHA,GENERATION)
from google2011_sqlite_source_digests import compute_digests,strict_resume

PIN="e8b134abc3f1f4e656d830ee5906548124daddd4ecbecb1cdcfe24c0bf8a83f5"

def rejected(fn,reason):
    try:fn()
    except ValueError as e:
        assert reason in str(e),(reason,str(e))
        return
    raise AssertionError("wrongly accepted corrupted or untrusted checkpoint")

def run(source_file):
    assert hashfile(source_file)==REAL_MIGRATED_DB_SHA
    with tempfile.TemporaryDirectory() as t:
        root=Path(t)
        db=root/"original.sqlite"
        shutil.copyfile(source_file,db)
        manifest=root/"checkpoint.json"
        manifest.write_bytes(canonical(issue(db)))
        assert hashfile(manifest)==PIN
        assert verify(db,manifest,trusted_sha=PIN,minimum_ordinal=1,expected_latest_ordinal=1)["status"]=="PASS"
        rejected(lambda:verify(db,manifest,trusted_sha="0"*64),"trusted checkpoint SHA mismatch")
        rejected(lambda:verify(db,manifest,trusted_sha=PIN,expected_latest_ordinal=2),"checkpoint head was rolled back")
        # Coordinated same-count change to BOTH SQL key and internal SQL digest.
        # Internal strict_resume can be tricked, but EXTERNAL SHA must fail.
        mutant=root/"mutant.sqlite"
        shutil.copyfile(db,mutant)
        con=sqlite3.connect(mutant)
        job,idx=con.execute("SELECT job_id,task_index FROM task_presence WHERE file_index=375 LIMIT 1").fetchone()
        con.execute("UPDATE task_presence SET task_index=? WHERE file_index=375 AND job_id=? AND task_index=?",
                    (idx+1000000000,job,idx))
        hashes=compute_digests(con,375)
        con.execute("""UPDATE file_digests SET jobs_sha256=?,tasks_sha256=?,events_sha256=?,
           jobs_n=?,tasks_n=?,events_n=? WHERE file_index=375""",hashes)
        con.commit()
        assert con.execute("SELECT count(*) FROM task_presence WHERE file_index=375").fetchone()[0]==44979
        assert strict_resume(con,375,GENERATION,SOURCE_SHA)==hashes
        con.close()
        rejected(lambda:verify(mutant,manifest,trusted_sha=PIN),"whole SQLite database differs")
        # A swapped manifest with a rewritten matching database SHA is still
        # detected because the caller PIN is independent of both objects.
        fake=root/"fake_checkpoint.json"
        injected=issue(mutant)
        fake.write_bytes(canonical(injected))
        assert hashfile(fake)!=PIN
        rejected(lambda:verify(mutant,fake,trusted_sha=PIN),"trusted checkpoint SHA mismatch")
        # Complete original legacy DB rollback is incompatible with pinned new
        # migrated DB SHA, even if old source metadata itself is sound.
        old=root/"old.sqlite"
        shutil.copyfile(db,old)
        c=sqlite3.connect(old)
        c.execute("DROP TABLE file_digests")
        c.commit();c.close()
        rejected(lambda:verify(old,manifest,trusted_sha=PIN),"whole SQLite database differs")
        # Chain metadata alone cannot provide a trusted head.
        successor=root/"successor.json"
        successor.write_bytes(canonical(issue(db,ordinal=2,previous_sha=PIN)))
        successor_sha=hashfile(successor)
        assert verify(db,successor,trusted_sha=successor_sha,
                      minimum_ordinal=2,expected_latest_ordinal=2,
                      expected_predecessor=PIN)["status"]=="PASS"
        rejected(lambda:verify(db,manifest,trusted_sha=successor_sha,
                      expected_latest_ordinal=2),"trusted checkpoint SHA mismatch")
    print("JPDC_SOURCE_SQLITE_DETACHED_PIN_COORDINATED_TAMPER_AND_ROLLBACK_NEGATIVES_PASS")

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("--archived-db",required=True)
    args=p.parse_args()
    run(Path(args.archived_db))
