#!/usr/bin/env python3
"""Only SYNTHETIC fixtures for original Google2011 v2.1 window algorithm."""
import csv
import gzip
import io
from google2011_longitudinal_history_window import (
    parse_original_prefix, LIMIT_COMPRESSED, SELECT_ROWS)

META={"name":"task_events/part-00375-of-00500.csv.gz","bucket":"clusterdata-2011-2",
      "generation":"42","size":"999999"}
def row(t,code,job,task):
    return [str(t),"",str(job),str(task),"",str(code),"anon","0","1",
            "0.5","0.2","",""]
def compress(src):
    o=io.StringIO(newline="")
    writer=csv.writer(o,lineterminator="\n")
    writer.writerows(src)
    data=gzip.compress(o.getvalue().encode(),mtime=0)
    assert len(data)<LIMIT_COMPRESSED
    return data + b"\0"*(LIMIT_COMPRESSED-len(data))

def reject(f):
    try:f()
    except (ValueError,AssertionError):
        return
    raise AssertionError("accepted invalid synthetic input")

def run():
    # Real scheduling events can repeat after FAIL and FINISH.
    special=[row(100,0,1,0),row(101,1,1,0),row(102,3,1,0),
             row(103,0,1,0),row(104,1,1,0),row(105,4,1,0),
             row(106,0,1,0),row(107,1,1,0),
             row(108,1,2,0)]  # schedule without observed pending submit
    rows=special+[row(109+i,0,100+i,i) for i in range(SELECT_ROWS-len(special))]
    result=parse_original_prefix(compress(rows),META)
    assert result["original_rows_audited"]==SELECT_ROWS
    assert result["event_type_counts"]["SUBMIT"]==SELECT_ROWS-6
    assert result["matched_schedule_classification_counts"]["MATCHED_OBSERVED_SUBMIT_TO_SCHEDULE"]==3
    assert result["matched_schedule_classification_counts"]["SCHEDULE_WITHOUT_OBSERVED_PENDING_SUBMIT"]==1
    assert result["matched_submit_schedule_gap_descriptive_us"]["FIRST_OBSERVED_SUBMIT_LEFT_CENSORED"]["count"]==1
    assert result["matched_submit_schedule_gap_descriptive_us"]["RESUBMIT_AFTER_OBSERVED_TERMINAL"]["count"]==2
    assert result["submit_classification_counts"]["TERMINAL_PREDECESSOR_FAIL"]==1
    assert result["submit_classification_counts"]["TERMINAL_PREDECESSOR_FINISH"]==1
    assert result["right_censored_pending_submit_keys"]==SELECT_ROWS-len(special)
    assert result["matched_gaps_distinct_jobs"]==1
    assert not result["independently_validated_scheduler_performance"]
    short=[row(i,0,i,i) for i in range(SELECT_ROWS-1)]
    reject(lambda:parse_original_prefix(compress(short),META))
    bad=rows.copy();bad[1]=row(-1,1,1,0)
    reject(lambda:parse_original_prefix(compress(bad),META))
    bad=rows.copy();bad[0]=bad[0][:-1]
    reject(lambda:parse_original_prefix(compress(bad),META))
    bad=rows.copy();bad[1]=row(101,9,1,0)
    reject(lambda:parse_original_prefix(compress(bad),META))
    bad=rows.copy();bad[2]=row(99,3,1,0)
    reject(lambda:parse_original_prefix(compress(bad),META))
    reject(lambda:parse_original_prefix(compress(rows),{**META,"name":"task_events/part-00250-of-00500.csv.gz"}))
    print("JPDC_GOOGLE2011_LONGITUDINAL_SYNTHETIC_HISTORY_NEGATIVE_TESTS_PASS")
if __name__=="__main__":run()
