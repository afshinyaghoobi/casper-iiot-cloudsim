#!/usr/bin/env python3
"""Explicitly synthetic-only SQLite transaction/overlap/resume negative fixtures."""
import gzip
import hashlib
import tempfile
from pathlib import Path
from google2011_sqlite_job_inventory import connection,ingest,summarize

def make_rows(path,records):
    raw=b"".join((",".join(map(str,row))+"\n").encode() for row in records)
    path.write_bytes(gzip.compress(raw,mtime=0))
    return hashlib.sha256(path.read_bytes()).hexdigest()

def line(at,job,task,event):
    return [at,"",job,task,"",event,"u","0","5","0.1","0.2","",""]

def rejects(call):
    try:call()
    except (ValueError,EOFError,OSError):return
    raise AssertionError("malformed source was accepted")

def main():
    with tempfile.TemporaryDirectory() as d:
        root=Path(d);source=root/"one.gz";db=root/"index.sqlite"
        rows=[line(i,10,i%17,i%9) for i in range(2100)]
        sha=make_rows(source,rows)
        con=connection(db)
        assert ingest(con,source,0,"111",sha)=="INGESTED_VERIFIED"
        baseline=summarize(con)
        assert baseline["original_source_rows"]==2100
        assert baseline["unique_file_job_presence"]==1
        assert baseline["unique_file_job_task_presence"]==17
        assert ingest(con,source,0,"111",sha)=="ALREADY_VERIFIED_NOOP"
        assert summarize(con)==baseline
        rejects(lambda:ingest(con,source,0,"112",sha))
        rejects(lambda:ingest(con,source,0,"111","0"*64))
        other=root/"two.gz"
        sha2=make_rows(other,[line(i,10 if i<100 else 20,i%11,0) for i in range(200)])
        assert ingest(con,other,1,"333",sha2)=="INGESTED_VERIFIED"
        combined=summarize(con)
        assert combined["cross_file_job_ids"]==1
        assert combined["cross_file_job_task_keys"]==11
        assert combined["complete_source_files"]==2
        assert not combined["train_dev_holdout_independence_certified"]
        before=combined
        invalid=root/"bad.gz"
        # 1024 flushed DB entries, then malformed one; transaction must rollback
        sha_bad=make_rows(invalid,[line(i,99,i,0) for i in range(1100)]+[line(1100,99,1100,9)])
        rejects(lambda:ingest(con,invalid,2,"444",sha_bad))
        assert summarize(con)==before
        assert con.execute("SELECT COUNT(*) FROM task_presence WHERE file_index=2").fetchone()[0]==0
        truncated=root/"truncated.gz"
        payload=other.read_bytes()
        truncated.write_bytes(payload[:-10])
        rejects(lambda:ingest(con,truncated,3,"555",hashlib.sha256(truncated.read_bytes()).hexdigest()))
        assert summarize(con)==before
        con.close()
    print("JPDC_GOOGLE_SQLITE_SYNTHETIC_RESUME_ROLLBACK_AND_CROSS_FILE_OVERLAP_PASS")

if __name__=="__main__":
    main()
