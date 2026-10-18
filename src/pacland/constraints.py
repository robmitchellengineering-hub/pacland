"""Constraint verification (Q2 of ``docs/new-approach.md``).

The second pillar of constraint-first string theory: turn a swampland /
consistency constraint into a measurable, certifiable statement — "this constraint
eliminates fraction p of the sampled vacua, with confidence 1-delta." A chain of
verified constraints is what narrows the landscape by elimination, without search.
"""
from __future__ import annotations

from .certificate import hoeffding_radius


def elimination_fraction(sample, keep) -> float:
    """Fraction of ``sample`` that FAILS ``keep`` (i.e. is eliminated by it)."""
    sample = list(sample)
    if not sample:
        raise ValueError("sample must be non-empty")
    kept = sum(1 for v in sample if keep(v))
    return (len(sample) - kept) / len(sample)


def elimination_certificate(sample, keep, delta: float = 0.05) -> dict:
    """Hoeffding interval on the elimination fraction.

    Reuses the same one-sided Hoeffding radius as the verification certificate
    (``docs/verification-formal.md``), applied to a *constraint* over a
    distribution of vacua rather than to a single candidate.
    """
    sample = list(sample)
    if not sample:
        raise ValueError("sample must be non-empty")
    p = elimination_fraction(sample, keep)
    r = hoeffding_radius(len(sample), delta)
    return {
        "eliminated": p,
        "lower": max(0.0, p - r),
        "upper": min(1.0, p + r),
        "n": len(sample),
        "delta": delta,
    }
