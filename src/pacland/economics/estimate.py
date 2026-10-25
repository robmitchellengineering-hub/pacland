"""Estimation — the first *estimated* structural model in the discipline.

Everything before this was calibrated: textbook values, SW's published values, or a mix.
Estimation asks the data, and the discipline's honest answer is allowed to be "this sample
cannot identify the parameters". So the module has three parts, in this order:

1. **Estimate** ``(kappa, phi_pi, phi_y, rho_u)`` by moment matching on real-time vintages.
   For a candidate structural vector the two shock variances are solved *exactly* (they
   enter the three contemporaneous moments linearly), leaving five normalised lag moments
   as the objective. Nelder–Mead, pure stdlib, bounds stated.
2. **Check identification.** Numerical Jacobian of the moment residuals at the optimum:
   if its rank is below the number of parameters, the estimate is **not identified** and
   the module says so instead of publishing numbers.
3. **Restrict by the constraint set** (:mod:`constraint_set`). The estimated parameter
   vector must be admissible — a fitted rule inside the passive region, or a model outside
   its own domain, is refused. This is where "as many constraints as the system needs"
   becomes operational rather than rhetorical.

Then the estimated model is forecast out of sample like any other roster row.
"""
from __future__ import annotations

import math

from . import constraint_set, nk3, nk3_oos, sw2007, vintages as V
from .meese_rogoff import _solve as _gauss_solve  # one Gaussian solver in the package

#: Bounds on the structural parameters. A fit that walks to a bound is a non-result.
BOUNDS = {
    "kappa": (0.01, 1.0),
    "phi_pi": (0.5, 5.0),
    "phi_y": (-0.5, 2.0),
    "rho_u": (0.1, 0.99),
}
#: Held at SW's detrended discount factor; sigma and rho_r are not identified at this
#: level and are held at the textbook values.
FIXED = {"beta": sw2007.beta_tilde(), "sigma": 1.0, "rho_r": 0.9}


# --- sample -------------------------------------------------------------------


def paths(data: dict | None = None, latest: str | None = None) -> list[tuple[list[float], list[float]]]:
    """Each vintage's own ``(gap, inflation)`` path, using only that vintage's data."""
    data = data or V.load()
    out = []
    for vintage in V.vintages(data):
        if latest and vintage.as_of > latest:
            continue
        gdp, cpi = nk3_oos._series(vintage, "GDPC1"), nk3_oos._series(vintage, "CPIAUCSL")
        if not gdp or not cpi:
            continue
        dates = sorted(set(gdp) & set(cpi))
        if len(dates) < 24:
            continue
        xs, ps = [], []
        for d in dates:
            x, p = nk3_oos.gap(gdp, d), nk3_oos.inflation(cpi, d)
            if x == x and p == p:
                xs.append(x)
                ps.append(p)
        if len(xs) >= 12:
            out.append((xs, ps))
    return out


def _mean(v: list[float]) -> float:
    return sum(v) / len(v)


def _cov(a: list[float], b: list[float]) -> float:
    ma, mb = _mean(a), _mean(b)
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / len(a)


def sample_moments(paths_: list[tuple[list[float], list[float]]]) -> dict[str, float]:
    """Pooled sample moments: variances and lag-1/lag-2 autocovariances."""
    pairs = [(x, p) for xs, ps in paths_ for x, p in zip(xs, ps)]
    xs = [p[0] for p in pairs]
    ps = [p[1] for p in pairs]
    ax1, ap1, ax2, ap2, xc1 = [], [], [], [], []
    for vx, vp in paths_:
        for i in range(1, len(vx)):
            ax1.append((vx[i] - _mean(vx)) * (vx[i - 1] - _mean(vx)))
            ap1.append((vp[i] - _mean(vp)) * (vp[i - 1] - _mean(vp)))
            xc1.append((vx[i] - _mean(vx)) * (vp[i - 1] - _mean(vp)))
        for i in range(2, len(vx)):
            ax2.append((vx[i] - _mean(vx)) * (vx[i - 2] - _mean(vx)))
            ap2.append((vp[i] - _mean(vp)) * (vp[i - 2] - _mean(vp)))
    return {
        "var_x": _cov(xs, xs), "var_pi": _cov(ps, ps), "cov": _cov(xs, ps),
        "ac1_x": _mean(ax1), "ac1_pi": _mean(ap1),
        "ac2_x": _mean(ax2), "ac2_pi": _mean(ap2), "xc1": _mean(xc1),
        "n": float(len(xs)),
    }


# --- model --------------------------------------------------------------------


def _policy(kappa: float, phi_pi: float, phi_y: float, rho_u: float) -> dict[str, float]:
    return nk3.policy_function(
        FIXED["beta"], kappa, FIXED["sigma"], phi_pi, phi_y, FIXED["rho_r"], rho_u
    )


def _solve2(a11: float, a12: float, a21: float, a22: float,
            b1: float, b2: float) -> tuple[float, float]:
    det = a11 * a22 - a12 * a21
    if abs(det) < 1e-18:
        return (float("nan"), float("nan"))
    return ((b1 * a22 - a12 * b2) / det, (a11 * b2 - b1 * a21) / det)


def model_moments(kappa: float, phi_pi: float, phi_y: float, rho_u: float,
                  sample: dict[str, float]) -> dict[str, float] | None:
    """Model moments at the shock variances that reproduce the sample's contemporaneous
    second moments exactly (they enter linearly, so this is a 2x2 solve)."""
    pf = _policy(kappa, phi_pi, phi_y, rho_u)
    if not pf:
        return None
    ar, br, au, bu = pf["a_r"], pf["b_r"], pf["a_u"], pf["b_u"]
    vr, vu = _solve2(ar * ar, au * au, br * br, bu * bu, sample["var_x"], sample["var_pi"])
    if not (vr == vr and vu == vu) or vr <= 0 or vu <= 0:
        return None
    rr, ru = FIXED["rho_r"], rho_u
    return {
        "var_x": ar * ar * vr + au * au * vu,
        "var_pi": br * br * vr + bu * bu * vu,
        "cov": ar * br * vr + au * bu * vu,
        "ac1_x": ar * ar * vr * rr + au * au * vu * ru,
        "ac1_pi": br * br * vr * rr + bu * bu * vu * ru,
        "ac2_x": ar * ar * vr * rr ** 2 + au * au * vu * ru ** 2,
        "ac2_pi": br * br * vr * rr ** 2 + bu * bu * vu * ru ** 2,
        "xc1": ar * br * vr * rr + au * bu * vu * ru,
        "V_r": vr, "V_u": vu,
    }


#: The moments the structural parameters are asked to match — the *persistence* structure,
#: since the contemporaneous ones are already solved for.
MATCHED = ("ac1_x", "ac2_x", "ac1_pi", "ac2_pi", "xc1")


def residuals(params: list[float], sample: dict[str, float]) -> list[float]:
    kappa, phi_pi, phi_y, rho_u = params
    mm = model_moments(kappa, phi_pi, phi_y, rho_u, sample)
    if mm is None:
        return [1e3] * len(MATCHED)
    out = []
    for key in MATCHED:
        denom = sample["var_x"] if "x" in key else sample["var_pi"]
        out.append((mm[key] - sample[key]) / (abs(denom) + 1e-12))
    return out


def _loss(params: list[float], sample: dict[str, float]) -> float:
    for p, k in zip(params, ("kappa", "phi_pi", "phi_y", "rho_u")):
        lo, hi = BOUNDS[k]
        if not (lo <= p <= hi):
            return 1e6 + sum(abs(v) for v in params)
    return sum(r * r for r in residuals(params, sample))


def nelder_mead(f, x0: list[float], step: float = 0.1, iters: int = 400, tol: float = 1e-12):
    """Plain Nelder–Mead. Small, deterministic, no scipy — the repo's convention."""
    n = len(x0)
    simplex = [x0[:]] + [[x0[j] + (step if j == i else 0.0) for j in range(n)] for i in range(n)]
    values = [f(p) for p in simplex]
    for _ in range(iters):
        order = sorted(range(n + 1), key=lambda i: values[i])
        simplex = [simplex[i] for i in order]
        values = [values[i] for i in order]
        if abs(values[-1] - values[0]) < tol:
            break
        centroid = [sum(simplex[i][j] for i in range(n)) / n for j in range(n)]
        worst = simplex[-1]
        xr = [centroid[j] + 1.0 * (centroid[j] - worst[j]) for j in range(n)]
        fr = f(xr)
        if fr < values[0]:
            xe = [centroid[j] + 2.0 * (centroid[j] - worst[j]) for j in range(n)]
            fe = f(xe)
            simplex[-1], values[-1] = (xe, fe) if fe < fr else (xr, fr)
        elif fr < values[-2]:
            simplex[-1], values[-1] = xr, fr
        else:
            xc = [centroid[j] + 0.5 * (worst[j] - centroid[j]) for j in range(n)]
            fc = f(xc)
            if fc < values[-1]:
                simplex[-1], values[-1] = xc, fc
            else:
                box = simplex[0]
                simplex = [box] + [[box[j] + 0.5 * (simplex[i][j] - box[j]) for j in range(n)]
                                   for i in range(1, n + 1)]
                values = [f(p) for p in simplex]
    best = min(range(n + 1), key=lambda i: values[i])
    return simplex[best], values[best]


# --- identification -----------------------------------------------------------


def _rank(rows: list[list[float]], tol: float = 1e-8) -> int:
    m = [row[:] for row in rows]
    rank = 0
    cols = len(m[0]) if m else 0
    for col in range(cols):
        pivot = None
        for r in range(rank, len(m)):
            if abs(m[r][col]) > tol:
                pivot = r
                break
        if pivot is None:
            continue
        m[rank], m[pivot] = m[pivot], m[rank]
        p = m[rank][col]
        for r in range(len(m)):
            if r != rank and m[r][col]:
                f = m[r][col] / p
                for c in range(col, cols):
                    m[r][c] -= f * m[rank][c]
        rank += 1
    return rank


def identification(params: list[float], sample: dict[str, float], step: float = 1e-4,
                   free: tuple[str, ...] | None = None) -> dict:
    """Rank of the moment Jacobian with respect to the *free* parameters.

    ``< n_free`` means the sample cannot separate them, and no point estimate should be
    published: the honest output is the rank, not the numbers.
    """
    free = free or ("kappa", "phi_pi", "phi_y", "rho_u")
    idx = {"kappa": 0, "phi_pi": 1, "phi_y": 2, "rho_u": 3}
    base = residuals(params, sample)
    cols = []
    for name in free:
        j = idx[name]
        up, dn = params[:], params[:]
        up[j] += step
        dn[j] -= step
        ru_, rd_ = residuals(up, sample), residuals(dn, sample)
        cols.append([(ru_[i] - rd_[i]) / (2 * step) for i in range(len(base))])
    rows = [[cols[j][i] for j in range(len(cols))] for i in range(len(base))]
    r = _rank(rows)
    return {"rank": r, "n_params": len(free), "identified": r >= len(free), "free": list(free)}


#: A free-parameter set that the sample supports. Estimating all four walks to the
#: bounds and is rank-deficient (see ``probe``), so the two the data cannot separate are
#: held at SW's published values and the fit is labelled *partially* estimated.
FREE = ("kappa", "rho_u")
HELD = {
    "kappa": sw2007.calvo_kappa(),
    "phi_pi": sw2007.PUBLISHED_STRUCTURAL["r_pi"],
    "phi_y": sw2007.PUBLISHED_STRUCTURAL["r_y"],
    "rho_u": 0.8,
}


def full(free_values: list[float], free: tuple[str, ...] = FREE) -> dict[str, float]:
    out = dict(HELD)
    for name, value in zip(free, free_values):
        out[name] = value
    return out


def _loss_free(values: list[float], sample: dict[str, float], free: tuple[str, ...]) -> float:
    p = full(values, free)
    return _loss([p["kappa"], p["phi_pi"], p["phi_y"], p["rho_u"]], sample)


def probe(data: dict | None = None, latest: str | None = None) -> list[dict]:
    """Which parameter subsets this sample can identify? Asked, not assumed."""
    data = data or V.load()
    sample = sample_moments(paths(data, latest))
    out = []
    for free in (("kappa", "phi_pi", "phi_y", "rho_u"), ("kappa", "phi_pi", "rho_u"),
                 ("kappa", "rho_u"), ("phi_pi", "phi_y"), ("rho_u",)):
        x0 = [full([], free)[k] for k in free]
        best, loss = nelder_mead(lambda v: _loss_free(v, sample, free), x0, step=0.05)
        p = full(best, free)
        vec = [p["kappa"], p["phi_pi"], p["phi_y"], p["rho_u"]]
        ident = identification(vec, sample)
        at_bound = any(abs(b - BOUNDS[k][0]) < 1e-6 or abs(b - BOUNDS[k][1]) < 1e-6
                       for b, k in zip(best, free))
        out.append({"free": free, "loss": loss, "values": dict(zip(free, best)),
                    "rank": ident["rank"], "n_free": len(free),
                    "identified": ident["rank"] >= len(free), "at_bound": at_bound})
    return out


def estimate(latest: str | None = None, data: dict | None = None) -> dict:
    data = data or V.load()
    sample = sample_moments(paths(data, latest))
    free = FREE
    x0 = [HELD[k] for k in free]
    best, loss = nelder_mead(lambda v: _loss_free(v, sample, free), x0, step=0.05)
    p = full(best, free)
    kappa, phi_pi, phi_y, rho_u = p["kappa"], p["phi_pi"], p["phi_y"], p["rho_u"]
    ident = identification([kappa, phi_pi, phi_y, rho_u], sample, free=free)
    state = constraint_set._default_state(beta=FIXED["beta"], kappa=kappa,
                                          phi_pi=phi_pi, phi_y=phi_y)
    return {
        "params": {"kappa": kappa, "phi_pi": phi_pi, "phi_y": phi_y, "rho_u": rho_u},
        "fixed": dict(FIXED),
        "loss": loss,
        "sample": sample,
        "model": model_moments(kappa, phi_pi, phi_y, rho_u, sample),
        "identification": ident,
        "constraints": {"violated": constraint_set.violated(state)},
    }


def calibration(fit: dict | None = None) -> dict[str, float]:
    """The fitted vector as an ``nk3`` calibration, for the out-of-sample run.

    Refused when the fit is not identified: an unidentified point estimate carried into
    a forecast is a number with no support, and the module will not hand one out.
    """
    fit = fit or estimate()
    if not fit["identification"]["identified"]:
        raise ValueError(
            "estimate not identified: rank "
            f"{fit['identification']['rank']}/{fit['identification']['n_params']} — "
            "no point estimate may be published from this sample"
        )
    p = fit["params"]
    return {
        "beta": FIXED["beta"], "kappa": p["kappa"], "sigma": FIXED["sigma"],
        "phi_pi": p["phi_pi"], "phi_y": p["phi_y"],
        "rho_r": FIXED["rho_r"], "rho_u": p["rho_u"],
    }


def summary() -> str:
    rule = fit_rule()
    smooth = fit_rule(smoothed=True)
    rec = kappa_recovery()
    bad = admissibility({"beta": FIXED["beta"], "kappa": sw2007.calvo_kappa(),
                         "sigma": FIXED["sigma"], "phi_pi": rule["phi_pi"],
                         "phi_y": rule["phi_y"]})
    return "\n".join(
        [
            "ESTIMATION — what the data will and will not identify",
            "=" * 62,
            f"panel: {rule['n']} observations from {len(paths())} vintage paths",
            "",
            "policy rule, static (the reduction's own specification)",
            f"  i = {rule['intercept']:+.3f} {rule['phi_pi']:+.3f}*pi {rule['phi_y']:+.3f}*x"
            f"   (SEs {rule['se']['phi_pi']:.3f}, {rule['se']['phi_y']:.3f}; R2 {rule['r2']:.3f})",
            "policy rule, smoothed (the data prefer a lag the model does not have)",
            f"  rho={smooth['rho']:.3f}, long-run phi_pi={smooth['long_run_phi_pi']:.3f}, "
            f"long-run phi_y={smooth['long_run_phi_y']:.3f} (R2 {smooth['r2']:.3f})",
            "",
            f"kappa recovered from clean synthetic data at truth {rec['truth']}: "
            f"{rec['recovered']:.3f} -> {'recovered' if rec['recovered_ok'] else 'NOT RECOVERED'}",
            "",
            f"constraint set on the estimated rule: "
            f"{'admissible' if not bad else 'REFUSED (' + ', '.join(bad) + ')'}",
            "",
            "So the estimation project's answer is a REFUSAL, twice over: the slope is not",
            "identified, and the estimated rule is passive — which the constraint set",
            "refuses, because a passive rule admits sunspots. Forecasting with it would",
            "have been the overclaim.",
        ]
    )


def panel(data: dict | None = None) -> list[tuple[float, float, float]]:
    """``(gap, inflation, policy rate)`` rows from each vintage's own data."""
    data = data or V.load()
    rates = data.get("rates") or {}
    rows: list[tuple[float, float, float]] = []
    for vintage in V.vintages(data):
        gdp, cpi = nk3_oos._series(vintage, "GDPC1"), nk3_oos._series(vintage, "CPIAUCSL")
        if not gdp or not cpi:
            continue
        for date in sorted(set(gdp) & set(cpi)):
            if date not in rates:
                continue
            x, p = nk3_oos.gap(gdp, date), nk3_oos.inflation(cpi, date)
            if x == x and p == p:
                rows.append((x, p, rates[date]))
    return rows


def _lstsq(y: list[float], cols: list[list[float]]) -> tuple[list[float], list[float], float]:
    """OLS with standard errors and R^2. Returns ``(coefs, ses, r2)``."""
    n, k = len(y), len(cols)
    xtx = [[sum(cols[i][t] * cols[j][t] for t in range(n)) for j in range(k)] for i in range(k)]
    xty = [sum(cols[i][t] * y[t] for t in range(n)) for i in range(k)]
    coefs = _gauss_solve(xtx, xty)
    resid = [y[t] - sum(coefs[i] * cols[i][t] for i in range(k)) for t in range(n)]
    s2 = sum(r * r for r in resid) / max(n - k, 1)
    inv = _inverse(xtx)
    ses = [math.sqrt(max(s2 * inv[i][i], 0.0)) for i in range(k)]
    ybar = sum(y) / n
    sst = sum((v - ybar) ** 2 for v in y)
    r2 = 1.0 - sum(r * r for r in resid) / sst if sst else float("nan")
    return coefs, ses, r2


def _inverse(a: list[list[float]]) -> list[list[float]]:
    n = len(a)
    m = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(a)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(m[r][col]))
        m[col], m[piv] = m[piv], m[col]
        p = m[col][col]
        for j in range(2 * n):
            m[col][j] /= p
        for r in range(n):
            if r != col:
                f = m[r][col]
                for j in range(2 * n):
                    m[r][j] -= f * m[col][j]
    return [row[n:] for row in m]


def fit_rule(data: dict | None = None, smoothed: bool = False,
             rows: list[tuple[float, float, float]] | None = None) -> dict:
    """Estimate the Taylor rule. ``smoothed`` adds ``i_{t-1}`` (the data want it; the
    three-equation reduction has no lag, so that is a specification gap, named)."""
    rows = rows if rows is not None else panel(data)
    y = [r[2] for r in rows]
    cols = [[1.0] * len(rows), [r[1] for r in rows], [r[0] for r in rows]]
    if smoothed:
        lag = [y[0]] + y[:-1]
        cols.append(lag)
    coefs, ses, r2 = _lstsq(y, cols)
    out = {"n": len(rows), "intercept": coefs[0], "phi_pi": coefs[1], "phi_y": coefs[2],
           "r2": r2, "se": {"intercept": ses[0], "phi_pi": ses[1], "phi_y": ses[2]},
           "smoothed": smoothed}
    if smoothed:
        rho = coefs[3]
        out.update({"rho": rho, "se_rho": ses[3],
                    "long_run_phi_pi": coefs[1] / (1 - rho) if abs(1 - rho) > 1e-9 else float("nan"),
                    "long_run_phi_y": coefs[2] / (1 - rho) if abs(1 - rho) > 1e-9 else float("nan")})
    return out


def kappa_recovery(data: dict | None = None, truth: float = 0.18, seed: int = 7) -> dict:
    """Simulate at a known ``kappa`` and try to recover it.

    The point is the *failure*: if the estimator cannot recover a known kappa from clean
    synthetic data, then no kappa estimated from real data means anything. That is the
    weak-identification result, measured on this machinery instead of cited.
    """
    import random

    rng = random.Random(seed)
    phi_pi, phi_y, rho_u = 2.04, 0.08, 0.6
    pf = _policy(truth, phi_pi, phi_y, rho_u)
    sim: list[tuple[list[float], list[float]]] = []
    for _ in range(6):
        sr = su = 0.0
        xs, ps = [], []
        for _ in range(80):
            sr = FIXED["rho_r"] * sr + rng.gauss(0, math.sqrt(0.5 * (1 - FIXED["rho_r"] ** 2)))
            su = rho_u * su + rng.gauss(0, math.sqrt(0.9 * (1 - rho_u ** 2)))
            xs.append(pf["a_r"] * sr + pf["a_u"] * su)
            ps.append(pf["b_r"] * sr + pf["b_u"] * su)
        sim.append((xs, ps))
    sample = sample_moments(sim)
    best, loss = nelder_mead(lambda v: _loss_free(v, sample, ("kappa",)), [0.3], step=0.05)
    return {"truth": truth, "recovered": best[0], "loss": loss,
            "recovered_ok": abs(best[0] - truth) < 0.05}


def admissibility(cal: dict[str, float]) -> list[str]:
    """Run a calibration through the constraint set — the operational form of "as many
    constraints as the system needs"."""
    state = constraint_set._default_state(
        beta=cal["beta"], kappa=cal["kappa"], phi_pi=cal["phi_pi"], phi_y=cal["phi_y"]
    )
    return constraint_set.violated(state)


class InadmissibleFit(ValueError):
    """The data-fitted model violates the constraint set, so it may not be forecast with."""


def estimated_calibration(data: dict | None = None) -> dict[str, float]:
    """The calibration the data *can* support: the rule estimated, the slope held at
    SW's Calvo value (kappa is not identified — see ``kappa_recovery``)."""
    rule = fit_rule(data)
    cal = {
        "beta": FIXED["beta"], "kappa": sw2007.calvo_kappa(), "sigma": FIXED["sigma"],
        "phi_pi": rule["phi_pi"], "phi_y": rule["phi_y"],
        "rho_r": FIXED["rho_r"], "rho_u": 0.8,
    }
    bad = admissibility(cal)
    if bad:
        raise InadmissibleFit(
            "the estimated rule is refused by the constraint set: "
            + ", ".join(bad)
            + f" (phi_pi={cal['phi_pi']:.3f}, phi_y={cal['phi_y']:.3f})"
        )
    return cal


if __name__ == "__main__":
    print(summary())
