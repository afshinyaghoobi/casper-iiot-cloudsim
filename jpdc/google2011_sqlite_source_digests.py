#!/usr/bin/env python3
"""Versioned canonical source-presence digests, strict resume, legacy migration.

Not cryptographic authentication: digest records are in the same mutable DB.
Protects non-coordinated deletion/edits, not an adversary rewriting both.
"""
import collections
import csv
import gzip
import hashlib
import sqlite3
import struct
from pathlib import Path

DIGEST_VERSION="source-presence-sha256-v1"
NAMES=("SUBMIT","SCHEDULE","EVICT","FAIL","FINISH","KILL","LOST",
       "UPDATE_PENDING","UPDATE_RUNNING")
MAX_PLAIN=128*1024*1024
MAX_ROWS=2000000

def ensure_schema(conn):
    conn.execute("""CREATE TABLE IF NOT EXISTS file_digests (
        file_index INTEGER PRIMARY KEY, algorithm TEXT NOT NULL,
        jobs_sha256 TEXT NOT NULL, tasks_sha256 TEXT NOT NULL,
        events_sha256 TEXT NOT NULL,
        jobs_n INTEGER NOT NULL, tasks_n INTEGER NOT NULL, events_n INTEGER NOT NULL)""")

def _encode_int(num):
    if not isinstance(num,int) or not -(2**63)<=num<2**63:
        raise ValueError("SQLite/source ID beyond signed 64 bit canonical format")
    return struct.pack(">q",num)

def _stream_digest(conn,file_index,table,columns,tag):
    h=hashlib.sha256(b"JPDC_GOOGLE2011\0"+tag.encode("ascii")+b"\0"+DIGEST_VERSION.encode("ascii")+b"\0")
    column_names=",".join(columns)
    order=",".join(columns)
    count=0
    query=f"SELECT {column_names} FROM {table} WHERE file_index=? ORDER BY {order}"
    for row in conn.execute(query,(file_index,)):
        for val in row:h.update(_encode_int(val))
        count+=1
    h.update(b"COUNT\0"+_encode_int(count))
    return h.hexdigest(),count

def compute_digests(conn,index):
    jobs,jn=_stream_digest(conn,index,"job_presence",("job_id",),"JOBS")
    tasks,tn=_stream_digest(conn,index,"task_presence",("job_id","task_index"),"TASKS")
    h=hashlib.sha256(b"JPDC_GOOGLE2011\0EVENTS\0"+DIGEST_VERSION.encode("ascii")+b"\0")
    en=0
    for name,num in conn.execute("SELECT event_type,n FROM event_counts WHERE file_index=? ORDER BY event_type",(index,)):
        if name not in NAMES or not isinstance(num,int) or num<=0:raise ValueError("bad event aggregate")
        coded=name.encode("ascii")
        h.update(struct.pack(">I",len(coded))+coded+_encode_int(num))
        en+=num
    h.update(b"COUNT\0"+_encode_int(en))
    return (jobs,tasks,h.hexdigest(),jn,tn,en)

def commit_digest(conn,index):
    ensure_schema(conn)
    values=compute_digests(conn,index)
    if min(values[3:])<=0:raise ValueError("empty original source presence")
    conn.execute("INSERT INTO file_digests VALUES(?,?,?,?,?,?,?,?)",
                 (index,DIGEST_VERSION,*values))
    return values

def strict_resume(conn,index,source_generation,source_sha):
    if conn.execute("PRAGMA quick_check").fetchone()[0]!="ok":
        raise ValueError("UNSAFE_RESUME_INTEGRITY_FAIL SQLite quick_check")
    old=conn.execute("SELECT generation,original_sha256,row_count,status FROM file_inventory WHERE file_index=?",(index,)).fetchone()
    if old is None or old[0]!=source_generation or old[1]!=source_sha or old[3]!="COMPLETE":
        raise ValueError("UNSAFE_RESUME_INTEGRITY_FAIL completed source provenance mismatch")
    try:
        digest=conn.execute("SELECT algorithm,jobs_sha256,tasks_sha256,events_sha256,jobs_n,tasks_n,events_n FROM file_digests WHERE file_index=?",(index,)).fetchone()
    except sqlite3.OperationalError as err:
        raise ValueError("UNSAFE_RESUME_INTEGRITY_FAIL legacy digest table missing") from err
    if digest is None or digest[0]!=DIGEST_VERSION:
        raise ValueError("UNSAFE_RESUME_INTEGRITY_FAIL legacy file digest unavailable")
    actual=compute_digests(conn,index)
    if actual!=tuple(digest[1:]) or actual[-1]!=old[2]:
        raise ValueError("UNSAFE_RESUME_INTEGRITY_FAIL source IDs or event totals altered")
    orphan=conn.execute("""SELECT 1 FROM task_presence t LEFT JOIN job_presence j
        ON j.file_index=t.file_index AND j.job_id=t.job_id
        WHERE t.file_index=? AND j.job_id IS NULL LIMIT 1""",(index,)).fetchone()
    if orphan is not None:raise ValueError("UNSAFE_RESUME_INTEGRITY_FAIL orphan tasks")
    return actual

def migrate_legacy_verified_source(conn,src,index,generation,sha,expected_events=None,
                                   max_compressed=None):
    """Source-backed exact set equality needed; never self-attest legacy DB."""
    if max_compressed is not None and src.stat().st_size>max_compressed:
        raise ValueError("source gzip size exceeds frozen limit")
    h=hashlib.sha256()
    with src.open("rb") as f:
        for chunk in iter(lambda:f.read(65536),b""):h.update(chunk)
    if h.hexdigest()!=sha:raise ValueError("original complete source SHA mismatch")
    old=conn.execute("SELECT generation,original_sha256,row_count,bytes_plain,first_us,last_us,status FROM file_inventory WHERE file_index=?",(index,)).fetchone()
    if old is None or old[0]!=generation or old[1]!=sha or old[-1]!="COMPLETE":
        raise ValueError("original legacy source provenance mismatch")
    if conn.execute("PRAGMA quick_check").fetchone()[0]!="ok":
        raise ValueError("original legacy DB corrupted")
    # TEMP in-memory SQLite B-tree, not a Python global source-row list.
    # Migration remains explicitly scoped to prior already-spent original part375.
    conn.execute("CREATE TEMP TABLE IF NOT EXISTS expected_jobs(job_id INTEGER PRIMARY KEY)")
    conn.execute("CREATE TEMP TABLE IF NOT EXISTS expected_tasks(job_id INTEGER,task_index INTEGER,PRIMARY KEY(job_id,task_index))")
    conn.execute("DELETE FROM expected_jobs")
    conn.execute("DELETE FROM expected_tasks")
    n=bytes_plain=0
    first=previous=None
    types=collections.Counter()
    try:
        with gzip.open(src,"rb") as fp:
            for line in fp:
                n+=1;bytes_plain+=len(line)
                if n>MAX_ROWS or bytes_plain>MAX_PLAIN or len(line)>16384 or not line.endswith(b"\n"):
                    raise ValueError("legacy original source stream exceeds quota/malformed")
                parsed=list(csv.reader([line.decode("utf-8","strict")]))
                if len(parsed)!=1 or len(parsed[0])!=13:
                    raise ValueError("original legacy source schema malformed")
                row=parsed[0]
                timestamp=int(row[0]);job=int(row[2]);task=int(row[3]);ev=int(row[5])
                if min(timestamp,job,task)<0 or not 0<=ev<9 or (previous is not None and timestamp<previous):
                    raise ValueError("invalid source timestamp, job or v2.1 event")
                if first is None:first=timestamp
                previous=timestamp
                types[NAMES[ev]]+=1
                conn.execute("INSERT OR IGNORE INTO expected_jobs VALUES(?)",(job,))
                conn.execute("INSERT OR IGNORE INTO expected_tasks VALUES(?,?)",(job,task))
        if (n,bytes_plain,first,previous)!=old[2:6]:
            raise ValueError("source records/time/bytes fail legacy expected original manifest")
        if expected_events is not None and types!=expected_events:
            raise ValueError("legacy source event totals differ from independently frozen result")
        actual=dict(conn.execute("SELECT event_type,n FROM event_counts WHERE file_index=?",(index,)))
        if actual!=dict(types):raise ValueError("legacy original event-type histogram mismatch")
        # SQL EXCEPT both directions, not merely matching cardinalities.
        checks=(
          """SELECT job_id FROM expected_jobs EXCEPT SELECT job_id FROM job_presence WHERE file_index=?""",
          """SELECT job_id FROM job_presence WHERE file_index=? EXCEPT SELECT job_id FROM expected_jobs""",
          """SELECT job_id,task_index FROM expected_tasks EXCEPT SELECT job_id,task_index FROM task_presence WHERE file_index=?""",
          """SELECT job_id,task_index FROM task_presence WHERE file_index=? EXCEPT SELECT job_id,task_index FROM expected_tasks""")
        if any(conn.execute(q,(index,)).fetchone() is not None for q in checks):
            raise ValueError("UNSAFE_RESUME_INTEGRITY_FAIL original vs SQLite exact key sets differ")
        conn.execute("BEGIN IMMEDIATE")
        try:
            ensure_schema(conn)
            if conn.execute("SELECT 1 FROM file_digests WHERE file_index=?",(index,)).fetchone():
                raise ValueError("legacy source already has digest; use strict resume")
            digest=commit_digest(conn,index)
            conn.commit()
        except BaseException:
            conn.rollback()
            raise
        return digest
    finally:
        conn.execute("DROP TABLE IF EXISTS temp.expected_jobs")
        conn.execute("DROP TABLE IF EXISTS temp.expected_tasks")
