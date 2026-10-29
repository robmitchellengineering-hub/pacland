"""X7 — the finite window: below a bound the flux lattice is finite, so enumeration is exact.

Two uses, and they are different questions:

**A4 — coverage.** The corpus is a *heuristic* sample (the ISD proposal). Its recall has never been
measured, and every "fraction of vacua" sentence silently assumes it is complete. In the smallest
window the truth is enumerable, so the comparison is exact: which primitive orbits in
`|F_i|, |H_i| <= 1` does the corpus contain? A window the sampler never visits is the point.

**D1 — the measure statement.** `docs/quantum-arm-agenda.md` Q3 and Q5 end at "this may be a measure
question". With a finite lattice, a fraction is exact and reproducible — so the interesting number is
not the fraction but **how far it moves between two reasonable measures** (uniform over all flux pairs
vs uniform over primitive pairs). If it moves, the "10^500 vacua" argument is a statement about the
measure. That is demonstrable, and this module is where the demonstration comes from.

Every report prints the **window** it was computed in. A fraction without its window is not a fact.

Run:        python3 scripts/exactness.py
Guarded by: tests/test_exactness_windows.py
"""
from __future__ import annotations

import itertools
import math

import numpy as np


def primitive(values) -> bool:
    g = 0
    for v in values:
        g = math.gcd(g, int(v))
    return g == 1


def primitive_key(flux) -> tuple[int, ...]:
    """The scaling class of a flux pair: `(F, H)` and `d(F, H)` are the same vacuum."""
    v = [int(round(float(x))) for x in flux]
    g = 0
    for x in v:
        g = math.gcd(g, x)
    if g == 0:
        return tuple(v)
    return tuple(x // g for x in v)


_ENUM_CACHE: dict[tuple[int, int], np.ndarray] = {}


def enumerate_window(b3: int, max_abs: int = 1) -> np.ndarray:
    """Every integral `(F, H)` pair with `|component| <= max_abs`. Shape `(m, 2*b3)`, cached."""
    key = (b3, max_abs)
    if key not in _ENUM_CACHE:
        span = range(-max_abs, max_abs + 1)
        rows = list(itertools.product(span, repeat=2 * b3))
        _ENUM_CACHE[key] = np.asarray(rows, dtype=np.int64)
    return _ENUM_CACHE[key]


def tadpoles(fluxes: np.ndarray) -> np.ndarray:
    """`N = F^T J H` for every row of an `(m, 2*b3)` array, vectorised."""
    fluxes = np.asarray(fluxes, dtype=np.int64)
    b3 = fluxes.shape[1] // 2
    n = b3 // 2
    f = fluxes[:, :b3]
    h = fluxes[:, b3:]
    return (f[:, :n] * h[:, n:] - f[:, n:] * h[:, :n]).sum(axis=1)


def window_report(b3: int, max_abs: int = 1, fluxes: np.ndarray | None = None) -> dict:
    """The exact census of one window: counts, the tadpole spectrum, and the two measures."""
    fluxes = enumerate_window(b3, max_abs) if fluxes is None else np.asarray(fluxes)
    n_vals = tadpoles(fluxes)
    prim = np.array([primitive(r) for r in fluxes])
    all_nonzero = n_vals > 0
    return {
        "window": f"b3={b3}, |F_i|,|H_i| <= {max_abs}",
        "pairs": int(len(fluxes)),
        "primitive_pairs": int(prim.sum()),
        "pairs_with_N_gt_0": int(all_nonzero.sum()),
        "primitive_pairs_with_N_gt_0": int((prim & all_nonzero).sum()),
        "N_min": int(n_vals.min()), "N_max": int(n_vals.max()),
        "distinct_N": int(len(set(int(x) for x in n_vals))),
    }


def convergence(b3: int, bounds: list[int], max_abs: int = 1,
                fluxes: np.ndarray | None = None) -> dict:
    """The fraction with `0 < N <= L` under two measures, at each bound. This is the D1 artefact.

    **Measure 1, flux-uniform**: every integral flux pair in the window counts once — the measure a
    sampling-based argument implicitly uses.
    **Measure 2, label-uniform**: every distinct tadpole value counts once — the measure a
    "N is of order one, N <= L" counting argument implicitly uses.

    A third column keeps the flux-uniform count restricted to *primitive* pairs. At `max_abs = 1` it
    is identical to measure 1, because every non-zero pair in that window is already primitive: the
    obvious pair of measures (all vs primitive) is empty there, and saying so is part of the result.
    """
    fluxes = enumerate_window(b3, max_abs) if fluxes is None else np.asarray(fluxes)
    n_vals = tadpoles(fluxes)
    prim = np.array([primitive(r) for r in fluxes])
    n_all = len(fluxes)
    positive = sorted({int(x) for x in n_vals if x > 0})
    n_labels = max(len(positive), 1)
    table = []
    for l in bounds:
        f_flux = float(((n_vals > 0) & (n_vals <= l)).sum()) / max(n_all, 1)
        f_label = sum(1 for x in positive if x <= l) / n_labels
        f_prim = float(((n_vals > 0) & (n_vals <= l) & prim).sum()) / max(int(prim.sum()), 1)
        table.append({"L": int(l), "fraction_all_pairs": f_flux, "fraction_label_uniform": f_label,
                      "fraction_primitive_pairs": f_prim,
                      "ratio_measures": (f_flux / f_label) if f_label else float("nan")})
    shifts = [abs(t["fraction_all_pairs"] - t["fraction_label_uniform"]) for t in table]
    return {"window": f"b3={b3}, |F_i|,|H_i| <= {max_abs}", "table": table,
            "distinct_positive_N": n_labels,
            "primitive_equals_flux": bool(np.all(prim | (np.abs(fluxes).sum(axis=1) == 0))),
            "max_shift": max(shifts) if shifts else 0.0,
            "measures_agree": bool(shifts and max(shifts) < 0.05)}


def coverage(corpus_fluxes: list, b3: int, max_abs: int = 1,
             fluxes: np.ndarray | None = None) -> dict:
    """Which primitive orbits of the smallest window the corpus actually contains."""
    fluxes = enumerate_window(b3, max_abs) if fluxes is None else np.asarray(fluxes)
    n_vals = tadpoles(fluxes)
    window_keys = {primitive_key(r): int(n) for r, n in zip(fluxes, n_vals)}
    window_orbits = {k for k in window_keys if any(x != 0 for x in k)}
    corpus_keys = {primitive_key(f) for f in corpus_fluxes}
    hit = window_orbits & corpus_keys
    norms = [max(abs(int(round(float(x)))) for x in f) for f in corpus_fluxes] if corpus_fluxes else [0]
    return {
        "window": f"b3={b3}, |F_i|,|H_i| <= {max_abs}",
        "window_orbits": len(window_orbits),
        "corpus_rows": len(corpus_fluxes),
        "corpus_orbits_in_window": len(hit),
        "coverage": (len(hit) / len(window_orbits)) if window_orbits else float("nan"),
        "corpus_max_component": int(max(norms)),
        "examples_uncovered": sorted(window_orbits - corpus_keys)[:5],
    }


__all__ = ["primitive", "primitive_key", "enumerate_window", "tadpoles", "window_report",
           "convergence", "coverage"]
