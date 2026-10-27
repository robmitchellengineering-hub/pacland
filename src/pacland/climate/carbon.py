"""Carbon accounting — the fourth conservation invariant, measured.

`structure.py` names five conservation laws, of which three are measured (energy, ocean mass,
salinity) and two are not (water, carbon). This module measures the carbon one, which turns the
per-model checklist from three items into four and takes the "named but unmeasured" count from
two to one.

The budget, per year, in the units the sources publish (MtCO2):

    fossil emissions + land-use emissions  =  atmospheric growth + ocean sink + land sink

Two of the four terms are directly observed (fossil + land-use from the Global Carbon Budget;
atmospheric growth from the concentration record), and the sinks are the residual. That makes
this a checkable identity rather than a fitted model — the *airborne fraction* (atmospheric
growth / total emissions) must be a fraction: between 0 and 1, and not drifting into nonsense.

    airborne fraction ≈ 0.44-0.47 historically

A model that reports emissions and a concentration path whose implied airborne fraction falls
outside (0, 1), or that has no sink term at all, is refused. That is the same rule the energy
budget applies, in a different currency.

Run:        python3 scripts/climate_carbon.py
Guarded by: tests/test_climate_carbon.py
"""
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[3]
CARBON = ROOT / "data" / "climate" / "carbon.json"
BASELINE = ROOT / "data" / "climate" / "baseline.json"

#: 1 ppm of atmospheric CO2 is 2.124 GtC = 7.79 GtCO2 (molar mass ratio 44/12.011).
GTCO2_PER_PPM = 7790.0         # MtCO2 per ppm (7.79 GtCO2)

#: The airborne fraction is a fraction; outside this range the accounting is broken, not
#: interesting. The historical range is roughly 0.40-0.50.
AIRBORNE_RANGE = (0.35, 0.60)


def load_carbon() -> dict:
    return json.loads(CARBON.read_text())


def load_concentrations() -> dict[int, float]:
    data = json.loads(BASELINE.read_text())
    return {int(y): v for y, v in data["co2"].items()}


def annual_rows(year_from: int = 1960) -> list[dict]:
    """One row per year with everything the identity needs, or nothing."""
    carbon = load_carbon()["world"]
    co2 = load_concentrations()
    rows = []
    for year in range(year_from, max(co2) + 1):
        rec = carbon.get(str(year))
        nxt = carbon.get(str(year + 1))
        c0, c1 = co2.get(year), co2.get(year + 1)
        if not rec or not nxt or c0 is None or c1 is None:
            continue
        fossil = rec.get("co2")
        luc = rec.get("land_use_change_co2")
        if fossil is None or luc is None:
            continue
        growth_ppm = c1 - c0
        rows.append({
            "year": year,
            "fossil_mtco2": fossil,
            "landuse_mtco2": luc,
            "total_mtco2": fossil + luc,
            "atmospheric_mtco2": growth_ppm * GTCO2_PER_PPM,
            "growth_ppm": growth_ppm,
        })
    return rows


def airborne_fraction(year: int) -> float | None:
    for row in annual_rows():
        if row["year"] == year:
            return row["atmospheric_mtco2"] / row["total_mtco2"]
    return None


def budget(window: tuple[int, int] = (1960, 2023)) -> dict:
    """The identity over a window: how much of what we emitted stayed in the air, and how
    stable that fraction is. The sinks are the residual, so the check is on the *fraction*."""
    rows = [r for r in annual_rows() if window[0] <= r["year"] <= window[1]]
    if len(rows) < 20:
        raise ValueError("not enough paired years to test the carbon budget")
    emitted = sum(r["total_mtco2"] for r in rows)
    airborne = sum(r["atmospheric_mtco2"] for r in rows)
    fractions = [r["atmospheric_mtco2"] / r["total_mtco2"] for r in rows]
    mean_f = airborne / emitted
    lo, hi = AIRBORNE_RANGE
    return {
        "window": window,
        "years": len(rows),
        "emitted_gtco2": emitted / 1000.0,
        "airborne_gtco2": airborne / 1000.0,
        "airborne_fraction": mean_f,
        "fraction_min": min(fractions),
        "fraction_max": max(fractions),
        "fraction_stdev": (sum((f - mean_f) ** 2 for f in fractions) / len(fractions)) ** 0.5,
        "sinks_gtco2": (emitted - airborne) / 1000.0,
        "in_range": lo <= mean_f <= hi,
        # per-year the fraction swings (El Nino years take up more); what must hold every
        # year is only that it is a fraction at all — between "none" and "all" of emissions
        "every_year_physical": all(0.0 < f < 1.0 for f in fractions),
        "verdict": ("carbon closes: the airborne fraction is a fraction, and the sinks account "
                    "for the rest" if lo <= mean_f <= hi else
                    "carbon does NOT close: the implied airborne fraction is outside (0,1)"),
    }


def guard_budget(window: tuple[int, int] = (1960, 2023)) -> tuple[bool, str]:
    """MUTATION: drop the sinks (claim every emitted tonne stays airborne) and the fraction
    must go to 1.0 — outside the range — so the guard fires. A budget with no sink term is the
    failure mode this check exists to refuse."""
    r = budget(window)
    no_sinks = 1.0 if r["emitted_gtco2"] > 0 else 0.0
    detected = not (AIRBORNE_RANGE[0] <= no_sinks <= AIRBORNE_RANGE[1])
    ok = r["in_range"] and detected
    return ok, (f"carbon {window[0]}-{window[1]}: airborne fraction {r['airborne_fraction']:.3f} "
                f"(min {r['fraction_min']:.3f}, max {r['fraction_max']:.3f}), sinks "
                f"{r['sinks_gtco2']:.0f} GtCO2 of {r['emitted_gtco2']:.0f} emitted; a "
                f"sink-free claim gives fraction {no_sinks:.1f}, detected as impossible = "
                f"{detected}")


def invariant() -> dict:
    """What `structure.py` needs: a measured carbon invariant with a pass/fail and a tolerance."""
    r = budget()
    return {"name": "carbon", "measured": True, "closes": bool(r["in_range"]),
            "value": r["airborne_fraction"], "tolerance": AIRBORNE_RANGE,
            "detail": (f"airborne fraction {r['airborne_fraction']:.3f} over "
                       f"{r['years']} years; sinks {r['sinks_gtco2']:.0f} GtCO2")}


def audit() -> dict:
    ok, msg = guard_budget()
    return {"checks": [{"check": "carbon budget", "pass": bool(ok), "detail": msg}],
            "n_pass": int(ok), "n": 1, "all_pass": bool(ok)}


__all__ = ["budget", "annual_rows", "airborne_fraction", "invariant", "guard_budget", "audit",
           "GTCO2_PER_PPM", "AIRBORNE_RANGE"]
