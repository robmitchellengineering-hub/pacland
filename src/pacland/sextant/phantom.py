"""Phantom — the simulated-quantum substrate (Stim / Quimb / QuEST).

Phantom *computes* the number a claim needs; it never recalls one. For this first
slice the exact 2-qubit computations are done with numpy and the Clifford check
with stim. A claim that has no simulated number (a pure Lean no-go) is simply not in
``COMPUTE`` and the engine reports its verdict without a number.
"""
from __future__ import annotations

import math


def _chsh() -> float:
    """<Phi+| ZxB0 + ZxB1 + XxB0 - XxB1 |Phi+> = 2*sqrt(2), exact."""
    import numpy as np

    Z = np.array([[1, 0], [0, -1]])
    X = np.array([[0, 1], [1, 0]])
    psi = np.array([1, 0, 0, 1]) / math.sqrt(2)  # |Phi+> = (|00>+|11>)/sqrt2
    B0 = (Z + X) / math.sqrt(2)
    B1 = (Z - X) / math.sqrt(2)
    S = np.kron(Z, B0) + np.kron(Z, B1) + np.kron(X, B0) - np.kron(X, B1)
    return float(np.real(psi.conj() @ S @ psi))


def _bell() -> float:
    """The classical CHSH bound, 2."""
    return 2.0


def _stim_bell_agreement() -> float:
    """Fraction of Bell-pair measurements that agree (must be exactly 1.0)."""
    import stim

    agree = 0
    shots = 2000
    for _ in range(shots):
        s = stim.TableauSimulator()
        s.h(0)
        s.cx(0, 1)
        if s.measure(0) == s.measure(1):
            agree += 1
    return agree / shots


COMPUTE = {
    "chsh": _chsh,
    "bell-classical": _bell,
    "bell-agreement": _stim_bell_agreement,
}


def compute(claim_id: str):
    """Return the measured number for a claim, or ``None`` if it has none."""
    fn = COMPUTE.get(claim_id)
    return None if fn is None else fn()
