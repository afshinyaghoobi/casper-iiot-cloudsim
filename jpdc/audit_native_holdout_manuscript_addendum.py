#!/usr/bin/env python3
"""Fail-closed manuscript transcription audit against immutable native result report.

This checks committed SOURCE REPORT NUMBERS, not independent GitHub artifact bytes.
The original preregistered primary inferential run is not rerun here.
"""
from pathlib import Path
import math,re

ROOT=Path(__file__).resolve().parents[1]
DRAFT=ROOT/"jpdc/JPDC_NATIVE_HOLDOUT_RESULTS_DISCUSSION_ADDENDUM_2026-11-04.md"
REPORT=ROOT/"jpdc/NATIVE_TEN_SEED_ALL_EIGHT_HOLDOUT_VERIFIED_2026-11-04.md"
PREREG=ROOT/"jpdc/NATIVE_EIGHT_POLICY_HOLDOUT_PREREG_2026-11-04.md"

def require(condition,msg):
    if not condition:raise AssertionError(msg)
    print("PASS",msg)

def cells(line):
    return [x.strip().replace("**","") for x in line.strip().strip("|").split("|")]

def find_rows(s,anchor):
    return [cells(line) for line in s.splitlines()
            if line.startswith("| ") and cells(line)[0]==str(anchor)]

def main():
    d=DRAFT.read_text(encoding="utf-8")
    r=REPORT.read_text(encoding="utf-8")
    p=PREREG.read_text(encoding="utf-8")
    require("60,61,62,63,64,65,66,67,68,69" in p,
            "original unseen ten-seed preregistration fixed")
    require("PRED_GREEDY" in p and "CASPER_FULL" in p and "TWO-SIDED" in p,
            "original contrast and inferential direction frozen")
    require("p-value was 1.000" in d and "p = 1.000" in r,
            "manuscript correctly reports nonsignificant original exact p=1")
    require("five differences favored CASPER_FULL, four favored PRED_GREEDY, and one was an exact tie" in d,
            "original five positive / four negative / one exact tie")
    require("−0.3060, +0.9882" in d and "-0.003060346399035438" in r,
            "source-scaled fixed 10000 seed-bootstrap descriptive interval")
    require("0.3208 percentage points" in d and "+0.3208 percentage points" in r.replace("**",""),
            "positive mean is correctly described only as small descriptive difference")
    require("4,800,000 task-policy executions" in d and "4,800,000 task-policy executions" in r,
            "complete 160×30000 task-policy evaluation cohort")
    require("80,000 calibration tasks" in d and "800,000 original-model calibration task executions" in r,
            "independent native calibration correctly scoped to ten seeds")
    diffs={60:-.1599,61:0.0,62:-.6931,63:1.5432,64:-1.3,
           65:.1009,66:-.1035,67:.1499,68:1.4344,69:2.2364}
    for seed,value in diffs.items():
        rr=find_rows(r,seed)
        dd=find_rows(d,seed)
        require(len(rr)==1 and len(dd)==1,
                f"unique original and manuscript seed {seed}")
        def number(val):
            return float(val.split()[0].replace("−","-").replace("+",""))
        observed=number(dd[0][1])
        source=number(rr[0][1])
        require(math.isclose(observed,source,abs_tol=1e-4,rel_tol=0)
                and math.isclose(observed,value,abs_tol=1e-4,rel_tol=0),
                f"seed {seed} benefit copied without altered sign")
    expected={
      ("S2 compute loss","PRED_GREEDY"):(3.2827,367,None),
      ("S2 compute loss","CASPER_HEALTH_STATIC"):(2.5580,299,93.8534),
      ("S2 compute loss","CASPER_FULL"):(2.5580,299,92.9462),
      ("S3 network loss","PRED_GREEDY"):(6.1300,647,None),
      ("S3 network loss","CASPER_HEALTH_STATIC"):(6.2131,655,96.8654),
      ("S3 network loss","CASPER_FULL"):(6.2131,655,87.9553),
    }
    for (scenario,policy),(rate,misses,cert) in expected.items():
        matching=[cells(line) for line in d.splitlines() if line.startswith("| ")
                  and len(cells(line))==5 and cells(line)[:2]==[scenario,policy]]
        require(len(matching)==1,f"one manuscript row {scenario}/{policy}")
        row=matching[0]
        require(math.isclose(float(row[2].rstrip("%")),rate,rel_tol=0,abs_tol=.0001)
                and int(row[3].replace(",",""))==misses
                and ((cert is None and row[4]=="Not applicable")
                     or (cert is not None and
                         math.isclose(float(row[4].rstrip("%")),cert,rel_tol=0,abs_tol=.0001))),
                f"scenario {scenario}/{policy} original descriptive counts and rates")
    for name,rank2 in (("CASPER_FULL",39),("CASPER_HEALTH_STATIC",9),
                       ("CASPER_ADAPT_NO_HEALTH",63),("RANKED_CP_STATIC",10)):
        require(re.search(rf"{name}.*?\*\*{rank2}\*\*",d,re.S) is not None,
                f"original {name} rank2 count present")
    require("rank 3 was never selected" in d.lower(),
            "no imaginary real rank3 activation")
    require("9.1214 ms" in d and "5 ms" in d and "not physically equivalent" in d.lower(),
            "original failed CloudSim FCFS physical transfer remains disclosed")
    require("p = .0625" in d and "p = .125" in d,
            "both original unsuccessful Java inference gates retained")
    require("not a YAFS replication" in d and "not an independent workload distribution" in d,
            "YAFS/source-model external-validity restrictions explicit")
    print("JPDC_NATIVE_HOLDOUT_MANUSCRIPT_NUMERIC_AND_CLAIM_AUDIT_PASS")

if __name__=="__main__":main()
