"""The known-truth battery: do causal estimators recover an effect we planted?

The replication crisis in medicine, economics and social science is, at bottom, a **known-truth**
problem. Nobody checks whether difference-in-differences recovers a known effect before using it on a
real policy. This module does exactly that: five data-generating processes with a **planted effect**,
four estimators, many replications, and one question per cell —

    does the estimator return the effect that was planted, on data that looks like real data?

What makes the answer trustworthy is not the claim but the construction: the truth is not estimated,
it is planted. A cell where an estimator fails is a property of the design, reproducible from the seed.

The five designs, each chosen because it is common *and* because it has a known failure mode:

  clean DiD            parallel trends hold: the textbook case, and the control
  broken trends        the treated group was already diverging: the DiD bias
  staggered adoption   units treated at different times with heterogeneous effects: the Goodman-Bacon
                       problem that made two-way fixed effects famous
  weak instrument      a first stage with almost no signal: 2SLS inherits the OLS bias
  measurement error    a mismeasured regressor: OLS is attenuated, a valid instrument is not

The result is a matrix, not a verdict: each estimator wins the designs matched to it and loses the
others. That matrix is the artefact — a table a journal could require and a reviewer could consult.

Run:        python3 scripts/causal_battery.py
Guarded by: tests/test_causal_battery.py
"""
from __future__ import annotations

import math
import random
from dataclasses import dataclass

#: A cell "recovers" when the estimate is within this relative distance of the planted effect.
TOLERANCE = 0.15

#: Replications per cell. Bias is a mean, so this is about precision of the mean, not of a single draw.
REPS = 60


@dataclass(frozen=True)
class Cell:
    dgp: str
    estimator: str
    truth: float
    estimates: tuple[float, ...]

    @property
    def estimate(self) -> float:
        return _median(self.estimates)

    @property
    def bias(self) -> float:
        return self.estimate - self.truth

    @property
    def recovery_rate(self) -> float:
        """The share of replications that land within tolerance — the honest summary.

        A mean alone mis-describes a weak-instrument estimator, whose draws are bimodal: it can be
        unbiased on average and still be wrong in most samples.
        """
        good = sum(1 for e in self.estimates if abs(e - self.truth) <= TOLERANCE * abs(self.truth))
        return good / len(self.estimates)

    @property
    def recovered(self) -> bool:
        return self.recovery_rate >= 0.5


# ---------------------------------------------------------------------------------------
# the data-generating processes: each plants an effect and a failure mode
# ---------------------------------------------------------------------------------------
def clean_did(rng: random.Random, tau: float = 1.0, n: int = 400) -> dict:
    """Parallel trends hold. The textbook case, and the battery's control."""
    rows = []
    for i in range(n):
        treated = i % 2 == 1
        unit = rng.gauss(0.0, 1.0)
        for post in (0, 1):
            y = unit + 0.5 * post + tau * (treated and post) + rng.gauss(0.0, 1.0)
            rows.append({"unit": i, "treated": treated, "post": post, "y": y})
    return {"rows": rows, "truth": tau}


def broken_trends(rng: random.Random, tau: float = 1.0, gamma: float = 0.8, n: int = 400) -> dict:
    """The treated group was already on a different trend: DiD inherits it as bias."""
    rows = []
    for i in range(n):
        treated = i % 2 == 1
        unit = rng.gauss(0.0, 1.0)
        for post in (0, 1):
            y = unit + 0.5 * post + tau * (treated and post) + gamma * treated * post + rng.gauss(0.0, 1.0)
            rows.append({"unit": i, "treated": treated, "post": post, "y": y})
    return {"rows": rows, "truth": tau}


def staggered(rng: random.Random, tau: float = 1.0, n: int = 150, growth: float = 0.6,
              periods: int = 5) -> dict:
    """Staggered adoption, five periods, three adoption dates, effects that grow with exposure.

    This is the design the two-way fixed effects literature is about. One period of exposure is
    worth `tau`, and each further period adds `growth` — so early-treated units are on a steeper path
    than late-treated ones, and TWFE, which uses already-treated units as controls, inherits that
    path. The not-yet-treated comparison measures each cohort at its own adoption date instead.

    `growth = 0` is the control: with flat effects the two estimators must agree.
    """
    cohorts = (2, 3, 4)
    rows = []
    for i in range(n):
        cohort = i % (len(cohorts) + 1)                 # 0 = never treated
        adoption = cohorts[cohort - 1] if cohort > 0 else None
        unit = rng.gauss(0.0, 1.0)
        for t in range(1, periods + 1):
            treated = adoption is not None and t >= adoption
            effect = tau * (1.0 + growth * (t - adoption)) if treated else 0.0
            y = unit + 0.3 * t + effect + rng.gauss(0.0, 1.0)
            rows.append({"unit": i, "cohort": cohort, "t": t, "treated": treated, "y": y})
    return {"rows": rows, "truth": tau}


def weak_instrument(rng: random.Random, tau: float = 1.0, n: int = 2000, pi0: float = 0.03) -> dict:
    """Almost no first stage, and the endogeneity is severe: 2SLS is dragged to the OLS bias."""
    rows = []
    for _ in range(n):
        z = rng.gauss(0.0, 1.0)
        v = rng.gauss(0.0, 1.0)
        u = 0.8 * v + rng.gauss(0.0, 1.0)          # endogeneity
        x = pi0 * z + v
        y = tau * x + u
        rows.append({"z": z, "x": x, "y": y})
    return {"rows": rows, "truth": tau}


def measurement_error(rng: random.Random, tau: float = 1.0, n: int = 2000) -> dict:
    """A mismeasured regressor: OLS is attenuated, a valid instrument is not."""
    rows = []
    for _ in range(n):
        x_star = rng.gauss(0.0, 1.0)
        z = x_star + rng.gauss(0.0, 0.5)          # instrument, correlated with the truth
        x = x_star + rng.gauss(0.0, 1.0)          # observed, with error
        y = tau * x_star + rng.gauss(0.0, 1.0)
        rows.append({"z": z, "x": x, "y": y, "x_star": x_star})
    return {"rows": rows, "truth": tau}


# ---------------------------------------------------------------------------------------
# the estimators
# ---------------------------------------------------------------------------------------
def _mean(xs: list[float]) -> float:
    return sum(xs) / len(xs)


def _median(xs: tuple[float, ...] | list[float]) -> float:
    ordered = sorted(xs)
    n = len(ordered)
    return ordered[n // 2] if n % 2 else 0.5 * (ordered[n // 2 - 1] + ordered[n // 2])


def did_two_by_two(rows: list[dict]) -> float:
    """The textbook difference-in-differences."""
    def cell(treated: bool, post: int) -> list[float]:
        return [r["y"] for r in rows if r["treated"] == treated and r["post"] == post]
    return ((_mean(cell(True, 1)) - _mean(cell(True, 0)))
            - (_mean(cell(False, 1)) - _mean(cell(False, 0))))


def twfe(rows: list[dict]) -> float:
    """Two-way fixed effects on the multi-period panel: demean by unit and by period until stable.

    This is the estimator that the staggered-design literature is about — it is included precisely
    because it is expected to fail there.
    """
    units = sorted({r["unit"] for r in rows})
    times = sorted({r["t"] for r in rows})
    y = {i: r["y"] for i, r in enumerate(rows)}
    d = {i: 1.0 if r["treated"] else 0.0 for i, r in enumerate(rows)}
    unit_of = [r["unit"] for r in rows]
    time_of = [r["t"] for r in rows]
    for _ in range(60):
        u_mean = {u: _mean([y[i] for i in range(len(rows)) if unit_of[i] == u]) for u in units}
        d_mean = {u: _mean([d[i] for i in range(len(rows)) if unit_of[i] == u]) for u in units}
        y = {i: y[i] - u_mean[unit_of[i]] for i in y}
        d = {i: d[i] - d_mean[unit_of[i]] for i in d}
        t_mean = {t: _mean([y[i] for i in range(len(rows)) if time_of[i] == t]) for t in times}
        td_mean = {t: _mean([d[i] for i in range(len(rows)) if time_of[i] == t]) for t in times}
        y = {i: y[i] - t_mean[time_of[i]] for i in y}
        d = {i: d[i] - td_mean[time_of[i]] for i in d}
    num = sum(d[i] * y[i] for i in y)
    den = sum(d[i] * d[i] for i in d)
    return num / den


def not_yet_treated(rows: list[dict]) -> float:
    """Each cohort measured at its own adoption date against units never treated.

    The estimator the staggered-adoption literature recommends: it never uses already-treated units
    as controls, so it does not inherit their dynamic effects. Each cohort contributes its own
    adoption-date contrast, and the cell reports the average across cohorts.
    """
    never = [r for r in rows if r["cohort"] == 0]
    cohorts = sorted({r["cohort"] for r in rows if r["cohort"] > 0})
    effects = []
    for cohort in cohorts:
        group = [r for r in rows if r["cohort"] == cohort]
        adoption = min(r["t"] for r in group if r["treated"])
        def mean_at(pool, t):
            vals = [r["y"] for r in pool if r["t"] == t]
            return _mean(vals) if vals else float("nan")
        d_treated = mean_at(group, adoption) - mean_at(group, adoption - 1)
        d_control = mean_at(never, adoption) - mean_at(never, adoption - 1)
        if d_treated == d_treated and d_control == d_control:
            effects.append(d_treated - d_control)
    return _mean(effects)


def staggered_sensitivity(reps: int = 8, seed: int = 31) -> dict:
    """The mechanism behind the staggered cell: TWFE's bias tracks effect growth, NYT's does not.

    This is a stronger statement than "TWFE is biased" — it identifies *why*, and it is the check
    that would fail if either estimator were mis-implemented.
    """
    key = ("sensitivity", reps, seed)
    if key in _RUN_CACHE:
        return _RUN_CACHE[key]
    out = {}
    for growth in (0.0, 1.2):
        twfe_est, nyt_est = [], []
        for r in range(reps):
            data = staggered(random.Random(seed + 17 * r), growth=growth)
            twfe_est.append(twfe(data["rows"]))
            nyt_est.append(not_yet_treated(data["rows"]))
        out[growth] = {"twfe": _median(twfe_est), "nyt": _median(nyt_est)}
    flat_twfe, flat_nyt = out[0.0]["twfe"], out[0.0]["nyt"]
    grow_twfe, grow_nyt = out[1.2]["twfe"], out[1.2]["nyt"]
    twfe_shift = abs(grow_twfe - flat_twfe)
    nyt_shift = abs(grow_nyt - flat_nyt)
    result = {"by_growth": out, "twfe_shift": twfe_shift, "nyt_shift": nyt_shift,
              "pass": twfe_shift > 2 * nyt_shift,
              "detail": (f"with flat effects both agree ({flat_twfe:+.3f} vs {flat_nyt:+.3f}); "
                         f"with growing effects TWFE moves {twfe_shift:+.3f} and not-yet-treated "
                         f"moves {nyt_shift:+.3f}")}
    _RUN_CACHE[key] = result
    return result


def _ols(y: list[float], xs: list[list[float]]) -> list[float]:
    k = len(xs[0])
    xtx = [[sum(row[i] * row[j] for row in xs) for j in range(k)] for i in range(k)]
    xty = [sum(row[i] * yi for row, yi in zip(xs, y)) for i in range(k)]
    a = [xtx[i] + [xty[i]] for i in range(k)]
    for col in range(k):
        pivot = max(range(col, k), key=lambda r: abs(a[r][col]))
        a[col], a[pivot] = a[pivot], a[col]
        d = a[col][col]
        if abs(d) < 1e-14:
            raise ValueError("singular design")
        a[col] = [v / d for v in a[col]]
        for r in range(k):
            if r != col and abs(a[r][col]) > 0:
                f = a[r][col]
                a[r] = [vr - f * vc for vr, vc in zip(a[r], a[col])]
    return [a[i][k] for i in range(k)]


def ols_slope(rows: list[dict]) -> float:
    """Plain OLS of y on x with an intercept: the estimator everyone runs first."""
    return _ols([r["y"] for r in rows], [[1.0, r["x"]] for r in rows])[1]


def iv_2sls(rows: list[dict]) -> float:
    """Just-identified 2SLS with one instrument."""
    z = [r["z"] for r in rows]
    x = [r["x"] for r in rows]
    y = [r["y"] for r in rows]
    pi = _ols(x, [[1.0, zi] for zi in z])[1]
    x_hat = [0.0 + pi * zi for zi in z]
    return _ols(y, [[1.0, xh] for xh in x_hat])[1]


# ---------------------------------------------------------------------------------------
# the battery
# ---------------------------------------------------------------------------------------
DESIGNS = {
    "clean DiD": (clean_did, ("did_two_by_two",)),
    "broken trends": (broken_trends, ("did_two_by_two",)),
    "staggered adoption": (staggered, ("twfe", "not_yet_treated")),
    "weak instrument": (weak_instrument, ("iv_2sls", "ols_slope")),
    "measurement error": (measurement_error, ("ols_slope", "iv_2sls")),
}

ESTIMATORS = {
    "did_two_by_two": did_two_by_two,
    "twfe": twfe,
    "not_yet_treated": not_yet_treated,
    "iv_2sls": iv_2sls,
    "ols_slope": ols_slope,
}


_RUN_CACHE: dict = {}


def run(reps: int = REPS, seed: int = 7) -> dict:
    """Score every estimator on every design it is plausible for.

    Cached per `(reps, seed)`: the battery is deterministic and expensive, and every caller asking
    for the same battery should get the same object rather than paying for it again.
    """
    key = (reps, seed)
    if key in _RUN_CACHE:
        return _RUN_CACHE[key]
    cells = []
    for d_index, (design, (dgp, estimators)) in enumerate(DESIGNS.items()):
        for name in estimators:
            estimates = []
            for r in range(reps):
                # the seed must not depend on hash(): it is salted per process, and a battery whose
                # numbers move between runs is not a battery
                rng = random.Random(seed + 1000 * r + 97 * d_index)
                data = dgp(rng)
                estimates.append(ESTIMATORS[name](data["rows"]))
            truth = dgp(random.Random(seed))["truth"]
            cells.append(Cell(dgp=design, estimator=name, truth=truth,
                              estimates=tuple(estimates)))
    result = {"cells": cells, "reps": reps, "tolerance": TOLERANCE,
              "n_cells": len(cells),
              "n_recovered": sum(1 for c in cells if c.recovered)}
    _RUN_CACHE[key] = result
    return result


def scoreboard(result: dict | None = None) -> dict:
    """Per-estimator and per-design summaries — the table that is the artefact."""
    result = result or run()
    by_estimator = {}
    by_design = {}
    for cell in result["cells"]:
        by_estimator.setdefault(cell.estimator, []).append(cell)
        by_design.setdefault(cell.dgp, []).append(cell)
    return {
        "cells": result["cells"],
        "by_estimator": {k: {"n": len(v), "recovered": sum(c.recovered for c in v),
                             "mean_recovery_rate": _mean([c.recovery_rate for c in v])}
                         for k, v in by_estimator.items()},
        "by_design": {k: {"n": len(v), "recovered": sum(c.recovered for c in v)}
                      for k, v in by_design.items()},
        "n_cells": result["n_cells"], "n_recovered": result["n_recovered"],
        "verdict": (f"{result['n_recovered']} of {result['n_cells']} cells recover the planted "
                    f"effect in at least half of replications (tolerance {TOLERANCE:.0%})"),
    }


def guard_designs_have_teeth() -> tuple[bool, str]:
    """MUTATION: a design with no failure mode would make the battery decorative.

    Each `broken trends` / `staggered` / `weak instrument` cell must FAIL for its naive estimator, or
    the design is not testing what it claims.
    """
    res = run(reps=20)
    def cell(design: str, est: str) -> Cell:
        return next(c for c in res["cells"] if c.dgp == design and c.estimator == est)
    broken = cell("broken trends", "did_two_by_two")
    weak = cell("weak instrument", "iv_2sls")
    meas = cell("measurement error", "ols_slope")
    stagger = staggered_sensitivity()
    ok = (not broken.recovered and not weak.recovered and not meas.recovered
          and stagger["pass"])
    return ok, (f"naive estimators fail where they must: broken trends recovered "
                f"{broken.recovery_rate:.0%} of replications, weak IV {weak.recovery_rate:.0%}, "
                f"OLS under measurement error {meas.recovery_rate:.0%}; and for staggered timing "
                f"TWFE's bias tracks effect growth while not-yet-treated's does not "
                f"({stagger['detail']})")


def guard_controls_recover() -> tuple[bool, str]:
    """MUTATION: the control design must be recoverable, or the battery fails everything and says
    nothing. A clean DiD with parallel trends has to come out right."""
    res = run(reps=20)
    clean = next(c for c in res["cells"] if c.dgp == "clean DiD")
    ok = clean.recovered
    return ok, f"the control design recovers the planted effect: {clean.estimate:.3f} vs {clean.truth:.3f}"


def audit() -> dict:
    checks = []
    for name, run_ in (("designs have teeth", guard_designs_have_teeth),
                       ("controls recover", guard_controls_recover)):
        ok, msg = run_()
        checks.append({"check": name, "pass": bool(ok), "detail": msg})
    return {"checks": checks, "n_pass": sum(c["pass"] for c in checks), "n": len(checks),
            "all_pass": all(c["pass"] for c in checks)}


__all__ = ["run", "scoreboard", "audit", "staggered_sensitivity", "Cell", "DESIGNS",
           "ESTIMATORS", "TOLERANCE", "clean_did", "broken_trends", "staggered",
           "weak_instrument", "measurement_error", "did_two_by_two", "twfe", "not_yet_treated",
           "iv_2sls", "ols_slope"]
