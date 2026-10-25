"""The NK 3-equation model, out of sample and in real time.

The model is fully specified now (`nk3.policy_function`): two AR(1) shocks, solved by
undetermined coefficients, so given an observed state it produces a forecast. This module
runs that forecast on the committed ALFRED vintages against the no-change null and an
AR(1), for the two things the model actually forecasts — **inflation** and the **output
gap** — and scores it against today's revised values.

Two honesty constraints are structural, not decorative:

- the calibration is **stated**, not estimated (``nk3.CALIBRATION``) — so this is the
  textbook NK model forecasting, and the doc says so;
- the output gap is built **inside each vintage** (a one-sided linear trend on that
  vintage's own data), so the "gap" the model sees contains no future information.

Pure stdlib.
"""
from __future__ import annotations

import math

from . import nk3, vintages

WINDOW = 20          # quarters in the one-sided trend
QUARTER_MONTHS = (1, 4, 7, 10)
MODELS = ("no-change", "AR(1)", "NK3")


def quarterly(obs: dict[str, float]) -> dict[str, float]:
    """Keep quarter-start observations only (a monthly series is sampled to quarters)."""
    return {d: v for d, v in obs.items() if int(d.split("-")[1]) in QUARTER_MONTHS and v > 0}


def gap(levels: dict[str, float], date: str, window: int = WINDOW) -> float:
    """One-sided linear-trend gap at ``date``, fitted only on observations up to it."""
    dates = sorted(d for d in levels if d <= date)
    if len(dates) < window:
        return float("nan")
    pts = [(i, math.log(levels[d])) for i, d in enumerate(dates[-window:])]
    n = len(pts)
    mx = sum(p[0] for p in pts) / n
    my = sum(p[1] for p in pts) / n
    sxx = sum((p[0] - mx) ** 2 for p in pts)
    sxy = sum((p[0] - mx) * (p[1] - my) for p in pts)
    slope = sxy / sxx if sxx else 0.0
    trend = my + slope * ((n - 1) - mx)
    return 100.0 * (pts[-1][1] - trend)


def inflation(levels: dict[str, float], date: str) -> float:
    """Annualised quarterly log change of the price level at ``date``."""
    dates = sorted(d for d in levels if d <= date)
    if len(dates) < 2:
        return float("nan")
    a, b = levels[dates[-2]], levels[dates[-1]]
    return 400.0 * math.log(b / a)


def _ar1(y: list[float], h: int) -> float:
    """AR(1) with intercept, fitted on the vintage's own observations, iterated."""
    if len(y) < 5:
        return y[-1]
    xs = [[1.0, y[i - 1]] for i in range(1, len(y))]
    ys = y[1:]
    n = len(ys)
    s1 = sum(r[1] for r in xs)
    s11 = sum(r[1] * r[1] for r in xs)
    s0 = float(n)
    sy = sum(ys)
    s1y = sum(r[1] * v for r, v in zip(xs, ys))
    det = s0 * s11 - s1 * s1
    if abs(det) < 1e-12:
        return y[-1]
    c = (s11 * sy - s1 * s1y) / det
    rho = (s0 * s1y - s1 * sy) / det
    v = y[-1]
    for _ in range(h):
        v = c + rho * v
    return v


def _series(vintage: vintages.Vintage, series: str) -> dict[str, float]:
    return quarterly(vintage.series.get(series, {}))


def evaluate(
    data: dict | None = None, horizons: tuple[int, ...] = (1, 2, 4),
    cal: dict | None = None,
) -> dict:
    data = data or vintages.load()
    cur = vintages.current(data)
    cur_gdp, cur_cpi = quarterly(cur["GDPC1"]), quarterly(cur["CPIAUCSL"])

    errs = {m: {t: {h: [] for h in horizons} for t in ("pi", "gap")} for m in MODELS}
    wins = {m: {t: {h: 0 for h in horizons} for t in ("pi", "gap")}
            for m in MODELS if m != "no-change"}
    n_forecasts, skipped = 0, 0

    for vintage in vintages.vintages(data):
        gdp, cpi = _series(vintage, "GDPC1"), _series(vintage, "CPIAUCSL")
        if not gdp or not cpi:
            skipped += 1
            continue
        t0 = min(max(gdp), max(cpi))
        x0 = gap(gdp, t0)
        pi0 = inflation(cpi, t0)
        if math.isnan(x0) or math.isnan(pi0):
            skipped += 1
            continue
        gdp_hist = [v for _, v in sorted(gdp.items()) if _ <= t0]
        x_hist = [gap(gdp, d) for d, _ in sorted(gdp.items()) if d <= t0]
        cpi_hist = [v for _, v in sorted(cpi.items()) if _ <= t0]
        pi_hist = [inflation(cpi, d) for d, _ in sorted(cpi.items()) if d <= t0]
        x_hist = [v for v in x_hist if not math.isnan(v)]
        pi_hist = [v for v in pi_hist if not math.isnan(v)]

        for h in horizons:
            target = _next_quarter(t0, h)
            try:
                truth_gap = gap(cur_gdp, target)
                truth_pi = inflation(cur_cpi, target)
            except (KeyError, IndexError):
                continue
            if math.isnan(truth_gap) or math.isnan(truth_pi):
                continue
            xh, pih = nk3.forecast_from_state(x0, pi0, h, cal)
            fc = {
                "pi": {"no-change": pi0, "AR(1)": _ar1(pi_hist, h), "NK3": pih},
                "gap": {"no-change": x0, "AR(1)": _ar1(x_hist, h), "NK3": xh},
            }
            truth = {"pi": truth_pi, "gap": truth_gap}
            for target_kind in ("pi", "gap"):
                e = {m: fc[target_kind][m] - truth[target_kind] for m in MODELS}
                for m in MODELS:
                    errs[m][target_kind][h].append(e[m])
                for m in wins:
                    if abs(e[m]) < abs(e["no-change"]):
                        wins[m][target_kind][h] += 1
            n_forecasts += 1

    out: dict = {}
    for m in MODELS:
        out[m] = {}
        for t in ("pi", "gap"):
            out[m][t] = {h: (math.sqrt(sum(e * e for e in v) / len(v)) if v else float("nan"))
                         for h, v in errs[m][t].items()}
            out[m][t]["n"] = {h: len(v) for h, v in errs[m][t].items()}
    for m in wins:
        out[m]["wins"] = wins[m]
    out["_meta"] = {"vintages": len(vintages.vintages(data)), "skipped": skipped,
                    "forecasts": n_forecasts, "calibration": "stated, not estimated",
                    "params": dict(cal or nk3.CALIBRATION),
                    "unit": "inflation: annualised pp; gap: pp"}
    ok, msg = vintages.guard_benchmark_present({m: out[m] for m in MODELS})
    if not ok:
        raise ValueError(msg)
    return out


def _next_quarter(date: str, h: int) -> str:
    from .meese_rogoff import next_quarter

    return next_quarter(date, h)


def summary() -> str:
    r = evaluate()
    lines = [
        "NK 3-EQUATION, OUT OF SAMPLE ON REAL-TIME VINTAGES",
        "=" * 62,
        f"vintages {r['_meta']['vintages']} · {r['_meta']['forecasts']} forecasts · "
        f"calibration {r['_meta']['calibration']}",
        "",
    ]
    for kind, label in (("pi", "INFLATION (annualised pp)"), ("gap", "OUTPUT GAP (pp)")):
        lines.append(label)
        for m in MODELS:
            vals = " ".join(f"h={h}: {r[m][kind][h]:.3f}" for h in (1, 2, 4))
            base = {h: r["no-change"][kind][h] for h in (1, 2, 4)}
            ratio = " ".join(f"{r[m][kind][h]/base[h]:.2f}x" if base[h] else "—" for h in (1, 2, 4))
            w = r.get(m, {}).get("wins", {}).get(kind)
            wt = ("  wins " + " ".join(f"{w[h]}/{r[m][kind]['n'][h]}" for h in (1, 2, 4))) if w else ""
            lines.append(f"  {m:<10} {vals}   {ratio}{wt}")
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    print(summary())
