#!/usr/bin/env python3
"""Stage51 transparent queue-pressure comparator; NOT original DFAQ-LB.

Inputs must already exist at issue-time. No scenario, affected-node or task
future / ground truth is accepted by this pure function.
"""
import math

NODES = 21
ALPHA = 0.5
MAX_QUEUE_PENALTY_MS = 20.0
MAX_E2E_PENALTY_MS = 20.0
QUEUE_ONLY = "QUEUE_PRESSURE_05"
QUEUE_E2E = "QUEUE_PRESSURE_E2E_05"
POLICIES = (QUEUE_ONLY, QUEUE_E2E)


def choose(pred, virtual_backlog_ms, delayed_e2e_penalty_ms, policy):
    """Return (node_id, queue_penalty_at_choice, delivered_e2e_penalty_at_choice)."""
    if policy not in POLICIES:
        raise ValueError("unknown baseline")
    if not all(len(x) == NODES for x in (pred, virtual_backlog_ms, delayed_e2e_penalty_ms)):
        raise ValueError("requires 21 nodes")
    if not all(math.isfinite(x) and x > 0 for x in pred):
        raise ValueError("predicted latency must be positive and finite")
    for values in (virtual_backlog_ms, delayed_e2e_penalty_ms):
        if not all(math.isfinite(x) and x >= 0 for x in values):
            raise ValueError("issue-time backlog/feedback must be finite nonnegative")
    q = [min(MAX_QUEUE_PENALTY_MS, ALPHA * x) for x in virtual_backlog_ms]
    e2e = ([min(MAX_E2E_PENALTY_MS, x) for x in delayed_e2e_penalty_ms]
           if policy == QUEUE_E2E else [0.0] * NODES)
    best = min(range(NODES), key=lambda j: (pred[j] + q[j] + e2e[j], j))
    return best, q[best], e2e[best]
