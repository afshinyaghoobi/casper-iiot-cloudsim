#!/usr/bin/env python3
"""Simple fixed examples for online adaptation of minimum-execution-time mapping."""
def pick_met(compute,eligible):
    options=[i for i,e in enumerate(eligible) if e]
    assert options
    return min(options,key=lambda i:(compute[i],i))
assert pick_met([11,7,4],[1,1,1])==2
assert pick_met([11,7,4],[1,1,0])==1
assert pick_met([7,7,8],[1,1,1])==0
# MET chooses lower compute duration even if predicted completion is longer
assert pick_met([1,2],[1,1])==0
assert min(range(2),key=lambda i:[100,3][i])==1
print("ONLINE_MET_UNIT_TEST_PASS")
