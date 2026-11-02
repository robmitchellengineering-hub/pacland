"""Padgett's intuition, made testable: primes as an interference pattern.

The papers' object is `I_PA(theta) = sum_{p in PA} exp(i p theta)` with **PA never defined**. This module does
the only thing that can be done with an undefined set: enumerate defensible definitions, and for each ask the
two questions that have standards of truth.

1. **Growth.** A random superposition grows like `sqrt(n)`; the exponent of `|S_k|` against `k` is 0.5. A set
   with real structure deviates from 0.5. `all odd numbers` is the control: if a definition matches it, the
   "primes" part did no work.
2. **Spacing statistics.** The ratio statistic `r = mean(min(s_i, s_{i+1}) / max(...))` on the set's own
   spacings: Poisson (integrable) ~ 0.386, GOE (chaotic) ~ 0.5307. A set whose spacings sit at Poisson is not a
   spectrum; one that repels is.

**The verdict is a table, not an opinion.** If every definition collapses to the control, the intuition has no
mathematical content in this form — a real negative. If one deviates, it is an object.

Run:        python3 scripts/prime_interference.py
Guarded by: tests/test_prime_interference.py
"""
from __future__ import annotations

import math

#: Poisson and GOE reference values for the ratio statistic (measured elsewhere in this repo).
RATIO_POISSON = 0.386
RATIO_GOE = 0.5307


def primes_upto(n: int) -> list:
    sieve = bytearray([1]) * (n + 1)
    sieve[0:2] = b"\x00\x00"
    for i in range(2, int(n ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = bytearray(len(sieve[i * i::i]))
    return [i for i in range(n + 1) if sieve[i]]


def _emirp(p: int) -> bool:
    r = int(str(p)[::-1])
    return r != p and r > 1 and all(r % d for d in range(2, int(r ** 0.5) + 1))


def definitions(n: int) -> dict:
    """Six defensible readings of "asymmetric primes", plus the null control."""
    P = primes_upto(n)
    return {
        "all primes": P,
        "primes = 1 mod 4": [p for p in P if p % 4 == 1],
        "primes = 3 mod 4": [p for p in P if p % 4 == 3],
        "emirps (p and reverse(p) prime)": [p for p in P if _emirp(p)],
        "primes containing digit 7": [p for p in P if "7" in str(p)],
        "twin-prime members": [p for p in P if (p + 2 in P) or (p - 2 in P)],
        "ALL ODD NUMBERS (control)": [k for k in range(3, n + 1, 2)],
    }


def growth_exponent(values, theta: float = 1.0) -> float:
    """Fit log|S_k| against log k — 0.5 means a random walk, >0.5 means structure survives."""
    s = 0j
    xs, ys = [], []
    for k, v in enumerate(values, start=2):
        s += complex(math.cos(theta * v), math.sin(theta * v))
        if k % max(1, len(values) // 200) == 0 and abs(s) > 0:
            xs.append(math.log(k)); ys.append(math.log(abs(s)))
    if len(xs) < 5:
        return float("nan")
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = sum((x - mx) ** 2 for x in xs)
    return num / den if den else float("nan")


def ratio_statistic(values) -> float:
    """Oganesyan-Huse ratio on the set's own spacings: Poisson ~0.386, GOE ~0.5307."""
    gaps = [b - a for a, b in zip(values, values[1:]) if b > a]
    rs = []
    for a, b in zip(gaps, gaps[1:]):
        lo, hi = min(a, b), max(a, b)
        if hi > 0:
            rs.append(lo / hi)
    return sum(rs) / len(rs) if rs else float("nan")


def table(n: int = 20000, theta: float = 1.0) -> list:
    rows = []
    for name, P in definitions(n).items():
        rows.append({
            "definition": name, "n": len(P),
            "growth": growth_exponent(P, theta),
            "ratio": ratio_statistic(P),
        })
    return rows


def verdicts(rows=None, growth_tol: float = 0.10, ratio_tol: float = 0.03) -> list:
    """Label each definition against the control and the random-matrix references."""
    rows = rows or table()
    control = next(r for r in rows if "control" in r["definition"].lower())
    out = []
    for r in rows:
        dg = r["growth"] - control["growth"]
        dr = r["ratio"] - control["ratio"]
        if "control" in r["definition"].lower():
            v = "control"
        elif abs(dg) <= growth_tol and abs(dr) <= ratio_tol:
            v = "matches the control — the prime property does no work"
        elif abs(r["growth"] - 0.5) <= growth_tol:
            v = "random-walk growth — no structure"
        else:
            v = "DEVIATES — worth a closer look"
        out.append({**r, "vs_control_growth": dg, "verdict": v})
    return out




def walk_ratio(values, theta: float = 1.0, at=(400, 1600, 6400)) -> list:
    """`|S_k| / sqrt(k)` at stated cut-offs — the doc's own instrument.

    A random superposition gives O(1) values that neither grow nor vanish. This is a better estimator than a
    log-log fit: the fit mixes in the early transient and reported exponents from 0.02 to 0.72 on sets whose
    behaviour is the same in kind.
    """
    out, s = [], 0j
    targets = set(t for t in at if t <= len(values))
    for k, v in enumerate(values, start=1):
        s += complex(math.cos(theta * v), math.sin(theta * v))
        if k in targets:
            out.append((k, abs(s) / math.sqrt(k)))
    return out

__all__ = ["walk_ratio", "primes_upto", "definitions", "growth_exponent", "ratio_statistic", "table", "verdicts",
           "RATIO_POISSON", "RATIO_GOE"]
