#!/usr/bin/env python3
"""Stage68 reproducible source-report-to-manuscript claim and nonclaim audit."""
from pathlib import Path
import hashlib,json,re

ROOT=Path(__file__).resolve().parents[1]
MATRIX=ROOT/"jpdc/STAGE68_JPDC_CLAIM_EVIDENCE_VALIDITY_MATRIX_2026-11-14.md"
DRAFT=ROOT/"jpdc/STAGE68_JPDC_MANUSCRIPT_VALIDITY_AND_NEGATIVE_RESULTS_DRAFT_2026-11-14.md"
REPORTS={
 "61":"STAGE61_SHADOW_WORLD_FEASIBILITY_VERIFIED_FAIL_2026-11-14.md",
 "62":"STAGE62_PARTIAL_SHADOW_FEASIBILITY_VERIFIED_2026-11-14.md",
 "63":"STAGE63_CHOSEN_NODE_TEMPORAL_COVERAGE_VERIFIED_2026-11-14.md",
 "65":"STAGE65_EIGHT_SOURCE_HOLDOUT_VERIFIED_SAFETY_FAIL_2026-11-14.md",
 "66":"STAGE66_POSTHOC_PAIRED_TASK_FORENSICS_VERIFIED_2026-11-14.md",
 "67":"STAGE67_NATIVE_SERVICE_SCALE_QUEUE_VERIFIED_2026-11-14.md",
}
SOURCE_EXPECT={
 "61":("0/4840","0/820","FAIL"),
 "62":("4349/4532","27/96","95.96%"),
 "63":("207/212","200/204","208/212"),
 "65":("24→17","31→14","p=1.000","p=0.125","SAFETYFAIL"),
 "66":("10306","11756","6877","4385","POSTHOC"),
 "67":("25.9500704","35.2733110","24.1204006","20.5416220","35.5386220","1/6"),
}
def normalized(s):
    return re.sub(r"[^a-z0-9.→/%]+","",s.lower())

def main():
    matrix=MATRIX.read_text()
    draft=DRAFT.read_text()
    data={}
    for key,name in REPORTS.items():
        p=ROOT/"jpdc"/name
        source=p.read_text()
        n=normalized(source)
        for token in SOURCE_EXPECT[key]:
            assert normalized(token) in n,(name,"missing source:",token)
        assert name in matrix,(name,"not referenced in matrix")
        data[key]=dict(source_path=str(p.relative_to(ROOT)),
                       sha256=hashlib.sha256(p.read_bytes()).hexdigest())
    for val in ("0/4840","4349/4532","Stage65","SAFETY","1.000","0.125",
                "9.12140093294972","5ms","Stage67","1/6","source seed",
                "counterfactual","external"):
        assert normalized(val) in normalized(matrix),("matrix lacks",val)
    for val in ("9.12140093294972","5 ms","4,840","4,349","4,532",
                "207/212","200/204","208/212","1.000","0.125",
                "eight new independent source seeds","counterfactual","retrospective",
                "no independently acquired"):
        assert normalized(val) in normalized(draft),("draft lacks",val)
    for bad in ("proves that our scheduler is superior",
                "statistically significant improvements in both shocks",
                "demonstrates distribution-free coverage",
                "java and python simulators are equivalent",
                "validated in industrial deployment",
                "stage65 safety pass"):
        assert bad not in draft.lower(),("false claim",bad)
    return dict(status="PASS",kind="ARCHIVED_REPORT_CLAIM_AUDIT_NOT_NEW_SCIENCE",
                no_new_experiment=True,original_stage65_safety="FAIL",
                original_java_python_30k_parity="FAIL",
                manuscript_only_draft=True,sources=data,
                matrix_sha256=hashlib.sha256(MATRIX.read_bytes()).hexdigest(),
                draft_sha256=hashlib.sha256(DRAFT.read_bytes()).hexdigest())
if __name__=="__main__":
    v=main()
    print("JPDC_STAGE68_EVIDENCE_CONTRACT",json.dumps(v,sort_keys=True))
    print("JPDC_STAGE68_MANUSCRIPT_EVIDENCE_NONCLAIMS_PASS")
