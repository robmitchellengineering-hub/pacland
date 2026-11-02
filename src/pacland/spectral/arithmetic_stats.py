"""Do the landscape's statistical arguments assume a universality their own objects break?

BGS says a chaotic system's spectrum shows random-matrix statistics (GOE, ratio ~0.5307) while an integrable
one shows Poisson (~0.386). But the theorem is **false for arithmetic systems**, which are "too symmetric" and
give intermediate statistics instead (arithmetic quantum unique ergodicity). Every object this estate studies is
arithmetic: integral flux lattices, zeta zeros, the modular surface, toric intersection numbers.

So the claim worth testing: **the statistical arguments used on the string landscape rest on a universality that
arithmetic objects violate**, and the size of that violation is measurable here.

Three spectra, same size, same statistic:

    zeta zeros            the arithmetic spectrum par excellence
    n^2 + m^2 (distinct)  a genuinely arithmetic lattice spectrum, computable in closed form
    uniform random        the control: what "no structure" looks like at this size

If the two arithmetic spectra sit away from both references while the random control sits at Poisson, then
quoting BGS for an arithmetic object is unsound until the correction is measured.

Run:        python3 scripts/arithmetic_stats.py
Guarded by: tests/test_arithmetic_stats.py
"""
from __future__ import annotations

import math
import random

#: References for the Oganesyan-Huse ratio statistic.
RATIO_POISSON = 0.386
RATIO_GOE = 0.5307


def ratio(values) -> float:
    """The mean ratio of adjacent spacings — Poisson ~0.386, GOE ~0.5307."""
    v = sorted(values)
    gaps = [b - a for a, b in zip(v, v[1:]) if b > a]
    rs = []
    for a, b in zip(gaps, gaps[1:]):
        lo, hi = min(a, b), max(a, b)
        if hi > 0:
            rs.append(lo / hi)
    return sum(rs) / len(rs) if rs else float("nan")


def zeta_zeros(n: int = 400, dps: int = 20) -> list:
    """The first `n` nontrivial zeros, from mpmath (arithmetic, not random)."""
    import mpmath as mp

    mp.mp.dps = dps
    return [float(mp.zetazero(k).imag) for k in range(1, n + 1)]


def sums_of_two_squares(limit: int) -> list:
    """Distinct `n^2 + m^2 <= limit` — a lattice spectrum with closed-form structure."""
    s = set()
    m = 0
    while m * m <= limit:
        n = 0
        while m * m + n * n <= limit:
            s.add(m * m + n * n)
            n += 1
        m += 1
    return sorted(s)


def uniform_control(n: int, seed: int = 7, spread: float = 1.0) -> list:
    """Sorted uniforms — the 'no structure' control at the same count."""
    rng = random.Random(seed)
    return sorted(rng.uniform(0, spread * n) for _ in range(n))


def nearest_reference(r: float) -> tuple:
    """Which reference the statistic sits closer to, and by how much."""
    d_p, d_g = abs(r - RATIO_POISSON), abs(r - RATIO_GOE)
    return ("Poisson" if d_p <= d_g else "GOE", min(d_p, d_g))


def table(n: int = 400) -> list:
    """The three spectra side by side."""
    rows = []
    for name, vals, kind in (
        ("zeta zeros", zeta_zeros(n), "arithmetic"),
        ("n^2 + m^2 (distinct)", sums_of_two_squares(n * n // 4)[:n], "arithmetic"),
        ("uniform random (control)", uniform_control(n), "control"),
    ):
        r = ratio(vals)
        ref, gap = nearest_reference(r)
        rows.append({"spectrum": name, "kind": kind, "n": len(vals), "ratio": r,
                     "nearest": ref, "gap": gap})
    return rows


def verdict(rows=None) -> dict:
    rows = rows or table()
    ctrl = next(r for r in rows if r["kind"] == "control")
    arith = [r for r in rows if r["kind"] == "arithmetic"]
    deviates = [r for r in arith if abs(r["ratio"] - ctrl["ratio"]) > 0.05]
    return {
        "rows": rows,
        "control_ratio": ctrl["ratio"],
        "control_sits_at": nearest_reference(ctrl["ratio"])[0],
        "arithmetic_deviating": [r["spectrum"] for r in deviates],
        "claim": ("the arithmetic spectra deviate from the random control, so BGS universality cannot be "
                  "quoted for them without a measured correction"
                  if deviates else
                  "the arithmetic spectra sit with the random control at this size: no deviation measured"),
    }


__all__ = ["RATIO_POISSON", "RATIO_GOE", "ratio", "zeta_zeros", "sums_of_two_squares",
           "uniform_control", "nearest_reference", "table", "verdict"]
