#!/usr/bin/env python3
"""Exact physical-identity sensitivity of FIRST_IDLE_TIER under label permutations.

For k distinct idle fog nodes with identical eligibility, treat their index order
as uniformly randomly permuted. The first-idle rule selects the first indexed node.
This is an enumeration of ordering outcomes, NOT a CloudSim experiment or
an assumption that the actual generator randomizes index order.
"""
from fractions import Fraction
from itertools import permutations

def exact_change(k):
    if not 2 <= k <= 7:
        raise ValueError("exhaustive fixture accepts 2..7 idle nodes")
    orders = list(permutations(range(k)))
    still_original = sum(order[0] == 0 for order in orders)
    fraction = Fraction(len(orders) - still_original, len(orders))
    assert fraction == Fraction(k-1,k)
    return fraction, len(orders)

if __name__ == "__main__":
    for k in (2,3,4,6):
        fraction,total=exact_change(k)
        print(f"k={k} permutations={total} changed={fraction}")
    print("FIRST_IDLE_PERMUTATION_ENUMERATION_PASS")
