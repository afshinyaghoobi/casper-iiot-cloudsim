#!/usr/bin/env python3
"""Read-only post-inspection structural check for original CloudSimPlus 8.5.7.

This test is a CORROBORATIVE static source analysis, not preregistered blind
validation, executable event replay or new Java simulation.
"""
import argparse,json,re
from pathlib import Path

def all_lines(cls):
    arr={}
    for ex in cls["excerpts"]:
        for line in ex["numbered_source"].splitlines():
            m=re.match(r"\s*(\d+) (.*)$",line)
            if m:arr[int(m.group(1))]=m.group(2)
    return arr

def check(path):
    src=json.loads(Path(path).read_text())
    assert src["status"]=="PASS" and src["library"]=="org.cloudsimplus:cloudsimplus:8.5.7:sources"
    lines={k:all_lines(v) for k,v in src["classes"].items()}
    a=lines["CloudletSchedulerAbstract.java"]
    s=lines["CloudletSchedulerSpaceShared.java"]
    # Pin checks to observed version and known source-line method context.
    submit="\n".join(a[i] for i in range(247,260))
    if "if (canExecuteCloudlet(cle))" not in submit:
        raise AssertionError("incoming cloudlet direct-admission guard not found")
    if "addCloudletToExecList(cle);" not in submit:
        raise AssertionError("direct execution admission not found")
    if "addCloudletToWaitingList(cle);" not in submit:
        raise AssertionError("fallback queue action not found")
    # No source-visible waiting-list-empty / older-queue priority condition in
    # the direct-admission guard. This does NOT rule out an indirect method check.
    guard=submit.split("if (canExecuteCloudlet(cle))",1)[1].split("addCloudletToExecList(cle);",1)[0]
    if "cloudletWaitingList" in guard or "getCloudletWaitingList" in guard:
        raise AssertionError("direct branch unexpectedly references queued tasks")
    checkspace="\n".join(s[i] for i in range(95,99))
    if "return isThereEnoughFreePesForCloudlet(cle);" not in checkspace:
        raise AssertionError("SpaceShared PE-based capability rule missing")
    update="\n".join(a[i] for i in range(477,496))
    if "moveNextCloudletsFromWaitingToExecList(currentTime)" not in update:
        raise AssertionError("waiting-list drain not called during update")
    drain="\n".join(a[i] for i in range(910,924))
    if "cloudletWaitingList.isEmpty()" not in drain or "findSuitableWaitingCloudlet()" not in drain:
        raise AssertionError("separate waiting queue drain not found")
    return dict(status="PASS",version=src["library"],archive_sha256=src["archive_sha256"],
        direct_admission="CloudletSchedulerAbstract.java:247-258",
        branch_guard="canExecuteCloudlet(cle)",
        explicit_waiting_list_priority_check_in_direct_branch=False,
        capacity_rule="CloudletSchedulerSpaceShared.java:95-98",
        wait_drain_call="CloudletSchedulerAbstract.java:477-494",
        wait_drain_method="CloudletSchedulerAbstract.java:910-923",
        interpretation="Two distinct admission paths can permit bypass when there is a waiting job and the new submit sees free PEs.",
        unproven="The precise event timeline which left older node14 task waiting when a PE was free is not established.",
        original_fcfs_fidelity="FAIL max wait error 9.12140093294972ms >5ms registered gate")
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--original",required=True);p.add_argument("--out",required=True)
    z=p.parse_args()
    result=check(z.original)
    out=Path(z.out);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("JPDC_STAGE18_SOURCE_IMPLEMENTATION_PATH_STATIC_CHECK_PASS")
    print(json.dumps(result,sort_keys=True))
