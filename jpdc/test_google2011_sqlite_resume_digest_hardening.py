#!/usr/bin/env python3
"""Synthetic negative/source-backed legacy migration and SAME-COUNT tamper tests."""
import gzip
import hashlib
import shutil
import sqlite3
import tempfile
from pathlib import Path

from google2011_sqlite_job_inventory import connection,ingest,summarize
from google2011_sqlite_source_digests import (
    migrate_legacy_verified_source,strict_resume,compute_digests)

def event(t,j,task,code):
    return f"{t},,{j},{task},,{code},u,0,0,0.1,0.2,,\n".encode()

def gz(path,rows):
    path.write_bytes(gzip.compress(b"".join(rows),mtime=0))
    return hashlib.sha256(path.read_bytes()).hexdigest()

def reject(func,part=""):
    try:func()
    except (ValueError,sqlite3.DatabaseError) as ex:
        if part:assert part in str(ex),(part,str(ex))
        return
    raise AssertionError("unsafe source/SQLite state incorrectly accepted")

def main():
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp)
        src=root/"synthetic.gz"
        rows=[event(t,10+t//50,t%50,0) for t in range(2200)]
        sha=gz(src,rows)
        con=connection(root/"index.sqlite")
        assert ingest(con,src,0,"123",sha)=="INGESTED_VERIFIED"
        expected=summarize(con)
        assert ingest(con,src,0,"123",sha)=="ALREADY_VERIFIED_NOOP"
        assert summarize(con)==expected
        # A different valid task ID without changing task cardinality.
        con.execute("UPDATE task_presence SET task_index=100000 WHERE file_index=0 AND job_id=10 AND task_index=0")
        con.commit()
        assert con.execute("SELECT COUNT(*) FROM task_presence").fetchone()[0]==2200
        reject(lambda:ingest(con,src,0,"123",sha),"UNSAFE_RESUME_INTEGRITY_FAIL")
        con.execute("UPDATE task_presence SET task_index=0 WHERE file_index=0 AND job_id=10 AND task_index=100000")
        con.commit()
        assert ingest(con,src,0,"123",sha)=="ALREADY_VERIFIED_NOOP"
        # Change one valid job ID without changing cardinality, AND keep task
        # table intact. Digest must catch job-table discrepancy.
        con.execute("UPDATE job_presence SET job_id=9999 WHERE file_index=0 AND job_id=10")
        con.commit()
        reject(lambda:ingest(con,src,0,"123",sha),"UNSAFE_RESUME_INTEGRITY_FAIL")
        con.execute("UPDATE job_presence SET job_id=10 WHERE file_index=0 AND job_id=9999")
        con.commit()
        con.execute("UPDATE event_counts SET n=n+1 WHERE file_index=0 AND event_type='SUBMIT'")
        con.commit()
        reject(lambda:ingest(con,src,0,"123",sha),"UNSAFE_RESUME_INTEGRITY_FAIL")
        con.execute("UPDATE event_counts SET n=n-1 WHERE file_index=0 AND event_type='SUBMIT'")
        con.commit()
        assert ingest(con,src,0,"123",sha)=="ALREADY_VERIFIED_NOOP"
        con.execute("DELETE FROM file_digests WHERE file_index=0")
        con.commit()
        reject(lambda:ingest(con,src,0,"123",sha),"UNSAFE_RESUME_INTEGRITY_FAIL")
        # Missing original digest must NOT be 'fixed' by hashing current DB
        # without checking the authentic source.
        con.execute("UPDATE task_presence SET task_index=100000 WHERE file_index=0 AND job_id=10 AND task_index=0")
        con.commit()
        reject(lambda:migrate_legacy_verified_source(con,src,0,"123",sha),"UNSAFE_RESUME_INTEGRITY_FAIL")
        con.execute("UPDATE task_presence SET task_index=0 WHERE file_index=0 AND job_id=10 AND task_index=100000")
        con.commit()
        assert migrate_legacy_verified_source(con,src,0,"123",sha)[-1]==2200
        assert ingest(con,src,0,"123",sha)=="ALREADY_VERIFIED_NOOP"
        assert summarize(con)==expected
        con.close()
    print("JPDC_ORIGINAL_SQLITE_ATOMIC_DIGEST_SYNTHETIC_SAME_COUNT_TAMPER_PASS")

if __name__=="__main__":main()
