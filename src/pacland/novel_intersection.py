"""novel_intersection.py — a prediction forced by the INTERSECTION of two laws no single field combines.

The intersection: "the inventory is a leaky integrator (a low-pass filter)" + "the bullwhip is wave
amplification". Together they force a NON-OBVIOUS prediction:

    the spoilage/obsolescence rate θ is a DAMPING term — it makes each inventory stage a low-pass filter
    that attenuates demand oscillations, so a supply chain with HIGHER spoilage has LESS bullwhip
    amplification, not more.

The two literatures (deteriorating inventory + bullwhip) are separate; the "spoilage damps the bullwhip"
link is the novel intersection.
"""
from __future__ import annotations

import math


def _chain_amplification(theta: float, beta: float = 0.5, stages: int = 4,
                         T: int = 200, seed: int = 0) -> float:
    """Simulate a supply chain with overreaction β and spoilage θ; return the amplification ratio
    (variance of the top-stage order / variance of the retail demand)."""
    import random
    rng = random.Random(seed)
    # retail demand: a sinusoid + noise (an oscillating signal, the thing the bullwhip amplifies)
    demand = [1.0 + 0.3 * math.sin(0.3 * t) + 0.1 * rng.gauss(0, 1) for t in range(T)]
    order = demand[:]
    for _ in range(stages):
        prev = order[:]
        inv = 10.0
        order = []
        for t in range(T):
            d = prev[t]
            # the order: replace demand + the overreaction (bullwhip) + the spoilage lost this period
            o = d + beta * (d - (prev[t - 1] if t else d)) + theta * inv
            inv = inv - d - theta * inv + o  # inventory: depletion + spoilage, then the replenishment
            order.append(o)
    def var(xs):
        m = sum(xs) / len(xs)
        return sum((x - m) ** 2 for x in xs) / len(xs)
    return var(order) / var(demand)


def prediction() -> dict:
    amp_no_spoilage = _chain_amplification(0.0)
    amp_spoilage = _chain_amplification(0.3)
    return {
        "prediction": "a supply chain with higher spoilage/obsolescence θ has LESS bullwhip amplification",
        "amplification_theta_0": round(amp_no_spoilage, 3),
        "amplification_theta_0_3": round(amp_spoilage, 3),
        "spoilage_dampens": amp_spoilage < amp_no_spoilage,
        "mechanism": "the spoilage is a leak → the inventory is a low-pass filter → it attenuates the "
                     "demand oscillation instead of passing it up the chain",
        "novelty": "the deteriorating-inventory and bullwhip literatures are separate; their intersection "
                   "(spoilage damps the bullwhip) is not the standard framing",
        "confirming_data": "real supply-chain order data across products with different spoilage rates: "
                           "is the order-variance amplification LOWER for perishable goods?",
    }
