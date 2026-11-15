#!/usr/bin/env python3
"""Synthetic-only fixture for original Google two-source source-overlap logic."""
import csv
import gzip
import io
import json
import tempfile
from pathlib import Path

from google2011_two_partition_overlap import KEYS,run,MAX_COMPRESSED,ROWS


def make_gzip_rows(timestamp_offset, job_start):
    o=io.StringIO(newline="")
    w=csv.writer(o,lineterminator="\n")
    for i in range(ROWS):
        t=timestamp_offset+i*1000
        code=0 if i%3==0 else (1 if i%3==1 else 4)
        row=[str(t),"",str(job_start+i//6),str(i%6),"",str(code),
             "u","0","1","0.2","0.1","",""]
        w.writerow(row)
    zipped=gzip.compress(o.getvalue().encode(),mtime=0)
    assert len(zipped)<MAX_COMPRESSED
    return zipped+b"\0"*(MAX_COMPRESSED-len(zipped))


def fill(out, offsets, jobs):
    for i,key in enumerate(KEYS):
        d=out/f"source_{i}"
        d.mkdir(exist_ok=True,parents=True)
        m={"bucket":"clusterdata-2011-2","name":key,"generation":"789",
           "size":"500000","crc32c":"synthetic-only"}
        h={"status":206,"content_range":"bytes 0-262143/500000"}
        (d/"metadata.json").write_text(json.dumps(m))
        (d/"http.json").write_text(json.dumps(h))
        (d/"original_prefix.gz").write_bytes(make_gzip_rows(offsets[i],jobs[i]))


def main():
    with tempfile.TemporaryDirectory() as folder:
        base=Path(folder)
        fill(base,[1000000,4000000],[100,10000])
        first=run(base,True)
        assert first["status"]=="PASS"
        assert not first["selected_timestamp_intervals_overlap"]
        assert first["shared_job_id_count"]==0
        assert first["shared_job_task_id_count"]==0
        assert first["full_partition_job_independence"]=="UNRESOLVED_FULL_SOURCE_INDEPENDENCE"
        fill(base,[1000000,1000000],[100,100])
        second=run(base,True)
        assert second["selected_timestamp_intervals_overlap"]
        assert second["shared_job_id_count"]>0
        assert second["shared_job_task_id_count"]>0
        assert second["sampled_overlap_classification"]=="OBSERVED_JOB_TASK_KEY_OVERLAP"
        fill(base,[1000000,1000000],[100,10000])
        third=run(base,True)
        assert third["selected_timestamp_intervals_overlap"]
        assert third["shared_job_id_count"]==0
        assert third["sampled_overlap_classification"]=="TIMESTAMP_WINDOWS_OVERLAP_NO_OBSERVED_JOB_ID_OVERLAP"
        assert third["original_stage65_safety"]=="FAIL"
    print("JPDC_GOOGLE2011_TWO_PARTITION_SYNTHETIC_OVERLAP_CONTRACT_PASS")


if __name__=="__main__":
    main()
