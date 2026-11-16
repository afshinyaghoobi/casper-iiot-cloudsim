#!/usr/bin/env python3
"""Synthetic-only mutation and deterministic batch boundaries; no source network."""
import sqlite3
from google2011_500file_offline_preflight import batches,check_source_db

def must_reject(fn):
    try:fn()
    except (ValueError,AssertionError):
        return
    raise AssertionError("unsafe source state admitted")

def valid_small_db():
    c=sqlite3.connect(":memory:")
    c.executescript("""
    CREATE TABLE file_inventory(file_index INTEGER,generation TEXT,original_sha256 TEXT,
      row_count INTEGER,bytes_plain INTEGER,first_us INTEGER,last_us INTEGER,status TEXT);
    CREATE TABLE job_presence(file_index INTEGER,job_id INTEGER);
    CREATE TABLE task_presence(file_index INTEGER,job_id INTEGER,task_index INTEGER);
    CREATE TABLE event_counts(file_index INTEGER,event_type TEXT,n INTEGER);
    """)
    return c

def main():
    records=[dict(file_index=i,size_bytes=n) for i,n in enumerate([9,10,1,10,10])]
    b=batches(records,budget=20)
    assert [r["indices"] for r in b]==[[0,1,2],[3,4]]
    assert sum(r["compressed_bytes"] for r in b)==40
    assert all(r["compressed_bytes"]<=20 for r in b)
    assert batches(records,budget=20)==b
    must_reject(lambda:batches(records,budget=9))
    must_reject(lambda:batches(records,budget=0))
    c=valid_small_db()
    must_reject(lambda:check_source_db(c))
    # Key failure mode: a SOURCE file_inventory status COMPLETE row does
    # NOT imply presence tables are complete or resume is safe.
    from google2011_500file_offline_preflight import EXPECTED_GENS,SOURCE_SHA
    c.execute("INSERT INTO file_inventory VALUES (?,?,?,?,?,?,?,?)",
              (375,EXPECTED_GENS[375],SOURCE_SHA,130812,14973713,
               1879800290193,1884810781196,"COMPLETE"))
    must_reject(lambda:check_source_db(c))
    c.execute("INSERT INTO job_presence VALUES(375,123)")
    c.execute("INSERT INTO task_presence VALUES(375,123,0)")
    must_reject(lambda:check_source_db(c))
    c.close()
    print("JPDC_GOOGLE2011_500_FILE_SYNTHETIC_BUDGET_RESUME_NEGATIVE_TEST_PASS")

if __name__=="__main__":main()
