"""Reality Guards — approach #2.

The measured Standard-Model parameters as a *falsification* guard-suite. Instead
of verifying that a candidate vacuum matches us, FALSIFY it: each guard asserts a
candidate's predicted observable falls within tolerance of the measured target.
A candidate that fails any guard is ruled out. The map of ruled-out vs
still-possible — under a named tolerance — is the product.

Targets below are the illustrative log-space values of ``docs/observable-measure.md``
§3 (order-of-magnitude correct, NOT authoritative — the real targets are a
scientific commitment to settle with the community). The *discipline* is the
deliverable: a falsification is only ever "computable AND outside tolerance"; a
non-computable observable (e.g. Lambda today) rules nothing out — it sits in the
prediction zone and is falsifiable later, not now.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RealityGuard:
    name: str
    target_log: float    # ln(c*) — the measured value
    tolerance: float     # allowed |ln(h/c*)| — the error bar, in log space


@dataclass(frozen=True)
class FalsificationVerdict:
    name: str
    predicted_log: float | None   # None = not computable by the oracle
    ruled_out: bool
    delta: float | None           # |predicted - target|, None if not computable

    @property
    def in_prediction_zone(self) -> bool:
        return self.predicted_log is None


def falsify(guard: RealityGuard, predicted_log: float | None) -> FalsificationVerdict:
    """Rule out a candidate iff its prediction is computable AND outside tolerance.

    ``predicted_log=None`` means the oracle cannot compute this observable — the
    candidate is NOT ruled out on it (prediction zone, ``docs/observable-measure.md``
    §6 top-right cell).
    """
    if predicted_log is None:
        return FalsificationVerdict(guard.name, None, False, None)
    delta = abs(predicted_log - guard.target_log)
    return FalsificationVerdict(guard.name, predicted_log, delta > guard.tolerance, delta)


def falsify_all(guards, predicted: dict) -> dict[str, FalsificationVerdict]:
    """Run every guard against a candidate (a dict of name -> predicted log or None)."""
    return {g.name: falsify(g, predicted.get(g.name)) for g in guards}


def ruled_out(verdicts: dict[str, FalsificationVerdict]) -> list[str]:
    """Names of observables that rule the candidate out."""
    return [name for name, v in verdicts.items() if v.ruled_out]


# Illustrative targets (docs/observable-measure.md §3); 1% log tolerance.
STANDARD_REALITY_GUARDS: tuple[RealityGuard, ...] = (
    RealityGuard("alpha_s_MZ",      -2.14, 0.01),
    RealityGuard("alpha_em_MZ",     -4.85, 0.01),
    RealityGuard("m_t_over_m_Z",     0.64, 0.01),
    RealityGuard("m_b_over_m_t",    -3.72, 0.01),
    RealityGuard("m_mu_over_m_tau", -2.82, 0.01),
    RealityGuard("m_u_over_m_d",    -0.75, 0.01),
    RealityGuard("theta_C",         -1.49, 0.01),
    RealityGuard("sin2_theta_W",    -1.46, 0.01),
    RealityGuard("m_H_over_m_Z",     0.32, 0.01),
    RealityGuard("Lambda_MPl4",   -280.90, 0.01),
)

__all__ = [
    "RealityGuard",
    "FalsificationVerdict",
    "falsify",
    "falsify_all",
    "ruled_out",
    "STANDARD_REALITY_GUARDS",
]
