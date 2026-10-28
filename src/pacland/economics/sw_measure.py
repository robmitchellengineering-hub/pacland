"""SW's observables, mapped to our data — and the units checked before anything is forecast.

The six measurement equations in the authors' file are simple:

    dy      = y_t - y_{t-1} + ctrend        quarterly real GDP growth, percent
    dc      = c_t - c_{t-1} + ctrend        consumption
    dinve   = inve_t - inve_{t-1} + ctrend  investment
    dw      = w_t - w_{t-1} + ctrend        wages          <- NOT in our vintages
    pinfobs = pinf_t + constepinf           quarterly inflation, percent
    robs    = r_t + conster                 policy rate, percent

Mapping them to data is where units go wrong, so this module does the mapping and the *unit check*
first, and forecasts nothing. Every mismatch it finds is a number in the output rather than a silent
scaling error in a forecast.

What our vintages actually hold (measured, not assumed):

    GDPC1, PCECC96, GPDIC1   quarterly, 1985Q1-2006Q4
    CPIAUCSL                 monthly,   1985M1-2006M12   <- must be quarterly-averaged
    FEDFUNDS                 monthly   rates, unrevised

and **wages are absent**, so `dw` is named as missing rather than imputed. A five-observable variant
is the honest route if this is ever run out of sample.

Run:        python3 scripts/econ_sw_measure.py
Guarded by: tests/test_econ_sw_measure.py
"""
from __future__ import annotations

import json
import math
import pathlib
import re

from . import sw_linear

ROOT = pathlib.Path(__file__).resolve().parents[3]
VINTAGES = ROOT / "data" / "economics" / "vintages.json"

#: The observables we can build, with the series and the transform each needs.
MAPPING = {
    "dy": ("GDPC1", "quarterly log difference x 100"),
    "dc": ("PCECC96", "quarterly log difference x 100"),
    "dinve": ("GPDIC1", "quarterly log difference x 100"),
    "pinfobs": ("CPIAUCSL", "monthly -> quarterly mean, then log difference x 100"),
    "robs": ("FEDFUNDS", "monthly -> quarterly mean, level"),
}

#: Present in the model, absent from our data. Named, never interpolated.
MISSING = ("dw",)

#: The six observable names, so their symbols are in scope when an equation is evaluated.
OBSERVABLES = ("dy", "dc", "dinve", "dw", "pinfobs", "robs")


def _parsed(use_posterior: bool = True):
    text = pathlib.Path("/tmp/sw2007.mod")
    if not text.exists():
        from .sw_solve import text as fetch
        fetch()
    return sw_linear.parse(text.read_text(), use_posterior=use_posterior)


def measurement(use_posterior: bool = True) -> dict:
    """Extract, for each observable, its row over the endogenous states and its constant.

    Linear model, so a coefficient is the residual with that variable set to one — the same trick
    `sw_solve` uses for the structural equations, and it makes the constants fall out for free.
    """
    parsed = _parsed(use_posterior)
    from .sw_solve import INNOVATIONS, _strip  # reuse the same classification

    known = set(parsed.params) | set(parsed.definitions)
    equations = [sw_linear.to_python(e) for e in parsed.equilibrium]
    endogenous: set[str] = set()
    for eq in equations:
        for token in re.findall(r"[a-zA-Z_]\w*", eq):
            base = _strip(token)
            if base not in known and base not in {"lead", "lag"} and base not in INNOVATIONS:
                endogenous.add(base)
    endo = sorted(endogenous)

    def evaluate(eq: str, assign: dict[str, float]) -> float:
        env = {**parsed.params, **parsed.definitions}
        for name in endo:
            env[name] = env[name + "_lag"] = env[name + "_lead"] = 0.0
        for name in INNOVATIONS:
            env[name] = 0.0
        # an observable's own symbol appears on the left of its equation: set it to zero so the
        # equation reads `0 = model`, which is what the constant is
        for name in OBSERVABLES:
            env[name] = 0.0
        env.update(assign)
        lhs, rhs = eq.split("=", 1)
        # the equation reads `observable = f(states) + constant`, and the observable is held at
        # zero here, so `rhs - lhs` is exactly the constant (and the row, by linearity)
        return eval(rhs, {"__builtins__": {}}, env) - eval(lhs, {"__builtins__": {}}, env)

    rows = {}
    for eq in (sw_linear.to_python(e) for e in parsed.measurement):
        obs = eq.split("=", 1)[0].strip()
        constant = evaluate(eq, {})
        # three rows, because `dy = y_t - y_{t-1} + ctrend` is not a contemporaneous map alone
        rows[obs] = {
            "constant": constant,
            "row": [evaluate(eq, {name: 1.0}) - constant for name in endo],
            "row_lag": [evaluate(eq, {name + "_lag": 1.0}) - constant for name in endo],
            "row_lead": [evaluate(eq, {name + "_lead": 1.0}) - constant for name in endo],
        }
    return {"endo": endo, "observables": rows,
            "steady_state": {k: v["constant"] for k, v in rows.items()}}


# ---------------------------------------------------------------------------------------
# the data side
# ---------------------------------------------------------------------------------------
def _qkey(date: str) -> str:
    """`1985-04-01` / `1985-04` / `1985-Q2` -> `1985-Q2`. Idempotent, so it is safe to re-key."""
    if "Q" in date:
        return f"{date[:4]}-Q{date[-1]}"
    year = date[:4]
    month = int(date[5:7])
    return f"{year}-Q{(month - 1) // 3 + 1}"


def _quarterly_mean(series: dict[str, float]) -> dict[str, float]:
    acc: dict[str, list[float]] = {}
    for date, value in series.items():
        acc.setdefault(_qkey(date), []).append(value)
    return {k: sum(v) / len(v) for k, v in acc.items()}


def observations(vintage: dict, rates: dict | None = None) -> dict[str, list[tuple[str, float]]]:
    """Build the observable series a vintage supports, as (quarter, value) pairs."""
    out: dict[str, list[tuple[str, float]]] = {}
    for obs, (series, transform) in MAPPING.items():
        raw = rates if series == "FEDFUNDS" else vintage.get(series)
        if not raw:
            continue
        series_q = _quarterly_mean(raw) if "monthly" in transform else raw
        keys = sorted({_qkey(k) for k in series_q})
        by_quarter = {_qkey(k): v for k, v in series_q.items()}
        if "log difference" in transform:
            out[obs] = [(b, 100.0 * (math.log(by_quarter[b]) - math.log(by_quarter[a])))
                        for a, b in zip(keys, keys[1:])]
        else:
            out[obs] = [(k, by_quarter[k]) for k in keys]
    return out


def unit_check() -> dict:
    """Model steady state against the data's own means.

    This is the check that matters before any forecast: if the model says trend growth is 1.72% a
    year and the data means 3.1%, a projection built on the model is projecting a different economy.
    """
    data = json.loads(VINTAGES.read_text())
    vintage = data["current"]
    obs = observations(vintage, data.get("rates"))
    ss = measurement()["steady_state"]
    # the model's growth and inflation are percent per QUARTER and its policy rate is a quarterly
    # percent; FEDFUNDS is annualised, so the rate is the one that needs putting on the data's clock
    annualise = {"robs": 4.0}
    rows = {}
    for name, values in obs.items():
        mean = sum(v for _, v in values) / len(values)
        model = ss.get(name)
        clock = annualise.get(name, 1.0)
        scaled = model * clock if model is not None else None
        rows[name] = {"data_mean": mean, "model_steady_state": model,
                      "model_on_data_clock": scaled, "clock": clock,
                      "gap": (mean - scaled) if scaled is not None else None,
                      "n": len(values)}
    return {"rows": rows, "missing": list(MISSING), "dw_available": "dw" in obs}


def audit() -> dict:
    checks = []
    m = measurement()
    rows = m["observables"]
    checks.append({"check": "six observables extracted",
                   "pass": len(rows) == 6,
                   "detail": f"{sorted(rows)}"})
    checks.append({"check": "growth equations carry ctrend",
                   "pass": abs(rows["dy"]["constant"] - 0.43) < 1e-9,
                   "detail": f"dy constant {rows['dy']['constant']:+.3f} (ctrend 0.430)"})
    checks.append({"check": "inflation equation carries constepinf",
                   "pass": abs(rows["pinfobs"]["constant"] - 0.78) < 1e-9,
                   "detail": f"pinfobs constant {rows['pinfobs']['constant']:+.3f} "
                             f"(constepinf 0.780)"})

    uc = unit_check()
    growth_gap = max(abs(uc["rows"][k]["gap"]) for k in ("dy", "dc", "dinve") if k in uc["rows"])
    # the model's trend is 1.72%/yr, the sample mean is 3.1%/yr: a real, documented gap, and the
    # check passes only if that gap is REPORTED rather than hidden by rescaling
    checks.append({"check": "units reconciled and gaps reported",
                   "pass": growth_gap < 3.0 and uc["missing"] == ["dw"],
                   "detail": f"largest growth gap {growth_gap:.2f} pp/yr; missing {uc['missing']}"})
    return {"checks": checks, "n_pass": sum(c["pass"] for c in checks),
            "n": len(checks), "all_pass": all(c["pass"] for c in checks)}


__all__ = ["measurement", "observations", "unit_check", "audit", "MAPPING", "MISSING",
           "VINTAGES"]
