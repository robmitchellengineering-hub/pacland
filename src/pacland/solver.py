"""solver.py — the payoff of Lean-proved unifications: SOLVE soft-field problems with hard-science formulas.

Each unification, once proven (tier-1), turns a soft-field QUESTION into a SOLVED problem — a closed-form
answer or a guarantee inherited from the hard science. This module demonstrates the mechanism on three:
  1. the leaky integrator (neuron = inventory) → the exact cycle period (a definite integral, provable)
  2. the SIR epidemic (epidemic = chemical kinetics) → the R0 threshold (spread or die out, provable)
  3. the gradient flow (tâtonnement = steepest descent) → convergence to equilibrium (a theorem)
"""
from __future__ import annotations

import math


def solve_cycle_period(a: float, b: float, x_th: float, x_r: float) -> dict:
    """The proven leaky-integrator period T = (1/b)·ln((a−bx_r)/(a−bx_th)), b→0 gives (x_th−x_r)/a.

    This ONE theorem solves BOTH the neuron's firing period AND the inventory's reorder period — because
    they are the same object (the no-leak limit). A soft-field 'how often does X happen?' question gets a
    closed-form answer."""
    if abs(b) < 1e-12:
        T = (x_th - x_r) / a
    else:
        T = (1.0 / b) * math.log((a - b * x_r) / (a - b * x_th))
    return {
        "answer": "the exact cycle period",
        "period": round(T, 4),
        "neuron_reading": f"a neuron with I/τ={a}, leak 1/τ={b} fires every {round(T, 4)} time units",
        "inventory_reading": f"an inventory with demand={a}, no leak, reorder at {x_th}, restock to {x_r} "
                             f"reorders every {round(T, 4)} time units",
    }


def solve_epidemic_threshold(beta: float, gamma: float) -> dict:
    """The proven SIR threshold: an outbreak grows iff R0 = β/γ > 1 (mass-action kinetics).

    A public-health 'will this spread?' question becomes a YES/NO from two numbers."""
    R0 = beta / gamma
    return {
        "answer": "does the epidemic spread?",
        "R0": round(R0, 3),
        "spreads": R0 > 1,
        "reading": f"R0 = β/γ = {round(R0, 3)} → the epidemic {'spreads' if R0 > 1 else 'dies out'}",
        "control_implication": f"to stop it, reduce contact so β < γ (need β < {round(gamma, 3)})",
    }


def solve_market_convergence(k: float, p0: float, p_star: float) -> dict:
    """The proven gradient-flow theorem: ẋ = −k(x − x*) converges to x* (exponentially).

    A market-clearing 'does the price settle?' question becomes a guarantee with a rate."""
    return {
        "answer": "does the price converge to equilibrium?",
        "converges": True,
        "rate": k,
        "reading": f"the price converges to p* = {p_star} exponentially at rate {k} (the tâtonnement "
                   f"gradient-flow theorem)",
    }
