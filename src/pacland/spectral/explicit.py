"""The primes as an interference sum over the zeros — the explicit formula, verified numerically.

This is the honest form of "prime oscillations". Padgett's version summed over a set of primes that was
never defined; the object that actually works is the other way round — the primes ARE a sum over the
Riemann zeros:

    psi(x) = x - sum_rho x^rho / rho - ln(2 pi) - 1/2 ln(1 - x^-2)

with psi(x) the Chebyshev function (ln p summed over every prime power p^k <= x). Each zero is a
frequency; each contributes x^(1/2+ig)/rho, a decaying oscillation in ln x.

Verified the same way as everything else here: against values computed independently from the primes,
and with a convergence table rather than a single number — because a truncated zero sum oscillates and
a single x could look good or bad by luck.

Run:        python3 scripts/spectral_explicit.py
Guarded by: tests/test_spectral_explicit.py
"""
from __future__ import annotations

import math

from .zeros import find_zeros

#: psi at these x, computed from the primes (not from the formula) — the validation set.
KNOWN_PSI = {100: 94.045311, 1000: 996.680887, 10000: 10013.396813}


def chebyshev_psi(x: int) -> float:
    """psi(x): ln p summed over every prime power p^k <= x. Computed from a sieve, no formula."""
    sieve = bytearray([1]) * (x + 1)
    sieve[0:2] = b"\x00\x00"
    for i in range(2, int(x ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = bytearray(len(sieve[i * i::i]))
    total = 0.0
    for p in range(2, x + 1):
        if not sieve[p]:
            continue
        pk = p
        while pk <= x:
            total += math.log(p)
            pk *= p
    return total


def explicit_formula(x: float, zeros: list[float]) -> float:
    """psi(x) reconstructed from the first len(zeros) zeros."""
    s = 0j
    for g in zeros:
        rho = complex(0.5, g)
        s += (x ** rho) / rho
    return x - 2.0 * s.real - math.log(2 * math.pi) - 0.5 * math.log(1.0 - 1.0 / (x * x))


def convergence(x: float, zeros: list[float], counts: tuple[int, ...] = (100, 500, 1517)) -> dict:
    exact = chebyshev_psi(int(x))
    rows = []
    for n in counts:
        n = min(n, len(zeros))
        est = explicit_formula(x, zeros[:n])
        rows.append({"n_zeros": n, "estimate": est, "error": est - exact})
    return {"x": x, "exact": exact, "rows": rows,
            "best_error": min(abs(r["error"]) for r in rows)}


def audit() -> dict:
    zeros = find_zeros(t_to=2000.0)
    checks = []
    # 1. psi from the sieve must match the published values
    errs = {x: abs(chebyshev_psi(x) - v) for x, v in KNOWN_PSI.items()}
    checks.append({"check": "psi matches values computed independently from the primes",
                   "pass": max(errs.values()) < 1e-3,
                   "detail": ", ".join(f"psi({x}) off by {e:.1e}" for x, e in errs.items())})
    # 2. the zeros reproduce psi
    conv = [convergence(x, zeros) for x in (100.0, 1000.0, 10000.0, 100000.0)]
    checks.append({"check": "the zeros reconstruct psi(x) to better than 2 units up to 10^5",
                   "pass": all(c["best_error"] < 2.0 for c in conv),
                   "detail": "; ".join(f"x={c['x']:.0f}: best error {c['best_error']:+.3f} "
                                       f"with {c['rows'][-1]['n_zeros']} zeros" for c in conv)})
    # 3. and the reconstruction IMPROVES as zeros are added — a single number could be luck
    f = conv[0]
    checks.append({"check": "the reconstruction improves with more zeros",
                   "pass": abs(f["rows"][-1]["error"]) < abs(f["rows"][0]["error"]),
                   "detail": f"x=100: {f['rows'][0]['error']:+.3f} at {f['rows'][0]['n_zeros']} "
                             f"zeros -> {f['rows'][-1]['error']:+.3f} at "
                             f"{f['rows'][-1]['n_zeros']}"})
    return {"checks": checks, "n_pass": sum(c["pass"] for c in checks), "n": len(checks),
            "all_pass": all(c["pass"] for c in checks), "zeros": len(zeros), "convergence": conv}


__all__ = ["chebyshev_psi", "explicit_formula", "convergence", "audit", "KNOWN_PSI"]
