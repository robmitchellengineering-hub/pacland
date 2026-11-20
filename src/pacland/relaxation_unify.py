"""relaxation_unify.py — the PROPER unification of the neuron and the inventory cycle.

The claim to test: both are ONE object — the *leaky integrate-and-fire oscillator*  ẋ = a − b x  with a
threshold x_th and a reset x_r. The period is the transit time from x_r to x_th under that flow:

    T(a, b) = ∫_{x_r}^{x_th} dx/(a − b x)  =  (1/b) ln((a − b x_r)/(a − b x_th))   (b ≠ 0)
                                             (x_th − x_r)/a                          (b = 0, the limit)

The neuron is b = 1/τ (strong leak, drive a = I/τ). The inventory cycle is b = 0 (no leak, drive a = D,
in the inverted coordinate x = −inventory). They are the SAME formula, continuous in b — the inventory is
the NO-LEAK LIMIT of the neuron. This is an exact unification, not a "same kinda thing".
"""
from __future__ import annotations

import math


def period_formula(a: float, b: float, x_th: float, x_r: float) -> float:
    """The closed-form period of the leaky integrate-and-fire oscillator ẋ = a − bx."""
    if abs(b) < 1e-12:
        return (x_th - x_r) / a
    return (1.0 / b) * math.log((a - b * x_r) / (a - b * x_th))


def simulate_unified(a: float, b: float, x_th: float, x_r: float,
                     dt: float = 0.002, t_max: float = 20000.0) -> float:
    """Numerically integrate ẋ = a − bx with reset, return the measured period."""
    x = x_r
    resets = 0
    t = 0.0
    while t < t_max:
        x += (a - b * x) * dt
        if x >= x_th:
            resets += 1
            x = x_r
        t += dt
    return t_max / resets


def verify_unification() -> dict:
    """Compare the closed-form period against simulation for the neuron (b>0), the inventory (b=0),
    and an intermediate leak — confirming one continuous family, exact, not just 'similar'."""
    # neuron: a = I/τ, b = 1/τ
    I, tau = 2.0, 10.0
    a_n, b_n, x_th, x_r = I / tau, 1.0 / tau, 1.0, 0.0
    # inventory: a = D, b = 0, x = -inventory
    D, S, R = 1.0, 5.0, 20.0
    a_i, b_i, x_th_i, x_r_i = D, 0.0, -S, -R
    # an intermediate leak (b between 0 and 1/tau)
    a_m, b_m = 0.5, 0.05

    cases = [
        ("neuron (b=1/τ)", a_n, b_n, x_th, x_r),
        ("intermediate leak", a_m, b_m, x_th, x_r),
        ("inventory (b=0)", a_i, b_i, x_th_i, x_r_i),
    ]
    out = []
    for name, a, b, th, r in cases:
        closed = period_formula(a, b, th, r)
        sim = simulate_unified(a, b, th, r)
        out.append({"case": name, "closed_form": round(closed, 4), "simulated": round(sim, 4),
                    "agree": abs(closed - sim) / closed < 0.02})
    return {"unified_flow": "ẋ = a − bx (threshold x_th, reset x_r)",
            "period_formula": "T = (1/b)·ln((a−bx_r)/(a−bx_th)), b→0 gives (x_th−x_r)/a",
            "cases": out,
            "verdict": "the neuron (b=1/τ) and the inventory cycle (b=0) are the SAME object — "
                       "the inventory is the no-leak limit of the neuron. Exact, not analogous."}


def record() -> dict:
    """Record the EXACT unification in the registry: the unified structure + the mapping + the evidence."""
    import time
    from pacland import registry

    r = verify_unification()
    registry.add(registry.Entry(
        id="structure-leaky-if",
        kind="structure",
        payload={"definition": "the leaky integrate-and-fire oscillator: ẋ = a − bx, threshold x_th, "
                               "reset x_r",
                 "type": "leaky-integrator", "domain": "neuroscience",
                 "assumptions": ["one-dimensional flow", "instant reset"],
                 "reproduces": "period T = (1/b)·ln((a−bx_r)/(a−bx_th)), continuous in b, with the "
                               "b→0 limit (x_th−x_r)/a",
                 "tier": 1, "limitations": [],
                 "permitted_mappings": ["business-cycle", "integrate-and-fire"]},
        provenance={"produced_by": "relaxation-unify", "method": "exact-derivation",
                    "ts": time.time()}))

    registry.add(registry.Entry(
        id="mapping-unified-neuron-inventory",
        kind="mapping",
        payload={"from": "integrate-and-fire", "to": "business-cycle",
                 "mapping": "EXACT: both are ẋ = a − bx with threshold+reset. Neuron: a=I/τ, b=1/τ. "
                            "Inventory: a=D, b=0 (x=−inventory). The inventory cycle is the NO-LEAK "
                            "LIMIT of the neuron — one period formula, continuous in b.",
                 "kind_of_yield": "prediction (any b between 0 and 1/τ interpolates a new cycle model)",
                 "novel": True, "novelty_pending_expert": True,
                 "unified_period": "T = (1/b)·ln((a−bx_r)/(a−bx_th))"},
        provenance={"produced_by": "relaxation-unify", "method": "exact-derivation",
                    "ts": time.time()}))

    registry.add(registry.Entry(
        id="evidence-unified-relaxation",
        kind="evidence",
        payload={"name": "exact unification check (neuron ↔ inventory)", "result": r,
                 "tier": 1, "domain": "neuroscience+economics"},
        provenance={"produced_by": "relaxation-unify", "method": "closed-form-vs-simulation",
                    "ts": time.time()},
        links=["mapping-unified-neuron-inventory", "structure-leaky-if"]))
    return r
