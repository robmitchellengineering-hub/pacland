"""chem_institutions.py — the chemistry↔institutions unification: catalysis = a transaction-cost cut.

The correspondence: an institution (a market, a contract, a standard, a court) is a CATALYST — it lowers the
activation energy of an exchange, so the rate rises by the Arrhenius law, NOT by an elasticity.

    Arrhenius:  rate = A · e^{−E_a/(RT)}
    analog:     transaction rate = A · e^{−C/T}     (C = the transaction cost, T = the 'social temperature')

The specific, testable prediction: the transaction rate responds to a cost reduction EXPONENTIALLY
(Arrhenius), not as a power law (the standard economics elasticity). Halving the cost C multiplies the rate
by e^{C/2T}, a fixed factor independent of the current level — the fingerprint of catalysis.
"""
from __future__ import annotations

import math


def transaction_rate(A: float, C: float, T: float) -> float:
    """The Arrhenius analog: the transaction rate at activation cost C and social temperature T."""
    return A * math.exp(-C / T)


def prediction() -> dict:
    A, T = 1.0, 1.0
    r_full = transaction_rate(A, 1.0, T)      # activation cost C = 1
    r_half = transaction_rate(A, 0.5, T)      # a catalyst halves the cost
    return {
        "prediction": "the transaction rate rises EXPONENTIALLY (Arrhenius) as an institution lowers the "
                      "transaction cost — not as a power-law elasticity",
        "rate_at_cost_1": round(r_full, 4),
        "rate_at_cost_0_5": round(r_half, 4),
        "halving_multiplier": round(r_half / r_full, 2),
        "fingerprint": "the multiplier from halving the cost is a CONSTANT factor (e^{C/2T}), independent "
                       "of the current rate — the signature of catalysis, absent from elasticity",
        "novelty": "economics models cost response as ELASTICITY (power law); the catalysis view forces "
                   "ARRHENIUS (exponential). A test of the functional form is a specific, checkable claim.",
        "confirming_data": "transaction volume vs a measured cost reduction (e.g., a payment-rail fee cut): "
                           "is the volume response exponential or power-law?",
    }
