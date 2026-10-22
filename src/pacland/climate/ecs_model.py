"""Best-prediction ECS — the trust-gated, conservation-gated estimate.

The future cannot be validated (the unmeasurable wall), so the best possible
prediction is the estimate built only from the reliable content: the models
that pass the gates we can actually run. Two views, over two data covers:

WIDENED — the full 53-model Zelinka et al. 2020 table, sensitivity + forcing
gates only (conservation drift exists for only 19 of them):

    naive (53)            ~3.78 K
    sens+forc gated (15)  ~3.08 K, 13 families, range 2.56-3.87 K

STRICT — the 19 models with conservation drift (Irving et al. 2021), all three
axes (conservation x sensitivity x forcing):

    naive (19)            ~4.08 K
    conservation (5)      ~3.86 K
    three-axis (2 GISS)   ~2.71 K, one family

The widened gate is the best prediction: a genuine multi-family ensemble at the
IPCC best estimate (~3.0 K). The strict three-axis gate shows conservation's
power but collapses to a single family. Together they bracket ECS at ~2.7-3.1 K.

Honest notes: the 19-model drift subset is hot-biased (naive 4.08 K vs the full
53's 3.78 K), so the two naives differ — each gate is reported over its own
cover and never mixed. Gates are HARD (pass/fail per axis), parameter-free.

Pure stdlib + pacland.climate.sensitivity_crosscheck.
"""
from __future__ import annotations

import re
from statistics import mean

from .sensitivity_crosscheck import crosscheck, load

# IPCC AR6 WG1 (2021) assessed ECS: likely 2.5-4.0 K, best estimate 3.0 K.
IPCC_BEST_ESTIMATE_K = 3.0


def family(name: str) -> str:
    """Model family by leading non-digit prefix (naming heuristic)."""
    return re.split(r"\d", name)[0].rstrip("-")


def _est(models: list[str], ecs: dict[str, float]) -> dict:
    vals = [ecs[m] for m in models]
    return {
        "n": len(models),
        "mean_K": mean(vals),
        "min_K": min(vals),
        "max_K": max(vals),
        "models": sorted(models),
    }


def ecs_estimates() -> dict:
    """Both views: widened (55, sens+forc) and strict (19, three-axis)."""
    d = load()
    ecs = d["ecs_K"]
    erf = d["erf2x_Wm2"]
    variants = set(d.get("approx_notes", {}))
    widened = [m for m in ecs if m not in variants]
    lo, hi = d["likely_range_K"]
    flo, fhi = d["forcing_range_Wm2"]
    sens_forc = [m for m in widened if lo <= ecs[m] <= hi and flo <= erf[m] <= fhi]

    rows = crosscheck()
    strict_naive = [r["model"] for r in rows]
    cons = [r["model"] for r in rows if r["ledgers_failed"] == 0]
    trust = [r["model"] for r in rows if r["n_axes_failed"] == 0]

    return {
        "widened_naive": _est(widened, ecs),
        "sens_forc_gated": _est(sens_forc, ecs),
        "strict_naive": _est(strict_naive, ecs),
        "conservation_gated": _est(cons, ecs),
        "trust_gated": _est(trust, ecs),
        "sens_forc_families": len({family(m) for m in sens_forc}),
        "trust_families": len({family(m) for m in trust}),
        "ipcc_likely_range_K": d["likely_range_K"],
        "ipcc_best_estimate_K": IPCC_BEST_ESTIMATE_K,
    }


def best_prediction() -> dict:
    """The widened best + the strict best + the honest bracket."""
    e = ecs_estimates()
    sf = e["sens_forc_gated"]
    t = e["trust_gated"]
    lo, hi = e["ipcc_likely_range_K"]
    return {
        **e,
        "best_estimate_K": sf["mean_K"],       # widened (the ensemble best)
        "strict_estimate_K": t["mean_K"],      # three-axis (the strictest subset)
        "bracket_K": [t["mean_K"], sf["mean_K"]],
        "shift_naive_to_widened_K": e["widened_naive"]["mean_K"] - sf["mean_K"],
        "shift_naive_to_strict_K": e["strict_naive"]["mean_K"] - t["mean_K"],
        "inside_ipcc_likely": (
            lo <= sf["mean_K"] <= hi and lo <= t["mean_K"] <= hi
        ),
    }


def summary() -> str:
    """One plain-text block for the record (and the report's headline)."""
    e = ecs_estimates()
    wn, sf = e["widened_naive"], e["sens_forc_gated"]
    sn, cg, tg = e["strict_naive"], e["conservation_gated"], e["trust_gated"]
    lo, hi = e["ipcc_likely_range_K"]
    return "\n".join([
        "BEST-PREDICTION ECS — trust-gated, conservation-gated",
        "=" * 52,
        "WIDENED (53 models, sensitivity + forcing gates):",
        f"  naive ({wn['n']:2d})       {wn['mean_K']:.2f} K  [{wn['min_K']:.2f}, {wn['max_K']:.2f}]",
        f"  sens+forc ({sf['n']:2d})   {sf['mean_K']:.2f} K  [{sf['min_K']:.2f}, {sf['max_K']:.2f}]  "
        f"({e['sens_forc_families']} families)",
        "STRICT (19 models with conservation drift, all three axes):",
        f"  naive ({sn['n']:2d})       {sn['mean_K']:.2f} K  [{sn['min_K']:.2f}, {sn['max_K']:.2f}]",
        f"  conservation ({cg['n']:2d}) {cg['mean_K']:.2f} K",
        f"  three-axis ({tg['n']:2d})    {tg['mean_K']:.2f} K  ({e['trust_families']} family)",
        "",
        f"best prediction {sf['mean_K']:.2f} K (widened ensemble), strict subset "
        f"{tg['mean_K']:.2f} K -> bracket [{tg['mean_K']:.2f}, {sf['mean_K']:.2f}] K",
        f"IPCC AR6 likely {lo}-{hi} K, best estimate {e['ipcc_best_estimate_K']} K",
    ])


if __name__ == "__main__":
    print(summary())
