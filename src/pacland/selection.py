"""Selection (L6) — the measure-verifier.

``docs/selection.md``. The selection problem ("why this vacuum, not another") is
the half verification does not touch. What is *buildable* is evaluation, not
derivation: certify whether a candidate measure over vacua predicts our universe
as *typical*, rather than deriving the correct measure.

This module is the statistical core of that: the typicality test. It is distinct
from ``measure.py`` (the *observable* measure D — weights over observables); here
the "measure" is a distribution over *vacua*.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite


def quantile(sample, observed: float) -> float:
    """Empirical CDF: fraction of ``sample`` <= ``observed``, in [0, 1]."""
    sample = list(sample)
    if not sample:
        raise ValueError("sample must be non-empty")
    if not isfinite(observed):
        raise ValueError("observed must be finite")
    return sum(1 for x in sample if x <= observed) / len(sample)


@dataclass(frozen=True)
class TypicalityVerdict:
    """Whether an observed value is typical of an empirical distribution."""

    observed: float
    n: int
    quantile: float      # fraction of the sample <= observed
    central_fraction: float
    typical: bool
    note: str


def typicality_test(
    sample, observed: float, central_fraction: float = 0.95
) -> TypicalityVerdict:
    """Is ``observed`` typical of ``sample``?

    "Typical" means the observed value falls inside the central band of the
    empirical distribution: the quantile lies in
    ``[(1 - central_fraction)/2, 1 - (1 - central_fraction)/2]``.

    This is the core of the Lambda-typicality test (``docs/selection.md``): with a
    sample of vacua and their cosmological constant, ask whether our observed
    Lambda is ordinary under the empirical measure. ``typical=False`` is a
    falsification signal against that candidate measure — a certificate over a
    *distribution*, not a single vacuum.
    """
    sample = list(sample)
    if len(sample) < 2:
        raise ValueError("need at least 2 samples")
    if not (0.0 < central_fraction < 1.0):
        raise ValueError("central_fraction must be in (0, 1)")
    q = quantile(sample, observed)
    lo = (1.0 - central_fraction) / 2.0
    hi = 1.0 - lo
    typical = lo <= q <= hi
    return TypicalityVerdict(
        observed=observed,
        n=len(sample),
        quantile=q,
        central_fraction=central_fraction,
        typical=typical,
        note="typical" if typical else "atypical",
    )


def ks_uniformity(sample, low: float, high: float) -> float:
    """Kolmogorov-Smirnov statistic of ``sample`` vs uniform on [low, high].

    The classic measure-level claim is "Lambda is ~uniformly distributed across
    vacua." This returns the KS distance between the empirical CDF and that
    uniform hypothesis; the larger the value, the more the data rejects
    uniformity. (Thresholds for rejection need a critical-value table — see
    scipy.stats.kstest for the exact p-value.)
    """
    sample = sorted(sample)
    n = len(sample)
    if n < 2:
        raise ValueError("need at least 2 samples")
    if high <= low:
        raise ValueError("require high > low")
    d = 0.0
    for i, x in enumerate(sample, start=1):
        f_emp = i / n
        f_prev = (i - 1) / n
        f_unif = (x - low) / (high - low)
        d = max(d, abs(f_emp - f_unif), abs(f_prev - f_unif))
    return d
