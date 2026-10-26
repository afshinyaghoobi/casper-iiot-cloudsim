#!/usr/bin/env python3
"""Executable elementary properties of the policy's mathematical score."""
def route(pred,backlog,eligible):
    return min((i for i,x in enumerate(eligible) if x),
               key=lambda i:(pred[i]+backlog[i],i))
assert route([10,10],[5,1],[True,True])==1
assert route([9,11],[3,0],[True,True])==1
assert route([9,11],[3,0],[True,False])==0
assert route([4,8],[0,0],[True,True])==0
print("QUEUE_AWARE_SCORE_TEST_PASS")
