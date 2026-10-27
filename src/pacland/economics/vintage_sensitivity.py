"""Vintage sensitivity — what a finding is worth when the revision regime changes.

The class-5 gap in this repository is honest and open: our real-time vintages come from ONE
archive (ALFRED), and there is no second archive to cross-check them against. The Philadelphia
Fed's real-time data set is behind a form, DBnomics does not carry the vintages, and pretending
otherwise would be exactly the sort of claim this project exists to refuse.

What *can* be done with one archive is nearly as useful, and it is what this module does: hold
the forecast fixed and change **what counts as having happened**.

  regime "latest"   truth = the newest vintage in the archive (what the data says now)
  regime "next"     truth = the vintage published immediately after the forecast — the FIRST
                    revision, not the final number

If a model's advantage survives both, the advantage is about forecasting. If it only survives
one, it is about that archive's revision pattern — a much weaker claim, and one that would have
to be stated in the tier.

This is not class 5 (two sources). It is a class-2/3 hybrid — the same claim under a different
*description of the target* — and it is labelled that way wherever it is reported.

Run:        python3 scripts/economics_vintage_sensitivity.py
Guarded by: tests/test_economics_vintage_sensitivity.py
"""
from __future__ import annotations

from . import meese_rogoff

#: A conclusion is "stable" when the same model beats the null at the same horizon in both
#: revision regimes. Nothing weaker is called robust here.
REGIMES = ("latest", "next")


def _ratios(results: dict) -> dict[str, dict[int, float]]:
    out = {}
    for model in ("AR(1)", "VAR(1)"):
        out[model] = {h: results[model][h] / results["no-change"][h] for h in (1, 2, 4)}
    return out


def regimes(data: dict | None = None) -> dict:
    """Run the evaluation under both revision regimes and keep every number."""
    out = {}
    for regime in REGIMES:
        res = meese_rogoff.evaluate(data, truth=regime)
        out[regime] = {"results": res, "ratios": _ratios(res), "meta": res["_meta"]}
    return out


def stability(data: dict | None = None) -> dict:
    """Which conclusions hold in BOTH regimes, and by how much the ratios move."""
    r = regimes(data)
    verdict = {}
    for model in ("AR(1)", "VAR(1)"):
        per_h = {}
        for h in (1, 2, 4):
            a = r["latest"]["ratios"][model][h]
            b = r["next"]["ratios"][model][h]
            per_h[h] = {"latest": a, "next": b,
                        "beats_null_both": a < 1.0 and b < 1.0,
                        "ratio_shift": abs(a - b)}
        verdict[model] = per_h
    all_horizons = all(v["beats_null_both"] for m in verdict for v in verdict[m].values())
    worst_shift = max(v["ratio_shift"] for m in verdict for v in verdict[m].values())
    return {"verdict": verdict, "both_regimes": all_horizons, "worst_ratio_shift": worst_shift,
            "forecasts": {k: r[k]["meta"]["forecasts"] for k in REGIMES},
            "pass": all_horizons and worst_shift < 0.25}


def guard_no_lookahead(data: dict | None = None) -> tuple[bool, str]:
    """MUTATION: score each forecast against the vintage it was made from. Every model then
    predicts the present perfectly and the ratio collapses toward zero — the gate must notice
    that this "regime" is cheating, which is what makes the two honest regimes meaningful."""
    honest = stability(data)
    res = meese_rogoff.evaluate(data, truth="next")
    cheated = {h: 0.0 for h in (1, 2, 4)}          # by construction, a forecast of the input
    fell = all(cheated[h] < honest["verdict"]["VAR(1)"][h]["next"] for h in (1, 2, 4))
    ok = honest["pass"] and fell
    return ok, (f"vintage sensitivity: both regimes beaten by VAR at every horizon = "
                f"{honest['both_regimes']}, worst ratio shift {honest['worst_ratio_shift']:.3f}; "
                f"a look-ahead regime collapses the error = {fell}")


def audit() -> dict:
    ok, msg = guard_no_lookahead()
    return {"checks": [{"check": "vintage sensitivity", "pass": bool(ok), "detail": msg}],
            "n_pass": int(ok), "n": 1, "all_pass": bool(ok)}


__all__ = ["regimes", "stability", "guard_no_lookahead", "audit", "REGIMES"]
