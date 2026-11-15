#!/usr/bin/env python3
"""Stage69 metadata-only external trace source admission. NO row-level data loaded.

This is a fail-closed provenance/schema screening implementation. Never
certify full experimental readiness from official documentation alone.
"""
from dataclasses import dataclass,asdict
import hashlib,json

STATUS_DOCUMENTATION="DOCUMENTATION_ONLY_PENDING_ROWS"
STATUS_LICENSE="BLOCKED_PROVENANCE_OR_LICENSE"
STATUS_PLACEMENT="TRACE_PLACEMENT_AND_RESOURCE_ONLY"
STATUS_ARRIVAL="TRACE_ARRIVAL_RESOURCE_ONLY"
STATUS_FULL="FULL_EXTERNAL_ONLINE_DISPATCH"
STATUS_REJECTED="REJECTED_MALFORMED"

@dataclass(frozen=True)
class TraceEvidence:
    dataset_id:str
    publisher:str
    official_url:str
    docs_url:str
    dataset_license_confirmed:bool
    dataset_license_text:str
    original_rows_audited:int
    original_rows_sha256:str|None
    observed_submit_time:bool
    observed_execution_start:bool
    observed_cpu_work_physical_units:bool
    observed_cpu_resource_field:bool
    observed_per_task_network_mb:bool
    observed_task_relative_deadline:bool
    documented_node_capacity_topology:bool
    timestamp_units_confirmed:bool
    raw_time_semantics:str
    context:str
    preliminary_evidence_only:bool=True

CANDIDATES=(
TraceEvidence(
 "alibaba_cluster_trace_2018","Alibaba Group","https://github.com/alibaba/clusterdata",
 "https://github.com/alibaba/clusterdata/blob/master/cluster-trace-v2018/schema.txt",
 False,"UNVERIFIED_PUBLISHER_DATA_REUSE_TERMS",0,None,False,True,False,True,
 False,False,False,True,"task_instance_start_end_relative_seconds",
 "production data-center task/instance/machine/resource traces, not IIoT devices"),
TraceEvidence(
 "google_clusterdata_2011_v21","Google","https://github.com/google/cluster-data",
 "https://github.com/google/cluster-data/blob/master/ClusterData2011_2.md",
 True,"CC-BY_OFFICIAL_ROOT",0,None,False,True,False,True,False,False,
 False,True,"event_and_resource_traces_row_schema_not_yet_audited",
 "production Borg cluster task events/usage, not factory edge"),
TraceEvidence(
 "google_clusterdata_2019_v3","Google","https://github.com/google/cluster-data",
 "https://github.com/google/cluster-data/blob/master/ClusterData2019.md",
 True,"CC-BY_OFFICIAL_ROOT",0,None,False,False,False,True,False,False,
 False,False,"resource_requests_and_usage_bigquery_no_rows_loaded",
 "8 Borg cells May2019; 2.4TiB compressed per official metadata"),
)

def classify(e,*,fixture=False):
    if not isinstance(e,TraceEvidence):raise TypeError("TraceEvidence required")
    if not e.dataset_id or not e.publisher or not e.official_url.startswith("https://"):
        return STATUS_REJECTED
    if e.original_rows_audited<0:return STATUS_REJECTED
    if e.original_rows_audited==0:
        if e.original_rows_sha256 is not None:
            return STATUS_REJECTED
        return STATUS_DOCUMENTATION
    if e.original_rows_sha256 is None or len(e.original_rows_sha256)!=64:
        return STATUS_REJECTED
    try:int(e.original_rows_sha256,16)
    except ValueError:return STATUS_REJECTED
    if not e.timestamp_units_confirmed:return STATUS_REJECTED
    if not e.dataset_license_confirmed:
        return STATUS_LICENSE
    if e.observed_submit_time:
        if not e.observed_cpu_resource_field and not e.observed_cpu_work_physical_units:
            return STATUS_REJECTED
        full=all((e.observed_cpu_work_physical_units,e.observed_per_task_network_mb,
                  e.observed_task_relative_deadline,e.documented_node_capacity_topology))
        return STATUS_FULL if full else STATUS_ARRIVAL
    if e.observed_execution_start and e.observed_cpu_resource_field:
        return STATUS_PLACEMENT
    return STATUS_REJECTED

def evaluate(candidates=CANDIDATES):
    if len({x.dataset_id for x in candidates})!=len(candidates):
        raise ValueError("duplicate candidate id")
    rows=[]
    for e in candidates:
        status=classify(e)
        assert status==STATUS_DOCUMENTATION and e.original_rows_audited==0
        missing=[]
        if not e.dataset_license_confirmed:missing.append("verify dataset redistribution/usage rights")
        if not e.observed_submit_time:missing.append("verify original submission not execution start")
        if not e.observed_cpu_work_physical_units:missing.append("derive valid measured CPU work units or explicitly limit resource-only replay")
        if not e.observed_per_task_network_mb:missing.append("obtain real per-task network input/output, not normalized machine usage")
        if not e.observed_task_relative_deadline:missing.append("find observed task deadline, otherwise only synthetic SLO experiments")
        if not e.documented_node_capacity_topology:missing.append("identify machine capacities and topology map")
        missing.append("acquire legitimate original rows, immutable checksum, unit and missingness audit")
        rows.append(dict(dataset_id=e.dataset_id,status=status,
             observed_actual_workload_rows=0,source_metadata_only=True,
             licensing=e.dataset_license_text,official_url=e.official_url,
             docs_url=e.docs_url,missing_requirements=missing))
    return dict(status="PASS",
        task="SOURCE_METADATA_ONLY_NO_RAW_DATA_ACQUISITION",
        real_workload_dispatch_benchmark_admitted=False,
        real_experimental_rows_examined=0,
        dataset_candidates=rows,
        original_stage65_independent_safety="FAIL",
        original_java_python_cross_runtime_parity="FAIL",
        new_algorithms_evaluated=0,
        original_stage65_source_seeds_reused=0)

if __name__=="__main__":
    out=evaluate()
    print("JPDC_STAGE69_DATA_ADMISSION",json.dumps(out,sort_keys=True,allow_nan=False))
    print("JPDC_STAGE69_SOURCE_METADATA_FAIL_CLOSED_PASS")
