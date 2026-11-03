"""Carrier A, rung 1: the Einstein–Hilbert truncation of the functional renormalisation group.

The plan named two carriers. This is the first rung of the first one, and it is deliberately the
smallest thing that can produce a *verdict* rather than a gesture: two couplings, one cutoff, an
equation you can actually solve, and a published closed form to check the solver against.

**The flow** (Litim, *Fixed points of quantum gravity*, hep-th/0312114, eqs. (4)–(5)):

    beta_lambda = P1 / (P2 + 4(d+2) g)
    beta_g      = (d-2) g P2 / (P2 + 4(d+2) g)
    eta         = (d-2)(d+2) g / ((d-2) g - 2 (lambda - 1/2)^2)

with

    P1 = -16 l^3 + 4 l^2 (4 - 10 d g - 3 d^2 g + d^3 g)
         + 4 l (10 d g + d^2 g - d^3 g - 1)
         + d (2+d) (d - 16 g + 8 d g - 3) g
    P2 = 8 (l^2 - l - d g) + 2

**Where these came from, and why that matters.** They were first taken from the PDF, where the
superscripts are mangled — the extracted text is ambiguous between `d^3 g` and `d 3 g`, and the
substitution gave a cubic where the paper says the condition is quadratic. They were then re-read from
the **LaTeX source** (arXiv e-print), which is unambiguous. A number computed from the mangled version
would have looked entirely plausible. This is rung 0 of the discipline: verify the formula's *source*,
not just its output.

**The closed form** (same paper, eq. `gtilde-inf`), for d > 4:

    lambda* = (d^2 - d - 4 - sqrt(2 d (d^2 - d - 4))) / (2 (d-4) (d+1))
    g*phys  = 2 Gamma(d/2+2) (4 pi)^(d/2-1) * lambda*^2 / (d^2 - d - 4)

At exactly d = 4 that expression is 0/0 and the limit is `lambda* = 1/4`, which the paper states in
words ("increasing from 1/4 to 0.4 for d ranging from 4 to 40"). The solver must reproduce both — that is
the known-answer gate this rung is built on.

**What this is not.** It is one truncation. Reproducing a published fixed point is not evidence that the
fixed point survives the next truncation, which is the open question in the field. The verdict this rung
can support is exactly: *the Einstein–Hilbert truncation with this cutoff has a non-Gaussian fixed point,
and here are its coordinates and exponents.*

Pure stdlib; no scipy in this environment, so the root-finder is a small Newton iteration.
"""
from __future__ import annotations

import math

# The paper inserts c_d into g for its closed form; the beta functions use g / c_d.
def cd(d: float) -> float:
    """The numerical factor Litim scales into the gravitational coupling."""
    return math.gamma(d / 2.0 + 2.0) * (4.0 * math.pi) ** (d / 2.0 - 1.0)


def p1(lam: float, g: float, d: float) -> float:
    return (-16.0 * lam ** 3
            + 4.0 * lam ** 2 * (4.0 - 10.0 * d * g - 3.0 * d ** 2 * g + d ** 3 * g)
            + 4.0 * lam * (10.0 * d * g + d ** 2 * g - d ** 3 * g - 1.0)
            + d * (2.0 + d) * (d - 16.0 * g + 8.0 * d * g - 3.0) * g)


def p2(lam: float, g: float, d: float) -> float:
    return 8.0 * (lam ** 2 - lam - d * g) + 2.0


def beta_lambda(lam: float, g: float, d: float = 4.0) -> float:
    return p1(lam, g, d) / (p2(lam, g, d) + 4.0 * (d + 2.0) * g)


def beta_g(lam: float, g: float, d: float = 4.0) -> float:
    return (d - 2.0) * g * p2(lam, g, d) / (p2(lam, g, d) + 4.0 * (d + 2.0) * g)


def eta(lam: float, g: float, d: float = 4.0) -> float:
    return (d - 2.0) * (d + 2.0) * g / ((d - 2.0) * g - 2.0 * (lam - 0.5) ** 2)


def fixed_point_closed_form(d: float) -> tuple[float, float]:
    """(lambda*, g*_physical) from the paper's closed form; d = 4 is the stated limit."""
    if abs(d - 4.0) < 1e-12:
        lam = 0.25
    else:
        a = d * d - d - 4.0
        lam = (a - math.sqrt(2.0 * d * a)) / (2.0 * (d - 4.0) * (d + 1.0))
    a = d * d - d - 4.0
    g_phys = 2.0 * math.gamma(d / 2.0 + 2.0) * (4.0 * math.pi) ** (d / 2.0 - 1.0) * lam ** 2 / a
    return lam, g_phys


def solve(d: float = 4.0, tol: float = 1e-13, max_iter: int = 200) -> tuple[float, float]:
    """Newton on (beta_lambda, beta_g), in the scaled couplings the beta functions use.

    Start from the closed form's scaled value (g_scaled = g_phys / c_d), falling back to a small
    positive seed. Returns (lambda*, g*_scaled).
    """
    lam, g_phys = fixed_point_closed_form(d)
    g = g_phys / cd(d)
    if not (0.0 < g < 1.0) or not (0.0 < lam < 1.0):
        lam, g = 0.2, 0.05
    for _ in range(max_iter):
        b1, b2 = beta_lambda(lam, g, d), beta_g(lam, g, d)
        if abs(b1) + abs(b2) < tol:
            return lam, g
        h = 1e-8
        j11 = (beta_lambda(lam + h, g, d) - b1) / h
        j12 = (beta_lambda(lam, g + h, d) - b1) / h
        j21 = (beta_g(lam + h, g, d) - b2) / h
        j22 = (beta_g(lam, g + h, d) - b2) / h
        det = j11 * j22 - j12 * j21
        if abs(det) < 1e-18:
            break
        lam -= (j22 * b1 - j12 * b2) / det
        g -= (-j21 * b1 + j11 * b2) / det
    return lam, g


def critical_exponents(d: float = 4.0) -> tuple[complex, complex]:
    """Critical exponents: theta = -eigenvalue of the stability matrix at the fixed point.

    They are **complex** at d = 4, and that is the published result, not a defect: the paper states
    theta_pm = (5 +/- i sqrt(167))/3, i.e. theta' = 1.667 and theta'' = 4.308, and notes the pair stays
    complex for all 2.56 < d < 21.4. A solver that refuses complex exponents here would fail on the
    known answer - which is exactly what this one did before the LaTeX was read.
    """
    lam, g = solve(d)
    h = 1e-7
    b1 = (beta_lambda(lam, g, d), beta_g(lam, g, d))
    j11 = (beta_lambda(lam + h, g, d) - b1[0]) / h
    j12 = (beta_lambda(lam, g + h, d) - b1[0]) / h
    j21 = (beta_g(lam + h, g, d) - b1[1]) / h
    j22 = (beta_g(lam, g + h, d) - b1[1]) / h
    tr, det = j11 + j22, j11 * j22 - j12 * j21
    disc = tr * tr - 4.0 * det
    if disc >= 0.0:
        r = math.sqrt(disc)
        return (-(tr + r) / 2.0, -(tr - r) / 2.0)
    r = math.sqrt(-disc)
    return (complex(-tr / 2.0, r / 2.0), complex(-tr / 2.0, -r / 2.0))


def verdict(d: float = 4.0) -> dict:
    """The rung-1 verdict: does a non-Gaussian fixed point exist, and does it match the closed form?"""
    lam, g = solve(d)
    lam_ref, g_phys_ref = fixed_point_closed_form(d)
    g_phys = g * cd(d)
    return {
        "d": d,
        "lambda_star": lam,
        "g_star_scaled": g,
        "g_star_physical": g_phys,
        "closed_form": {"lambda_star": lam_ref, "g_star_physical": g_phys_ref},
        "beta_at_fixed_point": {"beta_lambda": beta_lambda(lam, g, d), "beta_g": beta_g(lam, g, d)},
        "eta_star": eta(lam, g, d),
        "critical_exponents": critical_exponents(d),
        "matches_closed_form": abs(lam - lam_ref) < 1e-8 and abs(g_phys - g_phys_ref) < 1e-6,
    }


def main() -> int:
    v = verdict(4.0)
    print("Carrier A, rung 1 - Einstein-Hilbert truncation, optimized cutoff (Litim hep-th/0312114)")
    print(f"  lambda*        = {v['lambda_star']:.10f}")
    print(f"  g* (scaled)    = {v['g_star_scaled']:.10f}")
    print(f"  g* (physical)  = {v['g_star_physical']:.10f}")
    print(f"  closed form    = lambda* {v['closed_form']['lambda_star']:.10f}, "
          f"g* {v['closed_form']['g_star_physical']:.10f}")
    print(f"  beta at fixpt  = ({v['beta_at_fixed_point']['beta_lambda']:.2e}, "
          f"{v['beta_at_fixed_point']['beta_g']:.2e})")
    print(f"  eta*           = {v['eta_star']:.6f}  (expected 2 - d = -2)")
    th = v["critical_exponents"]
    print(f"  theta          = {th[0].real:.6f} +/- {abs(th[0].imag):.6f} i   "
          f"(paper: (5 +/- i sqrt(167))/3 = 1.6667 +/- 4.3074 i)")
    print(f"  matches closed form: {v['matches_closed_form']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
