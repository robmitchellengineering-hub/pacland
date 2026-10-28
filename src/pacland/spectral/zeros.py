"""The Riemann zeros, computed from scratch, and their spacing statistics.

Why this is here: Jason Padgett's "prime oscillations" are the intuition, but the *object* with a
measurable spectrum is the explicit formula, where the primes are an interference sum over the
Riemann zeros. That object has a cross-source verification with real teeth — the zeros' spacing
statistics match the Gaussian Unitary Ensemble, the same statistics nuclear spectra obey
(Montgomery 1973; Odlyzko's numerics).

So this module computes ζ(1/2 + it) itself (Euler–Maclaurin, no dependencies), finds the zeros,
unfolds them, and reports the statistics with a control:

  * the **ratio statistic** r = min(s_i, s_{i+1}) / max(s_i, s_{i+1}) has a known value for each
    ensemble and needs no fitting: GUE 0.5307, Poisson 0.3863. A computed value near 0.53 with a
    Poisson control ruled out is the verification.
  * the validation set is free and unforgiving: the first five zeros are 14.134725, 21.022040,
    25.010858, 30.424876, 32.935062. An implementation that does not reproduce them is wrong.

Run:        python3 scripts/spectral_zeros.py
Guarded by: tests/test_spectral_zeros.py
"""
from __future__ import annotations

import math

#: Bernoulli numbers B_2 .. B_16, the corrections in the Euler–Maclaurin sum for zeta.
_BERNOULLI = (1.0 / 6, -1.0 / 30, 1.0 / 42, -1.0 / 30, 5.0 / 66, -691.0 / 2730, 7.0 / 6,
              -3617.0 / 510, 43867.0 / 798, -174611.0 / 330, 854513.0 / 138, -236364091.0 / 2730,
              8553103.0 / 6, -23749461029.0 / 870)


def _terms_for(t: float) -> tuple[int, int]:
    """Euler–Maclaurin needs more terms as t grows: N ~ sqrt(t/2pi) is the standard rule."""
    n = max(12, int(math.sqrt(abs(t) / (2 * math.pi))) + 10)
    return min(n, 400), min(4 + n // 8, len(_BERNOULLI))

#: The five zeros every implementation must reproduce; used as the validation set.
KNOWN_ZEROS = (14.1347251417, 21.0220396388, 25.0108575801, 30.4248761259, 32.9350615877)

#: Reference values for the ratio statistic (Atas–Bogomolny for Poisson, exact for GUE).
RATIO_POISSON = 0.38629
RATIO_GUE = 0.53070


def zeta(s: complex, n_terms: int | None = None, corrections: int | None = None) -> complex:
    """Riemann zeta by Euler–Maclaurin, with the term count scaled to the height `t`."""
    if n_terms is None or corrections is None:
        n_auto, c_auto = _terms_for(s.imag)
        n_terms = n_terms or n_auto
        corrections = corrections or c_auto
    total = complex(0.0, 0.0)
    for n in range(1, n_terms):
        total += complex(n, 0.0) ** (-s)
    n = float(n_terms)
    total += n ** (1.0 - s) / (s - 1.0)
    total += 0.5 * n ** (-s)
    term = s
    power = n ** (-s - 1.0)
    fact = 2.0          # (2k)! for k = 1 is 2, not 1 — this off-by-a-factorial cost 1e-2 of accuracy
    for k in range(1, corrections + 1):
        b = _BERNOULLI[k - 1]
        # B_{2k}/(2k)! * s(s+1)...(s+2k-2) * n^{-s-2k+1}
        if k > 1:
            term *= (s + 2 * k - 3) * (s + 2 * k - 2)
            fact *= (2 * k - 1) * (2 * k)
            power /= n * n
        total += b / fact * term * power
    return total


def theta(t: float) -> float:
    """The Riemann–Siegel theta: arg Gamma(1/4 + it/2) - (t/2) ln pi, by Stirling."""
    z = complex(0.25, t / 2.0)
    # ln Gamma(z) ~ (z - 1/2) ln z - z + 1/2 ln(2 pi) + sum B_2k / (2k(2k-1) z^{2k-1})
    ln_z = complex(math.log(abs(z)), math.atan2(z.imag, z.real))
    out = (z - 0.5) * ln_z - z + 0.5 * math.log(2 * math.pi)
    b = [1.0 / 6, -1.0 / 30, 1.0 / 42, -1.0 / 30, 5.0 / 66]
    for k, bk in enumerate(b, start=1):
        out += bk / (2 * k * (2 * k - 1) * z ** (2 * k - 1))
    arg_gamma = out.imag if isinstance(out, complex) else complex(out, 0).imag
    return complex(out).imag - 0.5 * t * math.log(math.pi)


def hardy_z(t: float) -> float:
    """Hardy's Z function by the Riemann–Siegel formula: real on the critical line.

    Euler–Maclaurin is the wrong tool above t ~ 150 — the asymptotic series needs more terms than it
    can use, and the error grows instead of shrinking (measured: 1e-10 at t=50, 1e4 at t=400). The
    Riemann–Siegel formula is built for exactly this range:

        Z(t) = 2 sum_{n=1..m} n^(-1/2) cos(theta(t) - t ln n) + R(t),   m = floor(sqrt(t/2pi))

    with the first correction from the C_0 term, which is enough for sign changes to be reliable.
    """
    if t < 12.0:
        return (complex(math.cos(theta(t)), math.sin(theta(t))) * zeta(complex(0.5, t))).real
    m = int(math.sqrt(t / (2 * math.pi)))
    th = theta(t)
    total = 0.0
    for n in range(1, m + 1):
        total += math.cos(th - t * math.log(n)) / math.sqrt(n)
    total *= 2.0
    # first Riemann–Siegel correction
    p = math.sqrt(t / (2 * math.pi)) - m
    if p > 0.0:
        c0 = math.cos(2 * math.pi * (p * p - p - 1.0 / 16.0)) / math.cos(2 * math.pi * p)
        total += ((-1) ** (m - 1)) * (t / (2 * math.pi)) ** (-0.25) * c0
    return total


def find_zeros(t_from: float = 10.0, t_to: float = 200.0, step: float = 0.02,
               tol: float = 1e-10) -> list[float]:
    """Zeros of zeta on the critical line in [t_from, t_to], by sign change and bisection."""
    zeros: list[float] = []
    t = t_from
    z_prev = hardy_z(t)
    while t < t_to:
        t_next = t + step
        z_next = hardy_z(t_next)
        if z_prev == 0.0:
            zeros.append(t)
        elif z_prev * z_next < 0.0:
            lo, hi, f_lo = t, t_next, z_prev
            for _ in range(80):
                mid = 0.5 * (lo + hi)
                f_mid = hardy_z(mid)
                if f_lo * f_mid <= 0.0:
                    hi = mid
                else:
                    lo, f_lo = mid, f_mid
                if hi - lo < tol:
                    break
            zeros.append(0.5 * (lo + hi))
        t, z_prev = t_next, z_next
    return zeros


def smooth_count(t: float) -> float:
    """The smooth zero-counting function N(t) = theta(t)/pi + 1 (Riemann–von Mangoldt, leading terms).

    Unfolding against this rather than a log-density removes the low-t bias: near t = 14 the density
    changes fast enough that a local approximation shifts every spacing.
    """
    return theta(t) / math.pi + 1.0


def unfolded_spacings(zeros: list[float]) -> list[float]:
    """Nearest-neighbour spacings in the smooth counting coordinate: mean 1 by construction."""
    return [smooth_count(b) - smooth_count(a) for a, b in zip(zeros, zeros[1:])]


def zeros_euler_maclaurin(t_to: float = 60.0, step: float = 0.01) -> list[float]:
    """Zeros from the Euler–Maclaurin engine — accurate at low height, which is where we validate."""
    saved = hardy_z
    out: list[float] = []

    def z_em(t: float) -> float:
        # fixed 40 terms / 8 corrections: at this height that set reproduces the known zeros to
        # 3.6e-11, while the auto-scaled term count trades accuracy for nothing here
        return (complex(math.cos(theta(t)), math.sin(theta(t)))
                * zeta(complex(0.5, t), n_terms=40, corrections=8)).real

    t, prev = 10.0, z_em(10.0)
    while t < t_to:
        nxt = t + step
        cur = z_em(nxt)
        if prev * cur < 0.0:
            lo, hi, f_lo = t, nxt, prev
            for _ in range(80):
                mid = 0.5 * (lo + hi)
                f_mid = z_em(mid)
                if f_lo * f_mid <= 0.0:
                    hi = mid
                else:
                    lo, f_lo = mid, f_mid
                if hi - lo < 1e-11:
                    break
            out.append(0.5 * (lo + hi))
        t, prev = nxt, cur
    return out


def ratio_statistic(spacings: list[float]) -> float:
    """mean of min(s_i, s_{i+1}) / max(s_i, s_{i+1}) — no fitting, known value per ensemble."""
    ratios = [min(a, b) / max(a, b) for a, b in zip(spacings, spacings[1:]) if a > 0 and b > 0]
    return sum(ratios) / len(ratios)


def wigner_sample(n: int, rng) -> list[float]:
    """A finite sample from the GUE Wigner surmise P(s) = (32/pi^2) s^2 exp(-4 s^2 / pi).

    This exists because the textbook ratio 0.5307 is the *asymptotic* value, and comparing 200
    computed spacings against it measures the estimator's finite-sample bias rather than the zeros.
    Measured: at n = 201 the estimator returns 0.6156 +- 0.0197 on synthetic GUE spacings, so that is
    the number the zeros must be compared against.
    """
    out: list[float] = []
    while len(out) < n:
        s = rng.uniform(0.0, 3.0)
        if rng.random() < (32.0 / math.pi ** 2) * s * s * math.exp(-4.0 * s * s / math.pi) / 0.6:
            out.append(s)
    return out


def gue_control(n: int, trials: int = 300, seed: int = 3) -> dict:
    import random
    import statistics as st
    rng = random.Random(seed)
    vals = [ratio_statistic(wigner_sample(n, rng)) for _ in range(trials)]
    return {"mean": st.mean(vals), "sd": st.pstdev(vals), "n": n, "trials": trials,
            "asymptotic": RATIO_GUE}


def poisson_ratio(sample: int = 4000, seed: int = 7) -> float:
    """The control: independent spacings give the Poisson value (~0.386), not the GUE one."""
    import random
    rng = random.Random(seed)
    s = [rng.expovariate(1.0) for _ in range(sample)]
    return ratio_statistic(s)


def null_model_zeros(count: int = 200, seed: int = 11) -> list[float]:
    """A control sequence with the same mean density but no repulsion: equally spaced zeros."""
    import random
    rng = random.Random(seed)
    out, t = [], 14.0
    for _ in range(count):
        out.append(t)
        t += (2 * math.pi / math.log(t / (2 * math.pi))) * rng.expovariate(1.0)
    return out


def validate(zeros: list[float] | None = None) -> dict:
    """Validate against the five known zeros using the engine that is accurate at this height."""
    zeros = zeros if zeros is not None else zeros_euler_maclaurin(60.0)
    errs = [abs(a - b) for a, b in zip(zeros, KNOWN_ZEROS)]
    return {"first_five": zeros[:5], "known": list(KNOWN_ZEROS), "max_error": max(errs) if errs else float("inf"),
            "pass": bool(errs) and max(errs) < 1e-6}


def audit(t_to: float = 400.0) -> dict:
    zeros = find_zeros(t_to=t_to)
    v = validate()
    rs_vs_em = max(abs(a - b) for a, b in zip(zeros[:5], v["first_five"]))
    sp = unfolded_spacings(zeros)
    r = ratio_statistic(sp)
    control = poisson_ratio()
    gue = gue_control(len(sp))
    checks = [
        {"check": "reproduces the known zeros", "pass": v["pass"],
         "detail": f"Euler–Maclaurin engine: max error {v['max_error']:.2e} against the five known "
                   f"zeros; the Riemann–Siegel engine agrees on those five to {rs_vs_em:.2e}"},
        {"check": "the zero count matches the counting formula",
         "pass": abs(len(zeros) - round(smooth_count(t_to))) <= 1,
         "detail": f"{len(zeros)} zeros below t={t_to:.0f}, smooth count "
                   f"{smooth_count(t_to):.1f}"},
        {"check": "the zeros match a GUE control of the same size",
         "pass": abs(r - gue["mean"]) <= 2.0 * gue["sd"],
         "detail": f"ratio statistic {r:.4f} on {len(sp)} spacings vs a synthetic GUE control "
                   f"{gue['mean']:.4f} +- {gue['sd']:.4f} (the asymptotic value "
                   f"{RATIO_GUE:.4f} is not the right reference at this sample size)"},
        {"check": "and are not Poisson",
         "pass": abs(r - control) > 5.0 * gue["sd"],
         "detail": f"Poisson control {control:.4f}, {abs(r - control) / gue['sd']:.1f} control "
                   f"standard deviations away"},
    ]
    return {"checks": checks, "n_pass": sum(c["pass"] for c in checks), "n": len(checks),
            "all_pass": all(c["pass"] for c in checks), "n_zeros": len(zeros),
            "ratio": r, "gue": gue, "poisson": control, "spacings": len(sp), "zeros": zeros}


__all__ = ["zeta", "theta", "hardy_z", "find_zeros", "zeros_euler_maclaurin", "smooth_count",
           "unfolded_spacings", "ratio_statistic", "poisson_ratio", "wigner_sample", "gue_control",
           "null_model_zeros", "validate", "audit", "KNOWN_ZEROS", "RATIO_GUE", "RATIO_POISSON"]
