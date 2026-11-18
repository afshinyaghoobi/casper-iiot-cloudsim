#!/usr/bin/env python3
"""A3 passive clock-origin correction of original A2 reference using same frozen workloads.
The study is an explicitly labeled posthoc measurement-construct sensitivity.
"""
import argparse,csv,json,math
from pathlib import Path
P=(8,13,5,19,7,11,17,6,14,9,16,10)
def main():
 p=argparse.ArgumentParser()
 p.add_argument("--instrumented",required=True);p.add_argument("--original-a2",required=True)
 p.add_argument("--out",required=True)
 args=p.parse_args()
 orig=Path(args.original_a2).read_text().splitlines()
 instrumented=Path(args.instrumented).read_text().splitlines()
 stripped=[s for s in instrumented if not s.startswith("A3_CLOCK,")]
 if stripped != orig:
  raise ValueError("A3 instrumentation changed original A2 event outputs")
 a={};nclock=0
 for s in instrumented:
  if not s.startswith(("A2_","A3_")):continue
  row=next(csv.reader([s]));tag,name=row[:2]
  d=a.setdefault(name,{"submit":[],"finish":{},"clock":{},"done":0})
  if tag=="A2_SUBMIT" and row[2]=="AFTER":d["submit"].append((int(row[4]),float(row[3])))
  elif tag=="A2_FINISH":
   j=int(row[2]);d["finish"][j]=dict(zip(("fin","wait","exec","nominal","requested"),(float(x) for x in row[4:])))
  elif tag=="A3_CLOCK":
   if len(row)!=7:raise ValueError("A3 clock columns invalid")
   j=int(row[2]);d["clock"][j]=dict(zip(("dc","start","wait","fin"),(float(x) for x in row[3:])))
   nclock+=1
  elif tag=="A2_DONE":
   if row[2]!="12":raise ValueError("not all done")
   d["done"]+=1
 if len(a)!=24 or nclock!=288:raise ValueError("incomplete 24-case clock trace")
 cells=[]
 for name,d in sorted(a.items()):
  if d["done"]!=1 or len(d["submit"])!=12 or len(d["finish"])!=12 or len(d["clock"])!=12:raise ValueError("bad case "+name)
  pes=int(name.rsplit("_P",1)[1]);free=[d["submit"][0][1]]*pes
  max_wait_native=0;max_wait_submit_based=0;origin=[]
  nnonzero=0;errors=[]
  deadline_n=deadline_ref=disagree=0
  for j,t in d["submit"]:
   f=d["finish"][j];c=d["clock"][j]
   if not all(map(math.isfinite,[t,*f.values(),*c.values()])):raise ValueError("not finite")
   if abs(f["requested"]-P[j])>1e-6:raise ValueError("service mismatch")
   if abs(c["start"]-c["dc"]-c["wait"])>1e-5:raise ValueError("source waiting identity broken")
   if abs(c["wait"]-f["wait"])>1e-6:raise ValueError("cloudlet waiting mismatch")
   if abs(c["fin"]-f["fin"])>1e-6:raise ValueError("final time mismatched")
   origin.append(c["dc"]-t)
   nnonzero+=int(abs(c["dc"]-t)>1e-6)
   s=min(range(pes),key=lambda i:(free[i],i))
   start_ref=max(t,free[s])
   wait_ref=start_ref-t
   free[s]=start_ref+P[j]
   max_wait_native=max(max_wait_native,abs(f["wait"]-wait_ref))
   corrected=c["start"]-t
   max_wait_submit_based=max(max_wait_submit_based,abs(corrected-wait_ref))
   errors.append((f["wait"]-wait_ref,corrected-wait_ref,c["dc"]-t))
  cells.append({"case":name,"max_abs_native_reported_wait_minus_fifo_ms":round(max_wait_native,9),
    "max_abs_submit_to_native_start_minus_fifo_ms":round(max_wait_submit_based,9),
    "count_datacenter_arrival_differs_from_scheduler_submit":nnonzero,
    "max_abs_dc_arrival_minus_submit_ms":round(max(abs(x) for x in origin),9),
    "mean_signed_dc_arrival_minus_submit_ms":round(sum(origin)/12,9)})
 out={"status":"PASS_MEASUREMENT_CONSTRUCT_DIAGNOSTIC","all_cases":24,"jobs":288,
     "original_a2_trace_byte_identical_without_added_clock_rows":True,
     "different_dc_arrival_vs_submit_jobs":sum(x["count_datacenter_arrival_differs_from_scheduler_submit"] for x in cells),
     "max_abs_native_wait_minus_fifo_ms":max(x["max_abs_native_reported_wait_minus_fifo_ms"] for x in cells),
     "max_abs_submit_to_start_minus_fifo_ms":max(x["max_abs_submit_to_native_start_minus_fifo_ms"] for x in cells),
     "max_abs_dc_arrival_minus_submit_ms":max(x["max_abs_dc_arrival_minus_submit_ms"] for x in cells),
     "source_version":"8.5.7","original_30k_fidelity":"FAIL","stage65_safety":"FAIL","cells":cells}
 Path(args.out).write_text(json.dumps(out,sort_keys=True,indent=2)+"\n")
 print("JPDC_A3_NATIVE_CLOCK_ORIGIN_CHECK",json.dumps({k:v for k,v in out.items() if k!="cells"},sort_keys=True))
if __name__=="__main__":main()
