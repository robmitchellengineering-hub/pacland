"""The Meese–Rogoff question, asked on real-time data: does anything beat "no change"?

The field's best-known out-of-sample table (Smets–Wouters 2007, Table 3) benchmarks a
VAR(1) — not "tomorrow equals today". This module asks the question that table leaves
out, on data *as it was published*, with three models and the null:

- ``no-change``  — tomorrow equals today (the null; Meese–Rogoff's unit of account)
- ``AR(1)``      — univariate, intercept + one lag, iterated to the horizon
- ``VAR(1)``     — the three quarterly series jointly, intercept + one lag, iterated

Every model sees only the vintage it was given (``vintages.guard_no_lookahead``), is
scored against today's revised value at the target date, and is never handed the target
(``vintages.guard_truth_is_not_input``).

**Errors are in growth, not levels.** An old vintage is not on the same base as today's:
GDPC1 in the 2003 vintage reads ~10,493 (2000 dollars) while the current vintage reads
~15,163 (2017 chained dollars). That is a rebasing, not a revision, so level errors
would measure the rebasing and swamp the forecast. Growth — a log difference taken
within one vintage for the forecast and within the current vintage for the truth — is
rebasing-invariant, which is why ``guard_growth_not_levels`` exists.

Pure stdlib — the OLS is a normal-equation solve, small and checkable.
"""
from __future__ import annotations

import math

from . import vintages

#: The three quarterly series with vintage coverage across the window SW evaluate.
PANEL = ("GDPC1", "PCECC96", "GPDIC1")
MODELS = ("no-change", "AR(1)", "VAR(1)")


# --- linear algebra ----------------------------------------------------------


def _solve(a: list[list[float]], b: list[float]) -> list[float]:
    """Gaussian elimination with partial pivoting (small, dense, square)."""
    n = len(a)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(m[r][col]))
        if abs(m[piv][col]) < 1e-12:
            raise ValueError("singular normal equations")
        m[col], m[piv] = m[piv], m[col]
        p = m[col][col]
        for j in range(col, n + 1):
            m[col][j] /= p
        for r in range(n):
            if r == col:
                continue
            f = m[r][col]
            if f:
                for j in range(col, n + 1):
                    m[r][j] -= f * m[col][j]
    return [m[i][n] for i in range(n)]


def _ols(x: list[list[float]], y: list[float]) -> list[float]:
    """Least squares via normal equations; ``x`` rows include the constant."""
    k = len(x[0])
    xtx = [[sum(x[r][i] * x[r][j] for r in range(len(x))) for j in range(k)] for i in range(k)]
    xty = [sum(x[r][i] * y[r] for r in range(len(x))) for i in range(k)]
    return _solve(xtx, xty)


# --- the models --------------------------------------------------------------


def no_change(y: list[float], h: int = 1) -> float:
    return y[-1]


def ar1(y: list[float], h: int = 1) -> float:
    """AR(1) with intercept fitted on the vintage's data, iterated h steps."""
    x = [[1.0, y[i - 1]] for i in range(1, len(y))]
    c, rho = _ols(x, y[1:])
    v = y[-1]
    for _ in range(h):
        v = c + rho * v
    return v


def var1(panel: list[list[float]], h: int = 1) -> list[float]:
    """VAR(1) with intercept on a balanced panel; iterated h steps."""
    k = len(panel)
    rows = min(len(s) for s in panel)
    x = [[1.0] + [panel[j][i - 1] for j in range(k)] for i in range(1, rows)]
    coefs = [_ols(x, panel[j][1:]) for j in range(k)]
    v = [s[-1] for s in panel]
    for _ in range(h):
        v = [c[0] + sum(c[1 + j] * v[j] for j in range(k)) for c in coefs]
    return v


# --- date helpers ------------------------------------------------------------


def next_quarter(date: str, h: int) -> str:
    y, m, _ = (int(p) for p in date.split("-"))
    idx = (y * 4 + (m - 1) // 3) + h
    return f"{idx // 4:04d}-{(idx % 4) * 3 + 1:02d}-01"


# --- evaluation --------------------------------------------------------------


def _balanced(vintage: vintages.Vintage) -> tuple[list[str], list[list[float]]] | None:
    per = {s: dict(vintage.observations(s)) for s in PANEL}
    common = sorted(set.intersection(*(set(d) for d in per.values())))
    if len(common) < 25:
        return None
    return common, [[math.log(per[s][d]) for d in common] for s in PANEL]


def evaluate(data: dict | None = None, horizons: tuple[int, ...] = (1, 2, 4)) -> dict:
    """Real-time out-of-sample errors, per model and horizon (log-level RMSE)."""
    data = data or vintages.load()
    truth = vintages.current(data)
    errs: dict[str, dict[int, list[float]]] = {m: {h: [] for h in horizons} for m in MODELS}
    #: paired comparisons against the null: how often is a model closer than no-change?
    wins: dict[str, dict[int, int]] = {m: {h: 0 for h in horizons} for m in MODELS if m != "no-change"}
    n_forecasts = 0
    skipped = 0

    for vintage in vintages.vintages(data):
        ok, _ = vintages.guard_no_lookahead(vintage)
        if not ok:
            raise ValueError(f"look-ahead in vintage {vintage.as_of}")
        bal = _balanced(vintage)
        if bal is None:
            skipped += 1
            continue
        dates, panel = bal
        t0 = dates[-1]
        for h in horizons:
            target = next_quarter(t0, h)
            # growth, not levels: rebasing-invariant (see the module docstring)
            realised, base_level = [], []
            for s in PANEL:
                val = truth.get(s, {}).get(target)
                b0 = truth.get(s, {}).get(t0)
                if val is None or b0 is None or val <= 0 or b0 <= 0:
                    realised = []
                    break
                realised.append(math.log(val) - math.log(b0))
                base_level.append(math.log(b0))
            if not realised:
                continue
            # guard: the target may not be in the forecast's input
            for s in PANEL:
                if not vintages.guard_truth_is_not_input(vintage.observations(s), target)[0]:
                    raise ValueError(f"target {target} leaked into {s} at {vintage.as_of}")
            fc = {
                "no-change": [no_change(panel[j], h) for j in range(len(PANEL))],
                "AR(1)": [ar1(panel[j], h) for j in range(len(PANEL))],
                "VAR(1)": var1(panel, h),
            }
            per_model_errors = {}
            for model, values in fc.items():
                # forecast growth = log F(h) - log y0, same vintage for both
                growth = [v - panel[j][-1] for j, v in enumerate(values)]
                e = [g - a for g, a in zip(growth, realised)]
                per_model_errors[model] = e
                errs[model][h].extend(e)
            null_abs = [abs(e) for e in per_model_errors["no-change"]]
            for model in wins:
                wins[model][h] += sum(
                    1 for a, b in zip((abs(e) for e in per_model_errors[model]), null_abs) if a < b
                )
            n_forecasts += 1

    out = {}
    for model in MODELS:
        out[model] = {
            h: (math.sqrt(sum(e * e for e in v) / len(v)) if v else float("nan"))
            for h, v in errs[model].items()
        }
        out[model]["n"] = {h: len(v) for h, v in errs[model].items()}
    for model, hw in wins.items():
        out[model]["wins"] = hw
    ok, msg = vintages.guard_benchmark_present(out)
    if not ok:
        raise ValueError(msg)
    out["_meta"] = {"vintages": len(vintages.vintages(data)), "skipped": skipped,
                    "forecasts": n_forecasts, "unit": "log-growth RMSE"}
    ok, msg = guard_growth_not_levels(out)
    if not ok:
        raise ValueError(msg)
    return out


def guard_growth_not_levels(results: dict, ceiling: float = 0.2) -> tuple[bool, str]:
    """A quarterly growth forecast cannot have a level-sized error. If the RMSE is huge
    the evaluation is comparing levels across vintages — i.e. measuring a rebasing — so
    it is refused rather than reported. The seeded fault is exactly that mistake."""
    worst = max(
        (results[m][h] for m in MODELS for h in (1, 2, 4) if results.get(m, {}).get(h) is not None),
        default=0.0,
    )
    ok = worst <= ceiling
    return ok, f"error scale: worst RMSE {worst:.4f} (ceiling {ceiling}) — {'growth' if ok else 'LEVELS?'}"


def findables() -> dict:
    r = evaluate()
    base = r["no-change"]
    rel = {m: {h: (r[m][h] / base[h] if base[h] else float("nan")) for h in (1, 2, 4)}
           for m in MODELS}
    return {"rmse": r, "ratio_to_no_change": rel}


def summary() -> str:
    res = findables()
    r, rel = res["rmse"], res["ratio_to_no_change"]
    lines = [
        "REAL-TIME OUT-OF-SAMPLE: does anything beat 'no change'?",
        "=" * 62,
        f"vintages {r['_meta']['vintages']} · {r['_meta']['forecasts']} forecasts · "
        f"{r['_meta']['skipped']} vintages skipped (too short) · log-growth RMSE",
        "",
        f"{'model':<10} " + " ".join(f"h={h:<8}" for h in (1, 2, 4)) + "   ratio to no-change",
    ]
    for m in MODELS:
        rm = " ".join(f"{r[m][h]:<10.4f}" for h in (1, 2, 4))
        rt = " ".join(f"{rel[m][h]:.2f}x" for h in (1, 2, 4))
        wins = r.get(m, {}).get("wins")
        wt = ("  wins " + " ".join(f"{wins[h]}/{r[m]['n'][h]}" for h in (1, 2, 4))) if wins else ""
        lines.append(f"{m:<10} {rm}   {rt}{wt}")
    lines += [
        "",
        "Real-time data only: each forecast sees the series as published on its vintage",
        "date, and is scored against today's revised value. A ratio below 1 means the",
        "model beat 'tomorrow equals today'. Errors are growth, so a rebasing between",
        "the vintage and today cancels instead of masquerading as forecast error.",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    print(summary())
