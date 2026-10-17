"""The two-level Valiant certificate (L3) — build #1.

Implements Theorem 2 of ``docs/verification-formal.md``: an upper bound on the true
error ``p_* = Pr[|h - c*| > eps]``, composed from a candidate-vs-oracle term and an
oracle-vs-truth term, each bounded by a one-sided Hoeffding interval.

Pure stdlib; no physics. The certificate is the load-bearing object of the whole
framework: it replaces "prove this vacuum is our universe" with "certify it is
observationally indistinguishable within an explicit (eps, delta) tolerance."
"""
from __future__ import annotations

from dataclasses import dataclass
from math import log, sqrt


def hoeffding_radius(n: int, delta: float) -> float:
    """One-sided Hoeffding radius.

    For i.i.d. Bernoulli with mean ``p`` and empirical mean ``p_hat``,
    ``Pr[p_hat - p >= t] <= exp(-2 n t^2)``, hence the one-sided confidence radius
    at level ``delta`` is ``sqrt(ln(1/delta) / (2n))``:

        p <= p_hat + hoeffding_radius(n, delta)   with probability >= 1 - delta.
    """
    if n <= 0:
        raise ValueError("n must be positive")
    if not (0.0 < delta < 1.0):
        raise ValueError("delta must be in (0, 1)")
    return sqrt(log(1.0 / delta) / (2.0 * n))


@dataclass(frozen=True)
class Certificate:
    """A Valiant certificate (``docs/verification-formal.md`` §5)."""

    p_hat_g: float      # empirical candidate-vs-oracle disagreement rate
    n: int | None       # candidate sample size (None when the term is exact)
    p_hat_e: float      # empirical oracle exceedance rate
    m: int              # validation sample size (measurable points)
    delta_s: float      # candidate-sampling confidence budget
    delta_e: float      # oracle-validation confidence budget
    radius_s: float     # Hoeffding radius, candidate term
    radius_e: float     # Hoeffding radius, oracle term
    bound: float        # upper bound on p_*
    confidence: float   # total confidence 1 - delta_s - delta_e
    exact: bool         # True if the candidate term is exact (finite D)


def two_level_certificate(
    p_hat_g: float,
    n: int,
    p_hat_e: float,
    m: int,
    delta_s: float,
    delta_e: float,
) -> Certificate:
    """Theorem 2: bound the true error of a candidate against reality.

    ``p_hat_g`` and ``p_hat_e`` are empirical rates in [0, 1]. Returns the bound

        p_* <= p_hat_g + p_hat_e + radius_s(n, delta_s) + radius_e(m, delta_e)

    with total confidence ``1 - delta_s - delta_e``.
    """
    _check_rate(p_hat_g, "p_hat_g")
    _check_rate(p_hat_e, "p_hat_e")
    radius_s = hoeffding_radius(n, delta_s)
    radius_e = hoeffding_radius(m, delta_e)
    return Certificate(
        p_hat_g=p_hat_g,
        n=n,
        p_hat_e=p_hat_e,
        m=m,
        delta_s=delta_s,
        delta_e=delta_e,
        radius_s=radius_s,
        radius_e=radius_e,
        bound=p_hat_g + p_hat_e + radius_s + radius_e,
        confidence=1.0 - delta_s - delta_e,
        exact=False,
    )


def finite_d_certificate(
    p_g_exact: float,
    p_hat_e: float,
    m: int,
    delta_e: float,
) -> Certificate:
    """Finite observable set: the candidate term is exact (no sampling).

    ``docs/observable-measure.md`` §5: with a finite, fully-computable observable
    set, ``p_g`` is computed exactly, so the sampling term vanishes and only the
    oracle-validation term remains:

        p_* <= p_g_exact + p_hat_e + radius_e(m, delta_e)

    with confidence ``1 - delta_e``.
    """
    _check_rate(p_g_exact, "p_g_exact")
    _check_rate(p_hat_e, "p_hat_e")
    radius_e = hoeffding_radius(m, delta_e)
    return Certificate(
        p_hat_g=p_g_exact,
        n=None,
        p_hat_e=p_hat_e,
        m=m,
        delta_s=0.0,
        delta_e=delta_e,
        radius_s=0.0,
        radius_e=radius_e,
        bound=p_g_exact + p_hat_e + radius_e,
        confidence=1.0 - delta_e,
        exact=True,
    )


def empirical_exceedance(values, threshold: float) -> float:
    """Empirical rate at which ``values`` exceed ``threshold``, in [0, 1]."""
    values = list(values)
    if not values:
        raise ValueError("values must be non-empty")
    return sum(1 for v in values if v > threshold) / len(values)


def _check_rate(p: float, name: str) -> None:
    if not (0.0 <= p <= 1.0):
        raise ValueError(f"{name} must be in [0, 1], got {p}")
