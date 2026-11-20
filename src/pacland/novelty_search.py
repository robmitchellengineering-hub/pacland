"""novelty_search.py — automated candidate generation: derive novel predictions from constraint intersections.

The loop: for each PAIR of constraints from SEPARATE fields, derive the forced prediction; then the novelty
check (a web search) settles known-vs-novel. This module generates the candidates; the search is run on each
until one comes back novel.
"""
from __future__ import annotations

import math


def _gini_exponential() -> float:
    """The Gini coefficient of a pure exponential (Boltzmann) distribution — a forced number."""
    # For P(w) = (1/T)e^{−w/T}, the Gini is EXACTLY 1/2 (the Lorenz curve is analytic).
    return 0.5


def candidates() -> list[dict]:
    out = []
    # 1. inventory (leaky integrator) × wealth (Boltzmann): the inventory's "temperature" = D/θ.
    D, theta = 10.0, 0.2
    out.append({
        "intersection": "inventory (leaky integrator) × wealth (Boltzmann)",
        "prediction": "the equilibrium inventory level is the fluctuation-dissipation balance I* = D/θ "
                      "(demand ÷ spoilage), the direct analog of the Boltzmann temperature",
        "specific": f"I* = {D/theta:.0f} at demand {D}, spoilage {theta}",
        "novelty_prior": "high — inventory theory and econophysics are separate literatures",
    })
    # 2. Gini (entropy) × wealth (Boltzmann): the Gini of a pure exponential is 1/2.
    out.append({
        "intersection": "Gini (entropy) × wealth (Boltzmann)",
        "prediction": "a pure-thermal (conservation-only) economy has Gini = 1/2 exactly; the observed "
                      "deviation from 0.5 is entirely the Pareto (super-rich) tail's contribution",
        "specific": f"G = {_gini_exponential()}",
        "novelty_prior": "medium — the Gini of the exponential is a known number, but its use as a "
                         "pure-thermal baseline for the tail's contribution is less standard",
    })
    # 3. central bank (thermostat) × inventory (leaky integrator): the same stability criterion.
    out.append({
        "intersection": "central bank (thermostat) × inventory (leaky integrator)",
        "prediction": "monetary policy and inventory control have the SAME stability bound: the feedback "
                      "gain must exceed the leak rate (k > θ) or the system overshoots — one criterion "
                      "for two disciplines",
        "specific": "stable iff k > θ (the same first-order stability condition)",
        "novelty_prior": "high — control-theory economics and inventory control are separate literatures",
    })
    # 4. Phillips (isotherm) × quantity theory (ideal gas): the economic temperature is shared.
    out.append({
        "intersection": "Phillips (isotherm) × quantity theory (ideal gas)",
        "prediction": "the velocity V (the 'temperature' in MV=PY) and the inflation 'temperature' in "
                      "the Phillips hyperbola are the SAME intensive variable — forcing a relation "
                      "between V, π, and u",
        "specific": "V is the shared 'temperature' of both the price level and the inflation rate",
        "novelty_prior": "medium — the Saslow thermal-macro analogy is known, but the Phillips↔velocity "
                         "coupling is not standard",
    })
    return out
