#!/usr/bin/env python3
"""Analytic counterexample; NOT CloudSim data or calibrated probabilities."""
from math import erfc, sqrt
def sigma(pred, mult): return (3.0 + 0.1 * pred) * mult
def miss_probability(pred, sd, deadline):
    return 0.5 * erfc((deadline - pred) / (sd * sqrt(2)))
def test():
    deadline = 100.0
    nodes = [(80.0, 1.10), (90.0, 0.90)]
    s = [sigma(pred, mult) for pred, mult in nodes]
    feasible = [i for i, (pred, _) in enumerate(nodes) if pred <= deadline]
    chosen = min(feasible, key=lambda i: (s[i], nodes[i][0], i))
    p = [miss_probability(pred, sd, deadline) for (pred, _), sd in zip(nodes, s)]
    assert chosen == 1
    assert abs(s[0] - 12.1) < 1e-12 and abs(s[1] - 10.8) < 1e-12
    assert abs(p[0] - 0.04917636559452464) < 1e-12
    assert abs(p[1] - 0.17724223843665599) < 1e-12
    assert p[1] > p[0]
    print("ANALYTIC_COUNTEREXAMPLE_PASS", f"pA={p[0]:.9f}", f"pB={p[1]:.9f}")
if __name__ == "__main__": test()
