#!/usr/bin/env python3
"""Synthetic-only negative queue-audit fixture; not native execution evidence."""
import copy
from audit_native_arrival_offset_counterfactual import overtake

def main():
    submitted={0:1000.0,1:1010.0,2:1013.0}
    assert overtake(submitted,[2],[1])==[(1,2)]
    assert overtake(submitted,[1],[2])==[]
    assert overtake({0:1000.0,1:1010.0},[2],[1])==[]
    assert overtake({0:1000.0,2:1004.0,1:1010.0},[2],[1])==[]
    assert overtake({0:1000.0,2:1004.0,1:1010.0},[1],[2])==[(2,1)]
    print("JPDC_ARRIVALCF_SYNTHETIC_BYPASS_POSITIVE_NEGATIVE_CONTRACT_PASS")

if __name__=="__main__":main()
