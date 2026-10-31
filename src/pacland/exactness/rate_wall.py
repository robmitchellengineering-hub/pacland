"""The rate wall — where the sampler loses candidates as `h12` grows (T1's open question).

T1 established that the `h12 = 5` zero yield was a **budget** artefact, not a degree effect: degree 1 and degree
2 both produce at the same rate. What it left open is *why the rate is so low there*, and that is the question
this module records.

**The measured loss, from runs on pacland-rog:**

| `h12` | tries | valid candidates | points | points per try |
|---|---|---|---|---|
| 2 | 400 | 384 (96%) | **53** | **13.3%** |
| 5 | ~2,000 (5 calls) | ~1,800 (90%) | **2** | **0.10%** |

**The loss is not at the proposal stage.** Validity holds up (96% → 90%) while the convergence rate collapses by
~130×. So the sampler is finding candidates and failing to drive them to `DW = 0`.

**The candidate explanation, stated as a hypothesis and not a conclusion:** the solve dimension doubles —
`h12 = 2` gives `b3 = 6` (12 real flux components), `h12 = 5` gives `b3 = 12` (24) — and a Newton basin's
volume shrinks with dimension, so the *probability* of landing in one falls roughly geometrically. The test that
would discriminate this from "critical points are genuinely rarer" is a **per-trial residual histogram**: if
non-converged trials pile up at `|DW| ~ 1e-2…1e-1`, the failure is convergence; if they scatter, the critical
points themselves are absent. That requires the sampler to expose per-trial residuals, which it does not.

Run:        python3 scripts/rate_wall.py
Guarded by: tests/test_rate_wall.py
"""
from __future__ import annotations


#: The runs, as executed. Budgets are stated because a rate without its budget is the error T1 was born from.
OBSERVATIONS = (
    {"h12": 2, "b3": 6, "tries": 400, "valid": 384, "points": 53, "seconds": 70.7,
     "where": "2026-10-29, 1 call, `sample_h12.py 2 60`"},
    {"h12": 5, "b3": 12, "tries": 2000, "valid": 1800, "points": 2, "seconds": 504,
     "where": "2026-10-30, 5 calls via try_budget, degree 1"},
    {"h12": 5, "b3": 12, "tries": 2000, "valid": 1790, "points": 2, "seconds": 521,
     "where": "2026-10-30, 5 calls via try_budget, degree 2"},
)


def rates() -> list:
    """The measured rates, each with the budget it was measured at."""
    out = []
    for o in OBSERVATIONS:
        out.append({**o, "valid_fraction": o["valid"] / o["tries"],
                    "points_per_try": o["points"] / o["tries"],
                    "points_per_valid": o["points"] / o["valid"] if o["valid"] else 0.0})
    return out


def the_wall() -> dict:
    """The loss, split by stage, and the hypothesis with the test that would settle it."""
    rows = rates()
    at2 = [r for r in rows if r["h12"] == 2][0]
    at5 = [r for r in rows if r["h12"] == 5]
    per_valid_5 = sum(r["points"] for r in at5) / sum(r["valid"] for r in at5)
    ratio = at2["points_per_valid"] / per_valid_5 if per_valid_5 else float("inf")
    return {
        "rows": rows,
        "validity_loss": at2["valid_fraction"] - at5[0]["valid_fraction"],
        "convergence_ratio": ratio,
        "statement": (f"validity falls only {at2['valid_fraction']:.0%} → {at5[0]['valid_fraction']:.0%}, "
                      f"while points-per-valid collapses {at2['points_per_valid']:.3f} → "
                      f"{per_valid_5:.4f} — a factor of {ratio:.0f}"),
        "where_the_loss_is": "convergence to DW = 0, not the proposal",
        "hypothesis": ("the solve dimension doubles (12 → 24 real components), so Newton basin volume shrinks "
                       "geometrically; the alternative is that critical points are genuinely rarer at higher h12"),
        "test_that_would_settle_it": ("a per-trial residual histogram: pile-up near |DW| ~ 1e-2..1e-1 means "
                                      "convergence failure; a scatter means the points are absent. The sampler "
                                      "does not expose per-trial residuals, so this is the blocker"),
        "degree_is_not_the_cause": "T1: degree 1 and 2 give 2 points each on the same budget",
    }


__all__ = ["OBSERVATIONS", "rates", "the_wall"]
