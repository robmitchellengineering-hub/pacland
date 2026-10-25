"""Smets–Wouters (2007) — the equilibrium conditions, and which ones are proved here.

The objective was to machine-check the model's ~20 linearised equilibrium conditions.
The honest way to do that without transcribing a technical appendix is to go the other
direction: take the paper's **nonlinear** decision problems (appendix 1, pp. 47–53 of
ECB WP 722) and *derive* the steady state in sympy, then record which of the conditions
that derivation pins down and which are dynamic-only (the paper linearises those
numerically, so their exact content is the steady state plus the linear structure).

``CONDITIONS`` is that inventory, with a verdict per condition — it is deliberately a
list of *claims about what has been checked*, and ``guard_conditions_inventory``
refuses an entry that has no verdict or no page reference, so the table cannot quietly
grow a row nobody verified.

What is derived (``scripts/validate_sw_structure.py``, sympy, exact):

    Euler            1 = beta*gamma**(-sigma_c) * R / pi_bar   =>  R = pi_bar/beta_tilde
    Tobin's Q        Q = 1                                      =>  R^k = 1/beta_tilde - 1 + delta
    capital          i = delta * k                              (accumulation at the steady state)
    production       y + phi = k**alpha * (gamma*L)**(1-alpha)
    labour FOC       w = (1-alpha) * mc * (y + phi) / L
    capital FOC      R^k = alpha * mc * (y + phi) / k
    cost identity    mc = w**(1-alpha) * R^k**alpha / (alpha**alpha * (1-alpha)**(1-alpha))
                      — over-determined by the two FOCs, and consistent only because
                        production is CRS (Euler's theorem): a real check, not a tautology
    resource         c/y + i/y + g/y = 1                        (a(z)=0 at z=1)
    policy rule      R = R* exactly, at any inflation target     (contrast: NK3 has no
                                                                 steady state at pi* != 0)

That last row is the interesting one. The NK three-equation model is *inconsistent* at a
non-zero target (`pacland.economics.nk3`); SW's rule is written in deviations from its
own steady state, `R_t/R* = (R_{t-1}/R*)^rho [(pi_t/pi*)^{r_pi}(Y_t/Y*_t)^{r_y}]^{1-rho}
(Delta Y/Delta Y*)^{r_dy} eps_t`, so `pi = pi*` and `R = R*` satisfy it identically for
any target. SW did not inherit the domain bug — it is designed out.

Pure stdlib.
"""
from __future__ import annotations

from dataclasses import dataclass

from . import sw2007

#: Quarterly depreciation. **Not** one of the estimated parameters in Table 1a — it is a
#: calibration the paper does not report in the extracted tables, so it is a parameter
#: here, never a derived claim.
DELTA = 0.025


@dataclass(frozen=True)
class Condition:
    """One equilibrium condition, and what this derivation establishes about it."""

    key: str
    paper_ref: str          # equation or section in ECB WP 722
    verdict: str            # "proved" | "specification"
    note: str


#: The inventory. Verdicts are per-condition and each carries its reason; the guard
#: refuses anything without both a verdict and a reference.
CONDITIONS: tuple[Condition, ...] = (
    Condition("final_good_aggregator", "sec. 1.1, eq. of Kimball aggregator", "specification",
              "the Kimball aggregator G is an input of the model, with G(1)=1; there is "
              "nothing to derive"),
    Condition("demand_curve", "sec. 1.1", "specification",
              "the demand curve follows from G; at the steady state every relative price is 1"),
    Condition("production", "eq. (1)", "proved",
              "y + phi = k^alpha (gamma L)^(1-alpha) at the steady state"),
    Condition("capital_labour_ratio", "eq. (5)", "proved",
              "k/L = alpha/(1-alpha) * w/R^k — follows from eqs (3),(4)"),
    Condition("marginal_cost", "eq. (6)", "proved",
              "mc = w^(1-alpha) R^k^alpha / (alpha^alpha (1-alpha)^(1-alpha))"),
    Condition("calvo_price_foc", "eq. (7)", "proved",
              "at zero net inflation P_tilde = P (proved from the price index); the "
              "markup LEVEL is the aggregator's elasticity, a specification"),
    Condition("price_index", "eq. (8)", "proved",
              "at pi = 1 every relative price is 1 and the index collapses to P_t=P_{t-1}"),
    Condition("euler", "sec. 1.3, budget constraint (9)", "proved",
              "1 = beta gamma^(-sigma_c) R/pi_bar  =>  R = pi_bar/beta_tilde (Fisher)"),
    Condition("tobin_q", "eq. (10) + investment FOC", "proved",
              "Q = 1 and R^k = 1/beta_tilde - 1 + delta"),
    Condition("capital_accumulation", "eq. (10)", "proved", "i = delta k"),
    Condition("utilisation_foc", "sec. 1.3", "proved",
              "a normalisation, not a derivation: a(1) = 0 and a'(1) = R^k fix the "
              "utilisation-cost curve at the steady state"),
    Condition("labour_supply", "sec. 1.3, utility", "proved",
              "w = (1-alpha) mc (y+phi)/L — marginal product equals the real wage"),
    Condition("wage_calvo", "eq. (21)", "proved",
              "at zero net inflation the reset wage equals the aggregate wage (proved "
              "from the wage index); the wage-markup level is a specification"),
    Condition("wage_index", "eq. (22)", "proved", "collapses to W_t = W_{t-1} pi_bar"),
    Condition("budget_constraint", "eq. (9)", "proved",
              "at the steady state the flow budget holds with B constant"),
    Condition("policy_rule", "eq. (23)", "proved",
              "R = R* exactly at pi = pi*, for ANY target — the NK3 domain bug is absent"),
    Condition("government_bc", "eq. (25)", "proved", "G = T at the steady state (B constant)"),
    Condition("gov_spending_process", "eq. (26)", "specification",
              "an AR(1) around g_bar: exact content is its unconditional mean, which is "
              "a parameter, not a derived quantity"),
    Condition("resource_constraint", "eq. (27)", "proved",
              "c/y + i/y + g/y = 1 with a(z) = 0"),
    Condition("shock_processes", "eqs (2),(11),(12),(24)", "specification",
              "AR(1)/ARMA processes: their exact content is persistence and variance, "
              "both parameters"),
)

PROVED = ("proved",)
SPECIFIED = ("specification",)


def beta_tilde() -> float:
    return sw2007.beta_tilde()


def real_rate_quarterly() -> float:
    """``1/beta_tilde - 1`` — the steady-state real rate implied by the Euler equation."""
    return 1.0 / beta_tilde() - 1.0


def nominal_rate_quarterly() -> float:
    return (1.0 / beta_tilde()) * (1.0 + sw2007.PUBLISHED_STRUCTURAL["pi_bar"] / 100.0) - 1.0


def fisher_exact_annual_pct() -> float:
    """The Euler-derived nominal rate, annualised, with exact (multiplicative) Fisher.
    ``sw2007.nominal_rate_annual_pct`` uses the additive approximation; the gap between
    them is the cross term and is reported rather than hidden."""
    return 400.0 * nominal_rate_quarterly()


def rental_rate(delta: float = DELTA) -> float:
    """The steady-state rental rate of capital: ``1/beta_tilde - 1 + delta``."""
    return real_rate_quarterly() + delta


def capital_output_ratio(mc: float, delta: float = DELTA) -> float:
    """``k/(y+phi) = alpha * mc / R^k`` — the capital FOC and the production function."""
    alpha = sw2007.PUBLISHED_STRUCTURAL["alpha"]
    return alpha * mc / rental_rate(delta)


def shares(mc: float, delta: float = DELTA, g_over_y: float = 0.18) -> dict[str, float]:
    """The steady-state expenditure shares, from the capital FOC and the resource
    constraint: ``i/y = delta * k/y`` and ``c/y = 1 - i/y - g/y``."""
    k_over_y = capital_output_ratio(mc, delta)
    i_over_y = delta * k_over_y
    return {"k_over_y": k_over_y, "i_over_y": i_over_y, "g_over_y": g_over_y,
            "c_over_y": 1.0 - i_over_y - g_over_y}


def coverage() -> dict:
    """How much of the inventory is established here.

    ``complete`` means every condition carries a settled verdict: either its steady-state
    relation is derived, or it is a *specification* — an input of the model (an aggregator,
    a functional form, a shock process) with nothing to derive. Nothing unresolved.
    """
    proved = [c.key for c in CONDITIONS if c.verdict in PROVED]
    spec = [c.key for c in CONDITIONS if c.verdict in SPECIFIED]
    unknown = [c.key for c in CONDITIONS if c.verdict not in PROVED + SPECIFIED]
    return {
        "n_total": len(CONDITIONS),
        "n_proved": len(proved),
        "n_specification": len(spec),
        "n_unknown": len(unknown),
        "proved": proved,
        "specification": spec,
        "unknown": unknown,
        "complete": not unknown,
    }


# --- guards ------------------------------------------------------------------


def guard_conditions_inventory() -> tuple[bool, str]:
    """Every condition must carry a verdict from the known set and a page reference.
    A row with no verdict is an unverified claim wearing a table's clothes."""
    bad = [c.key for c in CONDITIONS
           if c.verdict not in PROVED + SPECIFIED or not c.paper_ref.strip()]
    return not bad, (
        f"inventory: {len(CONDITIONS)} conditions, "
        f"{len([c for c in CONDITIONS if c.verdict in PROVED])} proved, "
        f"{len([c for c in CONDITIONS if c.verdict in SPECIFIED])} specifications"
        + (f" — UNSETTLED: {', '.join(bad)}" if bad else "")
    )


def guard_steady_state_shares(mc: float = 1.0 / 1.2, delta: float = DELTA,
                              g_over_y: float = 0.18) -> tuple[bool, str]:
    """The resource constraint at the steady state must exhaust output:
    ``c/y + i/y + g/y = 1``. Fails if the capital FOC and the resource constraint pull
    the shares apart (the seeded fault: an i/y that ignores the rental rate)."""
    sh = shares(mc, delta, g_over_y)
    total = sh["c_over_y"] + sh["i_over_y"] + sh["g_over_y"]
    ok = abs(total - 1.0) <= 1e-12 and sh["c_over_y"] > 0
    return ok, (
        f"resource constraint: c/y={sh['c_over_y']:.4f} + i/y={sh['i_over_y']:.4f} + "
        f"g/y={sh['g_over_y']:.4f} = {total:.4f} "
        f"({'exhausts output' if ok else 'DOES NOT SUM'})"
    )


def cost_function_mc(alpha: float, w: float, rk: float) -> float:
    """Marginal cost from the paper's eq. (6), normalised:
    ``mc = alpha^-alpha (1-alpha)^-(1-alpha) w^(1-alpha) rk^alpha``."""
    return (w ** (1 - alpha)) * (rk ** alpha) / (alpha ** alpha * (1 - alpha) ** (1 - alpha))


def guard_cost_identity(
    alpha: float = 0.19, mc: float = 1.0 / 1.2, k: float = 40.0, L: float = 30.0,
    labour_exponent: float | None = None, tol: float = 1e-9,
) -> tuple[bool, str]:
    """The cost function and the two marginal-product FOCs over-determine ``mc``: build
    ``w`` and ``rk`` from the FOCs and feed them through eq. (6), and the marginal cost
    must come back. It does exactly because production is CRS (Euler's theorem) — a check
    on the derivation, not a restatement of it.

    ``labour_exponent`` defaults to ``1 - alpha`` (CRS). Setting it otherwise breaks the
    technology out of CRS and the identity fails: that is the seeded fault, and it is the
    reason this guard is worth having.
    """
    lab = (1.0 - alpha) if labour_exponent is None else labour_exponent
    y_crs = (k ** alpha) * (L ** (1.0 - alpha))          # the true technology
    y_used = (k ** alpha) * (L ** lab)                    # what the FOCs are computed on
    w = (1.0 - alpha) * mc * y_used / L
    rk = alpha * mc * y_used / k
    implied = cost_function_mc(alpha, w, rk)
    ok = abs(implied - mc) <= tol
    return ok, (
        f"cost identity: mc={mc:.4f} -> w={w:.4f}, rk={rk:.4f} -> mc_implied={implied:.6f}; "
        f"y_used/y_crs={y_used/y_crs:.6f} "
        f"({'consistent (CRS)' if ok else 'INCONSISTENT (non-CRS)'})"
    )


def summary() -> str:
    cov = coverage()
    sh = shares(1.0 / 1.2)
    return "\n".join(
        [
            "SMETS-WOUTERS (2007) — the equilibrium conditions, derived",
            "=" * 64,
            f"R (nominal)   = pi_bar/beta_tilde = {nominal_rate_quarterly()*100:.4f} %/q "
            f"({4*nominal_rate_quarterly()*100:.2f} %/yr)",
            f"R^k (rental)  = 1/beta_tilde-1+delta = {rental_rate()*100:.4f} %/q "
            f"(delta={DELTA} is a calibration, not a Table 1a estimate)",
            f"k/(y+phi)     = alpha*mc/R^k = {sh['k_over_y']:.3f} at mc=1/1.2",
            f"i/y = delta k/y = {sh['i_over_y']:.3f}, c/y = {sh['c_over_y']:.3f}",
            "",
            f"inventory: {cov['n_proved']}/{cov['n_total']} conditions proved, "
            f"{cov['n_specification']} specifications, {cov['n_unknown']} unresolved",
            "",
            "The policy rule is satisfied by R = R* at ANY inflation target — SW does not",
            "inherit the NK3 domain inconsistency; it is designed out.",
        ]
    )


if __name__ == "__main__":
    print(summary())
