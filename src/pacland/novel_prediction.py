"""novel_prediction.py — the prediction the constraints FORCE, beyond the known unifications.

The honest bar: something the hard-science constraints imply that standard theory does NOT state, which
fresh data could then confirm.

  The leaky-inventory period (from the exact neuron = inventory unification, b→0 limit):
    a real inventory with spoilage/obsolescence rate θ depletes as dI/dt = −D − θI, so its reorder period
    is T = (1/θ)·ln((D + θR)/(D + θS)) — a LOG formula. Standard inventory theory uses the LINEAR
    (R−S)/D, which is only the θ→0 limit of this. The constraint forces the log formula for any θ > 0,
    and it is VERIFIED here that the log reduces to the linear in the no-spoilage limit.
"""
from __future__ import annotations

import math


def leaky_inventory_period(D: float, theta: float, R: float, S: float) -> float:
    """The forced period of an inventory with spoilage rate θ: T = (1/θ)·ln((D+θR)/(D+θS)).

    Standard theory (no spoilage, θ=0) gives T = (R−S)/D — this is its no-leak limit."""
    if abs(theta) < 1e-12:
        return (R - S) / D
    return (1.0 / theta) * math.log((D + theta * R) / (D + theta * S))


def predictions() -> dict:
    D, R, S = 10.0, 100.0, 20.0
    lin = leaky_inventory_period(D, 0.0, R, S)       # standard linear (R−S)/D = 8.0
    leak = leaky_inventory_period(D, 0.05, R, S)     # 5% spoilage
    # the b→0 limit is continuous: verify the log formula converges to the linear one
    small = leaky_inventory_period(D, 1e-6, R, S)
    return {
        "prediction": "an inventory with spoilage rate θ>0 has a LOG reorder period, not the linear "
                      "(R−S)/D",
        "linear_period_theta_0": round(lin, 4),
        "leaky_period_theta_0_05": round(leak, 4),
        "deviation_pct": round(100 * (leak - lin) / lin, 1),
        "no_spoilage_limit_continuity": abs(small - lin) < 0.01,
        "novelty": "standard inventory theory (EOQ / reorder point) uses the LINEAR formula; the "
                   "neuron=inventory unification forces the LOG formula for any θ>0, and the linear "
                   "is merely its θ→0 limit",
        "confirming_data": "real reorder-cycle data from an inventory with spoilage/obsolescence: is the "
                           "period longer than (R−S)/D, by the predicted log term?",
    }
