#!/usr/bin/env python3
"""Stage18 static-only forensic from exact Maven 8.5.7 source archive.

Outputs exact extracted numbered lines and SHA-256 to make claims auditable.
Does not invoke any simulation, read future physical state, or modify library.
"""
import argparse,hashlib,json,re,zipfile
from pathlib import Path
CLASSES=("CloudletSchedulerSpaceShared.java","CloudletSchedulerAbstract.java")
KEYS=("cloudletSubmitInternal","canExecuteCloudletInternal","updateProcessing",
      "moveNextCloudletsFromWaitingToExecList","addCloudletToWaitingList",
      "getCloudletWaitingList","getCloudletExecList",
      "moveNextCloudlets","resume","cloudletSubmit")
def numbered(lines,first,last):
    return "\n".join(f"{i+1:5d} {lines[i]}" for i in range(max(0,first),min(len(lines),last)))
def run(source):
    blob=Path(source).read_bytes()
    with zipfile.ZipFile(source) as z:
        names=z.namelist()
        entries={}
        for cls in CLASSES:
            matches=[p for p in names if p.endswith("/"+cls)]
            if len(matches)!=1:raise AssertionError(("expected one exact source",cls,matches))
            path=matches[0]
            contents=z.read(path)
            lines=contents.decode("utf-8").splitlines()
            hits=[i for i,l in enumerate(lines) if any(re.search(r"\b"+re.escape(k)+r"\b",l) for k in KEYS)]
            # Keep bounded context of each literal reference, including calls.
            windows=[]
            for i in hits:
                lo=max(0,i-9);hi=min(len(lines),i+19)
                if windows and lo<=windows[-1][1]:
                    windows[-1]=(windows[-1][0],max(windows[-1][1],hi))
                else:windows.append((lo,hi))
            entries[cls]=dict(source_path=path,source_sha256=hashlib.sha256(contents).hexdigest(),
                              line_count=len(lines),
                              matched_source_lines=[i+1 for i in hits],
                              excerpts=[dict(start=a+1,end=b,numbered_source=numbered(lines,a,b))
                                        for a,b in windows])
        return dict(status="PASS",library="org.cloudsimplus:cloudsimplus:8.5.7:sources",
                    archive_sha256=hashlib.sha256(blob).hexdigest(),classes=entries,
                    scope="static library code path, not observed event cause or achieved FCFS parity")
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--sources",required=True);p.add_argument("--out",required=True)
    a=p.parse_args();r=run(a.sources)
    dest=Path(a.out);dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(r,sort_keys=True,indent=2,ensure_ascii=False)+"\n")
    for cls,data in r["classes"].items():
        print("STAGE18_SOURCE_CLASS",cls,"line_count",data["line_count"],
              "hit_count",len(data["matched_source_lines"]),
              "source_sha256",data["source_sha256"])
        for item in data["excerpts"]:
            print("STAGE18_SOURCE_EXCERPT",cls,item["start"],item["end"])
            print(item["numbered_source"])
    print("JPDC_STAGE18_CLOUDSIM_857_SOURCE_EXTRACTION_PASS")
