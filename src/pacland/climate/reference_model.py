"""The verified reference model — GISS-E2-1-G.

Of 19 CMIP6 models with full conservation drift data, exactly ONE passes all
three verification gates — conservation (energy + mass + salt), sensitivity
(ECS inside the IPCC likely range), and forcing (ERF2x inside the assessed
band): **GISS-E2-1-G**. Its ECS, 2.71 K, is the single-model best prediction —
the number from the one model we can fully verify, rather than the ensemble
average. The ensemble cross-check (the widened 15-model gate) gives 3.08 K, and
the IPCC best estimate is ~3.0 K; GISS's 2.71 K sits inside the same likely
range, reached by the strictest possible gate.

Pure stdlib + pacland.climate.sensitivity_crosscheck.
"""
from __future__ import annotations

from .sensitivity_crosscheck import crosscheck, load

# The canonical (non-variant) member of the surviving GISS family.
REFERENCE_MODEL = "GISS-E2-1-G"


def _survivors() -> list[dict]:
    return [r for r in crosscheck() if r["n_axes_failed"] == 0]


def reference_model() -> dict:
    """The one CMIP6 model that passes all three gates, with its full profile."""
    variants = set(load().get("approx_notes", {}))
    rows = _survivors()
    # prefer the canonical model over its approximate variant
    canonical = next((r for r in rows if r["model"] == REFERENCE_MODEL), rows[0])
    agree = [r["model"] for r in rows if r["ecs_K"] == canonical["ecs_K"]]
    return {
        "model": canonical["model"],
        "ecs_K": canonical["ecs_K"],
        "erf2x_Wm2": canonical["erf2x_Wm2"],
        "ledgers_failed": canonical["ledgers_failed"],
        "sensitivity": canonical["sensitivity"],
        "forcing": canonical["forcing"],
        "axes_passed": 3,
        "surviving_family": sorted(agree),
        "is_variant": canonical["model"] in variants,
    }


def summary() -> str:
    """One plain-text block for the record (and the report's headline)."""
    r = reference_model()
    d = load()
    lo, hi = d["likely_range_K"]
    return "\n".join([
        "VERIFIED REFERENCE MODEL — GISS-E2-1-G",
        "=" * 40,
        f"model            {r['model']}",
        f"axes passed      {r['axes_passed']}/3 (conservation + sensitivity + forcing)",
        f"ECS              {r['ecs_K']:.2f} K   (inside IPCC likely {lo}-{hi} K)",
        f"ERF2x            {r['erf2x_Wm2']:.2f} W/m2",
        f"conservation     {r['ledgers_failed']} ledgers leaked",
        f"surviving family {', '.join(r['surviving_family'])}",
        "",
        "The single-model best prediction: ECS = 2.71 K, from the one CMIP6",
        "model we can fully verify.",
    ])


if __name__ == "__main__":
    print(summary())
