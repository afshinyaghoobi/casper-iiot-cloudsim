#!/usr/bin/env python3
"""A1 original 8.5.7 six-case preregistered observational/rescan intervention audit.

The intervention is BUNDLED: added post-update wait-promotion invocation plus
possible earlier next-event scheduling. No physical IoT validation or library bug.
"""
import argparse,collections,csv,json,hashlib
from pathlib import Path
CASES=("EARLY4_1US","EARLY4_5MS","ORIGINAL_1US","ORIGINAL_5MS","LATE10_1US","LATE10_5MS")
POSITIVES=("ORIGINAL_5MS","LATE10_5MS")
def parse(path):
    grouped=collections.defaultdict(lambda:{"submit":[],"outcomes":{},"rescan":[],"done":[]})
    for line in path.read_text().splitlines():
        if not(line.startswith(("ARRIVALTRACE_","SIMPAT_INTERVENTION,","JPDC_ARRIVALTRACE_"))):continue
        row=next(csv.reader([line]))
        if row[0]=="JPDC_ARRIVALTRACE_NATIVE_SIX_CASES_COMPLETE":continue
        if row[0]=="ARRIVALTRACE_CASE":continue
        if len(row)<2:continue
        name=row[1]
        assert name in CASES,(row[0],name)
        g=grouped[name]
        if row[0]=="ARRIVALTRACE_SUBMIT":
            g["submit"].append(row)
        elif row[0]=="ARRIVALTRACE_OUTCOME":
            idx=int(row[2]);assert idx not in g["outcomes"];g["outcomes"][idx]=row
        elif row[0]=="ARRIVALTRACE_CASE_DONE":
            g["done"].append(row)
        elif row[0]=="SIMPAT_INTERVENTION":
            g["rescan"].append(row)
    assert tuple(sorted(grouped))==tuple(sorted(CASES))
    for case,g in grouped.items():
        assert set(g["outcomes"])=={0,1,2}
        assert len(g["done"])==1
        assert g["done"][0][2:]==["submissions=3","finishes=3"]
    return grouped
def bypass(g):
    before=[row for row in g["submit"] if row[2]=="BEFORE" and row[4]=="2"]
    after=[row for row in g["submit"] if row[2]=="AFTER" and row[4]=="2"]
    assert len(before)==len(after)==1
    b,a=before[0],after[0]
    return (b[5]=="" and b[6]=="1" and a[5]=="2" and a[6]=="1")
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--original",type=Path,required=True)
    ap.add_argument("--control",type=Path,required=True)
    ap.add_argument("--treatment",type=Path,required=True)
    ap.add_argument("--out",type=Path,required=True)
    args=ap.parse_args()
    original=args.original.read_bytes();control=args.control.read_bytes()
    assert original==control,"CONTROL is not byte-identical to original completed six-case run!"
    original_records=parse(args.control); treated_records=parse(args.treatment)
    results=[]
    for case in CASES:
        c=original_records[case];t=treated_records[case]
        c_bypass=bypass(c);t_bypass=bypass(t)
        assert c_bypass==(case in POSITIVES),("not original fixture",case)
        deltas=[]
        for job in range(3):
            a=c["outcomes"][job];z=t["outcomes"][job]
            assert a[2:4]==z[2:4]
            deltas.append({"job_id":job,
               "control_wait_ms":float(a[4]),"treated_wait_ms":float(z[4]),
               "control_reported_service_ms":float(a[5]),"treated_reported_service_ms":float(z[5]),
               "wait_delta_ms":round(float(z[4])-float(a[4]),9),
               "reported_service_delta_ms":round(float(z[5])-float(a[5]),9)})
        rescan_observed=[]
        for row in t["rescan"]:
            # row: SIMPAT_INTERVENTION,name,clock,execbefore,waitbefore,execafter,waitafter,next,extra,chosen
            assert row[3]=="" and row[4]!=""
            rescan_observed.append({"clock_ms":float(row[2]),"wait_before":row[4],
                "exec_after":row[5],"wait_after":row[6],
                "original_next":float(row[7]),"extra_next":float(row[8]),"returned_next":float(row[9])})
        results.append({"case":case,
           "old_wait_young_exec_original":c_bypass,
           "old_wait_young_exec_treatment":t_bypass,
           "post_update_rescan_calls":len(rescan_observed),
           "post_update_rescan_moves_old_job1":any("1" in e["wait_before"].split(";") and "1" not in e["wait_after"].split(";") and "1" in e["exec_after"].split(";") for e in rescan_observed),
           "rescan_records":rescan_observed,
           "per_job_outcomes":deltas})
    positives=[x for x in results if x["case"] in POSITIVES]
    negatives=[x for x in results if x["case"] not in POSITIVES]
    result={
       "status":"PASS_SOURCE_VERIFIED_A1_PREREGISTERED_BUNDLED_RESCAN_INTERVENTION",
       "original_six_case_control_exact_bytes":True,"cases":6,"jobs_per_arm":18,
       "original_positive_cases":list(POSITIVES),
       "positive_cases_losing_old_wait_young_exec":[x["case"] for x in positives if not x["old_wait_young_exec_treatment"]],
       "positive_cases_preserving_old_wait_young_exec":[x["case"] for x in positives if x["old_wait_young_exec_treatment"]],
       "negative_cases_newly_showing_bypass":[x["case"] for x in negatives if x["old_wait_young_exec_treatment"]],
       "total_rescan_calls":sum(x["post_update_rescan_calls"] for x in results),
       "rescan_calls_with_recorded_job1_promotion":sum(x["post_update_rescan_moves_old_job1"] for x in results),
       "cases":results,
       "original_log_sha256":hashlib.sha256(original).hexdigest(),
       "treated_log_sha256":hashlib.sha256(args.treatment.read_bytes()).hexdigest(),
       "treatment_changes_future_event_scheduling_possible":True,
       "identifies_single_internal_cause":False,
       "library_defect_or_physical_cpu_claim":False,
       "research_input_fixtures_were_known_before_prereg":True,
       "original_strict_cross_runtime_parity":"FAIL","stage65_safety":"FAIL"}
    args.out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k!="cases"},indent=2,sort_keys=True))
if __name__=="__main__":main()
