"""Smets–Wouters (2007) — the published record, the derivations, and the mismatch.

The workhorse US DSGE. Unlike the NK three-equation model this one is *estimated*, and
its exact content is a long list of equilibrium conditions; what this module does is
narrower and checkable: it records the **published posterior estimates** verbatim with
provenance, re-derives the quantities the paper reports only in prose, and puts the two
of them in tension — so any transcription error shows up as a failed consistency check
rather than as a silently wrong number downstream.

Source (fetched, not recalled): Smets & Wouters, *Shocks and Frictions in US Business
Cycles: A Bayesian DSGE Approach*, ECB Working Paper No. 722 (February 2007) — the same
paper as AER 97(3). Structural parameters: Table 1a, p. 34. Shocks: Table 1b, p. 35.
Out-of-sample record: Table 3, p. 37. Policy rule: eq. (23), p. 52.

What is re-derived here, and checked against the paper's own prose:

- ``beta`` from the reported ``100(1/beta - 1) = 0.16`` per quarter;
- the *detrended* discount factor ``beta_tilde = beta * gamma**(-sigma_c)`` (growth
  γ = 0.43% per quarter, risk aversion σ_c = 1.38);
- the implied real rate — the paper says "about 3% on an annual basis";
- the implied nominal rate via Fisher — the paper says "about 6%";
- the Calvo slope ``kappa = (1-xi_p)(1 - beta_tilde*xi_p)/xi_p`` from the published
  price-stickiness estimate;
- the Taylor-principle boundary at the published output response (r_y = 0.08) and the
  margin of the published inflation response (r_pi = 2.04).

**The honest mismatch this module records.** The roster's own narrative said the
workhorse "fails to beat a VAR out of sample" (Gürkaynak–Kısacıkoğlu–Rossi). SW's own
Table 3 says the opposite for *their* model: against a VAR(1) over 1990:1–2004:4 the
DSGE gains +3.06 (1q) to +13.51 (12q) on the overall measure. What that table does
**not** contain is the no-change (random-walk) null — so the Meese–Rogoff question is
still open, and that is exactly what the vintage slice has to run.

Pure stdlib; no data, no estimation.
"""
from __future__ import annotations

from . import nk3

#: Posterior means, Table 1a (p. 34). Names follow the paper's notation; the mapping to
#: this module's symbols is in ``SYMBOL``.
PUBLISHED_STRUCTURAL: dict[str, float] = {
    "phi": 5.74,        # capital-utilisation elasticity
    "sigma_c": 1.38,    # risk aversion / inverse intertemporal elasticity
    "h": 0.71,          # external habit
    "xi_w": 0.70,       # Calvo wage stickiness
    "sigma_l": 1.83,    # inverse Frisch elasticity
    "xi_p": 0.66,       # Calvo price stickiness
    "iota_w": 0.58,     # wage indexation
    "iota_p": 0.24,     # price indexation
    "psi": 0.54,        # fixed-cost share
    "Phi": 1.60,        # investment-adjustment-cost elasticity
    "r_pi": 2.04,       # policy response to inflation (long run)
    "rho": 0.81,        # interest-rate smoothing
    "r_y": 0.08,        # policy response to the output gap
    "r_dy": 0.22,       # policy response to output growth
    "pi_bar": 0.78,     # steady-state inflation, % per quarter
    "tau": 0.16,        # 100(1/beta - 1), % per quarter
    "L_bar": 0.53,      # steady-state hours
    "gamma": 0.43,      # trend growth, % per quarter
    "alpha": 0.19,      # capital share
}

#: Posterior means of the shock processes, Table 1b (p. 35) — recorded for provenance,
#: not used by the derivations below.
PUBLISHED_SHOCKS: dict[str, float] = {
    "sigma_a": 0.45, "sigma_b": 0.23, "sigma_g": 0.53, "sigma_I": 0.45,
    "sigma_r": 0.24, "sigma_p": 0.14, "sigma_w": 0.24,
    "rho_a": 0.95, "rho_b": 0.22, "rho_g": 0.97, "rho_I": 0.71,
    "rho_r": 0.15, "rho_p": 0.89, "rho_w": 0.96,
    "mu_p": 0.69, "mu_w": 0.84, "rho_ga": 0.52,
}

SOURCE = (
    "Smets & Wouters (2007), ECB Working Paper 722 (Feb 2007); "
    "= AER 97(3). Tables 1a/1b pp. 34-35, Table 3 p. 37, policy rule eq. 23 p. 52."
)

#: The paper's own prose statements, which the derivations are checked against.
PAPER_SAYS = {"real_rate_annual_pct": 3.0, "nominal_rate_annual_pct": 6.0,
              "inflation_annual_pct": 3.0}

#: The model's observation set — Table 3's columns are the same seven series.
OBSERVABLES = (
    "GDP", "consumption", "investment", "hours", "wages", "inflation", "federal funds",
)


def beta() -> float:
    """``beta`` from the reported ``100(1/beta - 1) = 0.16`` per quarter."""
    return 1.0 / (1.0 + PUBLISHED_STRUCTURAL["tau"] / 100.0)


def gamma() -> float:
    """Gross trend growth per quarter (0.43% net)."""
    return 1.0 + PUBLISHED_STRUCTURAL["gamma"] / 100.0


def beta_tilde() -> float:
    """The detrended discount factor, ``beta * gamma**(-sigma_c)``."""
    p = PUBLISHED_STRUCTURAL
    return beta() * gamma() ** (-p["sigma_c"])


def real_rate_annual_pct() -> float:
    """The steady-state real rate the published parameters imply, % per year."""
    return 400.0 * (1.0 / beta_tilde() - 1.0)


def inflation_annual_pct() -> float:
    return 400.0 * PUBLISHED_STRUCTURAL["pi_bar"] / 100.0


def nominal_rate_annual_pct() -> float:
    """Fisher: nominal = real + expected inflation (quarterly rates, annualised)."""
    return 400.0 * ((1.0 / beta_tilde() - 1.0) + PUBLISHED_STRUCTURAL["pi_bar"] / 100.0)


def calvo_kappa() -> float:
    """The Calvo NKPC slope implied by the published price stickiness:

        kappa = (1 - xi_p)(1 - beta_tilde * xi_p) / xi_p
    """
    xi = PUBLISHED_STRUCTURAL["xi_p"]
    return (1.0 - xi) * (1.0 - beta_tilde() * xi) / xi


def determinacy() -> dict:
    """Does the *published* policy rule satisfy the Taylor principle?

    Checked on the three-equation reduction (``nk3``), at the published output response
    ``r_y`` and the Calvo-implied slope. Two things are deliberately outside this
    reduction and are listed rather than buried: the ``r_dy = 0.22`` growth term, and
    the ``rho = 0.81`` smoothing (which weakens the contemporaneous response to
    ``(1 - rho) * r_pi = 0.39`` while leaving the long-run response at 2.04).
    """
    boundary = nk3.taylor_boundary(PUBLISHED_STRUCTURAL["r_y"], beta_tilde(), calvo_kappa())
    margin = nk3.determinacy_margin(
        PUBLISHED_STRUCTURAL["r_pi"], PUBLISHED_STRUCTURAL["r_y"],
        beta_tilde(), nk3.SIGMA, calvo_kappa(),
    )
    return {
        "boundary": boundary,
        "margin": margin,
        "determinate": margin > 0.0,
        "r_pi": PUBLISHED_STRUCTURAL["r_pi"],
        "contemporaneous_response": (1.0 - PUBLISHED_STRUCTURAL["rho"]) * PUBLISHED_STRUCTURAL["r_pi"],
        "scope": "3-equation reduction; excludes r_dy and smoothing",
    }


# --- the paper's own out-of-sample table (Table 3, p. 37) --------------------
#: Percentage RMSE gains (+) / losses (-) against a VAR(1) model, 1990:1-2004:4.
PUBLISHED_OUT_OF_SAMPLE = {
    "DSGE": {1: 3.06, 2: 2.82, 4: 6.82, 8: 11.50, 12: 13.51},
    "BVAR(4)": {1: 3.25, 2: 0.17, 4: 0.51, 8: -4.10, 12: -9.84},
}
#: The benchmark SW compare against is a VAR(1) — **not** a no-change forecast.
PUBLISHED_BENCHMARK = "VAR(1)"
PUBLISHED_NO_CHANGE_NULL = False


def out_of_sample_vs_random_walk() -> dict:
    """What the field's best-known out-of-sample table does *not* contain.

    SW report gains against VAR(1) and BVAR(4) only. A no-change (random-walk) null is
    absent, so the Meese–Rogoff question — does the model beat "tomorrow equals today" —
    is untested there. This function returns that finding as data instead of a slogan.
    """
    return {
        "source": "Table 3, p. 37",
        "benchmark": PUBLISHED_BENCHMARK,
        "random_walk_present": PUBLISHED_NO_CHANGE_NULL,
        "dsge_beats_var1_at_every_horizon": all(
            v > 0 for v in PUBLISHED_OUT_OF_SAMPLE["DSGE"].values()
        ),
    }


# --- guards ------------------------------------------------------------------


def guard_provenance_consistency(
    tol_pp: float = 0.5,
) -> tuple[bool, str]:
    """The derived real/nominal/inflation rates must reproduce what the paper itself
    reports in prose (about 3%, 6%, 3% annual). A transcription error in the parameter
    record breaks this — which is the point: the record is checked against the source,
    not trusted."""
    real, nom, infl = real_rate_annual_pct(), nominal_rate_annual_pct(), inflation_annual_pct()
    worst = max(
        abs(real - PAPER_SAYS["real_rate_annual_pct"]),
        abs(nom - PAPER_SAYS["nominal_rate_annual_pct"]),
        abs(infl - PAPER_SAYS["inflation_annual_pct"]),
    )
    ok = worst <= tol_pp
    return ok, (
        f"provenance: real={real:.2f}% nominal={nom:.2f}% inflation={infl:.2f}% "
        f"(paper says ~3/~6/~3); worst gap {worst:.2f}pp (tol {tol_pp})"
    )


def guard_determinacy(
    r_pi: float | None = None, r_y: float | None = None, tol: float = 1e-9,
) -> tuple[bool, str]:
    """The published rule must sit in the determinate region. Fails on a passive rule —
    the seeded fault this guard exists to catch (a rule with r_pi below the boundary)."""
    d = determinacy()
    r_pi = d["r_pi"] if r_pi is None else r_pi
    bound = d["boundary"] if r_y is None else nk3.taylor_boundary(
        r_y, beta_tilde(), calvo_kappa()
    )
    ok = r_pi > bound - tol
    return ok, (
        f"determinacy: r_pi={r_pi:.4f} vs boundary {bound:.4f} "
        f"(margin {d['margin']:+.4f}) — {'determinate' if ok else 'INDETERMINATE'}"
    )


def guard_observation_set() -> tuple[bool, str]:
    """The model's m is seven series, and the published table has seven columns. A
    record that claims a different count has drifted from the source."""
    ok = len(OBSERVABLES) == 7
    return ok, f"observation set: {len(OBSERVABLES)} series (published table has 7)"


#: The paper reports its seven observed series fitted in-sample. That is the *backcast*
#: tier; it is not a validation out of sample, and it is recorded here as published.
IN_SAMPLE_VALIDATED = 7


def deficit(delta_e: float = 0.025):
    """Two-tier deficit for the workhorse: ``(ceiling, out_of_sample)``.

    Ceiling — seven observables, all validated: radius 0.513 at ``delta_e=0.025`` (a 1%
    certificate needs m ~ 18,000). The model cannot do better than seven.

    Out of sample — what is validated against a *measured future* with a no-change
    null: zero. The paper's Table 3 benchmarks a VAR(1), not the null, so the
    Meese–Rogoff question is not answered there.
    """
    from ..deficit import DeficitObservable, deficit_report

    ceiling = tuple(DeficitObservable(n, True, True, True) for n in OBSERVABLES)
    oos = tuple(DeficitObservable(n, False, True, False) for n in OBSERVABLES)
    return deficit_report(ceiling, delta_e), deficit_report(oos, delta_e)


def summary(delta_e: float = 0.025) -> str:
    d = determinacy()
    ceiling, oos = deficit(delta_e)
    oos_rec = out_of_sample_vs_random_walk()
    return "\n".join(
        [
            "SMETS-WOUTERS (2007) — published record, re-derived",
            "=" * 60,
            f"beta          = {beta():.8f}   (from 100(1/beta-1)=0.16 %/q)",
            f"beta_tilde    = {beta_tilde():.8f}   (detrended: beta*gamma^-sigma_c)",
            f"implied real  = {real_rate_annual_pct():.3f} %/yr  (paper: about 3%)",
            f"implied nom.  = {nominal_rate_annual_pct():.3f} %/yr  (paper: about 6%)",
            f"Calvo kappa   = {calvo_kappa():.6f}   (from xi_p=0.66)",
            f"Taylor bound. = {d['boundary']:.6f} at r_y=0.08; published r_pi={d['r_pi']:.2f}"
            f" -> {'determinate' if d['determinate'] else 'INDETERMINATE'} "
            f"(margin {d['margin']:+.4f})",
            "",
            f"deficit ceiling   m={ceiling.n_validation} of {ceiling.n_observables} "
            f"-> radius {ceiling.radius:.3f} at delta_e={delta_e}",
            f"validated in-sample  m={IN_SAMPLE_VALIDATED} (as published; backcast, not a forecast)",
            f"validated out-of-sample vs no-change  m={oos.n_validation}"
            f" -> {'VACUOUS' if oos.vacuous else f'{oos.radius:.3f}'}",
            "",
            f"published benchmark is {oos_rec['benchmark']}, not a random walk: "
            f"SW's own table shows the DSGE beating it at every horizon.",
            "The Meese-Rogoff null is still untested there — that is the next slice.",
        ]
    )


if __name__ == "__main__":
    print(summary())
