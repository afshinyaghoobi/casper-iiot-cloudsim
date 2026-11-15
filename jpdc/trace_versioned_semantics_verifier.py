#!/usr/bin/env python3
"""Versioned, fail-closed production trace event/arrival semantic boundaries.

These are *published schema labels*, not measured task rows. A decoder cannot
certify a raw trace or turn synthetic network/SLO into measured observations.
"""
from dataclasses import dataclass

GOOGLE2011_V21 = ("SUBMIT", "SCHEDULE", "EVICT", "FAIL", "FINISH",
                  "KILL", "LOST", "UPDATE_PENDING", "UPDATE_RUNNING")
GOOGLE2019_V3 = ("SUBMIT", "QUEUE", "ENABLE", "SCHEDULE", "EVICT", "FAIL",
                 "FINISH", "KILL", "LOST", "UPDATE_PENDING", "UPDATE_RUNNING")
GOOGLE_SCHEMAS = {
    "google_borg_2011_v2.1": GOOGLE2011_V21,
    "google_borg_2019_v3": GOOGLE2019_V3,
}
ALIBABA_SCHEMAS = {
    ("alibaba_cluster_v2017", "batch_task", "task create time"): "CREATION_TIME_CANDIDATE",
    ("alibaba_cluster_v2017", "batch_instance", "start_timestamp"): "EXECUTION_START_ONLY",
    ("alibaba_cluster_v2018", "batch_task", "start_time"): "EXECUTION_START_ONLY",
    ("alibaba_cluster_v2018", "batch_instance", "start_time"): "EXECUTION_START_ONLY",
}


@dataclass(frozen=True)
class EventSemantics:
    dataset_version: str
    event_name: str
    scheduler_submit_observed: bool
    machine_execution_observed: bool
    recorded_termination: bool


def decode_google_event(version, code):
    if type(code) is not int:
        raise TypeError("numeric event code must be exact integer, not coerced from string/bool")
    if version not in GOOGLE_SCHEMAS:
        raise ValueError("unknown version: event codes cannot be used across schemas")
    events = GOOGLE_SCHEMAS[version]
    if code < 0 or code >= len(events):
        raise ValueError("unsupported event code for this version")
    name = events[code]
    return EventSemantics(
        dataset_version=version, event_name=name,
        scheduler_submit_observed=(name == "SUBMIT"),
        # SCHEDULE only means placement on a machine; original docs note
        # execution need not physically begin at that precise instant.
        machine_execution_observed=False,
        recorded_termination=(name in {"FINISH", "FAIL", "EVICT", "KILL", "LOST"}))


def alibaba_time_semantics(version, table, exact_field):
    key = (version, table, exact_field)
    if key not in ALIBABA_SCHEMAS:
        raise ValueError("time field not verified from the exact published version/table schema")
    return ALIBABA_SCHEMAS[key]


def admission_from_schema_only(*, creation_or_submit_field=False,
                               original_rows_checked=0,
                               measured_deadline=False,
                               measured_network_bytes=False):
    """Explicitly deny 'full external workload' on published schema labels alone."""
    if type(original_rows_checked) is not int or original_rows_checked < 0:
        raise ValueError("invalid number of verified original rows")
    if original_rows_checked == 0:
        return "DOCUMENTATION_ONLY_PENDING_ROWS"
    if not creation_or_submit_field:
        return "TRACE_PLACEMENT_OR_USAGE_ONLY"
    if not measured_network_bytes or not measured_deadline:
        return "TRACE_ARRIVAL_RESOURCE_ONLY"
    # Other checks (legal rights, physically measured CPU work and node mapping)
    # still required, so this function NEVER marks a source FULL.
    return "PENDING_PHYSICAL_UNITS_AND_PROVENANCE_AUDIT"
