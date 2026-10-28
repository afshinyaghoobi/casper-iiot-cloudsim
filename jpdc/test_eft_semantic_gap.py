#!/usr/bin/env python3
"""Constructive check: model's additive predictor is NOT max-overlap EFT.
Numbers are synthetic unit fixtures, not CASPER simulation results.
"""
def additive(network, queue, service):
    return network+queue+service

def overlap(network, queue, service):
    return max(network,queue)+service

def argmin(scores):
    return min(range(len(scores)),key=lambda i:(scores[i],i))

def main():
    cases=[
        {'name':'ranking_reversal','network':[8.,3.],'queue':[0.,6.],'service':[1.,1.],'add_choice':0,'overlap_choice':1},
        {'name':'no_overlap_equal','network':[4.,8.],'queue':[0.,0.],'service':[1.,1.],'add_choice':0,'overlap_choice':0},
        {'name':'queue_only_equal','network':[0.,0.],'queue':[7.,2.],'service':[1.,1.],'add_choice':1,'overlap_choice':1},
        {'name':'low_index_tie','network':[2.,2.],'queue':[0.,0.],'service':[1.,1.],'add_choice':0,'overlap_choice':0},
    ]
    for case in cases:
        add=[additive(n,q,s) for n,q,s in zip(case['network'],case['queue'],case['service'])]
        ov=[overlap(n,q,s) for n,q,s in zip(case['network'],case['queue'],case['service'])]
        assert argmin(add)==case['add_choice'],(case['name'],add)
        assert argmin(ov)==case['overlap_choice'],(case['name'],ov)
        print(f"{case['name']}: additive={add}, max_overlap={ov}, chosen={argmin(add)}/{argmin(ov)}")
    print('EFT_SEMANTIC_GAP_PASS 4 fixtures; ranking reversal confirmed')
if __name__=='__main__':main()
