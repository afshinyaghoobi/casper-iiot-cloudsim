#!/usr/bin/env python3
"""Stage67 positive and negative no-fabrication native queue-state contracts."""
from audit_stage67_native_service_scale import detect_queue_bypass,ids
def event(wait,ex,clock=1000.,kind="SUBMIT_AFTER"):
    return dict(wait_ids=wait,exec_ids=ex,clock_ms=clock,kind=kind)
def run():
    times={10:1000.,11:1005.,12:1008.}
    no=detect_queue_bypass([
        event([], [10]),event([11],[10]),
        event([12],[11]),event([], [12])],times)
    assert no==[],no
    yes=detect_queue_bypass([event([11],[12],1013.,"SUBMIT_AFTER")],times)
    assert len(yes)==1 and yes[0]["older_cloudlet_id"]==11 and yes[0]["later_cloudlet_id"]==12
    assert yes[0]["observed_at_ms"]==1013.
    # Equal timestamps cannot prove later chronological arrival.
    assert detect_queue_bypass([event([11],[12])],{11:5.,12:5.})==[]
    # Do not mistake a later waiting job for a bypass.
    assert detect_queue_bypass([event([12],[11])],times)==[]
    try:
        detect_queue_bypass([event([11],[99])],times)
        raise AssertionError("unknown node was accepted")
    except AssertionError as e:
        assert "unknown submission" in str(e)
    assert ids("10;11")==[10,11]
    try:
        ids("10;10")
        raise AssertionError("duplicate accepted")
    except AssertionError as e:
        assert "duplicate" in str(e)
    print("JPDC_STAGE67_SYNTHETIC_BYPASS_POSITIVE_NEGATIVE_PASS")
if __name__=="__main__":run()
