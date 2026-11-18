#!/usr/bin/env python3
"""SIMPAT v1.9 journal-packet structure check. NOT a scientific/author approval check."""
from pathlib import Path
import csv,hashlib,json,re
root=Path(__file__).parent
title="Queue-Wait and Execution-Time Semantics in CloudSimPlus 8.5.7: Implications for IoT Scheduling Simulation"
p=root/"SIMPAT_MANUSCRIPT_V19_SOFTWARE_CONTRACT_AND_LIMITATIONS_2026-11-18.md"
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
assert "R. N. Calheiros" in t and "Calheiros et al. [1]" in t
assert "24 *different edge simulation frameworks*" in t
assert "Zakarya and Gillam [8]" in t
assert "Vondra and Šedivý [12]" in t
assert "10.1016/j.simpat.2016.10.005" in t
assert "Sufficiency of this narrow versioned empirical diagnostic" in t
assert "JPDC research article" not in t
assert "nonzero model disagreement is not in itself surprising" in t
assert "two distinct completion-time constructions" in t
assert "not an independently measured physical CPU service demand" in t
assert "GitHub Actions run artifacts may expire" in t
assert "Its exact editorial status" in t
assert "originally submitted FGCS CASPER" not in t
assert "### 5.6 Exploratory matched-configuration check" in t
assert "This is an exploratory sensitivity finding" in t
assert "increased in eight pairs" in t
assert "one to five of 12 tasks" in t
assert "SIMPAT_A2_POSTHOC_MATCHED_METRIC_DISCORDANCE_2026-11-18.md" in t
assert "Original-log, per-job margin diagnosis" in t
assert "73" in t and "13" in t and "102" in t and "5" in t
assert "only job ID **1**" in t
assert "2, 4, 5, 6 and 7" in t
assert "the run artifact\u0027s retention may be time-limited" in t
assert "### 5.7 Exploratory sensitivity of model disagreement" in t
assert "51-threshold sweep were designed after" in t
assert "nine" in t and "40" in t and "two" in t
assert "51 versus 47" in t and "64 versus 22" in t and "78 versus 1" in t
assert "SIMPAT_A2_POSTHOC_THRESHOLD_SENSITIVITY_VERIFIED_2026-11-18.md" in t
assert "neither of the original 25/50-ms results is a universal outcome" in t
assert "### 5.8 Passive waiting-promotion method observation" in t
assert "**33 method invocations**" in t and "**10 individual invocations" in t
assert "1013.0997406" in t and "1037.2200236" in t
assert "1023.0997406" in t and "1058.099623" in t
assert "byte-identical" in t and "post-outcome-motivated" in t
assert "SIMPAT_NATIVE_A1_WAIT_PROMOTION_HOOK_VERIFIED_2026-11-18.md" in t
assert "### 5.9 Retrospective event-order precondition" in t
assert "1013.099623 ms" in t and "1013.0997406 ms" in t
assert "1023.0997406 ms" in t and "10.0001176 ms" in t
assert "actual waiting-promotion method executed" in t
assert "two of six" in t and "posthoc reconstruction" in t
assert "SIMPAT_A1_EXECUTED_ELIGIBILITY_ORDER_PRECONDITION_VERIFIED_2026-11-18.md" in t
assert "an isolated causal effect of event timing" in t
assert "### 5.10 Prospectively specified end-of-update rescan counterfactual" in t
assert "exactly byte-identical" in t
assert "in neither case under TREATMENT" in t
assert "12 added post-update rescan calls" in t
assert "0.005 s" in t
assert "no independent held-out validation" in t
assert "SIMPAT_A1_PREREG_POSTUPDATE_RESCAN_INTERVENTION_VERIFIED_2026-11-18.md" in t
assert "a unique underlying Java branch" in t
assert "official CloudSimPlus 8.5.7 API documentation" in t
assert "documented software semantics" in t
assert "The original **24-case A2** run" in t
assert "A1** native microfixture did instrument" in t
assert "one- and two-PE VM configurations" in t
assert "**Software-contract and intervention scope.**" in t
assert "the two affected a1 conditions were known" in t.lower()
assert "the unique causal decomposition across the 24 a2 conditions" in t.lower()
assert "a waiting-promotion callback was not instrumented" not in t
assert "More precise attribution of waiting promotion and validation" not in t
assert "CloudletSchedulerAbstract.html" in t




assert "author verification required" in t.lower()
assert "## Declarations required before journal submission" in t
assert t.index("## Declarations required before journal submission") < t.index("## References")
numbers=[int(x) for x in re.findall(r"(?m)^\[(\d+)\] ",t.split("## References\n",1)[1])]
assert numbers==list(range(1,13)),numbers
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
