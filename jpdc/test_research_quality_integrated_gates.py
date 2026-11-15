#!/usr/bin/env python3
"""Nonredundant Stage65 exact-sign and external trace version semantics fixtures."""
from verify_original_stage65_independent_math import exact_two_sided_sign_by_enumeration
from trace_versioned_semantics_verifier import (
    decode_google_event, alibaba_time_semantics, admission_from_schema_only)


def must_raise(fn, expected):
    try:
        fn()
    except expected:
        return
    raise AssertionError("expected rejection, accepted invalid schema/source data")


def run():
    # v2.1 and v3 are *different*. Never conflate schedule with submit,
    # or v2.1 FAIL(3) with v3 SCHEDULE(3).
    assert decode_google_event("google_borg_2011_v2.1", 0).event_name == "SUBMIT"
    assert decode_google_event("google_borg_2011_v2.1", 1).event_name == "SCHEDULE"
    assert decode_google_event("google_borg_2011_v2.1", 3).event_name == "FAIL"
    assert decode_google_event("google_borg_2019_v3", 1).event_name == "QUEUE"
    assert decode_google_event("google_borg_2019_v3", 3).event_name == "SCHEDULE"
    assert decode_google_event("google_borg_2019_v3", 6).event_name == "FINISH"
    assert not decode_google_event("google_borg_2011_v2.1", 1).scheduler_submit_observed
    assert not decode_google_event("google_borg_2019_v3", 3).machine_execution_observed
    assert decode_google_event("google_borg_2019_v3", 0).scheduler_submit_observed
    must_raise(lambda: decode_google_event("google_borg_2011_v2.1", 10), ValueError)
    must_raise(lambda: decode_google_event("unknown", 0), ValueError)
    must_raise(lambda: decode_google_event("google_borg_2019_v3", "0"), TypeError)
    must_raise(lambda: decode_google_event("google_borg_2019_v3", True), TypeError)
    assert alibaba_time_semantics("alibaba_cluster_v2017","batch_task","task create time") == "CREATION_TIME_CANDIDATE"
    assert alibaba_time_semantics("alibaba_cluster_v2017","batch_instance","start_timestamp") == "EXECUTION_START_ONLY"
    assert alibaba_time_semantics("alibaba_cluster_v2018","batch_task","start_time") == "EXECUTION_START_ONLY"
    must_raise(lambda: alibaba_time_semantics("alibaba_cluster_v2018","batch_task","task create time"), ValueError)
    must_raise(lambda: alibaba_time_semantics("alibaba_cluster_v2017","batch_task","start_time"), ValueError)
    assert admission_from_schema_only(creation_or_submit_field=True,original_rows_checked=0,
                                      measured_deadline=True,measured_network_bytes=True)=="DOCUMENTATION_ONLY_PENDING_ROWS"
    assert admission_from_schema_only(creation_or_submit_field=False,original_rows_checked=100)=="TRACE_PLACEMENT_OR_USAGE_ONLY"
    assert admission_from_schema_only(creation_or_submit_field=True,original_rows_checked=100)=="TRACE_ARRIVAL_RESOURCE_ONLY"
    assert admission_from_schema_only(creation_or_submit_field=True,original_rows_checked=100,
                measured_deadline=True,measured_network_bytes=True)=="PENDING_PHYSICAL_UNITS_AND_PROVENANCE_AUDIT"
    must_raise(lambda: admission_from_schema_only(original_rows_checked=-1),ValueError)
    # Exact sign tests independently enumerate all conditional sign choices.
    assert exact_two_sided_sign_by_enumeration([])["two_sided_p"] == 1.0
    assert exact_two_sided_sign_by_enumeration([0,-2,0,-5,1,1,-2,0])["two_sided_p"] == 1.0
    assert exact_two_sided_sign_by_enumeration([0,0,-6,-2,-3,0,-6,0])["two_sided_p"] == .125
    assert exact_two_sided_sign_by_enumeration([-1]*8)["two_sided_p"] == .0078125
    assert exact_two_sided_sign_by_enumeration([1]*8)["two_sided_p"] == .0078125
    print("JPDC_RESEARCH_SKILL_INTEGRATION_NEGATIVE_TESTS_PASS")


if __name__=="__main__":
    run()
