"""The quintic's periods — solved from the Picard-Fuchs operator, with the tail bounded.

`docs/plan-facts.md` F2, milestone 1. #210 established that CYTools exposes no `picard_fuchs_equation`
and no monodromy, and named the operator for the mirror quintic:

    L = theta^4 - 5 z (5theta+1)(5theta+2)(5theta+3)(5theta+4),     theta = z d/dz,   z = 1/(5 psi)^5

with the conifold at `z = 1/5^5`.

**How the four solutions are built.** `L` has a fourfold indicial root `rho = 0` at `z = 0`, so no
solution is free of logarithms. The Frobenius recursion is fully determined:

    c_0(rho) = 1,   c_n(rho) = c_{n-1}(rho) * 5 P(rho+n-1) / (rho+n)^4,   P(s) = prod_{k=1..4}(5s+k)

and the solutions are `sum_j (log z)^j / j! f_j` with `f_j` the series whose n-th coefficient is
`d^{k-j} c_n / drho^{k-j}` at `rho = 0`.

**The derivatives are exact, not finite-differenced.** `c_n(rho)` is a product of four linear factors over
a fourth power, so a truncated Taylor algebra in `rho` to order 4 gives the derivatives with no step size
at all (`coeff_jets`). That is also the arithmetic an interval version would use.

**The checks, none of them fitted.**

1. `c_n(0)` must equal `(5n)!/(n!)^5`, the literature's coefficient, exactly.
2. `L omega_k = 0` for all four, with `L` applied through the log-algebra (`apply_L_logs`) — the operator
   and the solution are computed by completely separate code.
3. The monodromy around `z = 0` must be a single unipotent Jordan block of index 4.

**The bound, and the finding.** `|c_n z^n / c_{n-1} z^{n-1}| -> 5^5 |z|`, so the tail is bounded by
`|t_N| r/(1-r)` for `|z| < 1/5^5`. **The conifold sits exactly on that radius** (`z_c = 1/5^5`): the ratio
test degenerates there and no number of extra terms gives a bound. The conifold therefore needs its own
local expansion, and this milestone states that instead of working around it.

Run:        python3 scripts/quintic_periods.py
Guarded by: tests/test_quintic_periods.py
"""
from __future__ import annotations

import math

import mpmath as mp

#: The conifold point of the mirror quintic in the `z = 1/(5 psi)^5` coordinate.
Z_CONIFOLD = mp.mpf(1) / mp.mpf(5) ** 5

#: Taylor order in `rho` — one for each of the four solutions.
K = 4


def P(s):
    """prod_{k=1..4}(5s + k), the four Gamma-shifted factors of the operator."""
    out = mp.mpf(1)
    for k in range(1, 5):
        out *= 5 * s + k
    return out


def coeffs(n_max: int, rho=0) -> list:
    """`c_n(rho)` for n = 0..n_max, the Frobenius coefficients without any `z`."""
    rho = mp.mpf(rho)
    c = [mp.mpf(1)]
    for n in range(1, n_max + 1):
        c.append(c[-1] * 5 * P(rho + n - 1) / (rho + n) ** 4)
    return c


def closed_form_coeff(n: int):
    """`(5n)!/(n!)^5` — the same coefficient from the literature, for the independent check."""
    return mp.mpf(math.factorial(5 * n)) / mp.mpf(math.factorial(n)) ** 5


def terms(n_max: int, z, rho=0) -> list:
    """`c_n(rho) z^n` — the terms of the series, for the ratio test and the tail bound."""
    z = mp.mpf(z)
    return [c * z ** n for n, c in enumerate(coeffs(n_max, rho))]


def ratios(n_max: int, z, rho=0) -> list:
    """`|t_n / t_{n-1}|`; its limit is `5^5 |z|`."""
    t = terms(n_max, z, rho)
    return [abs(t[n] / t[n - 1]) for n in range(1, len(t)) if t[n - 1] != 0]


def tail_bound(n_max: int, z, rho=0):
    """A bound on everything dropped after n_max terms: `|t_N| r/(1-r)`.

    `mp.inf` when r >= 1, which is the honest answer at or beyond the radius of convergence — and is
    exactly what happens at the conifold.
    """
    t = terms(n_max + 1, z, rho)
    r = abs(t[-1] / t[-2])
    if r >= 1:
        return mp.inf
    return abs(t[-1]) * r / (1 - r)


# ---------------------------------------------------------------------------------------
# truncated Taylor algebra in rho: exact derivatives, no finite differences
# ---------------------------------------------------------------------------------------
def _jconst(v):
    out = [mp.mpf(0)] * K
    out[0] = mp.mpf(v)
    return out


def _jscale(a, s):
    return [x * mp.mpf(s) for x in a]


def _jmul(a, b):
    """Normalised Taylor coefficients multiply by plain convolution."""
    out = [mp.mpf(0)] * K
    for i in range(K):
        if a[i] == 0:
            continue
        for j in range(K - i):
            out[i + j] += a[i] * b[j]
    return out


def _jinv(b):
    out = [mp.mpf(0)] * K
    out[0] = 1 / b[0]
    for k in range(1, K):
        acc = mp.mpf(0)
        for i in range(1, k + 1):
            acc += b[i] * out[k - i]
        out[k] = -acc / b[0]
    return out


def _jdiv(a, b):
    return _jmul(a, _jinv(b))


def _jpow(b, n: int):
    out = _jconst(1)
    for _ in range(n):
        out = _jmul(out, b)
    return out


def coeff_jets(n_max: int) -> list:
    """`[jet(c_n)]` — normalised Taylor coefficients of `c_n(rho)` at rho = 0, to order K."""
    out = [_jconst(1)]
    cur = _jconst(1)
    for n in range(1, n_max + 1):
        prod = _jconst(1)
        for k in (1, 2, 3, 4):
            prod = _jmul(prod, [mp.mpf(5 * (n - 1) + k), mp.mpf(5), mp.mpf(0), mp.mpf(0)])
        prod = _jscale(prod, 5)
        denom = _jpow([mp.mpf(n), mp.mpf(1), mp.mpf(0), mp.mpf(0)], 4)
        cur = _jmul(cur, _jdiv(prod, denom))
        out.append(cur)
    return out


def as_log_parts(k: int, n_max: int, dps: int = 40) -> list:
    """`omega_k` as four coefficient series `f_0..f_3`; the solution is `sum_j (log z)^j/j! f_j`.

    `f_j[n]` is the (k-j)-th rho-derivative of `c_n` at rho = 0, exact from the jet.
    """
    mp.mp.dps = dps
    js = coeff_jets(n_max)
    parts = [[mp.mpf(0)] * (n_max + 1) for _ in range(K)]
    for j in range(k + 1):
        d = k - j
        parts[j] = [js[n][d] * mp.factorial(d) for n in range(n_max + 1)]
    return parts


# ---------------------------------------------------------------------------------------
# the operator on log-series — this is what verifies the solutions
# ---------------------------------------------------------------------------------------
def _theta(parts: list) -> list:
    """`theta = z d/dz` on `sum_k (log z)^k/k! f_k`:  `theta f_k + f_{k+1}`."""
    out = []
    for k, f in enumerate(parts):
        g = [mp.mpf(n) * a for n, a in enumerate(f)]
        if k + 1 < len(parts):
            nxt = parts[k + 1]
            g = [g[i] + (nxt[i] if i < len(nxt) else 0) for i in range(len(g))]
        out.append(g)
    return out


def _times_z(parts: list) -> list:
    """Multiplication by z: one power up, keeping the length (truncation)."""
    return [[mp.mpf(0)] + list(f[:-1]) for f in parts]


def _lin(parts: list, theta_scale, const: int) -> list:
    """`(theta_scale*theta + const)` applied to a log-series."""
    th = _theta(parts)
    return [[theta_scale * th[i][j] + const * parts[i][j] for j in range(len(th[i]))]
            for i in range(len(parts))]


def apply_L_logs(parts: list) -> list:
    """`L = theta^4 - 5z P(theta)` on a period `sum_k (log z)^k/k! f_k`.

    Independent of the recursion that produced the solution: only the operator and the log-algebra.
    """
    theta4 = _theta(_theta(_theta(_theta(parts))))
    p = parts
    for k in (1, 2, 3, 4):
        p = _lin(p, 5, k)                      # (5 theta + k), left to right, gives P(theta)
    p = [[5 * x for x in f] for f in p]        # the leading 5 of `5 z P(theta)`
    fivez = _times_z(p)
    return [[theta4[i][j] - fivez[i][j] for j in range(min(len(theta4[i]), len(fivez[i])))]
            for i in range(len(parts))]


def omega(z, k: int = 0, n_max: int = 60):
    """`omega_k` evaluated at `z` — a function of `z`, logarithms included.

    `omega_k = sum_j (log z)^j/j! f_j`, with `f_j` the series from `as_log_parts`.
    """
    z = mp.mpf(z)
    parts = as_log_parts(k, n_max)
    total = mp.mpf(0)
    for j, f in enumerate(parts):
        if j > k:
            break
        val = sum(a * z ** n for n, a in enumerate(f))
        total += mp.log(z) ** j / mp.factorial(j) * val
    return total


def functional_residual(k: int, z, n_max: int = 60, dps: int = 40) -> dict:
    """`|L omega_k(z)|` with `L` applied **to the function**, not to the coefficients.

    The coefficient-space check re-derives the recursion and is therefore a tautology; the honest check
    differentiates the function. The residual is compared against the size of `omega` and against the
    tail bound.
    """
    mp.mp.dps = dps
    z = mp.mpf(z)

    def theta(f):
        return lambda x: x * mp.diff(f, x)

    f = lambda x: omega(x, k, n_max)
    t1 = theta(f)
    t2 = theta(t1)
    t3 = theta(t2)
    t4 = theta(t3)
    # P(theta) = prod_k (5 theta + k), applied left to right as functions
    p = f
    for kk in (1, 2, 3, 4):
        p = (lambda g, kk=kk: (lambda x: 5 * (x * mp.diff(g, x)) + kk * g(x)))(p)
    Lf = t4(z) - 5 * z * p(z)
    scale = abs(f(z))
    return {"residual": abs(Lf), "scale": scale,
            "relative": float(abs(Lf) / scale) if scale else float("inf"),
            "tail": float(tail_bound(n_max, z)) if tail_bound(n_max, z) != mp.inf else float("inf")}


def _weight(parts: list, z) -> list:
    """Scale the n-th coefficient by `z^n`.

    `theta` is diagonal on `z^n` and `5z P(theta)` shifts by exactly one power, so the weighted arrays
    satisfy the same recursion — but the magnitudes are the *terms*, not the coefficients. Without this
    the check cancels numbers of order `c_n ~ 10^280` against each other and measures rounding.
    """
    z = mp.mpf(z)
    return [[a * z ** n for n, a in enumerate(f)] for f in parts]


def residual(k: int, n_max: int, z, dps: int = 40) -> float:
    """`max |L omega_k|` on the z-weighted series — compared against `tail_bound(n_max, z)`."""
    res = apply_L_logs(_weight(as_log_parts(k, n_max, dps), z))
    return float(max(abs(x) for f in res for x in f))


def monodromy_zero_point():
    """`M_0`, the monodromy around z = 0 in the (omega_0..omega_3) basis.

    `z -> e^{2 pi i} z` sends `log z -> log z + 2 pi i`; expanding and mapping back to the omega basis
    gives a single unipotent Jordan block of index 4.
    """
    m = [[mp.mpf(0)] * 4 for _ in range(4)]
    for k in range(4):
        for d in range(k + 1):
            m[k][k - d] = (2 * mp.pi * 1j) ** d / mp.factorial(d)
    return m


def radius_study(n_max: int = 300) -> dict:
    """The ratio test at fractions of z_c: bounded inside, degenerate exactly at the conifold."""
    out = {}
    for frac in ("0.5", "0.9", "0.99", "1.0"):
        z = Z_CONIFOLD * mp.mpf(frac)
        r = ratios(n_max, z)
        b = tail_bound(n_max, z)
        out[frac] = {"z": z, "r_last": r[-1],
                     "tail_bound": b if b == mp.inf else float(b), "bounded": b != mp.inf}
    return out


__all__ = ["Z_CONIFOLD", "K", "P", "coeffs", "closed_form_coeff", "terms", "ratios", "tail_bound",
           "coeff_jets", "as_log_parts", "apply_L_logs", "residual", "monodromy_zero_point",
           "radius_study"]
