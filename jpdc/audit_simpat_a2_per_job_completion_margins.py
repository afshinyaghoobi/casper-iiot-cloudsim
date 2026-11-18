#!/usr/bin/env python3
"""POSTHOC per-Cloudlet completion and deadline margin check of ORIGINAL native A2.
This script does NOT run CloudSim, assert an implementation defect, or make
causal/sampled-generalization claims. All clocks use milliseconds as logged.
"""
import argparse,csv,hashlib,json,statistics
from pathlib import Path
from collections import defaultdict
SHA_ORIGINAL_LOG="9fb08d07fe9741772b0de59a837046d0152362d3724da04daf02ccbc3d879391"
SHA_ORIGINAL_ZIP="1d29943e5e48d27f65eed186df23ff22d3dd7bdab381ebe63fca88dba1e3bb4b"
FIELDS=["case","job_id","submit_ms","native_finish_ms","fifo_finish_ms","native_wait_ms",
"fifo_wait_ms","requested_service_ms","native_reported_execution_ms","completion_delta_ms",
"wait_delta_ms","native_margin25_ms","fifo_margin25_ms","disagree25",
"native_margin50_ms","fifo_margin50_ms","disagree50"]
def run(native,casefile,outdir):
    assert hashlib.sha256(native.read_bytes()).hexdigest()==SHA_ORIGINAL_LOG, "Wrong original log"
    groups=defaultdict(lambda:{"sub":[],"fin":{},"done":0})
    for line in native.read_text().splitlines():
        if not line.startswith("A2_"): continue
        row=next(csv.reader([line]));kind,name=row[:2];g=groups[name]
        if kind=="A2_SUBMIT" and row[2]=="AFTER":
            g["sub"].append((int(row[4]),float(row[3])))
        elif kind=="A2_FINISH":
            job=int(row[2]); assert job==int(row[3]) and job not in g["fin"]
            g["fin"][job]=tuple(float(x) for x in row[4:])
        elif kind=="A2_DONE":
            assert row[2]=="12";g["done"]+=1
    assert len(groups)==24
    rows=[]
    for name,g in sorted(groups.items()):
        assert len(g["sub"])==12 and len(g["fin"])==12 and g["done"]==1
        assert sorted(i for i,t in g["sub"])==list(range(12))
        m=int(name.rsplit("_P",1)[1]); assert m in (1,2)
        free=[g["sub"][0][1]]*m
        for job,t in g["sub"]:
            nf,nw,ns,nominal,requested=g["fin"][job]
            server=min(range(m),key=lambda k:(free[k],k))
            start=max(t,free[server]);ff=start+requested;free[server]=ff
            fw=start-t
            rec={"case":name,"job_id":job,"submit_ms":t,"native_finish_ms":nf,
                 "fifo_finish_ms":ff,"native_wait_ms":nw,"fifo_wait_ms":fw,
                 "requested_service_ms":requested,"native_reported_execution_ms":ns,
                 "completion_delta_ms":nf-ff,"wait_delta_ms":nw-fw}
            for margin in (25,50):
                n=nf-(t+margin);f=ff-(t+margin)
                rec[f"native_margin{margin}_ms"]=n
                rec[f"fifo_margin{margin}_ms"]=f
                rec[f"disagree{margin}"]=int((n>1e-8)!=(f>1e-8))
                # algebraic identity, not an independent scientific discovery
                assert abs((n-f)-rec["completion_delta_ms"])<1e-7
            rows.append(rec)
    assert len(rows)==288
    source={r["case"]:r for r in csv.DictReader(casefile.open(newline=""))}
    assert len(source)==24
    for case in groups:
        z=[r for r in rows if r["case"]==case];original=source[case]
        assert abs(max(abs(r["wait_delta_ms"]) for r in z)-
            float(original["max_abs_native_minus_requested_fifo_wait_ms"]))<1e-6
        for margin in (25,50):
            assert sum(r[f"disagree{margin}"] for r in z)==int(original[f"deadline{margin}_model_disagreements"])
    assert sum(r["disagree25"] for r in rows)==86
    assert sum(r["disagree50"] for r in rows)==107
    assert abs(statistics.mean(abs(r["wait_delta_ms"]) for r in rows)-49.0960972223)<1e-8
    def caseexample(name):
        z=sorted((r for r in rows if r["case"]==name),key=lambda x:x["job_id"])
        assert len(z)==12
        return {"case":name,
          "max_abs_wait_gap_ms":round(max(abs(x["wait_delta_ms"]) for x in z),3),
          "deadline25_disagreements":sum(x["disagree25"] for x in z),
          "jobs_disagree25":[
              {"job_id":x["job_id"],"native_margin25_ms":round(x["native_margin25_ms"],3),
               "fifo_margin25_ms":round(x["fifo_margin25_ms"],3),
               "completion_delta_ms":round(x["completion_delta_ms"],3)}
              for x in z if x["disagree25"]]}
    examples=[caseexample("BURSTY_S0_1US_P1"),caseexample("BURSTY_S0_1US_P2")]
    assert len(examples[0]["jobs_disagree25"])==1
    assert len(examples[1]["jobs_disagree25"])==5
    by_pe={}
    for p in (1,2):
        z=[r for r in rows if r["case"].endswith("_P"+str(p))]
        by_pe[str(p)]={"jobs":len(z),
            "mean_abs_wait_difference_ms":round(statistics.mean(abs(x["wait_delta_ms"]) for x in z),6),
            "mean_abs_completion_difference_ms":round(statistics.mean(abs(x["completion_delta_ms"]) for x in z),6),
            "deadline25_disagreements":sum(x["disagree25"] for x in z),
            "deadline50_disagreements":sum(x["disagree50"] for x in z)}
    assert by_pe["1"]["deadline25_disagreements"]==27
    assert by_pe["2"]["deadline25_disagreements"]==59
    assert by_pe["1"]["deadline50_disagreements"]==49
    assert by_pe["2"]["deadline50_disagreements"]==58
    signed={}
    for margin in (25,50):
        z=[r for r in rows if r[f"disagree{margin}"]]
        signed[str(margin)]={"disagreements":len(z),
         "native_completes_later_than_fifo":sum(r["completion_delta_ms"]>0 for r in z),
         "native_completes_earlier_than_fifo":sum(r["completion_delta_ms"]<0 for r in z)}
    assert signed["25"]=={"disagreements":86,"native_completes_later_than_fifo":73,
                          "native_completes_earlier_than_fifo":13}
    assert signed["50"]=={"disagreements":107,"native_completes_later_than_fifo":102,
                          "native_completes_earlier_than_fifo":5}
    outdir.mkdir(parents=True,exist_ok=True)
    with (outdir/"a2_per_job_completion_margins.csv").open("w",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=FIELDS);writer.writeheader()
        writer.writerows({k:("%.9f"%v if isinstance(v,float) else v) for k,v in x.items()}
                         for x in sorted(rows,key=lambda r:(r["case"],r["job_id"])))
    result={
        "status":"PASS_VERIFIED_POSTHOC_PER_JOB_COMPLETION_MARGIN_DIAGNOSTIC",
        "source_native_log_sha256":SHA_ORIGINAL_LOG,
        "source_case_csv_sha256":hashlib.sha256(casefile.read_bytes()).hexdigest(),
        "cases":24,"jobs":288,"fixed_thresholds_ms":[25,50],
        "by_vm_pe":by_pe,"signed_disagreement_direction":signed,
        "two_case_example":examples,
        "classification_identity":"disagree iff native and FIFO completion margins lie on opposite sides of the synthetic threshold (strict > with 1e-8 tolerance)",
        "analysis_is_posthoc":True,"new_java_simulation":False,
        "causal_claim_or_real_iot_validation":False,
        "original_30k_crossruntime_parity":"FAIL","original_stage65_safety":"FAIL"}
    (outdir/"a2_per_job_completion_margin_audit.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--native",type=Path,required=True)
    ap.add_argument("--cases",type=Path,required=True)
    ap.add_argument("--outdir",type=Path,required=True)
    a=ap.parse_args();run(a.native,a.cases,a.outdir)
