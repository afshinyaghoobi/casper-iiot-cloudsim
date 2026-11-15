#!/usr/bin/env python3
"""SYNTHETIC FIXTURES ONLY for Google2011 mid-partition original-row semantics."""
import csv
import gzip
import io
from google2011_middle_temporal_probe import same_original_records, EXACT_KEY
from google2011_original_bounded_rows import MAX_COMPRESSED

FIXTURE_STORAGE={"bucket":"clusterdata-2011-2","name":EXACT_KEY,
                 "generation":"42","size":str(MAX_COMPRESSED),
                 "updated":"SYNTHETIC_TEST_ONLY"}

def pack(rows):
    out=io.StringIO(newline="")
    writer=csv.writer(out,lineterminator="\n")
    writer.writerows(rows)
    gz=gzip.compress(out.getvalue().encode("utf-8"),mtime=0)
    assert len(gz)<MAX_COMPRESSED
    return gz+b"\x00"*(MAX_COMPRESSED-len(gz))

def row(time_us,event,task,other=""):
    return [str(time_us),other,"42",str(task),"7",str(event),"anon",
            "0","5","0.25","0.125","",""]

def expect_reject(fn):
    try:fn()
    except (ValueError,AssertionError):
        return
    raise AssertionError("invalid synthetic input accepted")

def run():
    rows=[row(1000000,0,j) for j in range(100)]
    rows += [row(2000000,1,j) for j in range(28)]
    result=same_original_records(pack(rows),FIXTURE_STORAGE)
    assert result["original_rows_audited"]==128
    assert result["observed_submit_rows"]==100
    assert result["observed_schedule_rows"]==28
    assert result["new_nonzero_temporal_source_event_count"]==128
    assert result["nonzero_time_exploratory_gate"]=="PASS"
    assert result["within_prefix_observed_submit_schedule_pairs"]["count"]==28
    assert result["within_prefix_observed_submit_schedule_pairs"]["median_us"]==1000000
    assert not result["complete_external_dispatch_dataset_admitted"]
    # Real evidence may include events for tasks whose SUBMIT is outside
    # our bounded prefix: that is an unpaired observation, NOT 0 wait.
    unpaired=[row(1000000,1,j) for j in range(128)]
    q=same_original_records(pack(unpaired),FIXTURE_STORAGE)
    assert q["observed_schedule_rows"]==128
    assert q["within_prefix_observed_submit_schedule_pairs"]["status"]=="NO_PAIRED_SUBMIT_SCHEDULE_IN_PREFIX"
    assert q["observed_submit_rows"]==0
    # All timestamp-zero rows do not pass temporal usefulness.
    zero=same_original_records(pack([row(0,0,j) for j in range(128)]),FIXTURE_STORAGE)
    assert zero["nonzero_time_exploratory_gate"]=="NO_NONZERO_TEMPORAL_OBSERVATIONS"
    bad=rows.copy()
    bad[0]=row(1000000,9,0)
    expect_reject(lambda:same_original_records(pack(bad),FIXTURE_STORAGE))
    bad=rows.copy()
    bad[1]=row(-1,0,1)
    expect_reject(lambda:same_original_records(pack(bad),FIXTURE_STORAGE))
    bad=rows.copy()
    bad[0]=bad[0][:-1]
    expect_reject(lambda:same_original_records(pack(bad),FIXTURE_STORAGE))
    bad=rows.copy()
    bad[110]=row(500000,1,10)
    expect_reject(lambda:same_original_records(pack(bad),FIXTURE_STORAGE))
    expect_reject(lambda:same_original_records(pack(rows),
                       {**FIXTURE_STORAGE,"name":"task_events/part-00249-of-00500.csv.gz"}))
    print("JPDC_GOOGLE2011_MIDDLE_SYNTHETIC_TEMPORAL_AND_PAIR_CONTRACT_PASS")

if __name__=="__main__":run()
