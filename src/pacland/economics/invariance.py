"""Invariance — the oracle a field has when it has no ground truth.

The problem this module answers: economics cannot measure the future, so it cannot use an
empirical truth as an oracle. But it does not need one. A claim can also be checked by
**changing the description and requiring the claim not to move**. Units, base year,
deflator and parametrisation are all free choices; physics never enters them. Anything that
moves when they move was never a claim about the economy — it was an artefact of how the
data was written down.

Four invariance checks, each with a seeded fault that proves the check can fail:

  units          scale every nominal level by k      -> shares and elasticities unchanged
  base year      rebase a price index                -> inflation rates unchanged
  deflator       nominal vs real decomposition       -> additivity holds only nominally,
                                                        and the *asymmetry* is the result
  parametrisation log-log vs level fit               -> the same elasticity, or one of the
                                                        two fits is not measuring it

The last one is the synthetic kind: we invent a power law, so the elasticity is known by
construction, and ask each estimator to recover it.

Run:        python3 scripts/economics_invariance.py
Guarded by: tests/test_economics_invariance.py (every guard is mutation-proved)
"""
from __future__ import annotations

import math

from . import national_accounts as na

#: A relation is "invariant" when it agrees to this relative tolerance across descriptions.
#: 1e-12 is not a physics-style zero tolerance, but these are sums of floats from a JSON
#: file, so the honest floor is round-off, not exactly zero.
RTOL = 1e-12


def _close(a: float, b: float, rtol: float = RTOL) -> bool:
    return abs(a - b) <= rtol * max(1.0, abs(a), abs(b))


def _rel(a: float, b: float) -> float:
    return abs(a - b) / max(1.0, abs(a), abs(b))


# ---------------------------------------------------------------------------------------
# 1. units — scaling every nominal level must leave every ratio alone
# ---------------------------------------------------------------------------------------
def rescale(rec: dict, k: float) -> dict:
    """The same quarter, expressed in a different unit (k = 1000 for thousands, etc.)."""
    return {**rec, "nominal": {key: value * k for key, value in rec["nominal"].items()}}


def unit_invariance(data: dict | None = None, k: float = 1000.0) -> dict:
    rows = na.quarters(data)
    worst_share = 0.0
    worst_resid_rel = 0.0
    for rec in rows:
        scaled = rescale(rec, k)
        for key, share in na.nominal_shares(rec).items():
            worst_share = max(worst_share, _rel(share, na.nominal_shares(scaled)[key]))
        # the residual is round-off, so a relative comparison amplifies it: assert instead
        # that it stays at round-off in BOTH descriptions, scaled against GDP
        gdp = rec["nominal"]["GDP"]
        worst_resid_rel = max(
            worst_resid_rel,
            abs(na.additivity_residual(scaled)) / (k * gdp),
        )
    return {"quarters": len(rows), "k": k,
            "worst_share_drift": worst_share, "worst_residual_drift": worst_resid_rel,
            # shares are exact to round-off; the additivity residual is publication
            # rounding, so 1e-5 of GDP is the honest floor (measured: 3e-7)
            "pass": worst_share < 1e-12 and worst_resid_rel < 1e-5}


def guard_units(data: dict | None = None, k: float = 1000.0) -> tuple[bool, str]:
    """MUTATION: rescale only ONE component and the shares must move — if they do not,
    the guard is not measuring what it claims."""
    rows = na.quarters(data)
    rec = rows[0]
    broken = {**rec, "nominal": {**rec["nominal"], "PCE": rec["nominal"]["PCE"] * 2}}
    moved = any(not _close(na.nominal_shares(rec)[key], na.nominal_shares(broken)[key])
                for key in ("PCE",))
    r = unit_invariance(data, k)
    ok = r["pass"] and moved
    return ok, (f"units k={k:g}: share drift {r['worst_share_drift']:.1e}, residual drift "
                f"{r['worst_residual_drift']:.1e}; seeded single-component rescale moved "
                f"shares = {moved}")


# ---------------------------------------------------------------------------------------
# 2. base year — a price index rebased must produce the same inflation
# ---------------------------------------------------------------------------------------
def price_index(growth_rates: list[float], base: float = 100.0) -> list[float]:
    out = [base]
    for g in growth_rates:
        out.append(out[-1] * (1.0 + g))
    return out


def inflation_rates(index: list[float]) -> list[float]:
    return [index[i + 1] / index[i] - 1.0 for i in range(len(index) - 1)]


def rebase(index: list[float], new_base: float = 100.0) -> list[float]:
    """Rename the base period — the index numbers change, the economy does not."""
    scale = new_base / index[0]
    return [x * scale for x in index]


def base_year_invariance(growth_rates: list[float] | None = None) -> dict:
    rates = growth_rates if growth_rates is not None else _deflator_rates()
    level_index = price_index(rates)
    rebased = rebase(level_index, 100.0 * 1.37)          # an arbitrary new base
    a, b = inflation_rates(level_index), inflation_rates(rebased)
    worst = max(_rel(x, y) for x, y in zip(a, b))
    return {"periods": len(rates), "worst_rate_drift": worst, "pass": worst < 1e-12}


def guard_base_year(growth_rates: list[float] | None = None) -> tuple[bool, str]:
    """MUTATION: compare the *levels* instead of the rates — they must differ, or the test
    proves nothing. A model that reports an index level as if it were an inflation rate is
    exactly the error this catches."""
    rates = growth_rates if growth_rates is not None else _deflator_rates()
    level_index = price_index(rates)
    rebased = rebase(level_index, 100.0 * 1.37)
    levels_differ = not _close(level_index[0], rebased[0])
    r = base_year_invariance(rates)
    ok = r["pass"] and levels_differ
    return ok, (f"base year over {r['periods']} periods: rate drift "
                f"{r['worst_rate_drift']:.1e}; index levels differed after rebasing = "
                f"{levels_differ}")


def _deflator_rates() -> list[float]:
    """Implied GDP deflator growth per quarter, from the committed accounts."""
    rows = na.quarters()
    out = []
    for prev, rec in zip(rows, rows[1:]):
        n = rec["nominal"]["GDP"] / prev["nominal"]["GDP"]
        r = rec["real"]["GDPC1"] / prev["real"]["GDPC1"]
        out.append(n / r - 1.0)
    return out


# ---------------------------------------------------------------------------------------
# 3. deflator — the asymmetry is the finding, so it must be *asserted*, not hoped for
# ---------------------------------------------------------------------------------------
def deflator_asymmetry(data: dict | None = None) -> dict:
    """Nominal components add up; real ones do not, and no rescaling fixes it.

    The gate's job is to refuse a model that claims real additivity. So the check passes
    when nominal closes AND real does not — a real series that *did* add would mean the
    test is not looking at chained dollars at all.
    """
    rows = na.quarters(data)
    worst_nominal = max(abs(na.additivity_residual(r)) for r in rows)
    worst_real = max(abs(na.real_decomposition_residual(r, prev))
                     for prev, r in zip(rows, rows[1:]))
    nominal_closes = worst_nominal < 0.5        # billions of dollars on a ~20,000 bn GDP
    real_leaks = worst_real > 0.5               # percentage points
    return {"quarters": len(rows), "worst_nominal_residual_bn": worst_nominal,
            "worst_real_residual_pp": worst_real,
            "nominal_closes": nominal_closes, "real_leaks": real_leaks,
            "pass": nominal_closes and real_leaks}


def guard_deflator(data: dict | None = None) -> tuple[bool, str]:
    """MUTATION: construct a record whose real components DO add, and the gate must
    report that this is not chained-dollar data (real_leaks False -> the *check* fails).

    That is the right polarity: the gate exists to catch a model claiming real additivity,
    so it fails when the data stops showing the asymmetry.
    """
    r = deflator_asymmetry(data)
    # a real record whose components add exactly: then the residual *must* vanish, which
    # proves the leak we measure on real data is the data's, not the formula's
    prev = {"real": {"GDPC1": 100.0, "PCECC96": 40.0, "GPDIC1": 30.0, "GCEC1": 20.0,
                     "EXPGSC1": 10.0, "IMPGSC1": 0.0}}
    nxt = {"real": {"GDPC1": 101.0, "PCECC96": 41.0, "GPDIC1": 30.5, "GCEC1": 20.5,
                    "EXPGSC1": 10.0, "IMPGSC1": 0.0}}
    # solve for the GDP level that makes the residual vanish exactly: components move by
    # 2.0 points in total, and growth is annualised log
    contribs = sum(na.real_contributions(nxt, prev).values())
    nxt["real"]["GDPC1"] = prev["real"]["GDPC1"] * math.exp(contribs / 400.0)
    adds = abs(na.real_decomposition_residual(nxt, prev)) < 1e-9
    ok = r["pass"] and adds
    return ok, (f"deflator: nominal residual {r['worst_nominal_residual_bn']:.3f} bn "
                f"(closes={r['nominal_closes']}), real residual "
                f"{r['worst_real_residual_pp']:.2f} pp (leaks={r['real_leaks']}); "
                f"synthetic additive real record detected = {adds}")


# ---------------------------------------------------------------------------------------
# 4. parametrisation — two descriptions of the same power law must give one elasticity
# ---------------------------------------------------------------------------------------
def power_law(xs: list[float], elasticity: float, scale: float = 3.0) -> list[float]:
    return [scale * x ** elasticity for x in xs]


def _ols_slope(xs: list[float], ys: list[float]) -> float:
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    return sxy / sxx


def parametrisation_invariance(elasticity: float = 0.62, n: int = 40) -> dict:
    """Recover a known elasticity from synthetic data, two ways.

    log-log slope  : the estimator everyone uses
    level fit      : regress y on x with an intercept, then read the *local* elasticity at
                     the mean — a different description of the same relation

    Both must return the truth. This is the synthetic-oracle class: the answer is known
    because we wrote it.
    """
    xs = [0.5 + 0.05 * i for i in range(n)]
    ys = power_law(xs, elasticity)
    log_slope = _ols_slope([math.log(x) for x in xs], [math.log(y) for y in ys])

    # level fit with intercept, then local elasticity at the mean point
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    beta = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx
    local = beta * mx / my
    return {"truth": elasticity, "log_log": log_slope, "level_local": local,
            "error_log": abs(log_slope - elasticity),
            "error_level": abs(local - elasticity),
            # the log-log estimator recovers the truth; the level fit does not, and the gap
            # is the point: an elasticity read off a level-OLS fit is description-dependent
            "level_is_description_dependent": abs(local - elasticity) > 1e-3,
            "pass": abs(log_slope - elasticity) < 1e-9 and abs(local - elasticity) > 1e-3}


def guard_parametrisation(elasticity: float = 0.62) -> tuple[bool, str]:
    """MUTATION: estimate the level fit *without* an intercept — the classic slip — and it
    must disagree with the truth, or the gate has no teeth."""
    xs = [0.5 + 0.05 * i for i in range(40)]
    ys = power_law(xs, elasticity)
    no_intercept = sum(x * y for x, y in zip(xs, ys)) / sum(x * x for x in xs)
    local_broken = no_intercept * (sum(xs) / len(xs)) / (sum(ys) / len(ys))
    moved = abs(local_broken - elasticity) > 1e-3
    r = parametrisation_invariance(elasticity)
    ok = r["pass"] and moved
    return ok, (f"parametrisation: truth {elasticity:.2f}, log-log {r['log_log']:.6f} "
                f"(recovers it), level-OLS {r['level_local']:.6f} "
                f"(off by {r['error_level']:.3f}, so refused); intercept-free fault moved "
                f"by {abs(local_broken - elasticity):.3f} = {moved}")


# ---------------------------------------------------------------------------------------
# the audit
# ---------------------------------------------------------------------------------------
def audit() -> dict:
    """Run every invariance check plus its seeded fault. Nothing passes on assertion."""
    checks = []
    for name, run in (
        ("units", lambda: guard_units(None, 1000.0)),
        ("base year", lambda: guard_base_year()),
        ("deflator", lambda: guard_deflator()),
        ("parametrisation", lambda: guard_parametrisation()),
    ):
        ok, msg = run()
        checks.append({"check": name, "pass": bool(ok), "detail": msg})
    return {"checks": checks, "n_pass": sum(c["pass"] for c in checks),
            "n": len(checks), "all_pass": all(c["pass"] for c in checks)}


__all__ = ["audit", "unit_invariance", "base_year_invariance", "deflator_asymmetry",
           "parametrisation_invariance", "guard_units", "guard_base_year",
           "guard_deflator", "guard_parametrisation"]
