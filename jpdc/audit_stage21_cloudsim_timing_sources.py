#!/usr/bin/env python3
"""Exact CloudSimPlus v8.5.7 Maven source scanner, no simulator execution."""
import argparse,hashlib,json,re,zipfile
from pathlib import Path
TERMS=("0.01","MIN_TIME_BETWEEN_EVENTS","minTimeBetweenEvents","getMinTimeBetweenEvents",
       "schedulingInterval","getSchedulingInterval","updateCloudletProcessing",
       "updateProcessing","CLOUDLET_UPDATE","VM_UPDATE","getTotalExecutionTime",
       "nextSimulationDelay","scheduleEvent","CLOUDLET_SUBMIT")
IMPORTANT=("DatacenterAbstract.java","DatacenterSimple.java","VmAbstract.java",
           "CloudletSchedulerAbstract.java","CloudSimPlus.java","DatacenterBrokerAbstract.java",
           "CloudSim.java","CloudletExecution.java")
def scan(zipfile_path):
    blob=Path(zipfile_path).read_bytes()
    digest=hashlib.sha256(blob).hexdigest()
    assert digest=="8d3efcacfc661b2f1e018e279761fc4ae1e5584a770b2022d20930568688966c",digest
    hits=[]
    with zipfile.ZipFile(zipfile_path) as archive:
        for path in archive.namelist():
            if not path.endswith(".java") or "/test/" in path or "/examples/" in path:continue
            lines=archive.read(path).decode("utf-8").splitlines()
            where=[]
            for i,line in enumerate(lines):
                terms=[t for t in TERMS if t.lower() in line.lower()]
                if terms:where.append((i,terms))
            if not where:continue
            imp=any(path.endswith("/"+b) for b in IMPORTANT)
            slices=[]
            for i,terms in where:
                if not imp:continue
                lo=max(0,i-4);hi=min(len(lines),i+8)
                excerpt="\n".join(f"{j+1:5d} {lines[j]}" for j in range(lo,hi))
                slices.append(dict(line=i+1,terms=terms,source=excerpt))
            hits.append(dict(path=path,important=imp,line_count=len(lines),
                             matches=[dict(line=i+1,terms=terms,text=lines[i].strip()) for i,terms in where],
                             important_source_excerpts=slices))
    hits.sort(key=lambda x:(not x["important"],x["path"]))
    return dict(status="PASS",archive_sha256=digest,files_scanned_with_matches=len(hits),
                important_source_files=[x for x in hits if x["important"]],
                additional_matches=[dict(path=x["path"],matches=x["matches"]) for x in hits if not x["important"]],
                limitations="Text scan only, no reachable call-path or clock causality proven")
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--sources",required=True);p.add_argument("--out",required=True)
    a=p.parse_args();x=scan(a.sources)
    dest=Path(a.out);dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
    print("STAGE21_TOTAL_SOURCE_MATCH_FILES",x["files_scanned_with_matches"])
    for item in x["important_source_files"]:
        print("STAGE21_IMPORTANT_FILE",item["path"],"hits",len(item["matches"]))
        for m in item["matches"]:
            print("STAGE21_SOURCE_HIT",item["path"],m["line"],",".join(m["terms"]),m["text"][:240])
    for item in x["additional_matches"]:
        if any("0.01" in m["terms"] or "MIN_TIME_BETWEEN_EVENTS" in m["terms"] for m in item["matches"]):
            for m in item["matches"]:
                if "0.01" in m["terms"] or "MIN_TIME_BETWEEN_EVENTS" in m["terms"]:
                    print("STAGE21_OTHER_CADENCE_HIT",item["path"],m["line"],m["text"][:240])
    print("JPDC_STAGE21_EXACT_CLOUDSIM_SOURCE_SCAN_PASS")
