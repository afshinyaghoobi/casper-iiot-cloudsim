#!/usr/bin/env python3
"""Stage69 negative source admission fixture: no imputed deadline or arrival."""
from dataclasses import replace
import json
from external_trace_admission_stage69 import (CANDIDATES,TraceEvidence,classify,evaluate,
    STATUS_DOCUMENTATION,STATUS_LICENSE,STATUS_PLACEMENT,STATUS_ARRIVAL,STATUS_FULL,
    STATUS_REJECTED)
def main():
    d=evaluate()
    assert len(d["dataset_candidates"])==3
    assert all(r["status"]==STATUS_DOCUMENTATION and r["observed_actual_workload_rows"]==0
               for r in d["dataset_candidates"])
    alibaba,google2011,google2019=CANDIDATES
    assert not alibaba.dataset_license_confirmed
    assert google2011.dataset_license_confirmed and google2019.dataset_license_confirmed
    assert all(not e.observed_submit_time for e in CANDIDATES)
    assert all(not e.observed_per_task_network_mb and not e.observed_task_relative_deadline
               for e in CANDIDATES)
    digest="1"*64
    documented=replace(alibaba,original_rows_audited=10,original_rows_sha256=digest)
    assert classify(documented)==STATUS_LICENSE
    measured=replace(documented,dataset_license_confirmed=True)
    assert classify(measured)==STATUS_PLACEMENT, "execution-start is not submission"
    arrival=replace(measured,observed_submit_time=True)
    assert classify(arrival)==STATUS_ARRIVAL, "missing network/deadline not zero-filled"
    assert classify(replace(arrival,observed_per_task_network_mb=True))==STATUS_ARRIVAL
    assert classify(replace(arrival,observed_task_relative_deadline=True))==STATUS_ARRIVAL
    assert classify(replace(arrival,observed_per_task_network_mb=True,
             observed_task_relative_deadline=True))==STATUS_ARRIVAL
    full=replace(arrival,observed_per_task_network_mb=True,
         observed_task_relative_deadline=True,
         observed_cpu_work_physical_units=True,
         documented_node_capacity_topology=True)
    assert classify(full)==STATUS_FULL
    # A *synthetic* fixture only checks structural predicates; none of these
    # source rows is real, and the published report is documentation-only.
    assert classify(replace(full,original_rows_audited=0,
                            original_rows_sha256=None))==STATUS_DOCUMENTATION
    assert classify(replace(full,original_rows_sha256=None))==STATUS_REJECTED
    assert classify(replace(full,original_rows_sha256="not sha"))==STATUS_REJECTED
    assert classify(replace(full,timestamp_units_confirmed=False))==STATUS_REJECTED
    assert classify(replace(full,original_rows_audited=-1))==STATUS_REJECTED
    try:
        evaluate((alibaba,alibaba))
        raise AssertionError("accepted duplicate IDs")
    except ValueError as ex:
        assert "duplicate" in str(ex)
    print("JPDC_STAGE69_GATE_NEGATIVE_FIXTURES",json.dumps(dict(
       publisher_candidates=3,authentic_rows_observed=0,
       source_submission_not_inferred_from_start=True,
       no_synthetic_network_as_observed=True,
       no_invented_deadlines=True,
       structural_full_fixture_is_not_empirical_validation=True,
       stage65_scientific_safety_still_failed=True),sort_keys=True))
    print("JPDC_STAGE69_NEGATIVE_ADMISSION_CONTRACT_PASS")
if __name__=="__main__":main()
