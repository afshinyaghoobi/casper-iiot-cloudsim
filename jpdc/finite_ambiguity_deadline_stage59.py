#!/usr/bin/env python3
"""Stage59 conditional finite-ambiguity deadline-first minimax-regret mapper.

Proof-of-concept pure function only. Hypothetical costs are INPUT, not verified
causal uncertainty bounds, empirical coverage, or true future trajectories.
This is NOT proven to reduce actual CASPER miss rates.
"""
from dataclasses import dataclass
import math

NODES = 21

@dataclass(frozen=True)
class Selection:
    node: int
    nominal_greedy_node: int
    worst_case_deadline_miss: int
    worst_case_latency_regret_ms: float
    robust_feasible_in_given_worlds: bool
    switched_from_nominal: bool
    hypothetical_world_count: int
    conditional_only: bool = True


def _positive_number(v):
    return (isinstance(v, (int, float)) and not isinstance(v, bool)
            and math.isfinite(v) and v > 0)


def select(nominal, worlds, deadline_ms):
    """Return the lex-min (worst miss, worst regret, nominal, node ID).

    Exactly 21 eligible nodes, finite non-empty hypothetical worlds.
    No source of truth or future simulator data is queried here.
    """
    if not _positive_number(deadline_ms):
        raise ValueError("positive finite deadline required")
    if not isinstance(nominal, (list, tuple)) or len(nominal) != NODES:
        raise ValueError("exactly 21 nominal node costs required")
    if any(not _positive_number(x) for x in nominal):
        raise ValueError("nominal costs must be positive and finite")
    if not isinstance(worlds, (list, tuple)) or not worlds:
        raise ValueError("nonempty ambiguity-set worlds required")
    if any(not isinstance(row, (list, tuple)) or len(row) != NODES
           for row in worlds):
        raise ValueError("every hypothetical world must contain 21 nodes")
    if any(not _positive_number(x) for row in worlds for x in row):
        raise ValueError("hypothetical costs must be positive and finite")
    greedy = min(range(NODES), key=lambda j: (nominal[j], j))
    world_minima = [min(row) for row in worlds]
    missed = [max(int(row[j] > deadline_ms) for row in worlds)
              for j in range(NODES)]
    regret = [max(row[j] - low for row, low in zip(worlds, world_minima))
              for j in range(NODES)]
    j = min(range(NODES), key=lambda k: (missed[k], regret[k], nominal[k], k))
    return Selection(
        node=j,
        nominal_greedy_node=greedy,
        worst_case_deadline_miss=missed[j],
        worst_case_latency_regret_ms=regret[j],
        robust_feasible_in_given_worlds=(missed[j] == 0),
        switched_from_nominal=(j != greedy),
        hypothetical_world_count=len(worlds),
    )
