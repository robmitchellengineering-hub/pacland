"""The New Keynesian 3-equation model — its exact content, and what it forbids.

The positive control of the economics discipline. Three equations, five parameters, so
every constraint and every free parameter can be written in closed form — which is the
point: at this size a disagreement is a bug, not a judgement call.

    IS      x_t = x_{t+1} - sigma * (i_t - pi_{t+1} - r*)          (dynamic IS)
    NKPC    pi_t = beta * pi_{t+1} + kappa * x_t                   (Phillips curve)
    Taylor  i_t  = r* + pi* + phi_pi * (pi_t - pi*) + phi_y * x_t  (policy rule)

What is **exact** (proven in ``scripts/validate_economics_nk3.py``, sympy, zero
tolerance) and what is **free**:

- exact — the Fisher equation at the steady state, ``i = r* + pi``; the long-run
  Phillips relation ``x = (1 - beta)/kappa * pi``; the determinacy boundary
  ``phi_pi > 1 - (1 - beta)/kappa * phi_y``, which is **sigma-free**; and the fact
  that the only steady state this linearisation is *self-consistent* about is zero
  net inflation.
- free — ``beta`` (discounting), ``kappa`` (slope), ``sigma`` (IS), ``phi_pi``,
  ``phi_y``. None of them can move the long-run relation above; they only move the
  path and the stability region.

The uncomfortable result, and the reason this file exists: the simple NKPC is a
linearisation **about zero inflation**, so with ``beta < 1`` and ``phi_y > 0`` the
three equations have **no jointly consistent steady state at a non-zero inflation
target** — the NKPC puts the gap at ``(1-beta)/kappa * pi*`` while the Taylor rule and
the IS curve put it at zero. A central bank that targets 2% is therefore using a model
outside its own domain, and the size of the contradiction is exactly the long-run
Phillips slope. ``guard_target_consistency`` refuses the out-of-domain use instead of
silently averaging it in.

Pure stdlib (``cmath`` for the 2x2 spectrum); no data, no estimation.
"""
from __future__ import annotations

import cmath
from math import isclose

# Defaults are the textbook quarterly calibration (Clarida-Galí-Gertler / Taylor).
BETA = 0.99      # discount factor
KAPPA = 0.1      # NKPC slope
SIGMA = 1.0      # intertemporal elasticity (IS)
R_STAR = 0.005   # natural real rate, quarterly (~2% annual)
PI_STAR = 0.0    # the model's consistent target: zero net inflation (see below)


def steady_state(
    beta: float = BETA, kappa: float = KAPPA, r_star: float = R_STAR
) -> dict[str, float]:
    """The self-consistent steady state: ``pi = 0``, ``x = 0``, ``i = r*``.

    Solve the three equations with ``x = x_t = x_{t+1}`` and ``pi = pi_t = pi_{t+1}``:

    - NKPC gives ``x = (1-beta)/kappa * pi``. At ``beta < 1`` that is a *family* — the
      long-run Phillips curve is not vertical — so the steady state is pinned by domain
      (zero-inflation linearisation) rather than by the equations alone.
    - IS then gives ``i = r* + pi`` (Fisher), exactly.
    - At ``pi = 0`` the Taylor rule is satisfied with no gap and no intercept error.

    Returns ``pi``, ``x``, ``i`` and the exact real rate ``r = i - pi``.
    """
    pi = 0.0
    x = (1.0 - beta) / kappa * pi
    i = r_star + pi
    return {"pi": pi, "x": x, "i": i, "r": i - pi}


def lrpc_slope(beta: float = BETA, kappa: float = KAPPA) -> float:
    """The exact long-run Phillips slope, ``dx/dpi = (1-beta)/kappa``.

    Zero only when ``beta == 1``. Reads as: taking the linearisation literally, a
    permanent 1pp rise in inflation buys ``(1-beta)/kappa`` pp of output gap — which is
    also the size of the inconsistency with the Taylor rule, and hence the reason the
    model's domain is zero inflation.
    """
    return (1.0 - beta) / kappa


def taylor_boundary(phi_y: float = 0.0, beta: float = BETA, kappa: float = KAPPA) -> float:
    """The exact determinacy boundary in ``phi_pi``:

        phi_pi > 1 - (1 - beta)/kappa * phi_y

    Independent of ``sigma``. Reproduced by the eigenvalue search in
    :func:`determinacy_margin` to machine precision (see the validation script), so it
    is measured here, not cited.
    """
    return 1.0 - (1.0 - beta) / kappa * phi_y


def _system_matrix(phi_pi: float, phi_y: float, beta: float, sigma: float, kappa: float):
    """``z_t = M z_{t+1}`` with ``z = (x, pi)``, after substituting the Taylor rule.

    IS:     (1 + sigma*phi_y) x_t + sigma*phi_pi pi_t = x_{t+1} + sigma pi_{t+1}
    NKPC:   -kappa x_t + pi_t = beta pi_{t+1}
    """
    g0 = ((1.0 + sigma * phi_y, sigma * phi_pi), (-kappa, 1.0))
    g1 = ((1.0, sigma), (0.0, beta))
    det_g1 = g1[0][0] * g1[1][1] - g1[0][1] * g1[1][0]
    inv_g1 = (
        (g1[1][1] / det_g1, -g1[0][1] / det_g1),
        (-g1[1][0] / det_g1, g1[0][0] / det_g1),
    )
    return (
        (inv_g1[0][0] * g0[0][0] + inv_g1[0][1] * g0[1][0],
         inv_g1[0][0] * g0[0][1] + inv_g1[0][1] * g0[1][1]),
        (inv_g1[1][0] * g0[0][0] + inv_g1[1][1] * g0[1][0],
         inv_g1[1][0] * g0[0][1] + inv_g1[1][1] * g0[1][1]),
    )


def spectrum(
    phi_pi: float, phi_y: float = 0.0, beta: float = BETA,
    sigma: float = SIGMA, kappa: float = KAPPA,
) -> tuple[complex, complex]:
    """The two eigenvalues of the forward system (exact 2x2 formula)."""
    m = _system_matrix(phi_pi, phi_y, beta, sigma, kappa)
    tr = m[0][0] + m[1][1]
    det = m[0][0] * m[1][1] - m[0][1] * m[1][0]
    root = cmath.sqrt(tr * tr - 4.0 * det)
    return ((tr + root) / 2.0, (tr - root) / 2.0)


def determinacy_margin(
    phi_pi: float, phi_y: float = 0.0, beta: float = BETA,
    sigma: float = SIGMA, kappa: float = KAPPA,
) -> float:
    """``min |eigenvalue| - 1``. Positive => determinate (both roots outside the unit
    circle, no free initial condition for either jump variable)."""
    l1, l2 = spectrum(phi_pi, phi_y, beta, sigma, kappa)
    return min(abs(l1), abs(l2)) - 1.0


def is_determinate(phi_pi: float, phi_y: float = 0.0, **kw) -> bool:
    return determinacy_margin(phi_pi, phi_y, **kw) > 0.0


# ---------------------------------------------------------------------------
# The falsification guards: what the model forbids.
# ---------------------------------------------------------------------------


def guard_steady_state_admissible(
    pi: float = 0.0, x: float = 0.0, beta: float = BETA, kappa: float = KAPPA,
    tol: float = 1e-12,
) -> tuple[bool, str]:
    """The linearisation is self-consistent only about zero net inflation. A claimed
    steady state with ``pi != 0`` (and ``beta < 1``) is refused: the NKPC puts the gap
    at ``(1-beta)/kappa*pi`` *and* the Taylor rule requires it at zero — a model used
    outside its own domain.

    Green at ``pi = 0`` (and trivially at ``beta == 1``, where the long-run Phillips
    curve is vertical)."""
    if isclose(beta, 1.0, abs_tol=1e-15):
        return True, f"beta=1: long-run Phillips curve vertical, pi={pi:+.4f} admissible"
    implied = lrpc_slope(beta, kappa) * pi
    ok = abs(pi) <= tol and abs(x - implied) <= max(tol, 1e-9)
    return ok, (
        f"target-consistency: pi={pi:+.4f} with beta={beta} needs x={implied:+.3e} "
        f"(the Taylor rule requires x=0) — {'admissible' if ok else 'OUT OF DOMAIN'}"
    )


def guard_fisher(
    i: float, pi: float, r_star: float = R_STAR, tol: float = 1e-12
) -> tuple[bool, str]:
    """Fisher at the steady state: ``i = r* + pi`` exactly. Fails on a model whose
    nominal rate does not move one-for-one with expected inflation."""
    resid = i - (r_star + pi)
    ok = abs(resid) <= tol
    return ok, f"fisher residual={resid:+.3e} (tol {tol})"


def guard_superneutrality(
    pi_a: float, pi_b: float, r_a: float, r_b: float, tol: float = 1e-12
) -> tuple[bool, str]:
    """A pure nominal shift must leave the real rate unchanged (``i - pi`` invariant).
    Fails on a model with money illusion — a nominal rescaling that moves the real
    economy."""
    resid = (pi_a - pi_b) - (r_a - r_b)
    ok = abs(resid) <= tol
    return ok, f"superneutrality residual={resid:+.3e} (nominal shift moved the real rate)"


def guard_taylor_principle(
    phi_pi: float, phi_y: float = 0.0, beta: float = BETA,
    sigma: float = SIGMA, kappa: float = KAPPA, tol: float = 1e-9,
) -> tuple[bool, str]:
    """Determinacy: the policy rule must satisfy ``phi_pi > 1 - (1-beta)/kappa*phi_y``.
    Fails on a passive rule (indeterminate equilibrium — sunspots are admissible), which
    is the seeded fault this guard exists to catch."""
    boundary = taylor_boundary(phi_y, beta, kappa)
    margin = determinacy_margin(phi_pi, phi_y, beta, sigma, kappa)
    ok = margin > 0.0 and phi_pi > boundary - tol
    return ok, (
        f"taylor principle: phi_pi={phi_pi:.4f} vs boundary {boundary:.4f} "
        f"(min|eig|-1={margin:+.4f}) — {'determinate' if ok else 'INDETERMINATE'}"
    )


def guard_long_run_phillips(
    beta: float = BETA, kappa: float = KAPPA, claimed_vertical: bool = True,
    tol: float = 1e-12,
) -> tuple[bool, str]:
    """The long-run Phillips curve is vertical only when ``beta == 1``. A model (or a
    claim) that asserts a vertical LRPC at ``beta < 1`` is refused, and the exact slope
    is reported instead."""
    slope = lrpc_slope(beta, kappa)
    if claimed_vertical and abs(slope) > tol:
        return False, (
            f"long-run Phillips: claimed vertical but dx/dpi={slope:+.4e} "
            f"(= (1-beta)/kappa, zero only at beta=1)"
        )
    return True, f"long-run Phillips: dx/dpi={slope:+.4e} (consistent with the claim)"


# ---------------------------------------------------------------------------
# The deficit: what this model can be verified against, at best.
# ---------------------------------------------------------------------------

#: The model's three observables. It has no others — which is a ceiling, not a gap.
NK3_OBSERVABLES = ("output gap", "CPI inflation", "policy rate")


def deficit(delta_e: float = 0.025):
    """The two-tier deficit for this model, reusing the shared certificate machinery.

    Returns ``(ceiling, validated)``:

    - ``ceiling`` — all three observables validated at once: the **best this model can
      ever score**, because it has three observables and no more. At ``delta_e=0.025``
      that is a ~78% certificate; a 1% certificate would need m ~ 18,000.
    - ``validated`` — what is validated today: none. The model is not estimated against
      the measured series, and the prospective path has no measurement at all.
    """
    from ..deficit import DeficitObservable, deficit_report

    all_three = tuple(DeficitObservable(n, True, True, True) for n in NK3_OBSERVABLES)
    none_yet = tuple(DeficitObservable(n, True, True, False) for n in NK3_OBSERVABLES)
    return deficit_report(all_three, delta_e), deficit_report(none_yet, delta_e)


def summary(delta_e: float = 0.025) -> str:
    ceiling, validated = deficit(delta_e)
    return "\n".join(
        [
            "NEW KEYNESIAN 3-EQUATION — exact content and ceiling",
            "=" * 56,
            f"steady state    pi=0, x=0, i=r*={R_STAR}   (Fisher exact)",
            f"long-run Phillips  dx/dpi = (1-beta)/kappa = {lrpc_slope():+.4f}",
            f"determinacy boundary  phi_pi > 1 - (1-beta)/kappa*phi_y "
            f"= {taylor_boundary(0.0):+.4f} at phi_y=0",
            "",
            f"deficit ceiling  m={ceiling.n_validation} of {ceiling.n_observables} "
            f"observables -> radius {ceiling.radius:.3f} at delta_e={delta_e}",
            f"deficit today    m={validated.n_validation} validated "
            f"-> {'VACUOUS' if validated.vacuous else f'radius {validated.radius:.3f}'}",
            "",
            "The model can be verified against three series and no more; a 1% certificate",
            "would need m ~ 18,000. It has no steady state at a non-zero target.",
        ]
    )


if __name__ == "__main__":
    print(summary())
