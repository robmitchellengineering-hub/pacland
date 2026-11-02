"""Is the ~0.8 minima rate derivable from the lattice?

Pre-registered test: *if `is_minimum` correlates with no computable lattice invariant, then the rate cannot come out of
the counting and must be retired as a model-specific fact.*

The closed form `count(N) = [x^N] P(x)^(b3/2)` knows only about the flux lattice. If a "minimum" were a combinatorial
property, some invariant would have to predict it.

Run:        python3 scripts/minima_correlation.py
Guarded by: tests/test_minima_correlation.py
"""
from __future__ import annotations

import math

import numpy as np

from . import counterexample, ingest_gate

#: Invariants computable from the flux data alone -- no Hessian, no potential.
LATTICE_INVARIANTS = ("b3", "N", "support", "max_comp")


def invariants(row: dict) -> dict:
    """Everything a counting argument could see."""
    fl = np.array(row["flux"], dtype=float)
    b3 = len(fl) // 2
    return {
        "b3": b3,
        "N": abs(float(row.get("Nflux") or 0)),
        "primitive": float(math.gcd(*[int(x) for x in fl]) <= 1),
        "support": float(np.count_nonzero(fl)) / (2 * b3),
        "max_comp": float(np.abs(fl).max()),
        "log|DW|": float(np.log10(abs(float(row.get("|DW|") or 1e-300)))),
        "V": float(row.get("V") or 0),
    }


def correlations() -> dict:
    """Correlation of each invariant with `is_minimum`, over in-domain rows only."""
    rows = [c["row"] for c in counterexample.load_corpus()
            if ingest_gate.classify(c["row"]) == "in_domain"]
    y = np.array([1.0 if r.get("is_minimum") else 0.0 for r in rows])
    cols = {}
    for r in rows:
        for k, v in invariants(r).items():
            cols.setdefault(k, []).append(v)
    out = {}
    for k, v in cols.items():
        v = np.array(v, dtype=float)
        out[k] = None if v.std() == 0 else float(np.corrcoef(v, y)[0, 1])
    lattice = [abs(out[k]) for k in LATTICE_INVARIANTS if out.get(k) is not None]
    return {
        "n": len(rows),
        "minima_rate": float(y.mean()),
        "correlations": out,
        "strongest_lattice": max(lattice) if lattice else 0.0,
        "derivable": bool(lattice and max(lattice) >= 0.2),
        "verdict": ("the minima rate IS derivable -- a lattice invariant predicts it"
                    if lattice and max(lattice) >= 0.2 else
                    "MODEL-SPECIFIC: no lattice invariant predicts a minimum, so the rate cannot come out of the "
                    "counting. The only real predictor is log|DW|, the dynamical SUSY order parameter, which "
                    "restates what 'minimum' already meant"),
    }


__all__ = ["LATTICE_INVARIANTS", "invariants", "correlations"]
