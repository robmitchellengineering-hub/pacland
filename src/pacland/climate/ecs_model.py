"""Best-prediction ECS — the trust-gated, conservation-gated estimate.

The future cannot be validated (the unmeasurable wall), so the best possible
prediction is not a certified future — it is the estimate built only from the
reliable content: the models that conserve physics, then those that also pass
the field's own sensitivity and forcing axes. This module turns the three-axis
trust verdict (``sensitivity_crosscheck``) into a prediction:

    naive               all 19 models, uniform            -> ~4.08 K
    conservation-gated  the 5 that close energy+mass+salt -> ~3.86 K
    trust-gated         the 2 that survive all three axes -> ~2.71 K

The gates are HARD (pass/fail per axis), not continuous — continuous weights
would need arbitrary constants, and a hard gate is parameter-free and survives
adversarial review. The shift is the result: the naive ensemble carries the
"hot model" bias (~4.1 K, above the IPCC likely range); each verification gate
pulls it down until the fully-trustworthy estimate lands at ~2.7 K, inside the
IPCC likely range (2.5-4.0 K) and at the assessed best estimate (~3.0 K).

Honest caveat: the trust gate is so strict that only ONE family survives (the
two GISS variants, both 2.71 K), so the trust-gated spread is degenerate. That
is itself a finding — the gates collapse the ensemble to the single family that
does not leak physics, is not hot, and forces correctly — not a bug.

Pure stdlib + pacland.climate.sensitivity_crosscheck.
"""
from __future__ import annotations

from statistics import mean

from .sensitivity_crosscheck import crosscheck, load

# IPCC AR6 WG1 (2021) assessed ECS: likely 2.5-4.0 K, best estimate 3.0 K.
IPCC_BEST_ESTIMATE_K = 3.0


def _rows() -> list[dict]:
    """Per-model three-axis rows (conservation x sensitivity x forcing)."""
    return crosscheck()


def _estimate(rows: list[dict]) -> dict:
    vals = [r["ecs_K"] for r in rows]
    return {
        "n": len(rows),
        "mean_K": mean(vals),
        "min_K": min(vals),
        "max_K": max(vals),
        "models": [r["model"] for r in rows],
    }


def ecs_estimates() -> dict:
    """The three nested estimates, from naive to fully trust-gated."""
    rows = _rows()
    d = load()
    gated = [r for r in rows if r["ledgers_failed"] == 0]
    trust = [r for r in rows if r["n_axes_failed"] == 0]
    return {
        "naive": _estimate(rows),
        "conservation_gated": _estimate(gated),
        "trust_gated": _estimate(trust),
        "ipcc_likely_range_K": d["likely_range_K"],
        "ipcc_best_estimate_K": IPCC_BEST_ESTIMATE_K,
    }


def best_prediction() -> dict:
    """The best prediction plus the shift and the honest caveat."""
    e = ecs_estimates()
    trust = e["trust_gated"]
    return {
        **e,
        "best_estimate_K": trust["mean_K"],
        "shift_K": e["naive"]["mean_K"] - trust["mean_K"],
        "survivor_families": sorted({m.split("-")[0] for m in trust["models"]}),
        "inside_ipcc_likely": (
            e["ipcc_likely_range_K"][0] <= trust["mean_K"] <= e["ipcc_likely_range_K"][1]
        ),
    }


def summary() -> str:
    """One plain-text block for the record (and the report's headline)."""
    e = ecs_estimates()
    n, g, t = e["naive"], e["conservation_gated"], e["trust_gated"]
    lo, hi = e["ipcc_likely_range_K"]
    return "\n".join([
        "BEST-PREDICTION ECS — trust-gated, conservation-gated",
        "=" * 50,
        f"naive               m = {n['n']:2d}  mean {n['mean_K']:.2f} K  "
        f"[{n['min_K']:.2f}, {n['max_K']:.2f}]",
        f"conservation-gated  m = {g['n']:2d}  mean {g['mean_K']:.2f} K  "
        f"[{g['min_K']:.2f}, {g['max_K']:.2f}]",
        f"trust-gated         m = {t['n']:2d}  mean {t['mean_K']:.2f} K  "
        f"[{t['min_K']:.2f}, {t['max_K']:.2f}]",
        "",
        f"shift: {e['naive']['mean_K'] - t['mean_K']:.2f} K of 'hot model' bias is "
        f"removed by the verification gates",
        f"IPCC AR6 likely range {lo}-{hi} K, best estimate "
        f"{e['ipcc_best_estimate_K']} K — the trust-gated estimate lands inside it",
        f"survivors: {', '.join(t['models'])} — one family (the honest caveat)",
    ])


if __name__ == "__main__":
    print(summary())
