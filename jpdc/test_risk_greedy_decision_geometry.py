#!/usr/bin/env python3
"""Exact grid study of decision changes under CASPER's fixedSigma risk score.
Synthetic predictor values only; no CloudSim result.
"""
from itertools import product
TIERS=(1.10,1.00,0.90)
PRED=tuple(range(1,101))

def score(p,s):return p+(3+.1*p)*s

def run():
    same_tier_pairs=0
    same_tier_inversions=0
    cross_tier_pairs=0
    cross_tier_inversions=0
    example=None
    for s0,s1,p0,p1 in product(TIERS,TIERS,PRED,PRED):
        greedy=(p0>p1)-(p0<p1)
        risky=(score(p0,s0)>score(p1,s1))-(score(p0,s0)<score(p1,s1))
        inverted=greedy*risky<0
        if s0==s1:
            same_tier_pairs+=1
            same_tier_inversions+=inverted
        else:
            cross_tier_pairs+=1
            cross_tier_inversions+=inverted
            if inverted and example is None:example=(s0,s1,p0,p1,score(p0,s0),score(p1,s1))
    assert same_tier_inversions==0
    assert cross_tier_inversions>0
    assert example is not None
    print('SAME_TIER_INVERSION',same_tier_inversions,'/',same_tier_pairs)
    print('CROSS_TIER_INVERSION',cross_tier_inversions,'/',cross_tier_pairs)
    print('FIRST_CONSTRUCTIVE_INVERSION',example)
    print('RISK_GREEDY_DECISION_GEOMETRY_PASS')
if __name__=='__main__':run()
