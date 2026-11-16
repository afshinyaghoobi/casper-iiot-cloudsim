#!/usr/bin/env python3
"""Independent archived original-gzip versus actual SQLite source-presence audit.

Reads exact original part375 gzip from run43928939896 and SQLite DB from
run43936091950, never imports primary inventory code and never calls GCS.
"""
import argparse
import collections
import csv
import gzip
import hashlib
import json
import sqlite3
from pathlib import Path

ORIGINAL_SOURCE_SHA="0ca3c532707d1a291228d59c75d7831d654cd330579a4dc9e32cfa0685783025"
EXPECTED_SQLITE_SHA="692059aca2d6b8621f84693490d71c9243d5a41b37f3c0b826101a34e10f0cb2"
EXPECTED_COMMIT="ef6d5fd650571112ab829f51031449a003d3908d"
EXPECTED_EVENTS={"SUBMIT":44330,"SCHEDULE":44290,"FINISH":26802,
                 "KILL":13423,"FAIL":1241,"EVICT":725,"UPDATE_RUNNING":1}
NAMES=("SUBMIT","SCHEDULE","EVICT","FAIL","FINISH","KILL","LOST",
       "UPDATE_PENDING","UPDATE_RUNNING")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--old-original",required=True)
    p.add_argument("--new-inventory",required=True)
    p.add_argument("--out",required=True)
    args=p.parse_args()
    orig=Path(args.old_original)/"original_full.gz"
    inv=Path(args.new_inventory)
    sql=inv/"presence.sqlite"
    assert hashlib.sha256(orig.read_bytes()).hexdigest()==ORIGINAL_SOURCE_SHA
    assert hashlib.sha256(sql.read_bytes()).hexdigest()==EXPECTED_SQLITE_SHA
    assert (inv/"source_commit.txt").read_text().strip()==EXPECTED_COMMIT
    original_summary=json.loads((inv/"source_summary.json").read_text())
    restored=json.loads((inv/"resume_summary.json").read_text())
    assert original_summary["source_state"]=="INGESTED_VERIFIED"
    assert restored["source_state"]=="ALREADY_VERIFIED_NOOP"
    a={k:v for k,v in original_summary.items() if k!="source_state"}
    b={k:v for k,v in restored.items() if k!="source_state"}
    assert a==b
    c=sqlite3.connect("file:"+str(sql.resolve())+"?mode=ro",uri=True)
    assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
    objects={row[0] for row in c.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert objects=={"file_inventory","job_presence","task_presence","event_counts"}
    assert c.execute("SELECT count(*) FROM file_inventory").fetchone()[0]==1
    fi=c.execute("SELECT * FROM file_inventory").fetchone()
    assert fi[:3]==(375,"1416266880306000",ORIGINAL_SOURCE_SHA)
    assert fi[3]==130812
    assert c.execute("SELECT count(*) FROM job_presence").fetchone()[0]==1838
    assert c.execute("SELECT count(*) FROM task_presence").fetchone()[0]==44979
    events=collections.Counter()
    jobs=set()
    keys=set()
    count=0
    source_first=None;source_last=None
    with gzip.open(orig,"rt",newline="",encoding="utf-8") as f:
        for row in csv.reader(f):
            assert len(row)==13
            ts=int(row[0]);job=int(row[2]);task=int(row[3]);code=int(row[5])
            assert min(ts,job,task)>=0 and 0<=code<=8
            if source_first is None:source_first=ts
            assert source_last is None or source_last<=ts
            source_last=ts
            count+=1
            if count>2000000:raise AssertionError("original too many source rows")
            events[NAMES[code]]+=1
            jobs.add(job)
            keys.add((job,task))
    assert count==130812 and len(jobs)==1838 and len(keys)==44979
    assert events==EXPECTED_EVENTS
    assert fi[5:7]==(source_first,source_last)
    dbjobs={r[0] for r in c.execute("SELECT job_id FROM job_presence WHERE file_index=375")}
    dbkeys={(r[0],r[1]) for r in c.execute("SELECT job_id,task_index FROM task_presence WHERE file_index=375")}
    assert dbjobs==jobs and dbkeys==keys # stronger than counts-only equality
    sqlevents=dict(c.execute("SELECT event_type,n FROM event_counts WHERE file_index=375"))
    assert sqlevents==EXPECTED_EVENTS
    assert c.execute("SELECT COUNT(*) FROM job_presence WHERE file_index!=375").fetchone()[0]==0
    assert c.execute("SELECT COUNT(*) FROM task_presence WHERE file_index!=375").fetchone()[0]==0
    assert a["original_source_rows"]==count
    assert a["unique_file_job_presence"]==len(jobs)
    assert a["unique_file_job_task_presence"]==len(keys)
    assert not a["train_dev_holdout_independence_certified"]
    c.close()
    result=dict(status="PASS",
      original_archived_full_gzip_SHA256=ORIGINAL_SOURCE_SHA,
      generated_original_sqlite_SHA256=EXPECTED_SQLITE_SHA,
      original_rows=130812,source_jobs=1838,source_job_task_keys=44979,
      event_counts=dict(sorted(events.items())),
      entire_original_job_id_set_equal_to_SQLite=True,
      entire_original_job_task_key_set_equal_to_SQLite=True,
      sqlite_integrity_check="ok",
      offline_resume_source_manifest_unchanged=True,
      independent_archived_data_and_code_comparison=True,
      complete_source_files=1,
      all_500_complete_source_files_ingested=False,
      independent_holdout_certified=False,
      original_stage65_safety="FAIL",
      original_java_python_parity="FAIL")
    dest=Path(args.out);dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("JPDC_INDEPENDENT_SQLITE_ORIGINAL_GZIP_KEY_SET_AUDIT",json.dumps(result,sort_keys=True))
    print("JPDC_SQLITE_COMPLETE_ORIGINAL_SOURCE_KEY_SET_INDEPENDENT_AUDIT_PASS")

if __name__=="__main__":main()
