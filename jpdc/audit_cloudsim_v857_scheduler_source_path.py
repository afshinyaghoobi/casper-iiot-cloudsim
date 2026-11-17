#!/usr/bin/env python3
"""Exact CloudSimPlus 8.5.7 publisher-source and original Java native trace audit.
Does NOT prove causal execution of individual source branches.
"""
import argparse,csv,hashlib,json,re,zipfile
from pathlib import Path

SOURCE_NATIVE_SHA="b80536e332b04ffeb0285005b38a95563bac36c29201fc8f93693efc95e5c250"
SOURCE_PRIMARY_SHA="4d4454a11b59420c0ff17b064d7988f2bcd0f927e2cfa4ff3600b9ac7a6579a0"
PATHS={
 "abstract":"org/cloudsimplus/schedulers/cloudlet/CloudletSchedulerAbstract.java",
 "space_shared":"org/cloudsimplus/schedulers/cloudlet/CloudletSchedulerSpaceShared.java",
 "datacenter":"org/cloudsimplus/datacenters/DatacenterSimple.java"}
METHODS=("cloudletSubmitInternal","canExecuteCloudletInternal","moveNextCloudletsFromWaitingToExecList",
         "addWaitingCloudletToExecList","updateProcessing","processCloudletSubmit",
         "addCloudletToExecList","addCloudletToWaitingList","isThereEnoughFreePesForCloudlet")
TERMS=("canExecuteCloudletInternal","isThereEnoughFreePesForCloudlet",
       "addCloudletToExecList","addCloudletToWaitingList","addWaitingCloudletToExecList",
       "moveNextCloudletsFromWaitingToExecList","getCloudletWaitingList",
       "getCloudletExecList","updateProcessing","cloudletSubmitInternal")

def sha(data):return hashlib.sha256(data).hexdigest()
def extract_methods(src):
    # Bounded lexical inspection of version-pinned original Java source.
    # Not an AST or dynamic path coverage instrument.
    found={}
    pat=re.compile(r"(?m)^\s*(?:(?:public|protected|private|static|final|synchronized)\s+){1,4}[\w<>,.?\[\] ]+?\s+([A-Za-z]\w*)\s*\(")
    for m in pat.finditer(src):
        name=m.group(1)
        if name not in METHODS:continue
        start=src.find("{",m.end())
        term=src.find(";",m.end())
        if start<0 or (term>=0 and term<start):continue
        # Source snippets containing body quotes/comments can hold braces;
        # mark as lexical-only and do not overclaim AST correctness.
        depth=0;end=None
        for pos in range(start,len(src)):
            if src[pos]=="{":depth+=1
            elif src[pos]=="}":
                depth-=1
                if depth==0:
                    end=pos+1;break
        if end is None:continue
        snippet=src[m.start():end]
        line=src.count("\n",0,m.start())+1
        details=dict(start_line=line,end_line=line+snippet.count("\n"),
                     method_sha256=sha(snippet.encode()),source_characters=len(snippet),
                     referenced_calls=[t for t in TERMS if t+"(" in snippet],
                     reference_occurrences={t:snippet.count(t+"(") for t in TERMS if t+"(" in snippet})
        found.setdefault(name,[]).append(details)
    return found

def parse_state(s):
    return [] if s=="" else [int(i) for i in s.split(";")]

def observed_case(data):
    events={}
    for row in csv.reader(data.decode("utf-8").splitlines()):
        if not row or not row[0].startswith("ARRIVALCF_"):continue
        if len(row)<2:raise ValueError("malformed original native record")
        case=row[1];events.setdefault(case,[])
        if row[0]=="ARRIVALCF_SUBMIT":
            events[case].append(dict(event="SUBMIT",phase=row[2],ms=float(row[3]),
                job=int(row[4]),exec=parse_state(row[5]),wait=parse_state(row[6])))
        elif row[0]=="ARRIVALCF_UPDATE":
            events[case].append(dict(event="UPDATE",phase=row[2],ms=float(row[3]),
                job=None,exec=parse_state(row[4]),wait=parse_state(row[5])))
    result=[]
    for case in ("EARLY4_1US","EARLY4_5MS","ORIGINAL_1US","ORIGINAL_5MS",
                 "LATE10_1US","LATE10_5MS"):
        es=events.get(case,[])
        if not es:raise ValueError("source case absent")
        actual_submit={}
        first=None
        for n,e in enumerate(es):
            if e["event"]=="SUBMIT" and e["phase"]=="AFTER":
                actual_submit[e["job"]]=e["ms"]
                earlier=[job for job in e["wait"] if job in actual_submit]
                late=[job for job in e["exec"] if job in actual_submit]
                bypass=[(a,b) for a in earlier for b in late
                    if actual_submit[a]<actual_submit[b]-1e-7]
                if bypass and first is None:
                    if n==0 or es[n-1]["event"]!="SUBMIT" or es[n-1]["phase"]!="BEFORE" or es[n-1]["job"]!=e["job"]:
                        raise ValueError("observed bypass not at paired submit BEFORE->AFTER")
                    prior=es[n-1]
                    first=dict(time_ms=round(e["ms"],9),older_wait_job=bypass[0][0],
                        later_exec_job=bypass[0][1],job_just_submitted=e["job"],
                        submit_before_exec=prior["exec"],submit_before_wait=prior["wait"],
                        submit_after_exec=e["exec"],submit_after_wait=e["wait"],
                        preceding_update_count=sum(x["event"]=="UPDATE" for x in es[:n]),
                        previous_update_ms=next((round(x["ms"],9) for x in reversed(es[:n])
                            if x["event"]=="UPDATE"),None))
        result.append(dict(case=case,direct_bypass_at_submit=first is not None,
                           first_native_bypass_submit_transition=first,
                           observed_source_submit_count=len(actual_submit)))
    return result

def run(sourcejar,native,repeat,main_audit):
    source=Path(native).read_bytes()
    if sha(source)!=SOURCE_NATIVE_SHA or source!=Path(repeat).read_bytes():
        raise ValueError("original native log archive SHA/repeat mismatch")
    main_bytes=Path(main_audit).read_bytes()
    if sha(main_bytes)!=SOURCE_PRIMARY_SHA:
        raise ValueError("old independently checked native primary summary changed")
    with zipfile.ZipFile(sourcejar) as jar:
        inventory={}
        for label,path in PATHS.items():
            if path not in jar.namelist():raise ValueError(f"EXACT 8.5.7 source missing: {path}")
            content=jar.read(path)
            inventory[label]=dict(jar_path=path,source_sha256=sha(content),
                source_bytes=len(content),methods=extract_methods(content.decode("utf-8")))
    abstract=inventory["abstract"]["methods"]
    ss=inventory["space_shared"]["methods"]
    if "cloudletSubmitInternal" not in abstract or "canExecuteCloudletInternal" not in ss:
        raise ValueError("essential actual scheduler source method absent or unresolvable")
    cases=observed_case(source)
    old=json.loads(main_bytes)
    for c in cases:
        matched=next((x for x in old["cases"] if x["case"]==c["case"]),None)
        if matched is None or matched["native_queue_list_overtaking"]!=c["direct_bypass_at_submit"]:
            raise ValueError("original native submitted-bypass count not reconciled")
    return dict(status="PASS",classification="RETROSPECTIVE_PUBLISHER_V857_SOURCE_PATH_AND_ORIGINAL_NATIVE_EVENT_AUDIT",
        original_cloudsimplus_maven_coordinate="org.cloudsimplus:cloudsimplus:8.5.7:sources",
        original_v857_source_jar_sha256=sha(Path(sourcejar).read_bytes()),
        source_inventory=inventory,first_direct_bypass_at_submit=cases,
        source_lexical_method_inventory_not_dynamic_branch_trace=True,
        dynamic_branch_taken_proven=False,root_cause_unique_identified=False,
        original_30k_java_python_parity="FAIL",stage65_safety="FAIL",
        new_java_execution=False,independent_external_iiot_workload=False)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    for name in ("sources","native","repeat","old-audit","out"):
        p.add_argument("--"+name,required=True)
    a=p.parse_args()
    d=run(a.sources,a.native,a.repeat,a.old_audit)
    Path(a.out).write_text(json.dumps(d,sort_keys=True,indent=2)+"\n")
    print("JPDC_EXACT_CLOUDSIMPLUS_857_SOURCE_AND_ORIGINAL_SUBMIT_TRANSITIONS_PASS",json.dumps({
        k:v for k,v in d.items() if k not in ("source_inventory","first_direct_bypass_at_submit")},sort_keys=True))
