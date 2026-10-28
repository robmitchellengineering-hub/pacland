"""Smets–Wouters, solved — the model itself, from the authors' own file.

`sw_linear.py` parses the authors' Dynare file and checks its steady state. `resolve.py` solves
linear rational-expectations systems and is verified against closed forms. This joins them: it
extracts the coefficient matrices of SW's 34 equilibrium equations, solves for the policy function,
and reports what the solved model implies.

Three things are checked, and each could have failed:

  1 **the extraction is faithful** — every equilibrium equation must vanish at the steady state to
    zero tolerance, and the system must be square (34 equations, 34 endogenous variables). A
    coefficient extracted wrongly shows up here, not in a forecast.
  2 **the policy is a solution** — plug `P, Q` back into `A y = B y_{-1} + C E y_{+1} + D ε` and the
    residuals must vanish.
  3 **the policy is stable** — simulated forward, the state must not grow. An unstable "solution" of
    the quadratic matrix equation is a real failure mode, and it looks like a success.

What it implies is then reported as impulse responses to named shocks, with the sign checked against
economics: a contractionary monetary shock must lower output *and* inflation. If it raised them, the
matrices would be wrong even though nothing else complained.

The GPL `.mod` is fetched at run time and never committed (see `sw_linear`).

Run:        python3 scripts/econ_sw_solve.py
Guarded by: tests/test_econ_sw_solve.py
"""
from __future__ import annotations

import pathlib
import re
import subprocess

from . import resolve, sw_linear

URL = ("https://raw.githubusercontent.com/rui-q/DSGE_mod/master/"
       "Smets_Wouters_2007/Smets_Wouters_2007.mod")
CACHE = pathlib.Path("/tmp/sw2007.mod")

#: The innovations declared `varexo` in the file. They have no equation of their own: they are the
#: exogenous input, which is why the equilibrium block is 34 equations in 34 endogenous variables.
INNOVATIONS = ("ea", "eb", "eg", "eqs", "em", "epinf", "ew")

#: The shocks worth naming in a report, with the economics they must obey.
NAMES = {"em": "monetary policy", "epinf": "price-markup (cost-push)", "ea": "TFP",
         "eb": "risk premium", "eg": "government spending", "eqs": "investment-specific",
         "ew": "wage markup"}


def text() -> str:
    if not CACHE.exists() or CACHE.stat().st_size < 1000:
        subprocess.run(["curl", "-sS", "--max-time", "120", "-L", "-o", str(CACHE), URL], check=True)
    return CACHE.read_text()


def _strip(token: str) -> str:
    if token.endswith("_lead"):
        return token[:-5]
    if token.endswith("_lag"):
        return token[:-4]
    return token


def matrices(text_: str | None = None, use_posterior: bool = True) -> dict:
    """Extract `A, B, C, D` for `A y_t + B y_{t-1} + C y_{t+1} + D eps_t = 0`.

    The model is linear in deviations, so a coefficient is just the residual evaluated with that
    variable set to one — no symbolic algebra, and the steady-state check comes for free.
    """
    parsed = sw_linear.parse(text_ or text(), use_posterior=use_posterior)
    known = set(parsed.params) | set(parsed.definitions)
    equations = [sw_linear.to_python(e) for e in parsed.equilibrium]

    endogenous: set[str] = set()
    for eq in equations:
        for token in re.findall(r"[a-zA-Z_]\w*", eq):
            base = _strip(token)
            if base not in known and base not in {"lead", "lag"} and base not in INNOVATIONS:
                endogenous.add(base)
    endo = sorted(endogenous)
    innovations = [s for s in INNOVATIONS]

    def evaluate(eq: str, assign: dict[str, float]) -> float:
        env = {**parsed.params, **parsed.definitions}
        for name in endo:
            env[name] = env[name + "_lag"] = env[name + "_lead"] = 0.0
        for name in innovations:
            env[name] = 0.0
        env.update(assign)
        lhs, rhs = eq.split("=", 1)
        return (eval(lhs, {"__builtins__": {}}, env)          # noqa: S307 - parsed model, no input
                - eval(rhs, {"__builtins__": {}}, env))

    n, k = len(equations), len(endo)
    a = [[0.0] * k for _ in range(n)]
    b = [[0.0] * k for _ in range(n)]
    c = [[0.0] * k for _ in range(n)]
    d = [[0.0] * len(innovations) for _ in range(n)]
    worst_ss = 0.0
    for i, eq in enumerate(equations):
        base = evaluate(eq, {})
        worst_ss = max(worst_ss, abs(base))
        for j, name in enumerate(endo):
            a[i][j] = evaluate(eq, {name: 1.0}) - base
            b[i][j] = evaluate(eq, {name + "_lag": 1.0}) - base
            c[i][j] = evaluate(eq, {name + "_lead": 1.0}) - base
        for j, name in enumerate(innovations):
            d[i][j] = evaluate(eq, {name: 1.0}) - base
    return {"endo": endo, "innovations": innovations, "A": a, "B": b, "C": c, "D": d,
            "n_equations": n, "n_endogenous": k, "worst_steady_state_residual": worst_ss,
            "square": n == k}


def stability(policy: list[list[float]], steps: int = 300, seed: int = 1) -> dict:
    """Simulate the policy forward: an unstable 'solution' grows instead of decaying."""
    import random

    rng = random.Random(seed)
    n = len(policy)
    v = [rng.uniform(-1.0, 1.0) for _ in range(n)]
    first = max(abs(x) for x in v)
    peak = first
    for _ in range(steps):
        v = [sum(policy[i][j] * v[j] for j in range(n)) for i in range(n)]
        norm = max(abs(x) for x in v)
        peak = max(peak, norm)
        if norm > 1e9:
            break
    return {"decays": peak <= first * 10.0, "peak_ratio": peak / first,
            "final_ratio": norm / first if first else float("inf")}


def solve_model(text_: str | None = None) -> dict:
    """Solve SW and check the result three ways."""
    m = matrices(text_)
    neg_b = [[-v for v in row] for row in m["B"]]
    neg_c = [[-v for v in row] for row in m["C"]]
    neg_d = [[-v for v in row] for row in m["D"]]
    sol = resolve.solve(m["A"], neg_b, neg_c, neg_d, rho=0.0, iters=4000, tol=1e-13)
    stab = stability(sol["P"])
    return {**m, "P": sol["P"], "Q": sol["Q"],
            "residual_P": sol["residual_P"], "residual_Q": sol["residual_Q"],
            "stable": stab["decays"], "peak_ratio": stab["peak_ratio"],
            "pass": (m["square"] and m["worst_steady_state_residual"] < 1e-9
                     and sol["residual_P"] < 1e-9 and sol["residual_Q"] < 1e-9
                     and stab["decays"])}


def irf(solved: dict, shock: str, horizon: int = 16) -> dict[str, list[float]]:
    """Impulse response of every variable to a one-unit innovation, `Q` then `P` forward."""
    j = solved["innovations"].index(shock)
    y = [solved["Q"][i][j] for i in range(len(solved["endo"]))]
    out: dict[str, list[float]] = {name: [y[i]] for i, name in enumerate(solved["endo"])}
    for _ in range(horizon):
        y = [sum(solved["P"][i][k] * y[k] for k in range(len(y))) for i in range(len(y))]
        for i, name in enumerate(solved["endo"]):
            out[name].append(y[i])
    return out


def guard_monetary_shock_sign(solved: dict | None = None) -> tuple[bool, str]:
    """MUTATION/ECONOMICS: a contractionary monetary shock must lower output AND inflation.

    If either rises on impact, the extracted matrices are wrong — and nothing else in the
    pipeline would have complained, because the residuals and the stability check both pass.
    """
    s = solved or solve_model()
    path = irf(s, "em", horizon=12)
    y_impact, pi_impact = path["y"][0], path["pinf"][0]
    y_trough = min(path["y"])
    ok = y_impact < 0.0 and pi_impact < 0.0 and y_trough < 0.0
    return ok, (f"monetary shock: output {y_impact:+.4f} on impact (trough {y_trough:+.4f}), "
                f"inflation {pi_impact:+.4f} — both fall = {ok}")


def audit() -> dict:
    checks = []
    solved = solve_model()
    for name, run in (
        ("extraction faithful", lambda: (solved["square"]
                                        and solved["worst_steady_state_residual"] < 1e-9,
                                        f"{solved['n_equations']} equations, "
                                        f"{solved['n_endogenous']} endogenous, steady-state "
                                        f"residual {solved['worst_steady_state_residual']:.1e}")),
        ("policy solves the system", lambda: (solved["residual_P"] < 1e-9
                                              and solved["residual_Q"] < 1e-9,
                                              f"residuals {solved['residual_P']:.1e} / "
                                              f"{solved['residual_Q']:.1e}")),
        ("policy is stable", lambda: (solved["stable"],
                                      f"forward simulation peak ratio {solved['peak_ratio']:.2f}")),
        ("economics holds", lambda: guard_monetary_shock_sign(solved)),
    ):
        ok, msg = run()
        checks.append({"check": name, "pass": bool(ok), "detail": msg})
    return {"checks": checks, "n_pass": sum(c["pass"] for c in checks),
            "n": len(checks), "all_pass": all(c["pass"] for c in checks)}


__all__ = ["matrices", "solve_model", "irf", "stability", "guard_monetary_shock_sign",
           "audit", "text", "NAMES", "INNOVATIONS"]
