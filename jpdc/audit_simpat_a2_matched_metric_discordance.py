#!/usr/bin/env python3
"""Exploratory matched-configuration metric discordance audit for frozen A2 data.

IMPORTANT: POSTHOC descriptive screen. Not a preregistered hypothesis, an
independent experiment, a causal PE intervention or a population test.
Compares maximum within-case absolute WAIT-model discrepancy with per-case
synthetic deadline classification disagreement. These are different constructs.
"""
import csv, json, hashlib
from collections import defaultdict
from pathlib import Path
P=Path(__file__).with_name("manuscript_a2_primary_24_cases_2026-11-18.csv")
rows=list(csv.DictReader(P.open(newline="")))
assert len(rows)==24
D={}
for a in rows:
    key=(a["family"],int(a["variant"]),a["min_event_gap"],int(a["vm_pes"]))
    assert key not in D and a["case"]==f'{key[0]}_S{key[1]}_{key[2]}_P{key[3]}'
    D[key]={
      "case":a["case"],
      "wait_max_abs_ms":float(a["max_abs_native_minus_requested_fifo_wait_ms"]),
      "deadline25_disagreements":int(a["deadline25_model_disagreements"]),
      "deadline50_disagreements":int(a["deadline50_model_disagreements"])
    }
assert len(D)==24
def pairs(dimension):
    out=[]
    if dimension=="capacity":
      for family in ("BURSTY","STAGGERED"):
        for variant in (0,1,2):
          for gap in ("1US","5MS"):
            lo,hi=D[(family,variant,gap,1)],D[(family,variant,gap,2)]
            out.append({"pair_key":f"{family}_S{variant}_{gap}","lower":lo,"higher":hi})
    else:
      for family in ("BURSTY","STAGGERED"):
        for variant in (0,1,2):
          for pe in (1,2):
            lo,hi=D[(family,variant,"1US",pe)],D[(family,variant,"5MS",pe)]
            out.append({"pair_key":f"{family}_S{variant}_P{pe}","lower":lo,"higher":hi})
    assert len(out)==12
    return out
def directions(pairs,key):
    vals=[x["higher"][key]-x["lower"][key] for x in pairs]
    return {"increased":sum(z>0 for z in vals),
      "decreased":sum(z<0 for z in vals),
      "unchanged":sum(z==0 for z in vals)}
def summary(ps):
    return {"max_abs_wait_gap_ms":directions(ps,"wait_max_abs_ms"),
       "deadline25_disagreements":directions(ps,"deadline25_disagreements"),
       "deadline50_disagreements":directions(ps,"deadline50_disagreements")}
capacity=pairs("capacity");event=pairs("event_gap")
out={"status":"PASS_POSTHOC_DESCRIPTIVE_PAIR_AUDIT","n_cases":24,
     "jobs_per_case":12,"n_pe_matched_pairs":12,"n_event_gap_matched_pairs":12,
     "capacity_1pe_to_2pe":summary(capacity),
     "min_event_gap_1us_to_5ms":summary(event),
     "example":{"pair":"BURSTY_S0_1US",
       "one_pe":D[("BURSTY",0,"1US",1)],
       "two_pe":D[("BURSTY",0,"1US",2)]},
     "source_sha256":hashlib.sha256(P.read_bytes()).hexdigest(),
     "analysis_type":"EXPLORATORY_POSTHOC_DESCRIPTIVE",
     "causal_or_population_claim":False,
     "new_native_simulation":False}
assert out["capacity_1pe_to_2pe"]=={
  "max_abs_wait_gap_ms":{"increased":0,"decreased":12,"unchanged":0},
  "deadline25_disagreements":{"increased":8,"decreased":1,"unchanged":3},
  "deadline50_disagreements":{"increased":5,"decreased":4,"unchanged":3}}
assert out["min_event_gap_1us_to_5ms"]["max_abs_wait_gap_ms"]=={
  "increased":10,"decreased":2,"unchanged":0}
assert out["example"]["one_pe"]["wait_max_abs_ms"]==157.018
assert out["example"]["two_pe"]["wait_max_abs_ms"]==25.005
assert out["example"]["one_pe"]["deadline25_disagreements"]==1
assert out["example"]["two_pe"]["deadline25_disagreements"]==5
print(json.dumps(out,sort_keys=True,indent=2))
