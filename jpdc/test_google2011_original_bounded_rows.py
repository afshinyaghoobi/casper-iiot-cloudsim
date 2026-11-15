#!/usr/bin/env python3
"""Unit-only synthetic gzip fixtures. These are NOT original Google trace rows."""
import gzip
import io
import csv
import json
from google2011_original_bounded_rows import verify_original_prefix, MAX_COMPRESSED

META={"bucket":"clusterdata-2011-2","name":"task_events/part-00000-of-00500.csv.gz",
      "generation":"12345","size":"90000","updated":"fixture"}
def pack(rows):
    o=io.StringIO(newline="")
    w=csv.writer(o,lineterminator="\n")
    for row in rows:
        w.writerow(row)
    return gzip.compress(o.getvalue().encode(),mtime=0)

def must_reject(f):
    try:f()
    except (ValueError,TypeError,OverflowError):
        return
    raise AssertionError("malformed or false-source fixture unexpectedly accepted")

def go():
    good=["0","","123456789","1","","0","anon","0","5","0.3","0.2","",""]
    scheduled=["100","","123456789","1","123","1","anon","0","5","0.3","0.2","",""]
    source=pack([good,scheduled])
    result=verify_original_prefix(source,storage_metadata=META)
    assert result["original_rows_audited"]==2
    assert result["observed_submit_event_rows"]==1
    assert result["event_type_counts"]=={"SCHEDULE":1,"SUBMIT":1}
    assert result["missing_field_counts"]["missing_machine_id"]==1
    assert not result["real_per_task_network_bytes_observed"]
    assert not result["real_task_deadline_observed"]
    assert result["original_stage65_scientific_safety"]=="FAIL"
    assert result["classification"]=="ACTUAL_PRODUCTION_TRACE_EVENT_ROWS_ONLY" # parser output label; only real acquisition may assert origin
    # Synthetic examples must never count as empirical observations externally.
    must_reject(lambda:verify_original_prefix(pack([good[:-1]]),storage_metadata=META))
    must_reject(lambda:verify_original_prefix(pack([good[:5]+["3"]+good[6:]]),
                                         storage_metadata={**META,"name":"task_usage/example.gz"}))
    must_reject(lambda:verify_original_prefix(pack([[*good[:5],"9",*good[6:]]]),storage_metadata=META))
    must_reject(lambda:verify_original_prefix(pack([[*good[:5],"-1",*good[6:]]]),storage_metadata=META))
    must_reject(lambda:verify_original_prefix(pack([[*good[:5],"SCHEDULE",*good[6:]]]),storage_metadata=META))
    must_reject(lambda:verify_original_prefix(pack([scheduled,good]),storage_metadata=META))
    must_reject(lambda:verify_original_prefix(pack([good]),storage_metadata={**META,"generation":""}))
    must_reject(lambda:verify_original_prefix(pack([good]),storage_metadata={**META,"bucket":"evil"}))
    must_reject(lambda:verify_original_prefix(b"not gzip",storage_metadata=META))
    must_reject(lambda:verify_original_prefix(source[:5],storage_metadata=META))
    assert len(source)<MAX_COMPRESSED
    print("JPDC_ORIGINAL_TRACE_PARSER_SYNTHETIC_NEGATIVE_FIXTURES_PASS")
if __name__=="__main__":go()
