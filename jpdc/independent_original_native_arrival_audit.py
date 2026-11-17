#!/usr/bin/env python3
"""Independent archive-only native queue list overtaking audit, no primary import."""
import argparse,csv,hashlib,json
from pathlib import Path
EXPECTED=("EARLY4_1US","EARLY4_5MS","ORIGINAL_1US","ORIGINAL_5MS","LATE10_1US","LATE10_5MS")
EXPECTED_SERVICE=(8.099623,4.730689,9.120283)

def get_ids(s):
    return tuple() if s=="" else tuple(int(x) for x in s.split(";"))

def audit(native,original):
    logs=Path(native).read_bytes();o=json.loads(Path(original).read_text())
    submissions={name:{} for name in EXPECTED};logged={name:[] for name in EXPECTED}
    outcomes={name:[] for name in EXPECTED}
    counts={name:{"submit":0,"finish":0} for name in EXPECTED}
    for r in csv.reader(logs.decode().splitlines()):
        if not r or r[0]=="JPDC_ARRIVALCF_NATIVE_SIX_CASES_COMPLETE":continue
        kind=r[0];name=r[1]
        if name not in submissions:raise AssertionError("unregistered original case")
        if kind=="ARRIVALCF_SUBMIT":
            now=float(r[3]);who=int(r[4]);phase=r[2]
            if phase=="AFTER":
                if who in submissions[name]:raise AssertionError("duplicate original submit")
                submissions[name][who]=now;counts[name]["submit"]+=1
            logged[name].append((kind,phase,now,who,get_ids(r[5]),get_ids(r[6])))
        elif kind=="ARRIVALCF_UPDATE":
            logged[name].append((kind,r[2],float(r[3]),None,get_ids(r[4]),get_ids(r[5])))
        elif kind=="ARRIVALCF_FINISH":counts[name]["finish"]+=1
        elif kind=="ARRIVALCF_OUTCOME":
            who=int(r[2]);req=float(r[7])
            if abs(req-EXPECTED_SERVICE[who])>1e-7:raise AssertionError("changed original CPU")
            outcomes[name].append((who,float(r[4])))
    proof={}
    for name in EXPECTED:
        if counts[name]!={"submit":3,"finish":3} or len(outcomes[name])!=3:
            raise AssertionError("incomplete original six-case trace")
        before={}
        overtaking=[]
        for kind,phase,clock,job,execution,waiting in logged[name]:
            if kind=="ARRIVALCF_SUBMIT" and phase=="AFTER":
                before[job]=clock
            for w in waiting:
                for e in execution:
                    if w in before and e in before and before[w]<before[e]-1e-7:
                        overtaking.append((kind,phase,round(clock,9),w,e))
        proof[name]=dict(overtaken=bool(overtaking),snapshots=len(overtaking),
                         earliest_overtake=list(overtaking[0]) if overtaking else None,
                         actual_submission_order=sorted(before,key=lambda i:(before[i],i)),
                         native_wait_ms={str(w):round(v,9) for w,v in outcomes[name]})
    p={x["case"]:x for x in o["cases"]}
    if set(proof)!=set(p):raise AssertionError("main source cases differ")
    for name,result in proof.items():
        main=p[name]
        if result["overtaken"]!=main["native_queue_list_overtaking"] or (
            result["snapshots"]!=len(main["overtaking_snapshots"])):
            raise AssertionError("independent native queue overtaking disagrees")
        if result["actual_submission_order"]!=main["actual_native_submit_order"]:
            raise AssertionError("independent source submission order differs")
        for row in main["jobs"]:
            if abs(result["native_wait_ms"][str(row["job"])]-row["native_wait_ms"])>1e-7:
                raise AssertionError("original native wait differs")
    return dict(status="PASS",original_native_sha256=hashlib.sha256(logs).hexdigest(),
      real_native_cases=6,total_finished_native_cloudlets=18,
      direct_overtaking_cases=[name for name in EXPECTED if proof[name]["overtaken"]],
      source_same_clock_list_state_independently_reparsed=True,
      new_native_java_experiment=True,independent_external_source_seed=False,external_iiot_trace=False,
      original_30k_queue_parity="FAIL",stage65_safety="FAIL",cases=proof)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--native",required=True);p.add_argument("--primary",required=True);p.add_argument("--out",required=True)
    a=p.parse_args();v=audit(a.native,a.primary)
    Path(a.out).write_text(json.dumps(v,sort_keys=True,indent=2)+"\n")
    print("JPDC_REAL_NATIVE_ARRIVAL_OFFSET_INDEPENDENT_ARCHIVE_AUDIT_PASS",json.dumps({
      k:x for k,x in v.items() if k!="cases"},sort_keys=True))
