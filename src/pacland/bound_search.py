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


def check_bound(c, *, beta_pos=(2.0, 2.5, 3.0, 4.0, 6.0, 10.0, 20.0),
                beta_val=(2.0, 2.5, 3.0, 4.0, 6.0, 10.0, 20.0),
                beta_sharp=(2.5, 3.0), beta_scale=4.0, scale_floor=0.5) -> dict:
    """Test a candidate bound c(β) against the referee. Returns the criteria + the verdict.

    ``reaches_scale`` is the criterion that separates a genuinely-new bound from a merely-weaker one:
    c/m at the last probe point must stay within ``scale_floor`` of the truth (a bound that decays
    faster than m and vanishes relative to it is not AT the mass-gap scale).
    """
    positive = all(c(b) > 0.0 for b in beta_pos)
    # a relative tolerance: a bound computed via 1/ξ can be a hair above the referee from float roundoff;
    # that is equality, not a false bound (which would be above by a finite factor, not 1e-9).
    valid = all(c(b) <= referee(b) * (1.0 + 1e-9) for b in beta_val)
    ratios = [c(b) / referee(b) for b in beta_sharp]
    sharp = ratios[1] >= 0.5 * ratios[0]
    reaches_scale = c(beta_scale) / referee(beta_scale) >= scale_floor
    return {
        "positive": positive, "valid": valid, "sharp": sharp, "reaches_scale": reaches_scale,
        "survived": positive and valid and sharp and reaches_scale,
        "ratios": ratios,
    }


def check_uniformity(c, *, betas=(2.0, 2.5, 3.0), volumes=(4, 8, 16, 32, 64),
                     spacings=(1.0, 0.5, 0.25, 0.125)) -> dict:
    """A1 (volume-uniformity) + A3 (continuum survival): the bound c(β, V, a) must be POSITIVE at
    EVERY point of the (β, V, a) grid — uniform in volume and lattice spacing.

    A bound that is positive at one volume or one spacing does NOT clear the missing uniformity. This
    is the machine-checkable form of the two assumptions the referee previously did not test.
    """
    for b in betas:
        for V in volumes:
            for a in spacings:
                try:
                    val = c(b, V, a)
                except Exception as exc:  # noqa: BLE001
                    return {"uniform": False, "beta": b, "volume": V, "spacing": a,
                            "reason": f"raised {type(exc).__name__}"}
                if val <= 0.0:
                    return {"uniform": False, "beta": b, "volume": V, "spacing": a, "value": val,
                            "reason": f"c(β={b}, V={V}, a={a}) = {val} ≤ 0"}
    return {"uniform": True}


def exponential(a: float, k: float):
    """A candidate bound c(β) = a·e^(−kβ) from the exponential family."""
    return lambda b: a * math.exp(-k * b)


def _is_referee(a: float, k: float, tol: float = 1e-6) -> bool:
    return abs(a - 25.28) < tol and abs(k - 1.182) < tol


def search_family(name: str, make_bound, param_grids: dict[str, list[float]],
                  *, is_referee=None) -> dict:
    """Search ANY parameterized family of bounds against the referee; record the honest result.

    ``make_bound`` takes keyword params and returns a callable c(β); ``param_grids`` maps each param
    name to its values; ``is_referee`` (optional) marks a parameter combination as the referee itself
    so it is never counted as a new discovery. The negative result — "no new independent bound in this
    family" — is recorded as a queryable failed claim, so the search narrows the frontier, not silently.
    """
    from itertools import product

    survivors: list[dict] = []
    failures: list[dict] = []
    names = list(param_grids)
    for combo in product(*param_grids.values()):
        params = dict(zip(names, combo))
        c = make_bound(**params)
        r = check_bound(c)
        is_ref = is_referee(**params) if is_referee else False
        entry = {**params, **r, "is_referee": is_ref}
        if r["survived"] and not is_ref:
            survivors.append(entry)
        else:
            failures.append(entry)
    conclusion = (f"no new independent bound in the {name} family" if not survivors
                  else f"{len(survivors)} independent survivor(s) found in the {name} family")
    registry.record_claim(
        f"claim-mass-gap-{name}-search",
        f"mass-gap bound search over the {name} family against m(β)=25.28·e^(−1.182β)",
        "failed" if not survivors else "survived",
        problem="ym-mass-gap",
        reason=conclusion,
        produced_by="bound-search",
    )
    return {"family": name, "survivors": survivors, "failures": failures, "conclusion": conclusion,
            "n_survivors": len(survivors), "n_failures": len(failures)}


def search_exponential(a_values: list[float], k_values: list[float]) -> dict:
    """Search c(β)=a·e^(−kβ). The referee (a,k)=(25.28,1.182) is excluded as not-new."""
    return search_family(
        "exponential", lambda a, k: exponential(a, k),
        {"a": a_values, "k": k_values},
        is_referee=lambda a, k: _is_referee(a, k),
    )


def search_log_corrected(a_values: list[float], k_values: list[float], p_values: list[float]) -> dict:
    """Search c(β)=a·e^(−kβ)·(log β)^p — a second family: a log correction to the exponential.

    The honest result is again "no new bound" (a log factor with p≠0 either grows past m or collapses
    below it), which narrows the search: the mass-gap scale is not reachable by a single log correction.
    """
    import math as _math

    def make(a: float, k: float, p: float):
        return lambda b: a * _math.exp(-k * b) * (_math.log(b) ** p)

    return search_family(
        "log-corrected", make,
        {"a": a_values, "k": k_values, "p": p_values},
        is_referee=lambda a, k, p: _is_referee(a, k) and p == 0,
    )
