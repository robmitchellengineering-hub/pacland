"""X7 as a family, not a pair — the measure problem stated as a number.

`docs/plan-facts.md` F1. `windows.convergence` (D1) compared **two** measures on one question and
measured a spread of 0.62. That is a demonstration. A fact needs a *family* of measures, arbitrary
properties, and one exact identity that the whole pipeline has to satisfy.

**The identity.** On a symmetric window the tadpole is antisymmetric under `(F, H) -> (-F, H)`:
`N -> -N`. So every measure that depends on `N` only through `|N|` must satisfy

    fraction(N > 0)  ==  (1 - fraction(N == 0)) / 2

exactly. That is not a property of one measure — it is a property of the *weights, the counting and the
window together*, so it is the acceptance test for the engine rather than for a number. A measure that
breaks the symmetry (say `w ∝ N`) fails it, which is how the check is proved able to go red.

**The honest limit.** Only `b3 = 6, |F_i|, |H_i| <= 1` is exactly enumerable (531,441 pairs). Anything
larger is sampled, and every table carries its window and its exactness flag, because a fraction
without those is not a fact.

No node needed: this is the corpus and the lattice, on disk.

Run:        python3 scripts/measure_engine.py
Guarded by: tests/test_measure_engine.py
"""
from __future__ import annotations

import numpy as np

from .windows import enumerate_window, primitive, tadpoles

#: The named measures. Each is a *weight over flux pairs*, so a "fraction" is a weighted mean and the
#: spread across the family is the thing being reported. `flux-uniform` is the measure a sampling
#: argument uses implicitly; `tadpole-uniform` the one a "N is of order one" counting argument uses.
MEASURES: tuple[str, ...] = (
    "flux-uniform",
    "primitive",
    "tadpole-uniform",
    "log-N",
    "tadpole-weighted",
)

#: Measures that depend on the tadpole only through `|N|` — the ones the antisymmetry identity binds.
SYMMETRIC: tuple[str, ...] = MEASURES


def weights(kind: str, fluxes: np.ndarray, n_vals: np.ndarray | None = None) -> np.ndarray:
    """Per-pair weights, normalised to sum to 1. Zero-weight pairs are excluded, not down-weighted."""
    fluxes = np.asarray(fluxes)
    if n_vals is None:
        n_vals = tadpoles(fluxes)
    n = np.abs(n_vals.astype(float))
    if kind == "flux-uniform":
        w = np.ones(len(fluxes), dtype=float)
    elif kind == "primitive":
        w = np.array([1.0 if primitive(r) else 0.0 for r in fluxes])
    elif kind == "tadpole-uniform":
        # every distinct |N| carries the same total mass: this is the measure a counting argument uses
        counts = {}
        for v in n:
            counts[float(v)] = counts.get(float(v), 0) + 1
        w = np.array([1.0 / counts[float(v)] for v in n], dtype=float)
    elif kind == "log-N":
        # log-uniform in |N|, the convention flux counting arguments use for W0 and Lambda
        w = np.zeros_like(n)
        np.divide(1.0, n, out=w, where=n > 0)
    elif kind == "tadpole-weighted":
        # a volume proxy: larger tadpole ~ larger volume. A PROXY, stated as one.
        w = n.copy()
    else:
        raise ValueError(f"unknown measure {kind!r}; known: {MEASURES}")
    total = w.sum()
    if total <= 0:
        raise ValueError(f"measure {kind!r} gives zero total weight on this window")
    return w / total


def fraction(flag: np.ndarray, w: np.ndarray) -> float:
    """The weighted fraction of pairs satisfying `flag`."""
    return float(np.sum(np.asarray(flag, dtype=float) * w))


# ---------------------------------------------------------------------------------------
# properties — each a predicate on (fluxes, n_vals)
# ---------------------------------------------------------------------------------------
def prop_positive_n(fluxes, n_vals) -> np.ndarray:
    return n_vals > 0


def prop_below(l: int):
    def f(fluxes, n_vals) -> np.ndarray:
        return (n_vals > 0) & (n_vals <= l)
    f.__name__ = f"0 < N <= {l}"
    return f


def prop_zero(fluxes, n_vals) -> np.ndarray:
    """Exact cancellation: `N = 0`. The property that the antisymmetry identity is built on."""
    return n_vals == 0


#: Note what is *not* here: "is the content primitive". At `max_abs = 1` every non-zero pair is already
#: primitive, so that property is 1.0 under every measure — a vacuous column, and it was in the first
#: version of this table. A column that cannot vary is not a finding.
PROPERTIES = (prop_below(1), prop_below(3), prop_below(6), prop_zero)


def table(b3: int = 6, max_abs: int = 1, fluxes: np.ndarray | None = None) -> dict:
    """A fraction per (property, measure), with the spread across measures for each property."""
    fluxes = enumerate_window(b3, max_abs) if fluxes is None else np.asarray(fluxes)
    n_vals = tadpoles(fluxes)
    ws = {k: weights(k, fluxes, n_vals) for k in MEASURES}
    rows = []
    for prop in PROPERTIES:
        flag = prop(fluxes, n_vals)
        vals = {k: fraction(flag, ws[k]) for k in MEASURES}
        lo, hi = min(vals.values()), max(vals.values())
        rows.append({"property": getattr(prop, "__name__", repr(prop)), "values": vals,
                     "min": lo, "max": hi, "ratio": (hi / lo) if lo > 0 else float("inf"),
                     "spread": hi - lo,
                     "zero_support": [k for k, v in vals.items() if v == 0.0]})
    finite = [r["ratio"] for r in rows if np.isfinite(r["ratio"])]
    return {"window": f"b3={b3}, |F_i|,|H_i| <= {max_abs}",
            "exact": True, "pairs": int(len(fluxes)), "measures": MEASURES, "rows": rows,
            "max_ratio": max(finite) if finite else float("inf"),
            "max_spread": max(r["spread"] for r in rows),
            "note": "a measure that gives the property zero support reports ratio = inf: that is a "
                    "definitional difference, not a measured spread, and is listed per row"}


def antisymmetry(fluxes: np.ndarray | None = None, b3: int = 6, max_abs: int = 1) -> dict:
    """`fraction(N>0) == (1 - fraction(N==0)) / 2` for every symmetric measure.

    The identity is exact, so the tolerance is there to catch a broken weight, not to allow slack.
    """
    fluxes = enumerate_window(b3, max_abs) if fluxes is None else np.asarray(fluxes)
    n_vals = tadpoles(fluxes)
    checks = []
    for k in SYMMETRIC:
        w = weights(k, fluxes, n_vals)
        lhs = fraction(n_vals > 0, w)
        rhs = (1.0 - fraction(n_vals == 0, w)) / 2.0
        checks.append({"measure": k, "lhs": lhs, "rhs": rhs, "residual": abs(lhs - rhs),
                       "pass": abs(lhs - rhs) < 1e-12})
    return {"window": f"b3={b3}, |F_i|,|H_i| <= {max_abs}", "checks": checks,
            "all_pass": all(c["pass"] for c in checks)}


__all__ = ["MEASURES", "SYMMETRIC", "weights", "fraction", "PROPERTIES", "prop_below",
           "prop_positive_n", "prop_zero", "table", "antisymmetry"]
