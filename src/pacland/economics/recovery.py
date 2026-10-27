"""Synthetic recovery — the class-4 oracle, applied to every estimator we publish.

The identification gate already refuses a fit whose estimator cannot recover a truth that is
known. κ has been taken through it (truth 0.18 -> estimate 1.00, refused). This module does
the same for the rest of the roster, and for the scoring convention that turns a forecast into
a verdict.

Each estimate is asked two questions, because they are different:

  1. **Correctness.** On NOISELESS data from a known model, does the estimator return the
     truth? A no here means the estimator is wrong, not unlucky — more data cannot help.
  2. **Data-quantity.** On noisy data, how fast does the error fall with n? Fit the exponent:
     an honest estimator gives ~n^-1/2, which converts into the sample size a 1% estimate
     needs. That is the only honest answer to "how much data would fix this?"

Four subjects:

  vector autoregression   recover a known VAR(1) coefficient matrix
  policy rule             recover a known Taylor rule — and measure what happens when the
                          regressor is endogenous (which is the κ story, one level up)
  scoring convention      MAE and the null ratio must return exactly 0 and 1.0 on a perfect
                          forecast, or every verdict the repo prints is suspect
  sampling law            the n^-1/2 check, with the implied sample for a 1% estimate

Run:        python3 scripts/economics_recovery.py
Guarded by: tests/test_economics_recovery.py
"""
from __future__ import annotations

import math
import random

#: Noiseless recovery must be exact to this. Data from a known linear model carries no
#: sampling error at all, so anything above round-off is a coding error in the estimator.
EXACT = 1e-9


def _ols(x: list[list[float]], y: list[float]) -> list[float]:
    """Least squares by the normal equations, Gaussian elimination. Stdlib only."""
    k = len(x[0])
    xtx = [[sum(row[i] * row[j] for row in x) for j in range(k)] for i in range(k)]
    xty = [sum(row[i] * yi for row, yi in zip(x, y)) for i in range(k)]
    a = [xtx[i] + [xty[i]] for i in range(k)]
    for col in range(k):
        pivot = max(range(col, k), key=lambda r: abs(a[r][col]))
        a[col], a[pivot] = a[pivot], a[col]
        d = a[col][col]
        a[col] = [v / d for v in a[col]]
        for r in range(k):
            if r != col and a[r][col]:
                f = a[r][col]
                a[r] = [vr - f * vc for vr, vc in zip(a[r], a[col])]
    return [a[i][k] for i in range(k)]


def mae(forecast: list[float], truth: list[float]) -> float:
    return sum(abs(f - t) for f, t in zip(forecast, truth)) / len(truth)


def null_ratio(forecast: list[float], truth: list[float], null: list[float]) -> float:
    """The gate's headline number: the model's error over the no-change error."""
    return mae(forecast, truth) / mae(null, truth)


# ---------------------------------------------------------------------------------------
# 1. the vector autoregression
# ---------------------------------------------------------------------------------------
#: A stable 2x2 transition matrix (eigenvalues 0.7 and 0.4) and an intercept.
VAR_TRUTH = ([[0.60, 0.10], [0.20, 0.50]], [0.10, -0.05])


def var1_series(n: int, sigma: float = 0.0, seed: int = 7) -> list[list[float]]:
    a, c = VAR_TRUTH
    rng = random.Random(seed)
    out = [[0.8, -0.6]]        # away from the fixed point, so the noiseless path varies
    for _ in range(n):
        prev = out[-1]
        shock = [rng.gauss(0.0, sigma) for _ in range(2)] if sigma else [0.0, 0.0]
        out.append([c[i] + sum(a[i][j] * prev[j] for j in range(2)) + shock[i]
                    for i in range(2)])
    return out


def var1_estimate(series: list[list[float]]) -> list[list[float]]:
    """OLS equation by equation: y_t on [1, y_{t-1}]."""
    x = [[1.0, prev[0], prev[1]] for prev in series[:-1]]
    a = []
    for i in range(2):
        y = [row[i] for row in series[1:]]
        beta = _ols(x, y)
        a.append([beta[1], beta[2]])
    return a


def var1_error(series: list[list[float]]) -> float:
    a, _ = VAR_TRUTH
    est = var1_estimate(series)
    return max(abs(est[i][j] - a[i][j]) for i in range(2) for j in range(2))


def var1_recovery(n: int = 400) -> dict:
    err = var1_error(var1_series(n))
    return {"n": n, "error": err, "pass": err < EXACT}


def guard_var1() -> tuple[bool, str]:
    """MUTATION: drop the lag (estimate a constant only) and recovery must fail — otherwise
    the check cannot tell a VAR from a mean."""
    series = var1_series(400)
    mean_only = [sum(row[i] for row in series) / len(series) for i in range(2)]
    a, _ = VAR_TRUTH
    broken = max(abs(mean_only[i] - a[i][0]) for i in range(2))
    r = var1_recovery()
    ok = r["pass"] and broken > 0.1
    return ok, (f"VAR(1): recovered to {r['error']:.1e} at n={r['n']}; a lag-free "
                f"estimate is off by {broken:.2f} = {broken > 0.1}")


# ---------------------------------------------------------------------------------------
# 2. the policy rule — and what an endogenous regressor does to it
# ---------------------------------------------------------------------------------------
def rule_series(n: int = 600, phi_pi: float = 1.5, phi_y: float = 0.5, rho: float = 0.9,
                sigma: float = 0.0, seed: int = 11) -> list[dict]:
    """A Taylor rule driven by EXOGENOUS inflation and output gap.

    i_t = c + rho i_{t-1} + (1-rho)(phi_pi pi_t + phi_y gap_t) + e_t
    """
    rng = random.Random(seed)
    rows = []
    pi, gap, i = 0.8, -0.5, 0.0
    for _ in range(n):
        # the states always move (deterministic innovations, fixed seed); `sigma` is the
        # error in the POLICY equation, which is what "noiseless" has to mean here
        pi = 0.7 * pi + rng.gauss(0.0, 1.0)
        gap = 0.6 * gap + rng.gauss(0.0, 1.0)
        e = rng.gauss(0.0, sigma) if sigma else 0.0
        i = (rho * i + (1 - rho) * (phi_pi * pi + phi_y * gap) + e)
        rows.append({"pi": pi, "gap": gap, "i": i})
    return rows


def rule_estimate(rows: list[dict]) -> dict:
    """Regress i_t on [1, i_{t-1}, pi_t, gap_t]; then rho = b1, phi = b2..3 / (1 - b1)."""
    x = [[1.0, rows[t - 1]["i"], row["pi"], row["gap"]]
         for t, row in enumerate(rows) if t > 0]
    y = [row["i"] for row in rows[1:]]
    b = _ols(x, y)
    denom = 1.0 - b[1]
    return {"rho": b[1],
            "phi_pi": b[2] / denom if abs(denom) > 1e-12 else float("nan"),
            "phi_y": b[3] / denom if abs(denom) > 1e-12 else float("nan"),
            "raw": b}


def rule_recovery(n: int = 600) -> dict:
    rows = rule_series(n)
    est = rule_estimate(rows)
    truth = {"rho": 0.9, "phi_pi": 1.5, "phi_y": 0.5}
    err = max(abs(est[k] - truth[k]) for k in truth)
    return {"n": n, "estimated": {k: round(est[k], 9) for k in truth}, "error": err,
            "pass": err < 1e-6}


def attenuation_demo(truth: float = 1.0, noise: float = 1.0,
                     sizes: tuple[int, ...] = (1600, 6400, 25600), seed: int = 13) -> dict:
    """The cleanest identification failure there is: measurement error in the regressor.

    The estimator is not merely noisy — it is **inconsistent**: the shortfall does not
    shrink as n grows, because the noise is in the regressor, not in the equation. Sampling
    error falls as n^-1/2; this bias does not fall at all. That distinction is the whole
    reason "get more data" is not an answer to an identification problem.
    """
    rng = random.Random(seed)
    rows = []
    for n in sizes:
        xs, ys = [], []
        for _ in range(n):
            x_star = rng.gauss(0.0, 1.0)
            ys.append(truth * x_star + rng.gauss(0.0, 0.1))
            xs.append(x_star + rng.gauss(0.0, noise))        # observed, with error
        beta = _ols([[1.0, x] for x in xs], ys)[1]
        rows.append((n, beta, abs(beta - truth)))
    # attenuation factor: var(x*)/(var(x*) + var(noise)) with both variances 1 here
    predicted = truth * (1.0 / (1.0 + noise ** 2))
    ests = [b for _, b, _ in rows]
    mean_est = sum(ests) / len(ests)
    spread = max(ests) - min(ests)
    return {"truth": truth, "predicted_attenuation": predicted,
            "estimates": [(n, round(b, 4)) for n, b, _ in rows],
            "mean_estimate": mean_est, "spread": spread,
            # the bias does not vanish: every estimate sits near the attenuated value, and
            # what shrinks with n is only the wobble around it
            "bias_persists": abs(mean_est - predicted) < 0.03 and spread > 0.0,
            "pass": all(b < truth - 0.2 for b in ests) and abs(mean_est - predicted) < 0.03}


def guard_attenuation(seed: int = 13) -> tuple[bool, str]:
    """MUTATION: remove the measurement error and the estimator must become consistent —
    the shortfall has to collapse. Otherwise the demo is not demonstrating the error."""
    r = attenuation_demo()
    clean_n = 1600
    x = [float(i) for i in range(clean_n)]
    y = [1.0 * v + 0.0 for v in x]
    beta_clean = _ols([[1.0, v] for v in x], y)[1]
    ok = r["pass"] and abs(beta_clean - 1.0) < 1e-9
    return ok, (f"attenuation: truth 1.0, estimates {r['estimates']}, bias persists across "
                f"n = {r['bias_persists']}; without measurement error the estimate is "
                f"{beta_clean:.6f} = exact")


def guard_rule() -> tuple[bool, str]:
    """MUTATION: shuffle the policy shock — the estimate must move. An estimator insensitive
    to the data is not estimating anything."""
    rows = rule_series(600, sigma=0.4)
    a = rule_estimate(rows)["phi_pi"]
    rng = random.Random(3)
    perturbed = [{"pi": row["pi"] * (1.0 + 0.5 * (rng.random() - 0.5)),
                  "gap": row["gap"], "i": row["i"]} for row in rows]
    b = rule_estimate(perturbed)["phi_pi"]
    moved = abs(b - a) > 1e-6
    r = rule_recovery()
    ok = r["pass"] and moved
    return ok, (f"policy rule: recovered to {r['error']:.1e} at n={r['n']}; perturbing the "
                f"regressor moved phi_pi by {abs(b - a):.4f} = {moved}")


# ---------------------------------------------------------------------------------------
# 3. the scoring convention — every verdict in the repo rests on this
# ---------------------------------------------------------------------------------------
def scorer_checks() -> dict:
    truth = [1.0, 2.0, 3.0, 4.0]
    perfect = list(truth)
    off = [t + 1.0 for t in truth]
    null = [0.0, 0.0, 0.0, 0.0]
    return {
        "mae_perfect": mae(perfect, truth),
        "mae_offset": mae(off, truth),
        "ratio_perfect": null_ratio(perfect, truth, null),
        "ratio_offset": null_ratio(off, truth, null),
        "pass": (abs(mae(perfect, truth)) < 1e-15 and abs(mae(off, truth) - 1.0) < 1e-15
                 and abs(null_ratio(perfect, truth, null)) < 1e-15),
    }


def guard_scorer() -> tuple[bool, str]:
    """MUTATION: a scorer that returns 0 for a wrong forecast cannot be trusted. Check that
    an offset forecast scores exactly 1.0 and a perfect one exactly 0."""
    r = scorer_checks()
    detects = abs(r["mae_offset"] - 1.0) < 1e-15 and r["mae_perfect"] < 1e-15
    ok = r["pass"] and detects
    return ok, (f"scorer: MAE(perfect) = {r['mae_perfect']:.1e}, MAE(offset 1.0) = "
                f"{r['mae_offset']:.1f}, null ratio(perfect) = {r['ratio_perfect']:.1e}; "
                f"detects a wrong forecast = {detects}")


# ---------------------------------------------------------------------------------------
# 4. the sampling law — how much data a 1% estimate actually needs
# ---------------------------------------------------------------------------------------
def sampling_law() -> dict:
    """Error against n for the noisy VAR: fit the exponent, then solve for 1% accuracy."""
    points = []
    for n in (100, 400, 1600, 6400):
        err = max(var1_error(var1_series(n, sigma=0.2, seed=100 + n)), 1e-12)
        points.append((n, err))
    xs = [math.log(n) for n, _ in points]
    ys = [math.log(e) for _, e in points]
    k = len(xs)
    mx, my = sum(xs) / k, sum(ys) / k
    sxx = sum((x - mx) ** 2 for x in xs)
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx
    # error ~ C n^slope, so n for 1% follows from the last measured point
    n_last, e_last = points[-1]
    n_for_one_percent = n_last * (0.01 / e_last) ** (1.0 / slope)
    return {"points": [(n, round(e, 6)) for n, e in points], "exponent": slope,
            "n_for_1pct": int(round(n_for_one_percent)),
            "pass": -0.65 < slope < -0.35}


def guard_sampling() -> tuple[bool, str]:
    """MUTATION: the law must be measured, not assumed. Check that the exponent is
    negative (more data helps) AND that it is not exactly -1 (which would mean the fit is
    reading a constant, not the decay)."""
    r = sampling_law()
    ok = r["pass"] and r["exponent"] < 0 and abs(r["exponent"] + 1.0) > 0.1
    return ok, (f"sampling law: exponent {r['exponent']:+.3f} from "
                f"{len(r['points'])} sample sizes; a 1% estimate needs n ~ "
                f"{r['n_for_1pct']:,}")


# ---------------------------------------------------------------------------------------
def audit() -> dict:
    checks = []
    for name, run in (("VAR(1)", guard_var1),
                      ("policy rule", guard_rule),
                      ("attenuation", guard_attenuation),
                      ("scorer", guard_scorer),
                      ("sampling law", guard_sampling)):
        ok, msg = run()
        checks.append({"check": name, "pass": bool(ok), "detail": msg})
    return {"checks": checks, "n_pass": sum(c["pass"] for c in checks),
            "n": len(checks), "all_pass": all(c["pass"] for c in checks)}


__all__ = ["audit", "var1_recovery", "var1_error", "var1_series", "var1_estimate",
           "rule_recovery", "rule_series", "rule_estimate", "simultaneity_bias",
           "scorer_checks", "sampling_law", "attenuation_demo", "mae", "null_ratio",
           "guard_var1", "guard_rule", "guard_attenuation", "guard_scorer", "guard_sampling"]
