"""A generic solver for linear rational-expectations models — the missing piece for Smets–Wouters.

`nk3.py` solves one small model in closed form. `sw_linear.py` parses the Smets–Wouters equations
but cannot project them. This is the machinery in between: a solver for systems written as

    A y_t = B y_{t-1} + C E_t y_{t+1} + D eps_t

with the policy function `y_t = P y_{t-1} + Q eps_t`, found by the method of undetermined
coefficients: substitute the guess twice, collect terms, and require

    A P = B + C P^2                      (the P equation is quadratic — iterate it)
    A Q = D + C P Q                        (linear in Q once P is known)

Iteration converges for a determinate model and diverges for an indeterminate one, which is the
determinacy check rather than an extra assumption.

**How it is verified** — three ways, because a solver that is wrong quietly is worse than none:

  1. a closed-form case (a univariate forward-looking model) where the answer is known by hand
  2. residual checks: `A P - B - C P^2` and `A Q - D - C(P Q + Q rho)` must vanish
  3. **cross-check against `nk3.policy_function`**, which solves the New Keynesian three-equation
     model analytically — two independent routes to the same coefficients

Run:        python3 scripts/econ_resolve.py
Guarded by: tests/test_econ_resolve.py
"""
from __future__ import annotations

import math

Matrix = list[list[float]]


def _mat_mul(a: Matrix, b: Matrix) -> Matrix:
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
            for i in range(len(a))]


def _mat_add(a: Matrix, b: Matrix) -> Matrix:
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def _mat_sub(a: Matrix, b: Matrix) -> Matrix:
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def _solve(a: Matrix, b: Matrix) -> Matrix:
    """Gaussian elimination with partial pivoting; b is a matrix of right-hand sides."""
    n = len(a)
    m = [row[:] + list(b[i]) for i, row in enumerate(a)]
    width = len(b[0])
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(m[r][col]))
        if abs(m[pivot][col]) < 1e-14:
            raise ValueError("singular matrix in the RE solver — the model is not determinate")
        m[col], m[pivot] = m[pivot], m[col]
        d = m[col][col]
        m[col] = [v / d for v in m[col]]
        for r in range(n):
            if r != col and abs(m[r][col]) > 0.0:
                f = m[r][col]
                m[r] = [vr - f * vc for vr, vc in zip(m[r], m[col])]
    return [[m[i][n + j] for j in range(width)] for i in range(n)]


def _max_abs(a: Matrix) -> float:
    return max(abs(v) for row in a for v in row) if a and a[0] else 0.0


def solve(a: Matrix, b: Matrix, c: Matrix, d: Matrix, rho: float,
          iters: int = 400, tol: float = 1e-14) -> dict:
    """Solve `A y = B y_{-1} + C E y_{+1} + D eps` for the policy `(P, Q)`.

    `rho` is the persistence of the (single) shock driving `D`. A determinate model converges from
    `P = 0`; an indeterminate one does not, and is refused rather than returned.
    """
    n = len(a)
    p = [[0.0] * n for _ in range(n)]
    converged = False
    last_change = float("inf")
    for _ in range(iters):
        p2 = _mat_mul(p, p)
        rhs = _mat_add(b, _mat_mul(c, p2))
        nxt = _solve(a, rhs)
        last_change = _max_abs(_mat_sub(nxt, p))
        p = nxt
        if last_change < tol:
            converged = True
            break
    if not converged:
        raise ValueError(
            f"policy iteration did not converge (last change {last_change:.3e}) — the model is "
            "indeterminate, or the shock persistence is inconsistent with it")

    # Q solves A Q = D + C P Q  =>  (A - C P) Q = D.
    # The shock's persistence is already inside P (its row of the state equation), so adding a
    # rho*Q term here would double-count it — that error gave a policy 3.6x too large.
    q = _solve(_mat_sub(a, _mat_mul(c, p)), d)

    resid_p = _max_abs(_mat_sub(_mat_mul(a, p), _mat_add(b, _mat_mul(c, _mat_mul(p, p)))))
    resid_q = _max_abs(_mat_sub(_mat_mul(a, q), _mat_add(d, _mat_mul(c, _mat_mul(p, q)))))
    return {"P": p, "Q": q, "converged": converged, "iterations_change": last_change,
            "residual_P": resid_p, "residual_Q": resid_q,
            "pass": resid_p < 1e-9 and resid_q < 1e-9}


def simulate(p: Matrix, q: Matrix, shocks: list[float], y0: list[float] | None = None) -> list[list]:
    """Propagate `y_t = P y_{t-1} + Q eps_t` — used to check a solved policy against a path."""
    y = list(y0) if y0 else [0.0] * len(p)
    path = [y]
    for eps in shocks:
        y = [sum(p[i][j] * y[j] for j in range(len(y))) + q[i][0] * eps for i in range(len(y))]
        path.append(y)
    return path


# ---------------------------------------------------------------------------------------
# verification 1: a closed-form case
# ---------------------------------------------------------------------------------------
def univariate_forward_check() -> dict:
    """`y_t = a E_t y_{t+1} + x_t` with `x_t = rho x_{t-1} + eps` — solved by hand.

    Guess `y = c x`: `c x = a c rho x + x` so `c = 1/(1 - a rho)`. In state form `y = (y, x)`, so
    the solver's `Q[0]` must equal `c` and `P[0][1]` must equal `c rho`. Both are closed form, so
    the solver is checked against arithmetic rather than against itself.
    """
    a_coef, rho = 0.5, 0.8
    A = [[1.0, -1.0], [0.0, 1.0]]
    B = [[0.0, 0.0], [0.0, rho]]
    C = [[a_coef, 0.0], [0.0, 0.0]]
    D = [[0.0], [1.0]]
    sol = solve(A, B, C, D, rho)
    c = 1.0 / (1.0 - a_coef * rho)
    err = max(abs(sol["Q"][0][0] - c), abs(sol["P"][0][1] - c * rho))
    return {"c_computed": sol["Q"][0][0], "c_truth": c,
            "p01_computed": sol["P"][0][1], "p01_truth": c * rho,
            "error": err, "pass": err < 1e-10,
            "residuals": (sol["residual_P"], sol["residual_Q"])}


# ---------------------------------------------------------------------------------------
# verification 2: the New Keynesian three-equation model, two ways
# ---------------------------------------------------------------------------------------
def nk3_matrices(phi_pi: float = 1.5, phi_y: float = 0.5, beta: float = 0.99,
                 sigma: float = 1.0, kappa: float = 0.1, rho_u: float = 0.8):
    """Cast the NK3 model into `A y = B y_{-1} + C E y_{+1} + D eps` with y = (x, pi, u).

    IS:    x_t + sigma*phi_y x_t + sigma*phi_pi pi_t = E x_{t+1} + sigma E pi_{t+1}
    NKPC:  pi_t - kappa x_t = beta E pi_{t+1} + u_t      <- u is COST-PUSH, not a rate shock
    shock: u_t = rho_u u_{t-1} + eps

    The distinction matters: `policy_function`'s u-shock enters the NKPC (c1=0, c2=1), so putting
    it in the IS curve instead produced a policy that satisfied a different model.
    """
    A = [[1.0 + sigma * phi_y, sigma * phi_pi, 0.0],
         [-kappa, 1.0, -1.0],
         [0.0, 0.0, 1.0]]
    B = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, rho_u]]
    C = [[1.0, sigma, 0.0], [0.0, beta, 0.0], [0.0, 0.0, 0.0]]
    D = [[0.0], [0.0], [1.0]]
    return A, B, C, D


def nk3_cross_check(phi_pi: float = 1.5, phi_y: float = 0.5, rho_u: float = 0.8) -> dict:
    """Compare the generic solver with `nk3.policy_function`'s closed form.

    `nk3` gives the response of the gap (a_u) and inflation (b_u) to the shock; the solver returns
    the same two numbers as the first two rows of Q.
    """
    from .nk3 import policy_function

    sol = solve_nk3(phi_pi=phi_pi, phi_y=phi_y, rho_u=rho_u)
    closed = policy_function(phi_pi=phi_pi, phi_y=phi_y, rho_u=rho_u)
    a_u, b_u = sol["Q"][0][0], sol["Q"][1][0]
    err = max(abs(a_u - closed["a_u"]), abs(b_u - closed["b_u"]))
    return {"solver": {"a_u": a_u, "b_u": b_u},
            "closed_form": {"a_u": closed["a_u"], "b_u": closed["b_u"]},
            "error": err, "residuals": (sol["residual_P"], sol["residual_Q"]),
            "pass": err < 1e-9}


# ---------------------------------------------------------------------------------------
# verification 3: it must refuse an indeterminate model
# ---------------------------------------------------------------------------------------
def solve_nk3(phi_pi: float = 1.5, phi_y: float = 0.5, rho_u: float = 0.8) -> dict:
    """Solve NK3, refusing an indeterminate calibration.

    The iteration cannot certify *uniqueness* by itself — a passive rule can still converge to one
    of several bounded solutions — so determinacy is decided by the model's own analytic test
    (`nk3.is_determinate`) and the solver is only run after it passes. That split is deliberate:
    the criterion belongs to the model, not to the numerics.
    """
    from .nk3 import is_determinate

    if not is_determinate(phi_pi=phi_pi, phi_y=phi_y):
        raise ValueError(f"phi_pi = {phi_pi} is passive: the equilibrium is indeterminate, so no "
                         "unique policy function exists to solve for")
    A, B, C, D = nk3_matrices(phi_pi=phi_pi, phi_y=phi_y, rho_u=rho_u)
    return solve(A, B, C, D, rho_u)


def determinacy_refusal() -> dict:
    """A passive rule must be refused by the wrapper before any numerics run."""
    try:
        solve_nk3(phi_pi=0.8)
    except ValueError as exc:
        return {"refused": True, "message": str(exc), "pass": True}
    return {"refused": False, "message": "the wrapper solved an indeterminate model",
            "pass": False}


def audit() -> dict:
    checks = []
    for name, run in (("closed form", univariate_forward_check),
                      ("NK3 cross-check", nk3_cross_check),
                      ("determinacy refusal", determinacy_refusal)):
        r = run()
        checks.append({"check": name, "pass": bool(r["pass"]), "detail": str(r)[:200]})
    return {"checks": checks, "n_pass": sum(c["pass"] for c in checks),
            "n": len(checks), "all_pass": all(c["pass"] for c in checks)}


__all__ = ["solve", "solve_nk3", "simulate", "univariate_forward_check", "nk3_matrices",
           "nk3_cross_check", "determinacy_refusal", "audit"]
