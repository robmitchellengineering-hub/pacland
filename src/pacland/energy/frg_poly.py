"""Carrier A, rung 2: the polynomial f(R) truncation — and the term it cannot be closed without.

Rung 1 was the Einstein–Hilbert truncation (two couplings). This carries the same flow into a polynomial
ansatz `f(R) = sum u_i R^i`, following Machado & Saueressig, *On the renormalization group flow of
f(R)-gravity* (arXiv:0712.0445), whose dimensionless flow equation, polynomial ansatz and result tables
were read from the LaTeX source, not the PDF.

**The result, stated first because it is not the one the plan expected.**

`n = 1` reproduces the paper's Table 3 **exactly** — `u0* = 0.00523`, `u1* = -0.02021` against the
published `0.00523, -0.0202`. `n >= 2` does **not** reproduce it, and the reason is in the paper itself.

The flow equation this module implements is the paper's eq. `flowdimless`. It is not the whole story:
the trace decomposition it comes from, eq. `traces`, carries a **single-mode contribution**

    D_1(d,0) * (1/P_k) * d_t R_k   evaluated at  -D^2 = Lambda_1(d,0)

that is not a heat-kernel term and therefore does not appear in the dimensionless flow equation. The
authors' own footnote says so: the difference between their Table 3/4 and the earlier CPR computation
"can be traced back to the contribution of the single mode term". Our `n >= 2` values differ from their
table in exactly the way a missing term of that kind would produce — and `n = 1` is insensitive to it.

**What this module therefore claims, and does not.** It claims: the polynomial machinery is correct
(`n = 1` is an exact known-answer match), and the published `n >= 2` ladder cannot be reproduced from
the published flow equation alone. It does **not** claim a ladder exists, converges, or drifts. A
truncation ladder that silently omits a term is worse than no ladder, because it looks like convergence.

Closing rung 2 needs the single-mode term extracted and added. That is named work, not a mystery.

Run:
    python3 -m pacland.energy.frg_poly
"""
from __future__ import annotations

import math

import numpy as np

K = 384.0 * math.pi ** 2          # the prefactor of the dimensionless flow, eq. flowdimless
D = 4                              # spacetime dimension used throughout the paper

# Table 3 of arXiv:0712.0445, transcribed from the LaTeX source. These are the numbers the n=1 row must
# match and the n>=2 rows must be compared against (not silently dropped).
PAPER_TABLE_3 = {
    1: (0.00523, -0.0202),
    2: (0.00333, -0.0125, 0.00149),
    3: (0.00518, -0.0196, 0.00070, -0.0104),
    4: (0.00505, -0.0206, 0.00026, -0.0120, -0.0101),
    5: (0.00506, -0.0206, 0.00023, -0.0105, -0.0096, -0.00455),
    6: (0.00504, -0.0208, 0.00012, -0.0110, -0.0109, -0.00473, 0.00238),
}

MISSING_TERM = ("D_1(d,0) * (1/P_k) * d_t R_k at -D^2 = Lambda_1(d,0) "
                "(eq. 'traces'; the authors' footnote attributes the CPR difference to it)")


# ---------------------------------------------------------------- truncated power series

def _poly(n: int, terms) -> np.ndarray:
    a = np.zeros(n + 1)
    for p, c in terms:
        if p <= n:
            a[p] += c
    return a


def _mul(a: np.ndarray, b: np.ndarray, n: int) -> np.ndarray:
    c = np.zeros(n + 1)
    for i, x in enumerate(a):
        if x == 0.0:
            continue
        m = min(len(b), n + 1 - i)
        c[i:i + m] += x * np.asarray(b[:m])
    return c


def _inv(a: np.ndarray, n: int) -> np.ndarray:
    """Series inverse to order n. Requires a[0] != 0."""
    if a[0] == 0.0:
        raise ZeroDivisionError("series has no constant term")
    out = np.zeros(n + 1)
    out[0] = 1.0 / a[0]
    for k in range(1, n + 1):
        s = sum(a[i] * out[k - i] for i in range(1, min(k, len(a) - 1) + 1))
        out[k] = -s / a[0]
    return out


def _add(*arrs, n: int) -> np.ndarray:
    out = np.zeros(n + 1)
    for a in arrs:
        a = np.asarray(a)
        out[:min(len(a), n + 1)] += a[:min(len(a), n + 1)]
    return out


def _scale(a: np.ndarray, c: float, n: int) -> np.ndarray:
    out = np.zeros(n + 1)
    a = np.asarray(a)
    out[:min(len(a), n + 1)] = c * a[:min(len(a), n + 1)]
    return out


def _deriv(a: np.ndarray, n: int) -> np.ndarray:
    out = np.zeros(n + 1)
    for i in range(1, len(a)):
        if i <= n:
            out[i - 1] = i * a[i]
    return out


# ---------------------------------------------------------------- the flow

def rhs(u, du, n: int) -> np.ndarray:
    """Right-hand side of eq. (flowdimless), truncated to order rho^n.

    All theta-functions are set to 1: the paper expands for rho << 1, where every argument is positive.
    """
    F = np.zeros(n + 1)
    u = np.asarray(u, dtype=float)
    F[:min(len(u), n + 1)] = u[:n + 1]
    Fp, Fpp = _deriv(F, n), _deriv(_deriv(F, n), n)
    dF = _poly(n, [(i, c) for i, c in enumerate(du)])
    dFp, dFpp = _deriv(dF, n), _deriv(_deriv(dF, n), n)
    eta = _mul(_add(dFp, _scale(Fp, 2.0, n), _scale(Fpp, -2.0, n), n=n), _inv(Fp, n), n)

    r2 = _poly(n, [(2, 1.0)])
    A = _mul(_poly(n, [(2, 5.0), (0, -12.0), (1, -4.0), (2, 61 / 90.0)]),
             _inv(_poly(n, [(0, 1.0), (1, -1 / 3.0)]), n), n)
    B = _scale(r2, 10.0, n)
    C = _mul(_poly(n, [(2, 9.0), (0, -36.0), (1, -6.0), (2, 67 / 60.0)]),
             _inv(_poly(n, [(0, 1.0), (1, -1 / 4.0)]), n), n)

    den = _add(_poly(n, [(0, 1.0)]), _mul(F, _inv(Fp, n), n), _poly(n, [(1, -1 / 3.0)]), n=n)
    Dpoly = _poly(n, [(0, 10.0), (1, -5.0), (2, -271 / 36.0), (3, 7249 / 4536.0)])
    Drest = _poly(n, [(0, 60.0), (1, -20.0), (2, -271 / 18.0)])
    Dterm = _mul(_add(_mul(eta, Dpoly, n), Drest, n=n), _inv(den, n), n)

    Epoly = _poly(n, [(0, 3.0), (1, 2 / 3.0)])
    Eterm = _mul(_mul(_scale(r2, 2.5, n), _add(_mul(eta, Epoly, n), _poly(n, [(0, 6.0)]), n=n), n),
                 _inv(den, n), n)

    G1 = _poly(n, [(0, 6.0), (1, 3.0), (2, 29 / 60.0), (3, 37 / 1512.0)])
    G2 = _poly(n, [(0, 27.0), (2, -91 / 20.0), (3, -29 / 30.0), (4, -181 / 3360.0)])
    G3 = _poly(n, [(0, 216.0), (2, -91 / 5.0), (3, -29 / 15.0)])
    G4 = _poly(n, [(0, 36.0), (1, 12.0), (2, 29 / 30.0)])
    numF = _add(_mul(Fp, _mul(eta, G1, n), n),
                _mul(_add(dFpp, _scale(Fpp, -2.0, n), n=n), G2, n),
                _mul(Fpp, G3, n), _mul(Fp, G4, n), n=n)
    om = _poly(n, [(0, 1.0), (1, -1 / 3.0)])
    denF = _add(_scale(F, 2.0, n),
                _mul(_scale(Fp, 3.0, n), _poly(n, [(0, 1.0), (1, -2 / 3.0)]), n),
                _mul(_scale(Fpp, 9.0, n), _mul(om, om, n), n), n=n)
    Fterm = _mul(numF, _inv(denF, n), n)
    return _add(A, B, C, Dterm, Eterm, Fterm, n=n)


def betas(u, n: int) -> np.ndarray:
    """d_t u at coupling u — the flow is affine in d_t u, so it is one linear solve."""
    u = np.asarray(u, dtype=float)
    r0 = rhs(u, np.zeros(n + 1), n)
    delta = np.zeros((n + 1, n + 1))
    for i in range(n + 1):
        e = np.zeros(n + 1)
        e[i] = 1.0
        delta[:, i] = rhs(u, e, n) - r0
    lhs = K * np.array([(4 - 2 * i) * u[i] for i in range(n + 1)])
    M = -delta
    for i in range(n + 1):
        M[i, i] += K
    return np.linalg.solve(M, r0 - lhs)


def find_fixed_point(n: int, guess=None, iters: int = 80, tol: float = 1e-13) -> tuple[np.ndarray, float]:
    """Newton on d_t u = 0. Returns (u*, residual)."""
    u = np.array(guess if guess is not None else [0.01, -0.03] + [0.002] * (n - 1), dtype=float)
    res = float("inf")
    for _ in range(iters):
        b = betas(u, n)
        res = float(np.max(np.abs(b)))
        if res < tol:
            break
        J = np.zeros((n + 1, n + 1))
        h = 1e-8
        for j in range(n + 1):
            up = u.copy()
            up[j] += h
            J[:, j] = (betas(up, n) - b) / h
        try:
            step = np.linalg.solve(J, -b)
        except np.linalg.LinAlgError:
            break
        u = u + step
    return u, res


def ladder(nmax: int = 3) -> list[dict]:
    """Solve the truncation ladder and place each row beside the paper's."""
    out = []
    for n in range(1, nmax + 1):
        u, res = find_fixed_point(n)
        paper = PAPER_TABLE_3.get(n)
        match = None
        if paper is not None and len(paper) == len(u):
            match = bool(np.allclose(u, np.array(paper), atol=5e-5))
        out.append({"n": n, "u": u, "residual": res, "paper": paper, "matches_paper": match})
    return out


def main() -> int:
    print("Carrier A, rung 2 - polynomial f(R) truncation (Machado & Saueressig, arXiv:0712.0445)")
    print(f"  missing term: {MISSING_TERM}\n")
    for row in ladder(3):
        u = ", ".join(f"{x:+.5f}" for x in row["u"])
        print(f"  n={row['n']}  u* = [{u}]  |beta| = {row['residual']:.1e}  "
              f"matches paper: {row['matches_paper']}")
        if row["paper"]:
            p = ", ".join(f"{x:+.5f}" for x in row["paper"])
            print(f"        paper: [{p}]")
    print()
    print("  n=1 reproduces the published fixed point; n>=2 does not, and the paper's own footnote")
    print("  attributes the difference to the single-mode trace term this flow equation omits.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
