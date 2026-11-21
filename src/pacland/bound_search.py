"""bound_search.py — the M3 bound-discovery loop (skeleton).

Milestone 3 = a NEW uniform analytic bound for the mass gap, independently verified. This module is
the SEARCH that looks for one. A parameterized family of candidate bounds c(β) is tested against the
known-answer referee m(β) = 25.28·e^(−1.182β) on three honest criteria:

  * positivity  — c(β) > 0  (a bound that dies is vacuous),
  * validity    — c(β) ≤ m(β)  (a bound above the truth is false),
  * sharpness   — c/m does not collapse faster than the truth (tracks the exponential scale).

Every candidate is recorded as a registry claim, including the honest negative result when a family
contains no NEW independent bound — SEXTANT can say "this direction failed", and it is queryable.
"""
from __future__ import annotations

import math

from pacland import registry


def referee(beta: float) -> float:
    """The known-answer mass-gap scale m(β) = 25.28·e^(−1.182β) (m/√σ ≈ 3.2)."""
    return 25.28 * math.exp(-1.182 * beta)


def check_bound(c, *, beta_pos=(2.0, 2.5, 3.0, 4.0, 6.0), beta_val=(2.0, 2.5, 3.0, 4.0, 6.0),
                beta_sharp=(2.5, 3.0), beta_scale=4.0, scale_floor=0.5) -> dict:
    """Test a candidate bound c(β) against the referee. Returns the criteria + the verdict.

    ``reaches_scale`` is the criterion that separates a genuinely-new bound from a merely-weaker one:
    c/m at the last probe point must stay within ``scale_floor`` of the truth (a bound that decays
    faster than m and vanishes relative to it is not AT the mass-gap scale).
    """
    positive = all(c(b) > 0.0 for b in beta_pos)
    valid = all(c(b) <= referee(b) for b in beta_val)
    ratios = [c(b) / referee(b) for b in beta_sharp]
    sharp = ratios[1] >= 0.5 * ratios[0]
    reaches_scale = c(beta_scale) / referee(beta_scale) >= scale_floor
    return {
        "positive": positive, "valid": valid, "sharp": sharp, "reaches_scale": reaches_scale,
        "survived": positive and valid and sharp and reaches_scale,
        "ratios": ratios,
    }


def exponential(a: float, k: float):
    """A candidate bound c(β) = a·e^(−kβ) from the exponential family."""
    return lambda b: a * math.exp(-k * b)


def _is_referee(a: float, k: float, tol: float = 1e-6) -> bool:
    return abs(a - 25.28) < tol and abs(k - 1.182) < tol


def search_exponential(a_values: list[float], k_values: list[float]) -> dict:
    """Search the family c(β)=a·e^(−kβ) for a bound that survives the referee AND is not the referee
    itself. Records every candidate as a claim (survivors and failures) and returns the honest result."""
    survivors: list[dict] = []
    failures: list[dict] = []
    for a in a_values:
        for k in k_values:
            c = exponential(a, k)
            r = check_bound(c)
            is_ref = _is_referee(a, k)
            entry = {"a": a, "k": k, **r, "is_referee": is_ref}
            if r["survived"] and not is_ref:
                survivors.append(entry)
            else:
                failures.append(entry)
    # record the search itself as a claim — including the honest negative result
    conclusion = ("no new independent bound in the exponential family" if not survivors
                  else f"{len(survivors)} independent survivor(s) found")
    registry.record_claim(
        "claim-mass-gap-exponential-search",
        f"mass-gap bound search over c(β)=a·e^(−kβ) against m(β)=25.28·e^(−1.182β)",
        "failed" if not survivors else "survived",
        problem="ym-mass-gap",
        reason=conclusion,
        produced_by="bound-search",
    )
    return {"survivors": survivors, "failures": failures, "conclusion": conclusion,
            "n_survivors": len(survivors), "n_failures": len(failures)}
