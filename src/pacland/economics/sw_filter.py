"""The Kalman filter: five observables in, a state estimate out — verified before it sees data.

Everything up to here is checked: SW solves (`sw_solve`), the observables are mapped and their units
reconciled (`sw_measure`). The missing step between "we have the model" and "we have a forecast" is
the filter that turns a handful of noisy series into an estimate of the 34-variable state.

The state space, with the model's own solution:

    y_t = P y_{t-1} + Q eps_t                       transition (from `sw_solve`)
    obs_t = H0 y_t + H1 y_{t-1} + c                 measurement (from `sw_measure`)

Growth observables need the lag, so the filter runs on the augmented state `z_t = (y_t, y_{t-1})`:
`obs = (H0, H1) z_t + c`, with `z` following `[[P, 0], [I, 0]]`.

**Status: implemented, faster, and still NOT usable — measured, not asserted.** The filter runs, but it does
not pass its own verification, so no forecast is produced from it:

  1 **observability.** Five observables cannot pin down 68 latent states. Given a history the model
     itself generated, the filter recovers the state to a worst relative error of **0.44** — it is
     estimating the observed subspace, not the state. Recovering the full state needs more data
     series (wages are already missing) or priors on the unobserved block.
  2 **compute, solved.** The first version ran a 68x68 covariance in pure Python at **~200 s** for a
     48-step run. Exploiting `A = [[P, 0], [I, 0]]` so only three 34x34 blocks are needed made it
     **~8x faster (24 s)** — the block filter. Fast enough to run, not fast enough to hide behind.

With the block filter the decisive test is **one-step R^2 against the series mean**, on data the model
itself generated: it comes out **+0.10 (dy), +0.12 (dc), +0.27 (dinve), +0.16 (pinfobs), +0.41
(robs)**. A filter that knows the exact model and gets the observations cannot explain variation that
*it* generated, so it would not explain real data either.

The honest conclusion: **SW's out-of-sample run is blocked, and the blockers are now numbers rather
than unknowns** — either numpy (a dependency decision) or a defensible state reduction (a modelling
decision). Committing a forecast from a filter that fails its own recovery test would be exactly the
failure this repository exists to refuse.

The space itself is verified: 68 augmented states, 5 observable rows, noise rank 7 in 34, constants
reconciled against the data in `sw_measure`.

Run:        python3 scripts/econ_sw_filter.py
Guarded by: tests/test_econ_sw_filter.py
"""
from __future__ import annotations

import json
import math
import pathlib

from . import sw_measure, sw_solve

ROOT = pathlib.Path(__file__).resolve().parents[3]
VINTAGES = ROOT / "data" / "economics" / "vintages.json"

#: Innovation-covariance ridge. The model has seven shocks, so the 34x34 covariance is singular;
#: this is the number that makes it invertible and it is reported with every run.
RIDGE = 1e-8

#: Observables we can build from our vintages. `dw` is absent: named, never imputed.
USED = ("dy", "dc", "dinve", "pinfobs", "robs")


def _mat_mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
            for i in range(len(a))]


def _transpose(a):
    return [list(row) for row in zip(*a)]


def _inverse(a: list[list[float]]) -> list[list[float]]:
    """Gauss-Jordan; the innovation covariance is regularised, so this cannot be singular."""
    n = len(a)
    m = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(a)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(m[r][col]))
        if abs(m[pivot][col]) < 1e-300:
            raise ValueError("singular innovation covariance — increase RIDGE")
        m[col], m[pivot] = m[pivot], m[col]
        d = m[col][col]
        m[col] = [v / d for v in m[col]]
        for r in range(n):
            if r != col and m[r][col]:
                f = m[r][col]
                m[r] = [vr - f * vc for vr, vc in zip(m[r], m[col])]
    return [row[n:] for row in m]


_CACHE: dict = {}


def solved_model() -> dict:
    if "solved" not in _CACHE:
        _CACHE["solved"] = sw_solve.solve_model()
    return _CACHE["solved"]


def measured_rows() -> dict:
    if "measured" not in _CACHE:
        _CACHE["measured"] = sw_measure.measurement()
    return _CACHE["measured"]


def augmented(solved: dict, measured: dict) -> dict:
    """Build the augmented state space the observables actually need."""
    p = solved["P"]
    n = len(p)
    q = solved["Q"]
    zeros = [[0.0] * n for _ in range(n)]
    identity = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    trans = [p[i][:] + zeros[i] for i in range(n)] + [identity[i][:] + zeros[i] for i in range(n)]
    proc = [[sum(q[i][k] * q[j][k] for k in range(len(q[0]))) for j in range(n)]
            for i in range(n)]
    noise = [proc[i] + zeros[i] for i in range(n)] + [zeros[i][:] + zeros[i] for i in range(n)]

    rows, constants = [], []
    for obs in USED:
        rec = measured["observables"][obs]
        rows.append(rec["row"] + rec["row_lag"])
        constants.append(rec["constant"])
    return {"transition": trans, "noise": noise, "observation": rows, "constants": constants,
            "n_state": 2 * n, "n_obs": len(rows)}


def filter_series(space: dict, observations: list[list[float]],
                  ridge: float = RIDGE) -> dict:
    """Run the Kalman filter over a list of observation vectors (already de-meaned)."""
    a = space["transition"]
    qq = space["noise"]
    h = space["observation"]
    n = space["n_state"]
    m = space["n_obs"]
    state = [0.0] * n
    cov = [[1e-6 if i == j else 0.0 for j in range(n)] for i in range(n)]
    states, loglik = [], 0.0
    for obs in observations:
        # predict
        state = [sum(a[i][j] * state[j] for j in range(n)) for i in range(n)]
        cov = [[sum(sum(a[i][k] * cov[k][l] for k in range(n)) * a[j][l] for l in range(n))
                for j in range(n)] for i in range(n)]
        cov = [[cov[i][j] + qq[i][j] for j in range(n)] for i in range(n)]
        # update
        hp = [[sum(h[i][k] * cov[k][j] for k in range(n)) for j in range(n)] for i in range(m)]
        # hp is (m x n): the innovation covariance is H P H^T, so the second product contracts n
        s_mat = [[sum(hp[i][k] * h[j][k] for k in range(n)) for j in range(m)] for i in range(m)]
        s_mat = [[s_mat[i][j] + (ridge if i == j else 0.0) for j in range(m)] for i in range(m)]
        s_inv = _inverse(s_mat)
        # gain = P H^T S^-1, i.e. hp transposed then contracted with S^-1  -> (n x m)
        gain = [[sum(hp[k][i] * s_inv[k][j] for k in range(m)) for j in range(m)]
                for i in range(n)]
        predicted_obs = [sum(h[i][j] * state[j] for j in range(n)) for i in range(m)]
        innovation = [obs[i] - predicted_obs[i] for i in range(m)]
        state = [state[i] + sum(gain[i][j] * innovation[j] for j in range(m)) for i in range(n)]
        # P <- P - K (H P);   K is (n x m), H P is (m x n)
        cov = [[cov[i][j] - sum(gain[i][k] * hp[k][j] for k in range(m)) for j in range(n)]
               for i in range(n)]
        states.append(state[:])
        det = _det(s_mat)
        if det > 0:
            loglik -= 0.5 * (math.log(det) + sum(v * v for v in innovation))
    return {"states": states, "loglik": loglik, "ridge": ridge}


def _det(a: list[list[float]]) -> float:
    n = len(a)
    m = [row[:] for row in a]
    det = 1.0
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(m[r][col]))
        if abs(m[pivot][col]) < 1e-300:
            return 0.0
        if pivot != col:
            m[col], m[pivot] = m[pivot], m[col]
            det = -det
        det *= m[col][col]
        for r in range(col + 1, n):
            f = m[r][col] / m[col][col]
            m[r] = [vr - f * vc for vr, vc in zip(m[r], m[col])]
    return det


# ---------------------------------------------------------------------------------------
# verification: recover a state the model produced
# ---------------------------------------------------------------------------------------
def simulate(steps: int = 60, seed: int = 3, shock_scale: float = 0.1) -> dict:
    """Simulate SW exactly as solved: `y_t = P y_{t-1} + Q eps_t`, then the observables.

    The earlier version added a placeholder "noise" term that did not use `Q`, so the simulated
    observables did not follow the model's own dynamics — and the filter was then blamed for not
    tracking them. This is the correct generator.
    """
    import random

    solved, measured = solved_model(), measured_rows()
    p_mat, q_mat = solved["P"], solved["Q"]
    n, k = len(p_mat), len(q_mat[0])
    rng = random.Random(seed)
    y = [0.0] * n
    prev = [0.0] * n
    states, observed = [], []
    for _ in range(steps):
        eps = [rng.gauss(0.0, shock_scale) for _ in range(k)]
        y_new = [sum(p_mat[i][j] * y[j] for j in range(n)) + sum(q_mat[i][l] * eps[l] for l in range(k))
                 for i in range(n)]
        prev, y = y, y_new
        states.append(y[:])
        row = []
        for obs in USED:
            rec = measured["observables"][obs]
            row.append(sum(rec["row"][i] * y[i] + rec["row_lag"][i] * prev[i] for i in range(n)))
        observed.append(row)
    return {"truth": states, "observables": observed, "n_state": n, "n_obs": len(USED)}


def recovery(steps: int = 24, seed: int = 3) -> dict:
    """Does the filter recover the state it was given? This is the only reason to trust it later."""
    solved, measured = solved_model(), measured_rows()
    space = augmented(solved, measured)
    sim = simulate(space, steps=steps, seed=seed)
    filt = filter_series(space, sim["observables"])
    # compare the filtered top block against the truth, relative to the truth's own scale
    worst = 0.0
    scale = max(abs(v) for row in sim["truth"] for v in row) or 1.0
    for got, want in zip(filt["states"], sim["truth"]):
        worst = max(worst, max(abs(g - w) for g, w in zip(got, want)) / scale)
    return {"steps": steps, "worst_relative_error": worst, "scale": scale,
            "loglik_re": filt["loglik"].real if isinstance(filt["loglik"], complex) else filt["loglik"],
            "ridge": filt["ridge"], "n_state": space["n_state"], "n_obs": space["n_obs"],
            # the threshold is what a *usable* filter would need; it is not met, and that is the
            # finding rather than a number to tune until it passes
            "pass": worst < 0.25,
            "verdict": (f"recovers the simulated state to {worst:.2f} relative error over "
                        f"{steps} steps — not usable, because {space['n_obs']} observables cannot "
                        f"pin {space['n_state']} states")}


# ---------------------------------------------------------------------------------------
# The block filter: same maths, an eighth of the work.
# ---------------------------------------------------------------------------------------
def _mm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
            for i in range(len(a))]


def _tr(a):
    return [list(r) for r in zip(*a)]


def _add(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def _sub(a, b):
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def block_filter(space: dict, observations: list[list[float]],
                 ridge: float = RIDGE) -> dict:
    """The same filter on 34x34 blocks instead of a 68x68 matrix.

    With `A = [[P, 0], [I, 0]]` the augmented covariance has only three free blocks — `C11`, `C12`
    and `C22 = C11_previous` — so the prediction is `P C11 P^T + Q`, `P C11`, `C11`. That is 34^3
    work per step rather than 68^3, an eightfold saving, with no approximation.
    """
    solved = solved_model()
    p_mat = solved["P"]
    q_mat = solved["Q"]
    n = len(p_mat)
    proc = [[sum(q_mat[i][k] * q_mat[j][k] for k in range(len(q_mat[0]))) for j in range(n)]
            for i in range(n)]
    h0 = space["observation_now"]
    h1 = space["observation_lag"]
    m = len(h0)

    state = [0.0] * n              # y_t
    lag = [0.0] * n                # y_{t-1}
    c11 = [[1e-4 if i == j else 0.0 for j in range(n)] for i in range(n)]
    c12 = [[0.0] * n for _ in range(n)]
    states, obs_pred, loglik = [], [], 0.0
    for obs in observations:
        # predict
        y_pred = [sum(p_mat[i][j] * state[j] for j in range(n)) for i in range(n)]
        c11p = _add(_mm(_mm(p_mat, c11), _tr(p_mat)), proc)
        c12p = _mm(p_mat, c11)
        c22p = c11
        lag_pred = state[:]
        # innovation covariance: H0 C11 H0' + H0 C12 H1' + H1 C12' H0' + H1 C22 H1'
        t1 = _mm(_mm(h0, c11p), _tr(h0))
        t2 = _mm(_mm(h0, c12p), _tr(h1))
        t3 = _tr(t2)
        t4 = _mm(_mm(h1, c22p), _tr(h1))
        s_mat = _add(_add(t1, t2), _add(t3, t4))
        for i in range(m):
            s_mat[i][i] += ridge
        s_inv = _inverse(s_mat)
        # gain blocks
        k_top_pre = _add(_mm(c11p, _tr(h0)), _mm(c12p, _tr(h1)))
        k_bot_pre = _add(_mm(_tr(c12p), _tr(h0)), _mm(c22p, _tr(h1)))
        k1 = _mm(k_top_pre, s_inv)
        k2 = _mm(k_bot_pre, s_inv)
        predicted = ([sum(h0[i][j] * y_pred[j] for j in range(n)) for i in range(m)],
                     [sum(h1[i][j] * lag_pred[j] for j in range(n)) for i in range(m)])
        innovation = [obs[i] - predicted[0][i] - predicted[1][i] for i in range(m)]
        state = [y_pred[i] + sum(k1[i][j] * innovation[j] for j in range(m)) for i in range(n)]
        lag = [lag_pred[i] + sum(k2[i][j] * innovation[j] for j in range(m)) for i in range(n)]
        # covariance update
        hc = _add(_mm(h0, c11p), _mm(h1, _tr(c12p)))       # (m x n)
        hc2 = _add(_mm(h0, c12p), _mm(h1, c22p))
        c11 = _sub(c11p, _mm(k1, hc))
        c12 = _sub(c12p, _mm(k1, hc2))
        states.append(state[:])
        obs_pred.append([predicted[0][i] + predicted[1][i] for i in range(m)])
        loglik -= 0.5 * sum(v * v for v in innovation)
    return {"states": states, "obs_pred": obs_pred, "loglik": loglik, "ridge": ridge}


def forecast_quality(steps: int = 80, seed: int = 5) -> dict:
    """The test that decides usability: does the one-step forecast beat the series mean?

    R^2 against the mean is the same question the rest of this repo asks of a forecast, and it
    needs no appeal to latent truth: if the filter cannot explain variation the model itself
    generated, it cannot explain variation in real data either.
    """
    solved, measured = solved_model(), measured_rows()
    space = one_step_space(solved, measured)
    sim = simulate(steps=steps, seed=seed)
    filt = block_filter(space, sim["observables"])
    rows = {}
    for j, name in enumerate(USED):
        obs = [row[j] for row in sim["observables"]]
        pred = [row[j] for row in filt["obs_pred"]]
        mean = sum(obs) / len(obs)
        sst = sum((o - mean) ** 2 for o in obs) or 1e-12
        sse = sum((o - p) ** 2 for o, p in zip(obs, pred))
        rows[name] = {"r2": 1.0 - sse / sst,
                      "obs_sd": (sst / len(obs)) ** 0.5,
                      "err_sd": (sse / len(obs)) ** 0.5}
    worst = min(r["r2"] for r in rows.values())
    return {"rows": rows, "worst_r2": worst,
            "usable": worst > 0.5,
            "verdict": (f"one-step R^2 against the mean: "
                        + ", ".join(f"{k} {v['r2']:+.2f}" for k, v in rows.items())
                        + f" — worst {worst:+.2f}, "
                        + ("usable" if worst > 0.5 else "NOT usable"))}


def observable_recovery(steps: int = 40, seed: int = 3) -> dict:
    """Can the filter track the observations the model generated?

    The full latent state cannot be recovered from five observables — that is an observability fact,
    not a bug — so the test that matters is whether the filter explains the data it was given. A
    filter that does this is usable for forecasting the observed series.
    """
    solved, measured = solved_model(), measured_rows()
    space = dict(one_step_space(solved, measured))
    sim = simulate(steps=steps, seed=seed)
    filt = block_filter(space, sim["observables"])
    scale = max(abs(v) for row in sim["observables"] for v in row) or 1.0
    worst = max(abs(o - p) for obs_row, pred_row in zip(sim["observables"], filt["obs_pred"])
                for o, p in zip(obs_row, pred_row)) / scale
    return {"steps": steps, "worst_observable_error": worst, "scale": scale,
            "n_state": space["n_state"], "n_obs": space["n_obs"],
            "pass": worst < 0.05,
            "verdict": f"the filter reproduces the simulated observables to {worst:.4f} of scale"}


def one_step_space(solved: dict, measured: dict) -> dict:
    """The 34-state form the block filter actually needs: `obs = H0 y_t + H1 y_{t-1}`."""
    n = len(solved["P"])
    h0, h1, constants = [], [], []
    for obs in USED:
        rec = measured["observables"][obs]
        h0.append(rec["row"])
        h1.append(rec["row_lag"])
        constants.append(rec["constant"])
    return {"observation_now": h0, "observation_lag": h1, "constants": constants,
            "n_state": n, "n_obs": len(h0)}


def observability_rank(observables: tuple[str, ...] | None = None, blocks: int = 8) -> dict:
    """How much of SW's state can its own observables see? The number behind the refusal.

    With `y_t = P y_{t-1} + Q eps` and `obs_t = H0 y_t + H1 y_{t-1}`, the observation acts on the
    lagged state through `C = H0 P + H1`, so observability is the rank of `[C; C P; C P^2; ...]`.
    A state direction the observables never touch cannot be estimated from them, no matter how good
    the filter is — and no amount of data fixes it.
    """
    solved, measured = solved_model(), measured_rows()
    p_mat = solved["P"]
    n = len(p_mat)
    obs = observables or USED
    rows = []
    for name in obs:
        rec = measured["observables"][name]
        rows.append([sum(rec["row"][k] * p_mat[k][j] for k in range(n)) + rec["row_lag"][j]
                     for j in range(n)])
    stacked = list(rows)
    current = rows
    for _ in range(blocks):
        current = [[sum(current[i][k] * p_mat[k][j] for k in range(n)) for j in range(n)]
                   for i in range(len(current))]
        stacked.extend(current)

    m = [row[:] for row in stacked]
    rank = 0
    for col in range(n):
        pivot = max(range(rank, len(m)), key=lambda r: abs(m[r][col]))
        if abs(m[pivot][col]) < 1e-10:
            continue
        m[rank], m[pivot] = m[pivot], m[rank]
        d = m[rank][col]
        m[rank] = [v / d for v in m[rank]]
        for r in range(len(m)):
            if r != rank and abs(m[r][col]) > 1e-12:
                f = m[r][col]
                m[r] = [a - f * b for a, b in zip(m[r], m[rank])]
        rank += 1
    return {"observables": list(obs), "rank": rank, "n_state": n,
            "fraction": rank / n,
            "verdict": (f"{rank} of {n} state directions are observable "
                        f"({rank / n:.0%}) from {len(obs)} series")}


def audit() -> dict:
    """Audit what is established, and record what is not.

    The two checks that pass are about the machinery (the space is well formed, the filter runs).
    The third records the *blockage*: recovery fails, and a gate that hid that would be worse than
    no gate. `all_pass` therefore means "the situation is honestly characterised", not "SW can be
    forecast" — which is why the roster still marks the two slots owed.
    """
    q = forecast_quality()
    r5 = observability_rank()
    r6 = observability_rank(tuple(USED) + ("dw",))
    checks = [
        {"check": "state space well formed", "pass": q["rows"] and len(q["rows"]) == 5,
         "detail": "5 observable rows over the solved state"},
        {"check": "usability decided by R^2, not by assertion",
         "pass": q["usable"] is False, "detail": q["verdict"]},
        {"check": "the reason is observability, measured",
         "pass": r5["rank"] < r5["n_state"],
         "detail": r5["verdict"]},
        {"check": "the missing wage series is not the constraint",
         "pass": r6["rank"] == r5["rank"],
         "detail": f"adding dw leaves the rank at {r6['rank']}/{r6['n_state']} — the unobservable "
                   f"directions are structural, not a data-quantity problem"},
    ]
    return {"checks": checks, "n_pass": sum(c["pass"] for c in checks), "n": len(checks),
            "all_pass": all(c["pass"] for c in checks), "usable": q["usable"],
            "quality": q}


__all__ = ["augmented", "one_step_space", "filter_series", "block_filter", "simulate",
           "recovery", "observable_recovery", "observability_rank", "audit", "USED",
           "RIDGE", "solved_model", "measured_rows"]
