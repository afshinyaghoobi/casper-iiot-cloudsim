#!/usr/bin/env python3
"""Retrospective *event-order* evidence audit on original six A1 native traces.

No causal counterfactual, new Java execution or CloudSimPlus defect proof.
Case-level evidence combines recorded eligibility returns, list snapshots,
update state and later direct submission within the *same* original trace.
"""
import argparse,csv,json,hashlib,collections
from pathlib import Path

EXPECTED=("EARLY4_1US","EARLY4_5MS","ORIGINAL_1US","ORIGINAL_5MS","LATE10_1US","LATE10_5MS")
def parse_events(path):
    groups=collections.defaultdict(list)
    for line in path.read_text().splitlines():
        if not line.startswith("ARRIVALTRACE_"):continue
        z=next(csv.reader([line]))
        if len(z)<2 or z[1] not in EXPECTED:continue
        groups[z[1]].append(z)
    assert sorted(groups)==sorted(EXPECTED)
    return groups

def analyze(events):
    candidates=[]
    for case,rows in sorted(events.items()):
        for idx,r in enumerate(rows):
            if r[0]!="ARRIVALTRACE_UPDATE" or r[2]!="BEFORE" or r[5]!="1" or "0" not in r[4].split(";"):continue
            clock=r[3]
            # The nested native method call is entered before the same update returns.
            end=next((j for j in range(idx+1,len(rows))
                      if rows[j][0]=="ARRIVALTRACE_UPDATE" and rows[j][2]=="AFTER" and rows[j][3]==clock),None)
            assert end is not None
            mid=rows[idx+1:end]
            p_before=next((z for z in mid if z[0]=="ARRIVALTRACE_PROMOTION" and z[2]=="BEFORE"),None)
            p_after=next((z for z in mid if z[0]=="ARRIVALTRACE_PROMOTION" and z[2]=="AFTER"),None)
            eligible=next((z for z in mid if z[0]=="ARRIVALTRACE_ELIGIBILITY" and z[3]=="1"),None)
            if not (p_before and p_after and eligible):continue
            assert p_before[3]==clock==p_after[3]
            if not (eligible[4]=="false" and p_before[4]=="0" and p_before[5]=="1"
                    and p_after[4]=="0" and p_after[5]=="1"
                    and rows[end][4]=="" and rows[end][5]=="1"):continue
            following=rows[end+1:]
            for k,s in enumerate(following):
                if s[0]=="ARRIVALTRACE_SUBMIT" and s[2]=="BEFORE" and s[4]=="2" and s[5]=="" and s[6]=="1":
                    nexts=following[k+1:]
                    elig=next((z for z in nexts if z[0]=="ARRIVALTRACE_ELIGIBILITY" and z[3]=="2"),None)
                    aft=next((z for z in nexts if z[0]=="ARRIVALTRACE_SUBMIT" and z[2]=="AFTER" and z[4]=="2"),None)
                    assert elig and aft
                    if elig[4]=="true" and aft[5]=="2" and aft[6]=="1":
                        candidates.append({"case":case,"update_clock_ms":float(clock),
                         "older_job1_eligible_during_update":False,
                         "old_exec_before":"0","old_wait_before":"1",
                         "old_exec_after":"","old_wait_after":"1",
                         "new_submit_clock_ms":float(s[3]),
                         "job2_eligible_at_submit":True,
                         "new_exec_after":"2","older_wait_after":"1",
                         "clock_delta_ms":round(float(s[3])-float(clock),9)})
                    break
    return candidates
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--original",type=Path,required=True)
    ap.add_argument("--promotion",type=Path,required=True)
    ap.add_argument("--out",type=Path,required=True)
    a=ap.parse_args()
    promoted=a.promotion.read_text().splitlines()
    filtered=[line for line in promoted if not line.startswith("ARRIVALTRACE_PROMOTION,")]
    original=a.original.read_text().splitlines()
    assert filtered==original,"New tracing changed prior original control trace"
    groups=parse_events(a.promotion)
    matches=analyze(groups)
    assert [q["case"] for q in matches]==["LATE10_5MS","ORIGINAL_5MS"],matches
    assert all(q["clock_delta_ms"]>0 for q in matches)
    assert abs(next(q for q in matches if q["case"]=="ORIGINAL_5MS")["clock_delta_ms"]-0.0001176)<1e-7
    assert abs(next(q for q in matches if q["case"]=="LATE10_5MS")["clock_delta_ms"]-10.0001176)<1e-7
    result={"status":"PASS_ORIGINAL_LOG_EXECUTED_EVENT_ORDER_AUDIT",
     "original_source_cases":6,"observed_precursor_sequences":len(matches),
     "observed_cases":matches,"negative_control_cases":[c for c in EXPECTED if c not in {q["case"] for q in matches}],
     "source_control_sha256":hashlib.sha256(a.original.read_bytes()).hexdigest(),
     "source_promotion_sha256":hashlib.sha256(a.promotion.read_bytes()).hexdigest(),
     "original_instrumentation_trace_equal_after_filter":True,
     "science_classification":"RETROSPECTIVE_EVENT_SEQUENCE_NOT_CAUSAL_ISOLATION",
     "claim_of_library_defect":False,"causal_effect_proven":False,
     "new_native_java_simulations":False,
     "old_crossruntime_parity":"FAIL","stage65_safety":"FAIL"}
    a.out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result,sort_keys=True))
if __name__=="__main__":main()
