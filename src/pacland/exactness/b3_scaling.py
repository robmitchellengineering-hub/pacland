"""The two `b3` scales, and their product — does the landscape get more or less discoverable?

Two independent instruments produced a `b3` dependence this week:

    CONTENT        exact gauge-invariant orbits with 0 < N <= 1, |component| <= 1
                   b3 = 2 -> 20,  b3 = 4 -> 1,480,  b3 = 6 -> 107,100
    ACCESSIBILITY  sampler points per try
                   b3 = 6 -> 0.1325,  b3 = 10 -> 0.01446,  b3 = 12 -> 0.00137

Each is fitted as `X(b3) = X0 * f**(b3 - b3_0)`, giving per-unit-b3 factors **A** (content, >1) and **B**
(accessibility, <1). Their product `A*B` is the question: does the reachable content grow or shrink with dimension?

**The honest caveat, which limits the claim.** Content is counted in the *enumerable* window, whose size grows
like `3^(2 b3)`; the sampler draws fluxes from its own range, and nothing establishes that the two windows scale
together. So `A*B` is a **heuristic** comparison of two measured scales, not a physical rate. It is reported as
such, and the module refuses to present it as a derivation.

Run:        python3 scripts/b3_scaling.py
Guarded by: tests/test_b3_scaling.py
"""
from __future__ import annotations

import math

#: Exact content counts: orbits with 0 < N <= 1 in the |component| <= 1 window.
CONTENT = ((2, 20), (4, 1480), (6, 107100))

#: Measured sampler yields, points per try, with the budget each was measured at.
ACCESSIBILITY = ((6, 0.1325), (10, 81 / 5600), (12, 0.00137))


def per_unit_factor(points) -> dict:
    """Least-squares slope of `ln X` against `b3`, exponentiated — plus the per-interval factors.

    Reporting the per-interval factors alongside the global fit is the honest part: if they disagree, the
    exponential form is not established and a single number would hide that.
    """
    xs = [b for b, _ in points]
    ys = [math.log(v) for _, v in points]
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = sum((x - mx) ** 2 for x in xs)
    slope = num / den if den else float("nan")
    intervals = []
    for (b0, v0), (b1, v1) in zip(points, points[1:]):
        intervals.append((b0, b1, (v1 / v0) ** (1.0 / (b1 - b0))))
    return {"factor": math.exp(slope), "exponent": slope,
            "intervals": intervals,
            "consistent_exponential": _consistent(intervals)}


def _consistent(intervals, tol: float = 0.25) -> bool:
    """Are the per-interval factors within `tol` relative of each other?"""
    if len(intervals) < 2:
        return True
    fs = [f for _, _, f in intervals]
    return (max(fs) - min(fs)) / (sum(fs) / len(fs)) <= tol


def scales() -> dict:
    """Both factors and the product, with the range the intervals imply."""
    a = per_unit_factor(CONTENT)
    b = per_unit_factor(ACCESSIBILITY)
    prod = a["factor"] * b["factor"]
    lo = min(f for _, _, f in b["intervals"]) if b["intervals"] else b["factor"]
    hi = max(f for _, _, f in b["intervals"]) if b["intervals"] else b["factor"]
    return {
        "content": a, "accessibility": b,
        "A": a["factor"], "B": b["factor"],
        "product": prod,
        "product_range": (a["factor"] * lo, a["factor"] * hi),
        "verdict": ("reachable content GROWS with b3" if prod > 1.2 else
                    "reachable content SHRINKS with b3" if prod < 0.8 else
                    "knife-edge: the two scales nearly cancel"),
        "caveat": ("content is counted in the enumerable window (which grows like 3^(2b3)) while accessibility is "
                   "measured in the sampler's own range; nothing establishes that the windows scale together, so "
                   "the product is a heuristic comparison of two scales, not a physical rate"),
        "falsifier": ("a fourth b3 where either series breaks the exponential — the per-interval factors already "
                      "differ by more than the 25% tolerance for accessibility, which is a warning, not a refutation"),
    }


#: The extrapolation test, **pre-registered** before the `b3 = 14` measurement (dispatch
#: `2026-11-02T1020Z-pacland-rog-h12-6-rate`, 20 calls of 400 tries). Two branches, because the accessibility
#: intervals disagree: the steepening one and the global fit. The measurement decides between them.
PREDICTION_B3_14 = {
    "b3": 14,
    "steepening_branch_per_try": 0.00137 * 0.308 ** 2,     # apply the 10->12 factor twice
    "global_fit_per_try": 0.00137 * 0.481 ** 2,
    "calls": 20,
    "tries_per_call": 400,
}
PREDICTION_B3_14["steepening_points"] = PREDICTION_B3_14["steepening_branch_per_try"] * 20 * 400
PREDICTION_B3_14["global_fit_points"] = PREDICTION_B3_14["global_fit_per_try"] * 20 * 400


def check_prediction(measured_points, calls: int = 20, tries_per_call: int = 400) -> dict:
    """Compare a measured point count against the two pre-registered branches."""
    measured_rate = measured_points / (calls * tries_per_call)
    steep = PREDICTION_B3_14["steepening_branch_per_try"]
    glob = PREDICTION_B3_14["global_fit_per_try"]
    return {
        "measured_points": measured_points, "measured_rate": measured_rate,
        "steepening_branch": steep, "global_fit": glob,
        "ratio_to_steepening": measured_rate / steep if steep else float("inf"),
        "ratio_to_global": measured_rate / glob if glob else float("inf"),
        "verdict": ("closer to the steepening branch" if abs(measured_rate / steep - 1) < abs(measured_rate / glob - 1)
                    else "closer to the global fit"),
    }


__all__ = ["CONTENT", "ACCESSIBILITY", "PREDICTION_B3_14", "check_prediction", "per_unit_factor", "scales"]
