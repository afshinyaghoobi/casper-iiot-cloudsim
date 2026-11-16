#!/usr/bin/env python3
"""Synthetic-only negative controls for original-source job split gate."""
from google2011_original_job_identity_split_gate import split_gate

def main():
    overlap=split_gate([{1,2,3},{4,2,5}],
        complete_frames_verified=True,temporal_embargo_verified=True)
    assert overlap["observed_shared_jobs"]==1
    assert not overlap["full_source_job_disjointness_certified"]
    assert overlap["split_status"]=="NOT_CERTIFIED_FOR_INDEPENDENT_HOLDOUT"
    disjoint_but_only_prefix=split_gate([{1,2},{3,4}],
        complete_frames_verified=False,temporal_embargo_verified=True)
    assert disjoint_but_only_prefix["job_disjoint_in_supplied_records"]
    assert not disjoint_but_only_prefix["full_source_job_disjointness_certified"]
    disjoint_but_no_embargo=split_gate([{1},{2}],
        complete_frames_verified=True,temporal_embargo_verified=False)
    assert not disjoint_but_no_embargo["full_source_job_disjointness_certified"]
    whole_valid=split_gate([{1},{2},{3}],
        complete_frames_verified=True,temporal_embargo_verified=True)
    assert whole_valid["full_source_job_disjointness_certified"]
    assert whole_valid["split_status"]=="FULL_SOURCE_SPLIT_CERTIFIED"
    for case in ([],[{1}]):
        try:split_gate(case)
        except ValueError:pass
        else:raise AssertionError("invalid count of data cohorts not rejected")
    print("JPDC_2011_ORIGINAL_JOB_IDENTITY_SPLIT_SYNTHETIC_NEGATIVE_GATES_PASS")

if __name__=="__main__":main()
