#!/usr/bin/env python3
"""Independent read-only source Stage27 algebra and tail forensic.

Original immutable artifact only. No simulation, source truth, or re-selection.
"""
import argparse,json,math
from collections import Counter
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("--original",required=True);p.add_argument("--out",required=True);a=p.parse_args()
x=json.loads(Path(a.original).read_text())
assert x["status"]=="PASS" and x["scientific_seed"]==90
assert len(x["rows"])==4 and x["dependent_task_policy_observations"]==48000
results=[]
for arm in x["rows"]:
    records=arm["trace"]
    meta=arm["stats"]
    assert len(records)==12000 and meta["stage6_exact_parity"]
    classes={}
    for period,label in (([r for r in records if r["task_index"]<10000],"pre"),
                         ([r for r in records if r["task_index"]>=10000],"post")):
        assert len(period)==(10000 if label=="pre" else 2000)
        count={name:Counter() for name in ("NORMAL","HIGH","MISSION")}
        largest=[]
        for r in period:
            actual_cpu=r["delivered_cpu_finish_ms"]-r["actual_start_ms"]
            wait=r["actual_start_ms"]-r["arrival_ms"]
            pred_cpu=r["predicted_cpu_at_dispatch_ms"]
            pred_wait=r["predicted_wait_at_dispatch_ms"]
            assert abs(actual_cpu-r["actual_cpu_ms"])<1e-8
            assert abs(wait-r["actual_wait_ms"])<1e-8
            assert abs((actual_cpu-pred_cpu)-r["signed_cpu_residual_ms"])<1e-8
            assert abs((wait-pred_wait)-r["signed_wait_residual_ms"])<1e-8
            assert abs((r["delivered_cpu_finish_ms"]-r["arrival_ms"])-(pred_wait+pred_cpu)-r["signed_nonnetwork_residual_ms"])<1e-8
            assert abs(r["signed_wait_residual_ms"]+r["signed_cpu_residual_ms"]-r["signed_nonnetwork_residual_ms"])<1e-8
            cls=r["task_class"];assert cls in count
            count[cls]["n"]+=1
            for component in ("signed_wait_residual_ms","signed_cpu_residual_ms","signed_nonnetwork_residual_ms"):
                count[cls][component+"_abs_over_10ms"]+=int(abs(r[component])>10)
            largest.append((abs(r["signed_nonnetwork_residual_ms"]),r["task_index"],
                            r["node"],cls,r["signed_wait_residual_ms"],r["signed_cpu_residual_ms"],
                            r["signed_nonnetwork_residual_ms"]))
        largest.sort(reverse=True)
        classes[label]=dict(n=len(period),
            by_task_class={name:dict(v) for name,v in count.items()},
            top_five_absolute_nonnetwork_outliers=[
                dict(abs_error_ms=z[0],task_index=z[1],node=z[2],
                     task_class=z[3],wait_error_ms=z[4],cpu_error_ms=z[5],total_error_ms=z[6])
                for z in largest[:5]])
    result=dict(scenario=meta["scenario"],policy=meta["policy"],periods=classes,
                exact_nonnetwork_decomposition_for_12000=True)
    results.append(result)
    print("STAGE27_IMMUTABLE_OUTLIER_SUMMARY",json.dumps(result,sort_keys=True),flush=True)
out=dict(status="PASS",original_run=42269844289,scientific_units=1,
         caveat="one DEVELOPMENT source seed; outliers describe actual simulator labels, not predictable certificates",
         results=results)
dst=Path(a.out);dst.parent.mkdir(parents=True,exist_ok=True)
dst.write_text(json.dumps(out,sort_keys=True,indent=2,allow_nan=False)+"\n")
print("JPDC_STAGE27_IMMUTABLE_NONNETWORK_DECOMPOSITION_AUDIT_PASS")
