#!/usr/bin/env python3
"""SIMPAT v0.9 journal-packet structure check. NOT a scientific/author approval check."""
from pathlib import Path
import csv,hashlib,json,re
root=Path(__file__).parent
title="Queue-Wait and Execution-Time Semantics in CloudSimPlus 8.5.7: Implications for IoT Scheduling Simulation"
p=root/"SIMPAT_MANUSCRIPT_V09_SOURCE_TO_FIGURE_METHOD_2026-11-18.md"
h=root/"SIMPAT_HIGHLIGHTS_DRAFT_2026-11-18.md"
c=root/"SIMPAT_COVER_LETTER_AUTHOR_REVIEW_DRAFT_2026-11-18.md"
d=root/"SIMPAT_AUTHOR_DISCLOSURES_AND_TITLE_PAGE_WORKSHEET_2026-11-18.md"
data=root/"manuscript_a2_primary_24_cases_2026-11-18.csv"
svg=root/"figure_a2_24_case_native_vs_fifo_2026-11-18.svg"
t=p.read_text(); lines=t.splitlines()
assert lines[0]=="# "+title
abstract=t.split("## Abstract\n",1)[1].split("**Keywords:**",1)[0]
words=len(re.findall(r"\b[\w]+(?:[-/–][\w]+)*\b",abstract))
assert words<=250,("abstract too long",words) # provisional: recheck current SIMPAT Guide
assert "Industrial Internet of Things" not in lines[0]
assert "### 4.3 Reproducible source-to-figure analysis" in t
assert "posthoc" in t.lower() and ("one vm" in t.lower() or "single vm" in t.lower())
assert "AI-assisted tools were used" in t
assert "not empirical fidelity" in t
numbers=[int(x) for x in re.findall(r"(?m)^\[(\d+)\] ",t.split("## References\n",1)[1])]
assert numbers==list(range(1,12)),numbers
highlights=[x[2:] for x in h.read_text().splitlines() if x.startswith("- ")]
assert 3<=len(highlights)<=5 and max(map(len,highlights))<=85
assert title in h.read_text() and title in c.read_text() and title in d.read_text()
assert "NOT FOR DIRECT SUBMISSION" in c.read_text()
assert "TO BE CONFIRMED" in d.read_text()
with data.open(newline="") as fp:rows=list(csv.DictReader(fp))
assert len(rows)==24 and len({r["case"] for r in rows})==24
assert sum(int(x["deadline25_model_disagreements"]) for x in rows)==86
assert sum(int(x["deadline50_model_disagreements"]) for x in rows)==107
assert max(float(x["max_abs_native_minus_requested_fifo_wait_ms"]) for x in rows)==246
assert all(x["case"] in svg.read_text() for x in rows)
assert title in c.read_text()
print(json.dumps({"status":"PASS_STATIC_PACKET_CHECK","title_locked":True,"abstract_words":words,
"references_numbered":len(numbers),"highlight_lengths":list(map(len,highlights)),
"source_cases":24,"unresolved_author_approvals":True,"publisher_submission":False,
"files_sha256":{x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in [p,h,c,d,data,svg]}},indent=2,sort_keys=True))
