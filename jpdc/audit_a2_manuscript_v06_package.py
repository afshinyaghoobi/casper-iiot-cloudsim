#!/usr/bin/env python3
"""Check source-backed 24-cell manuscript package consistency (static QA only).
Does not measure originality, journal suitability, empirical validity, or referee acceptance.
"""
from pathlib import Path
import csv,re,math,hashlib,json

ROOT=Path(__file__).resolve().parent
P=ROOT/"JPDC_A_JOURNAL_FACING_MANUSCRIPT_V06_2026-11-18.md"
C=ROOT/"manuscript_a2_primary_24_cases_2026-11-18.csv"
S=ROOT/"figure_a2_24_case_native_vs_fifo_2026-11-18.svg"
m=P.read_text()
with C.open(newline="") as f:
    rows=list(csv.DictReader(f))
assert len(rows)==24
ids={r["case"] for r in rows}
assert len(ids)==24
assert set(re.findall(r'(?:BURSTY|STAGGERED)_S[0-2]_(?:1US|5MS)_P[12]',S.read_text()))==ids
all_mins=[float(r["max_abs_native_minus_requested_fifo_wait_ms"]) for r in rows]
assert max(all_mins)==246.0
a=sum(int(r["deadline25_model_disagreements"]) for r in rows)
b=sum(int(r["deadline50_model_disagreements"]) for r in rows)
assert (a,b)==(86,107)
for r in rows:
    id=r["case"]
    matches=[line for line in m.splitlines() if line.startswith("| "+id+" |")]
    assert len(matches)==1,(id,len(matches))
    parts=[x.strip() for x in matches[0].split("|")[1:-1]]
    assert parts==[id,r["max_abs_native_minus_requested_fifo_wait_ms"],r["deadline25_model_disagreements"],r["deadline50_model_disagreements"]],(id,parts)
assert "49.0961 ms" in m
assert "250/288" in m or "250 of 288" in m
assert "154 ms" in m and "246 ms" in m
assert "288/288" in m or "all 288" in m
assert "figure_a2_24_case_native_vs_fifo_2026-11-18.svg" in m
assert "manuscript_a2_primary_24_cases_2026-11-18.csv" in m
assert not re.search(r'\b(?:AUTHOR TO COMPLETE|TODO|FIGURE 1 CREATED|TABLE 1 GENERATED|NOT SUBMISSION-READY|EDITORIAL GO/NO-GO STILL OPEN)\b',m)
assert "not proof of a simulator defect" in m.lower()
assert "one VM" in m or "single VM" in m
assert "10.1002/cpe.3983" in m and "10.1016/j.simpat.2019.02.003" in m
result={"status":"PASS_STATIC_CROSS_ARTIFACT_QA","cases":24,"tasks":288,"deadline25_disagreements":a,"deadline50_disagreements":b,
"largest_wait_gap_ms":max(all_mins),
"files":{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [P,C,S]},
"scientific_contribution_certified":False,"journal_submission_approved":False}
print(json.dumps(result,sort_keys=True,indent=2))
