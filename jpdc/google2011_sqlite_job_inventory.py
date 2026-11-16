#!/usr/bin/env python3
"""Bounded atomic SQLite job/task PRESENCE inventory, not a workload replay.

Production workflow ingests only archived previously spent Google Borg2011
part375. Generic interface enables SYNTHETIC rollback/resume tests.
"""
import argparse
import collections
import csv
import gzip
import hashlib
import json
import os
import sqlite3
from pathlib import Path

EVENTS=("SUBMIT","SCHEDULE","EVICT","FAIL","FINISH","KILL","LOST",
        "UPDATE_PENDING","UPDATE_RUNNING")
MAX_PLAIN_BYTES=128*1024*1024
MAX_LINES=2_000_000
MAX_LINE_BYTES=16384
BATCH=1024
DB_MAX_BYTES=256*1024*1024
ORIGINAL_PART375_SHA="0ca3c532707d1a291228d59c75d7831d654cd330579a4dc9e32cfa0685783025"
ORIGINAL_PART375_GENERATION="1416266880306000"
ORIGINAL_PART375_SIZE=1502643
ORIGINAL_PART375_EVENTS={"SUBMIT":44330,"SCHEDULE":44290,"FINISH":26802,
 "KILL":13423,"FAIL":1241,"EVICT":725,"UPDATE_RUNNING":1}

def connection(db):
    db.parent.mkdir(parents=True,exist_ok=True)
    conn=sqlite3.connect(str(db))
    conn.execute("PRAGMA journal_mode=DELETE")
    conn.execute("PRAGMA synchronous=FULL")
    conn.execute("PRAGMA cache_size=-8192")
    conn.execute("PRAGMA temp_store=FILE")
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS file_inventory(
      file_index INTEGER PRIMARY KEY, generation TEXT NOT NULL,
      original_sha256 TEXT NOT NULL, row_count INTEGER NOT NULL,
      bytes_plain INTEGER NOT NULL, first_us INTEGER NOT NULL,
      last_us INTEGER NOT NULL, status TEXT NOT NULL CHECK(status='COMPLETE'));
    CREATE TABLE IF NOT EXISTS job_presence(
      file_index INTEGER NOT NULL, job_id INTEGER NOT NULL,
      PRIMARY KEY(file_index,job_id));
    CREATE TABLE IF NOT EXISTS task_presence(
      file_index INTEGER NOT NULL, job_id INTEGER NOT NULL,
      task_index INTEGER NOT NULL,
      PRIMARY KEY(file_index,job_id,task_index));
    CREATE TABLE IF NOT EXISTS event_counts(
      file_index INTEGER NOT NULL, event_type TEXT NOT NULL,
      n INTEGER NOT NULL,
      PRIMARY KEY(file_index,event_type));
    """)
    return conn

def source_sha(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk=f.read(65536)
            if not chunk:break
            h.update(chunk)
    return h.hexdigest()

def ingest(conn, source, file_index, generation, expected_sha, expected_events=None,
           max_compressed=None):
    if not isinstance(file_index,int) or not 0<=file_index<500:
        raise ValueError("file index outside original Google2011 task_events scope")
    if not generation.isdecimal() or len(expected_sha)!=64:
        raise ValueError("unversioned source or bad source SHA")
    if max_compressed is not None and source.stat().st_size>max_compressed:
        raise ValueError("source exceeds frozen compressed bound")
    digest=source_sha(source)
    if digest!=expected_sha:
        raise ValueError("source gzip does not match preregistered SHA256")
    old=conn.execute("SELECT generation,original_sha256,status FROM file_inventory WHERE file_index=?",
                     (file_index,)).fetchone()
    if old is not None:
        if old!=(generation,expected_sha,"COMPLETE"):
            raise ValueError("resume source identity mismatch")
        return "ALREADY_VERIFIED_NOOP"
    # One transaction for entire file. No partial-success manifest survives
    # syntax/schema/EOF errors, even if some rows were already processed.
    rows=0;bytes_plain=0;first=last=None
    events=collections.Counter()
    batch=[]
    try:
        conn.execute("BEGIN IMMEDIATE")
        with gzip.open(source,"rb") as fp:
            for binary in fp:
                rows+=1
                bytes_plain+=len(binary)
                if rows>MAX_LINES or bytes_plain>MAX_PLAIN_BYTES or len(binary)>MAX_LINE_BYTES:
                    raise ValueError("source streaming quota exceeded")
                if not binary.endswith(b"\n"):
                    raise ValueError("unterminated original CSV line")
                record=list(csv.reader([binary.decode("utf-8","strict")]))
                if len(record)!=1 or len(record[0])!=13:
                    raise ValueError("Google2011 task_events v2.1 must contain 13 columns")
                r=record[0]
                time=int(r[0]);job=int(r[2]);task=int(r[3]);etype=int(r[5])
                if min(time,job,task)<0 or not 0<=etype<len(EVENTS):
                    raise ValueError("invalid original source time/key/event")
                if last is not None and time<last:raise ValueError("unordered source time")
                if first is None:first=time
                last=time
                events[EVENTS[etype]]+=1
                batch.append((file_index,job,task))
                if len(batch)==BATCH:
                    _flush(conn,batch)
                    batch.clear()
        if batch:_flush(conn,batch)
        if rows==0:raise ValueError("empty source")
        if expected_events is not None and dict(events)!=expected_events:
            raise ValueError("original source event conservation mismatch")
        conn.executemany("INSERT INTO event_counts VALUES(?,?,?)",
                         [(file_index,key,n) for key,n in sorted(events.items())])
        conn.execute("INSERT INTO file_inventory VALUES(?,?,?,?,?,?,?,'COMPLETE')",
                     (file_index,generation,expected_sha,rows,bytes_plain,first,last))
        conn.commit()
    except BaseException:
        conn.rollback()
        raise
    return "INGESTED_VERIFIED"

def _flush(conn,batch):
    conn.executemany("INSERT OR IGNORE INTO job_presence VALUES(?,?)",
                     [(fi,j) for fi,j,_ in batch])
    conn.executemany("INSERT OR IGNORE INTO task_presence VALUES(?,?,?)",batch)

def summarize(conn):
    files=conn.execute("SELECT file_index,generation,original_sha256,row_count,bytes_plain,first_us,last_us FROM file_inventory ORDER BY file_index").fetchall()
    return dict(status="PASS",classification="DISK_BACKED_SOURCE_IDENTITY_SOFTWARE_INDEX",
        files=[dict(file_index=r[0],generation=r[1],sha256=r[2],rows=r[3],
                    uncompressed_bytes=r[4],first_us=r[5],last_us=r[6]) for r in files],
        original_source_rows=sum(r[3] for r in files),
        unique_file_job_presence=conn.execute("SELECT COUNT(*) FROM job_presence").fetchone()[0],
        unique_file_job_task_presence=conn.execute("SELECT COUNT(*) FROM task_presence").fetchone()[0],
        cross_file_job_ids=conn.execute("""SELECT COUNT(*) FROM
          (SELECT job_id FROM job_presence GROUP BY job_id HAVING COUNT(DISTINCT file_index)>1)""").fetchone()[0],
        cross_file_job_task_keys=conn.execute("""SELECT COUNT(*) FROM
          (SELECT job_id,task_index FROM task_presence GROUP BY job_id,task_index
          HAVING COUNT(DISTINCT file_index)>1)""").fetchone()[0],
        events=[dict(file_index=r[0],event=r[1],count=r[2]) for r in
                conn.execute("SELECT file_index,event_type,n FROM event_counts ORDER BY file_index,event_type")],
        complete_source_files=len(files),
        whole_500_file_inventory_complete=len(files)==500,
        train_dev_holdout_independence_certified=False,
        original_stage65_scientific_safety="FAIL",
        original_java_python_queue_parity="FAIL")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--db",required=True)
    p.add_argument("--source",required=True)
    p.add_argument("--out",required=True)
    p.add_argument("--file-index",type=int,default=375)
    p.add_argument("--generation",default=ORIGINAL_PART375_GENERATION)
    p.add_argument("--expected-sha",default=ORIGINAL_PART375_SHA)
    a=p.parse_args()
    source=Path(a.source);db=Path(a.db)
    if a.file_index!=375 or a.generation!=ORIGINAL_PART375_GENERATION or a.expected_sha!=ORIGINAL_PART375_SHA:
        raise ValueError("real CI pilot is frozen to already-spent part375")
    if source.stat().st_size!=ORIGINAL_PART375_SIZE:
        raise ValueError("original complete source bytes mismatch")
    c=connection(db)
    try:
        state=ingest(c,source,a.file_index,a.generation,a.expected_sha,
                     expected_events=ORIGINAL_PART375_EVENTS,
                     max_compressed=ORIGINAL_PART375_SIZE)
        result=summarize(c)
        result["source_state"]=state
        if result["original_source_rows"]!=130812 or (
            result["unique_file_job_presence"]!=1838 or
            result["unique_file_job_task_presence"]!=44979):
            raise ValueError("SQLite event source identity summary differs from independently verified original source")
        if db.stat().st_size>DB_MAX_BYTES:
            raise ValueError("SQLite pilot DB storage exceeds preregistered 256MiB cap")
        Path(a.out).write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
        print("JPDC_SQLITE_FULL_SPENT_SOURCE_IDENTITY",json.dumps(
            {k:v for k,v in result.items() if k not in ("files","events")},sort_keys=True))
        print("JPDC_SQLITE_ORIGINAL_FULL_SOURCE_IDENTITY_INDEX_PASS")
    finally:
        c.close()

if __name__=="__main__":
    main()
