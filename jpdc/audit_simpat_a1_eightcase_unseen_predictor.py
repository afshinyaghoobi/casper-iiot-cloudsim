#!/usr/bin/env python3
"""FROZEN 8-case unseen A1 fixture test, source-event predictor without AFTER leakage.

See SIMPAT_A1_EIGHTCASE_UNSEEN_INPUT_PREDICTION_PREREG_2026-11-18.md.
Pure audit of original versioned Java trace, NOT IoT physical validation.
"""
import argparse,csv,collections,hashlib,json
from pathlib import Path

CASES=tuple(f"H_{x}_{g}" for x in "ABCD" for g in ("1US","5MS"))
EXPECTED={
 "H_A":((7.35,5.10,6.65),(0.,4.40,7.42)),
 "H_B":((11.60,3.75,8.20),(0.,6.85,11.71)),
 "H_C":((5.85,6.25,4.90),(0.,3.30,6.17)),
 "H_D":((9.45,7.10,5.40),(0.,5.85,10.05))
}
def ids(s):return set(s.split(";")) if s else set()
def parse(path):
    groups=collections.defaultdict(list)
    full=path.read_text().splitlines()
    assert full[-1]=="JPDC_ARRIVALTRACE_NATIVE_EIGHT_HOLDOUT_COMPLETE"
    for line in full:
        if not line.startswith("ARRIVALTRACE_"):continue
        row=next(csv.reader([line]))
        assert row[1] in CASES, row[:2]
        groups[row[1]].append(row)
    assert set(groups)==set(CASES)
    return groups
def audit(groups):
    summaries=[]
    for name in CASES:
        rows=groups[name]
        fin=[r for r in rows if r[0]=="ARRIVALTRACE_FINISH"]
        outcome=[r for r in rows if r[0]=="ARRIVALTRACE_OUTCOME"]
        done=[r for r in rows if r[0]=="ARRIVALTRACE_CASE_DONE"]
        submissions=[r for r in rows if r[0]=="ARRIVALTRACE_SUBMIT"]
        assert len(fin)==len(outcome)==3 and len(done)==1
        assert len(submissions)==6 and len([r for r in submissions if r[2]=="BEFORE"])==3
        assert done[0][2:]==["submissions=3","finishes=3"]
        family=name[:3]; services,arrivals=EXPECTED[family]
        for o in outcome:
            job=int(o[2]);assert job in (0,1,2)
            assert abs(float(o[6])-arrivals[job])<1e-7
            assert abs(float(o[7])-services[job])<1e-7
        target=[(i,r) for i,r in enumerate(rows)
                if r[0]=="ARRIVALTRACE_SUBMIT" and r[2]=="BEFORE" and r[4]=="2"]
        assert len(target)==1
        sidx,sbefore=target[0]
        safter=next((r for r in rows[sidx+1:]
                    if r[0]=="ARRIVALTRACE_SUBMIT" and r[2]=="AFTER" and r[4]=="2"),None)
        assert safter is not None
        # LABEL: only after admission, never in predictor.
        y=(sbefore[5]=="" and "1" in ids(sbefore[6]) and
            "2" in ids(safter[5]) and "1" in ids(safter[6]))
        # Predictor: ONLY event records occurring before the SUBMIT BEFORE
        # for job2, plus that BEFORE list. No job2 eligibility nor after states.
        predictor=False;latest_past_update=None
        if sbefore[5]=="" and "1" in ids(sbefore[6]):
            for i,r in enumerate(rows[:sidx]):
                if r[0]!="ARRIVALTRACE_UPDATE" or r[2]!="BEFORE":continue
                if "0" not in ids(r[4]) or "1" not in ids(r[5]):continue
                finish=next((k for k in range(i+1,sidx)
                    if rows[k][0]=="ARRIVALTRACE_UPDATE" and rows[k][2]=="AFTER" and rows[k][3]==r[3]),None)
                if finish is None:continue
                mids=rows[i+1:finish]
                promoted_before=any(x[0]=="ARRIVALTRACE_PROMOTION" and x[2]=="BEFORE" and
                    "0" in ids(x[4]) and "1" in ids(x[5]) for x in mids)
                eligfalse=any(x[0]=="ARRIVALTRACE_ELIGIBILITY" and x[3]=="1" and x[4]=="false" for x in mids)
                end=rows[finish]
                if not(promoted_before and eligfalse and end[4]=="" and "1" in ids(end[5])):continue
                # Reject if job1 was removed from WAIT or promoted in the
                # intervening records before job2 is submitted.
                intervening=rows[finish+1:sidx]
                if any(x[0]=="ARRIVALTRACE_PROMOTION" and x[2]=="AFTER"
                       and "1" in ids(x[4]) and "1" not in ids(x[5]) for x in intervening):continue
                latest_past_update=float(r[3]);predictor=True
        summaries.append({"case":name,"event_gap":name.split("_")[-1],
           "predicted_bypass_P":predictor,
           "observed_old_wait_young_exec":y,
           "before_submit_exec":sbefore[5],"before_submit_wait":sbefore[6],
           "new_job_eligibility_used_in_prediction":False,
           "predictor_latest_update_clock_ms":latest_past_update,
           "source_jobs_completed":3})
    confusion={"TP":sum(r["predicted_bypass_P"] and r["observed_old_wait_young_exec"] for r in summaries),
               "FP":sum(r["predicted_bypass_P"] and not r["observed_old_wait_young_exec"] for r in summaries),
               "FN":sum(not r["predicted_bypass_P"] and r["observed_old_wait_young_exec"] for r in summaries),
               "TN":sum(not r["predicted_bypass_P"] and not r["observed_old_wait_young_exec"] for r in summaries)}
    rates={k:sum(r["observed_old_wait_young_exec"] for r in summaries if r["event_gap"]==k) for k in ("1US","5MS")}
    return summaries,confusion,rates
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--log",type=Path,required=True)
    ap.add_argument("--out",type=Path,required=True)
    x=ap.parse_args()
    result,confusion,rates=audit(parse(x.log))
    assert len(result)==8 and all(r["source_jobs_completed"]==3 for r in result)
    output={
     "status":"PASS_UNSEEN_EIGHT_INPUT_TRACE_AUDIT",
     "frozen_input_prereg":"SIMPAT_A1_EIGHTCASE_UNSEEN_INPUT_PREDICTION_PREREG_2026-11-18.md",
     "exact_version":"CloudSimPlus 8.5.7","independently_configured_synthetic_fixtures":8,
     "jobs_completed":24,"confusion_pre_submit_event_predicate":confusion,
     "source_only_prediction_numerically_scoped":True,
     "positive_P_sufficiency_counterexamples":confusion["FP"],
     "P_negative_bypass_coverage_counterexamples":confusion["FN"],
     "input_only_gap_counts":rates,
     "weak_input_H_5MS_greater_than_1US":rates["5MS"]>rates["1US"],
     "uninformative_predicate_if_all_one_label":(confusion["TP"]+confusion["FP"] in (0,8)),
     "cases":result,
     "native_log_sha256":hashlib.sha256(x.log.read_bytes()).hexdigest(),
     "new_sampling_population_or_real_iot":False,
     "predictor_uses_downstream_admission_result":False,
     "novel_method_or_library_defect_proven":False,
     "prior_strict30k_crossruntime_gate":"FAIL","prior_stage65_safety":"FAIL"}
    x.out.write_text(json.dumps(output,sort_keys=True,indent=2)+"\n")
    print(json.dumps({k:v for k,v in output.items() if k!="cases"},sort_keys=True,indent=2))
if __name__=="__main__":main()
