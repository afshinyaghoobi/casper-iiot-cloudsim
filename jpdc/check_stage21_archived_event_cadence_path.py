#!/usr/bin/env python3
"""Corroborative archived-only Stage21 8.5.7 implementation path gate.

This was authored AFTER seeing Stage21 source results: no blind provenance claim.
"""
import argparse,json,re
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("--original",required=True);p.add_argument("--out",required=True)
a=p.parse_args()
x=json.loads(Path(a.original).read_text())
assert x["archive_sha256"]=="8d3efcacfc661b2f1e018e279761fc4ae1e5584a770b2022d20930568688966c"
files={item["path"].split("/")[-1]:item for item in x["important_source_files"]}
assert "DatacenterSimple.java" in files and "CloudletSchedulerAbstract.java" in files
dc=files["DatacenterSimple.java"]
byline={m["line"]:m["text"] for m in dc["matches"]}
checks={
    749:"host.updateProcessing(clock())",
    754:"getSimulation().getMinTimeBetweenEvents()+0.01",
    755:"Math.max(nextSimulationDelay, minTimeBetweenEvents)",
    782:"getCloudletProcessingUpdateInterval(nextSimulationDelay)",
    783:"schedule(nextSimulationDelay, CloudSimTag.VM_UPDATE_CLOUDLET_PROCESSING)"
}
for ln,statement in checks.items():
    if statement not in byline.get(ln,""):
        raise AssertionError(("source code changed or unsupported path",ln,byline.get(ln)))
# Reconfirm this is in the actual library's DatacenterSimple update path, not a random literal
cloudsim=files["CloudSimPlus.java"]
assert any("minTimeBetweenEvents" in k["text"] for k in cloudsim["matches"])
result=dict(status="PASS",source="CloudSimPlus Maven v8.5.7 exact SHA256",
    effective_min_event_seconds=0.010001,
    effective_min_event_ms=10.001,
    path="DatacenterSimple.updateHostsProcessing host update -> max(delay,sim.minTimeBetweenEvents+0.01) -> updateCloudletProcessing schedule",
    source_lines=list(checks),
    observation="Stage20 update timestamps differ by 10.001ms after 1008.100623ms",
    claim_boundary="Explains source-imposed minimum nonzero update delay; does not prove all execution-time accounting or event-order details",
    still_failed="Original strict-FCFS cross-engine max wait 9.12140093294972ms >5ms")
Path(a.out).write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
print("JPDC_STAGE21_ARCHIVED_CADENCE_PATH_CHECK_PASS")
print(json.dumps(result,sort_keys=True))
