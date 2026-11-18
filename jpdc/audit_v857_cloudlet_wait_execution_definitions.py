#!/usr/bin/env python3
"""Exact publisher CloudSimPlus 8.5.7 source extraction: lexical definition audit only.
No claims about dynamic code path or runtime semantics from static source text.
"""
import argparse,hashlib,json,re,zipfile
from pathlib import Path

TARGETS={
"org/cloudsimplus/cloudlets/CloudletAbstract.java":[r'getStartWaitTime\s*\(',r'getDcArrivalTime\s*\(',r'getExecStartTime\s*\('],
"org/cloudsimplus/cloudlets/CloudletExecution.java":[r'getActualCpuTime\s*\(',r'getCloudletArrivalTime\s*\(',r'getCloudlet\s*\('],
"org/cloudsimplus/core/ExecDelayableAbstract.java":[r'getTotalExecutionTime\s*\(',r'getStartTime\s*\(',r'getFinishTime\s*\('],
"org/cloudsimplus/schedulers/cloudlet/CloudletSchedulerAbstract.java":[r'cloudletSubmitInternal\s*\(',r'updateProcessing\s*\(',r'moveNextCloudletsFromWaitingToExecList\s*\('],
}
EXPECTED_SHA="8d3efcacfc661b2f1e018e279761fc4ae1e5584a770b2022d20930568688966c"
def main():
 p=argparse.ArgumentParser();p.add_argument("--sources",required=True);p.add_argument("--out",required=True)
 args=p.parse_args()
 jar=Path(args.sources)
 actual=hashlib.sha256(jar.read_bytes()).hexdigest()
 if actual!=EXPECTED_SHA:raise ValueError("Publisher sources JAR SHA256 mismatch")
 output={"artifact":"org.cloudsimplus:cloudsimplus:8.5.7:sources","jar_sha256":actual,
         "status":"SOURCE_ONLY_REVIEW","dynamic_branch_trace":False,"files":[]}
 with zipfile.ZipFile(jar) as z:
  paths=set(z.namelist())
  for name,patterns in TARGETS.items():
   if name not in paths: raise ValueError("missing publisher source "+name)
   lines=z.read(name).decode("utf-8").splitlines()
   entries=[]
   for term in patterns:
    hits=[]
    for ix,line in enumerate(lines):
     if re.search(term,line) and not line.strip().startswith(("import ","//","*")):
      lo=max(0,ix-8);hi=min(len(lines),ix+17)
      hits.append({"line":ix+1,"context":"\n".join(f"{j+1}: {lines[j]}" for j in range(lo,hi))})
    entries.append({"search":term,"hits":hits[:8],"number_of_hits":len(hits)})
   output["files"].append({"path":name,"queries":entries})
 Path(args.out).write_text(json.dumps(output,sort_keys=True,indent=2)+"\n")
 print("JPDC_V857_PUBLISHER_SOURCE_WAIT_EXEC_MEASUREMENT_REVIEW",json.dumps({
 "status":output["status"],"jar_sha256":actual,"files":len(output["files"]),
 "hits":{n["path"]:sum(x["number_of_hits"] for x in n["queries"]) for n in output["files"]}},sort_keys=True))
if __name__=="__main__":main()
