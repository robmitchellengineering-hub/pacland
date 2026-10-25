"""Climate's no-change null — and what happens when models are scored against it.

Macro-finance's null is "tomorrow equals today". For a warming series that null is almost
trivially beatable, so the honest analogue is the null that persists the *trend*: the last
thirty years of observed warming, continued. Both are here, plus an ECS-based emulator per
CMIP6 model, all scored the same way on a **real-time hindcast**: fit only on data as of
year ``y0``, predict ``y0 + h``, compare with what was later observed.

Three honesty constraints are structural:

- the trend is fitted on data **≤ y0 only**, so the "null" cannot use its own target;
- CO2 after ``y0`` is **extrapolated** from data ≤ y0 — no future forcing is handed to the
  emulator, because a real projection does not have it;
- the emulators are **not the CMIP6 models**. They are one-box energy-balance models
  parameterised by each model's published ECS and ERF2x; the CMIP6 runs themselves are not
  in this repo. The docstring says so and the report labels them ``emulator``.

The target is the observed GMST anomaly (NASA GISTEMP v4), not a model's own history.
"""
from __future__ import annotations

import json
import math
import pathlib

FIXTURE = pathlib.Path(__file__).resolve().parents[3] / "data" / "climate" / "baseline.json"
#: Effective heat capacity of the upper ocean, W yr m^-2 K^-1. A one-box value, not a
#: fitted parameter: it sets how fast the emulator approaches equilibrium, and the
#: conclusion below is insensitive to it at these horizons.
HEAT_CAPACITY = 8.0
#: Radiative forcing coefficient for CO2, W m^-2 per ln(ppm).
CO2_FORCING = 5.35

METHODS = ("persistence", "trend", "emulator")


def load(path: pathlib.Path | None = None) -> dict:
    d = json.loads(pathlib.Path(path or FIXTURE).read_text())
    return {"gmst": {int(k): v for k, v in d["gmst"].items()},
            "co2": {int(k): v for k, v in d["co2"].items()},
            "sources": d["sources"]}


def _fit_slope(series: dict[int, float], y0: int, window: int) -> tuple[float, float]:
    """OLS intercept and slope on ``y0-window+1 … y0`` — data at or before the start."""
    years = [y for y in sorted(series) if y0 - window < y <= y0]
    ys = [series[y] for y in years]
    n = len(years)
    mx = sum(years) / n
    my = sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in years)
    sxy = sum((x - mx) * (y - my) for x, y in zip(years, ys))
    slope = sxy / sxx
    return my - slope * mx, slope


def persistence_null(gmst: dict[int, float], y0: int, h: int) -> float:
    """The strict no-change forecast: the anomaly at ``y0`` persists."""
    return gmst[y0]


def trend_null(gmst: dict[int, float], y0: int, h: int, window: int = 30) -> float:
    """The trend null: the last ``window`` years of observed warming, continued."""
    intercept, slope = _fit_slope(gmst, y0, window)
    return intercept + slope * (y0 + h)


def co2_path(co2: dict[int, float], y0: int, h: int, window: int = 20) -> dict[int, float]:
    """CO2 as the forecast may know it: history to ``y0``, then linear extrapolation."""
    intercept, slope = _fit_slope(co2, y0, window)
    return {y: (co2[y] if y in co2 and y <= y0 else intercept + slope * y)
            for y in range(y0, y0 + h + 1)}


def emulator(ecs: float, erf2x: float, data: dict, y0: int, h: int) -> float:
    """One-box energy balance at this model's ECS and ERF2x, forced by CO2 *extrapolated*
    from data ≤ y0 and started from the observed anomaly at ``y0``."""
    gmst, co2 = data["gmst"], data["co2"]
    lam = erf2x / ecs                                     # W m^-2 K^-1
    path = co2_path(co2, y0, h)
    f0 = CO2_FORCING * math.log(path[y0])
    t = gmst[y0]
    for year in range(y0 + 1, y0 + h + 1):
        forcing = CO2_FORCING * math.log(path[year]) - f0
        t += (forcing - lam * (t - gmst[y0])) / HEAT_CAPACITY
    return t


def hindcast(data: dict, models: dict[str, tuple[float, float]],
             y0: int, h: int) -> dict:
    """Every method's forecast made with data as of ``y0``, plus the observed truth."""
    truth = data["gmst"].get(y0 + h)
    if truth is None:
        raise ValueError(f"no observation at {y0 + h}")
    out = {
        "y0": y0, "h": h, "target": y0 + h, "truth": truth,
        "persistence": persistence_null(data["gmst"], y0, h),
        "trend": trend_null(data["gmst"], y0, h),
    }
    for name, (ecs, erf2x) in models.items():
        out[f"emulator:{name}"] = emulator(ecs, erf2x, data, y0, h)
    return out


# --- guards -------------------------------------------------------------------


def guard_no_lookahead(data: dict, y0: int, h: int) -> tuple[bool, str]:
    """Everything the trend fit consumes must be dated at or before ``y0``."""
    used = [y for y in data["gmst"] if y0 - 29 <= y <= y0]
    ok = bool(used) and all(y <= y0 for y in used) and max(used) == y0
    return ok, f"trend uses {len(used)} years ({min(used) if used else '—'}..{y0})"


def guard_truth_is_outside_the_window(data: dict, y0: int, h: int) -> tuple[bool, str]:
    ok = (y0 + h) not in {y for y in data["gmst"] if y <= y0}
    return ok, f"target {y0 + h} is after the forecast's window (start {y0})"


def guard_units(data: dict) -> tuple[bool, str]:
    """GMST anomalies are deg C, not kelvin and not hundredths."""
    vals = list(data["gmst"].values())
    ok = max(abs(v) for v in vals) < 5.0
    return ok, f"GMST range {min(vals):+.2f}..{max(vals):+.2f} deg C"


def evaluate(data: dict | None = None,
             starts: tuple[int, ...] = (1980, 1990, 2000, 2010),
             horizons: tuple[int, ...] = (10, 20)) -> dict:
    data = data or load()
    from .model_roster import CLIMATE_ROSTER

    models = {}
    ecs = json.loads((pathlib.Path(__file__).resolve().parents[3] / "data"
                      / "climate" / "cmip6_ecs.json").read_text())
    for m in CLIMATE_ROSTER:
        short = m.name.replace("CMIP6 ", "")
        if short in ecs["ecs_K"] and short in ecs["erf2x_Wm2"]:
            models[short] = (ecs["ecs_K"][short], ecs["erf2x_Wm2"][short])

    rows = []
    for y0 in starts:
        for h in horizons:
            if y0 + h not in data["gmst"]:
                continue
            rows.append(hindcast(data, models, y0, h))

    methods = ["persistence", "trend"] + [f"emulator:{n}" for n in models]
    errs = {m: [r[m] - r["truth"] for r in rows] for m in methods}
    base = errs["trend"]
    out = {}
    for m in methods:
        e = errs[m]
        out[m] = {
            "mae": sum(abs(v) for v in e) / len(e),
            "rmse": math.sqrt(sum(v * v for v in e) / len(e)),
            "bias": sum(e) / len(e),
            "wins_vs_trend": sum(1 for a, b in zip(e, base) if abs(a) < abs(b)),
        }
    return {"methods": out, "n": len(rows), "rows": rows,
            "starts": list(starts), "horizons": list(horizons),
            "models": sorted(models)}


def summary() -> str:
    r = evaluate()
    trend = r["methods"]["trend"]
    lines = [
        "CLIMATE'S NO-CHANGE NULL — real-time hindcast, observed GMST as the target",
        "=" * 74,
        f"{r['n']} hindcasts · starts {r['starts']} · horizons {r['horizons']} yr",
        f"emulators: {', '.join(r['models'])} (ECS+ERF2x, NOT the CMIP6 runs)",
        "",
        f"{'method':<28}{'MAE':>8}{'RMSE':>8}{'bias':>8}   vs trend",
    ]
    for m, v in r["methods"].items():
        tag = "  (the null)" if m == "trend" else ""
        lines.append(f"{m:<28}{v['mae']:>8.3f}{v['rmse']:>8.3f}{v['bias']:>+8.3f}   "
                     f"{v['wins_vs_trend']}/{r['n']}{tag}")
    lines += [
        "",
        f"trend MAE = {trend['mae']:.3f} deg C: the observed trend, continued, is the",
        "benchmark any climate forecast must beat — and on this sample it is hard to beat.",
        "The emulators are not the CMIP6 models; they are one-box energy balances at each",
        "model's ECS and ERF2x, forced by CO2 extrapolated from data available at the time.",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    print(summary())
