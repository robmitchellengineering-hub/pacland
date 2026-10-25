"""The constraint set — plural, by design.

Physics gave us the *shape* of the machine, not a licence to insist on one constraint.
The landscape has a single invariant because it has a duality group and a finite-generation
theorem (Weyl's FFT); macro-finance has neither, and pretending otherwise would have been
the overclaim. What macro-finance does have is a **set** of exact constraints — the
accounting identities that hold by construction, and the model relations every admissible
solution must satisfy. This module makes that set a first-class object and asks the two
questions that matter:

1. **How many constraints do we actually have?** Not "how many did we write down" — the
   *independent* count, measured by the rank of the constraint Jacobian at a live point.
   Two constraints that are algebraically dependent are one constraint wearing two hats.
2. **Which ones bind?** A constraint the data never approaches is decoration; the ones
   with small slack are the ones doing work.

That distinction is what replaces "the one invariant": a set with a measured independent
rank, and a slack report. A discipline that needs four constraints to be accurate should
have four — and should say which four are independent.

Pure stdlib (numeric Jacobian + elimination; small and checkable).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from . import nk3, sw_structure

TOL = 1e-9


@dataclass(frozen=True)
class Constraint:
    """One constraint, with its kind, its source, and a residual function.

    ``residual(s)`` returns a number that is ~0 when an equality holds, and >0 when an
    inequality is satisfied. ``kind`` is ``identity`` (true by construction), ``model``
    (true of the model's own solution), or ``domain`` (where the model is defined).
    """

    key: str
    kind: str              # identity | model | domain
    statement: str
    source: str
    residual: Callable[[dict], float]
    inequality: bool = False
    #: A differentiable equivalent, used only by the independence Jacobian. Needed where
    #: the checker is non-smooth by design (a max(), an abs()): its central-difference
    #: gradient at the kink is zero, which would make the row look dependent.
    smooth: Callable[[dict], float] | None = None

    def gradient_residual(self, s: dict) -> float:
        return (self.smooth or self.residual)(s)


def _s(**kw) -> dict:
    """A state point with every field a constraint may need."""
    base = {
        "income": 100.0, "expenditure": 100.0, "output": 100.0,
        "private_balance": 20.0, "gov_balance": -15.0, "foreign_balance": -5.0,
        "d_stock": 3.0, "flow": 3.0,
        "spend": 100.0, "earn": 90.0, "borrow": 10.0,
        "price": 1.0, "quantity": 1.0,
        "i": 0.0204, "pi": 0.0078, "r_star": 0.0126,
        "x": 0.0, "pi_star": 0.0,
        "beta": nk3.BETA, "kappa": nk3.KAPPA,
        "phi_pi": 1.5, "phi_y": 0.5,
        "mc": 1 / 1.2, "alpha": 0.19, "delta": 0.025, "k": 40.0, "y_phi": 100.0,
        "c_over_y": 0.69, "i_over_y": 0.12, "g_over_y": 0.19,
        "k_over_y": 3.5, "rental": 0.03,
    }
    base.update(kw)
    return base


def _default_state(**overrides) -> dict:
    """A state that satisfies every constraint **by construction** — the model's own
    steady state joined to a closed set of accounts.

    Built from the same functions the models use (``nk3.lrpc_slope``,
    ``sw_structure.rental_rate``), so the set is consistent at a point that is not
    hand-tuned. If this ever stops satisfying the set, a constraint and a model have
    drifted apart — which is what ``guard_default_state_is_admissible`` is for.
    """
    beta, kappa = nk3.BETA, nk3.KAPPA
    pi = 0.0078
    mc, alpha, delta = 1 / 1.2, 0.19, sw_structure.DELTA
    rental = sw_structure.rental_rate(delta)
    k_over_y = alpha * mc / rental
    i_over_y = delta * k_over_y
    g_over_y = 0.18
    return _s(
        beta=beta if "beta" not in overrides else overrides["beta"],
        kappa=kappa if "kappa" not in overrides else overrides["kappa"],
        pi=pi,
        r_star=nk3.R_STAR, i=nk3.R_STAR + pi,
        x=nk3.lrpc_slope(overrides.get("beta", beta), overrides.get("kappa", kappa)) * pi,
        mc=mc, alpha=alpha, delta=delta, rental=rental,
        k_over_y=k_over_y, i_over_y=i_over_y, g_over_y=g_over_y,
        c_over_y=1.0 - i_over_y - g_over_y,
        **{k: v for k, v in overrides.items() if k not in ("beta", "kappa")},
    )


CONSTRAINTS: tuple[Constraint, ...] = (
    Constraint("circular_flow", "identity",
               "income = expenditure = output",
               "docs/economics-accounting-closure.md",
               lambda s: max(abs(s["income"] - s["expenditure"]),
                             abs(s["income"] - s["output"])),
               smooth=lambda s: ((s["income"] - s["expenditure"]) ** 2
                                 + (s["income"] - s["output"]) ** 2)),
    Constraint("sectoral_balances", "identity",
               "(S-I) + (T-G) + (M-X) = 0",
               "src/pacland/economics/guards.py",
               lambda s: s["private_balance"] + s["gov_balance"] + s["foreign_balance"]),
    Constraint("stock_flow", "identity",
               "change in stock = flow",
               "src/pacland/economics/guards.py",
               lambda s: s["d_stock"] - s["flow"]),
    Constraint("budget", "identity",
               "spending <= income + borrowing",
               "src/pacland/economics/guards.py",
               lambda s: s["earn"] + s["borrow"] - s["spend"],
               inequality=True),
    Constraint("nonneg_price", "domain",
               "prices and quantities are non-negative",
               "src/pacland/economics/guards.py",
               lambda s: min(s["price"], s["quantity"]),
               inequality=True),
    Constraint("fisher", "model",
               "i = r* + pi at the steady state",
               "src/pacland/economics/nk3.py",
               lambda s: s["i"] - (s["r_star"] + s["pi"])),
    Constraint("taylor_principle", "model",
               "phi_pi > 1 - (1-beta)/kappa * phi_y",
               "scripts/validate_economics_nk3.py",
               lambda s: s["phi_pi"] - nk3.taylor_boundary(s["phi_y"], s["beta"], s["kappa"]),
               inequality=True),
    Constraint("zero_inflation_domain", "domain",
               "the linearisation has no steady state at pi* != 0 (beta < 1, phi_y > 0)",
               "docs/falsifiable-predictions.md",
               lambda s: -abs(s["pi_star"]),
               smooth=lambda s: -(s["pi_star"] ** 2)),
    Constraint("lrpc", "model",
               "x = (1-beta)/kappa * pi on the long-run Phillips curve",
               "src/pacland/economics/nk3.py",
               lambda s: s["x"] - nk3.lrpc_slope(s["beta"], s["kappa"]) * s["pi"]),
    Constraint("resource_shares", "model",
               "c/y + i/y + g/y = 1",
               "src/pacland/economics/sw_structure.py",
               lambda s: s["c_over_y"] + s["i_over_y"] + s["g_over_y"] - 1.0),
    Constraint("capital_output", "model",
               "k/y = alpha * mc / R^k",
               "scripts/validate_sw_structure.py",
               lambda s: s["k_over_y"] - s["alpha"] * s["mc"] / s["rental"]),
)


def evaluate(state: dict | None = None) -> list[dict]:
    """Every constraint's residual and slack at a state point."""
    s = state or _default_state()
    out = []
    for c in CONSTRAINTS:
        r = c.residual(s)
        ok = (r >= -TOL) if c.inequality else (abs(r) <= TOL)
        out.append({"key": c.key, "kind": c.kind, "residual": r,
                    "ok": ok, "inequality": c.inequality})
    return out


def violated(state: dict | None = None) -> list[str]:
    return [row["key"] for row in evaluate(state) if not row["ok"]]


# --- independence -------------------------------------------------------------


def _variables() -> list[str]:
    """Every state field any constraint reads, discovered from the state dict."""
    return sorted(_default_state())


def _rank(rows: list[list[float]], tol: float = 1e-8) -> int:
    """Row rank by Gaussian elimination — how many constraints are independent."""
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
            if r != rank and abs(m[r][col]) > 0.0:
                f = m[r][col] / p
                for c2 in range(col, cols):
                    m[r][c2] -= f * m[rank][c2]
        rank += 1
        if rank == len(m):
            break
    return rank


def _generic(state: dict, spread: float = 0.011) -> dict:
    """A deterministic *generic* point: every field nudged off the solution.

    Rank is a property of the constraint set, not of one point, so it is measured where
    no residual is accidentally zero — the standard structural-rank convention. Without
    this, squared or max-form residuals have zero gradient at the reference state and
    look dependent when they are not.
    """
    out = {}
    for i, (k, v) in enumerate(sorted(state.items())):
        out[k] = v * (1.0 + spread * ((i % 7) - 3) / 3.0) if v else v + spread * ((i % 5) - 2)
    return out


def independence(state: dict | None = None, step: float = 1e-6) -> dict:
    """The measured independent rank of the *equality* constraints.

    Each equality constraint contributes a row: its central-difference gradient with
    respect to every state variable. Two constraints that are algebraically dependent
    produce parallel rows, and the rank says so.
    """
    s = _generic(state or _default_state())
    names = _variables()
    rows, keys = [], []
    for c in CONSTRAINTS:
        if c.inequality:
            continue
        grad = []
        for name in names:
            up, dn = dict(s), dict(s)
            up[name] = s[name] + step
            dn[name] = s[name] - step
            grad.append((c.gradient_residual(up) - c.gradient_residual(dn)) / (2 * step))
        if any(abs(g) > 1e-12 for g in grad):
            rows.append(grad)
            keys.append(c.key)
    rank = _rank(rows)
    return {"n_equality": len(rows), "rank": rank, "independent": keys,
            "dependent": len(rows) - rank}


def slack(state: dict | None = None) -> list[tuple[str, float]]:
    """Constraints sorted by how close they are to binding (smallest slack first)."""
    s = state or _default_state()
    rows = []
    for c in CONSTRAINTS:
        r = c.residual(s)
        rows.append((c.key, abs(r) if not c.inequality else r))
    return sorted(rows, key=lambda t: t[1])


# --- guards -------------------------------------------------------------------


def guard_every_constraint_sourced() -> tuple[bool, str]:
    """A constraint with no statement or no source is a claim wearing a label."""
    bad = [c.key for c in CONSTRAINTS if not c.statement.strip() or not c.source.strip()]
    return not bad, (
        f"constraint set: {len(CONSTRAINTS)} constraints, "
        f"{sum(1 for c in CONSTRAINTS if c.inequality)} inequalities"
        + (f" — UNSOURCED: {', '.join(bad)}" if bad else "")
    )


def guard_kinds_are_known() -> tuple[bool, str]:
    known = {"identity", "model", "domain"}
    bad = [c.key for c in CONSTRAINTS if c.kind not in known]
    counts = {k: sum(1 for c in CONSTRAINTS if c.kind == k) for k in sorted(known)}
    return not bad, f"kinds: {counts}" + (f" — UNKNOWN KIND: {bad}" if bad else "")


def guard_default_state_is_admissible() -> tuple[bool, str]:
    """The reference state must satisfy every constraint — otherwise the set is
    internally inconsistent and every slack number is meaningless."""
    v = violated()
    return not v, f"reference state: {'admissible' if not v else 'VIOLATES ' + ', '.join(v)}"


def summary() -> str:
    ind = independence()
    lines = [
        "THE MACRO-FINANCE CONSTRAINT SET — plural, and measured",
        "=" * 62,
        f"constraints {len(CONSTRAINTS)} · equalities {ind['n_equality']} · "
        f"independent rank {ind['rank']} · dependent {ind['dependent']}",
        "",
        "kind        key                     slack      status",
    ]
    sl = dict(slack())
    for c in CONSTRAINTS:
        val = c.residual(_default_state())
        status = "holds" if (val >= -TOL if c.inequality else abs(val) <= TOL) else "VIOLATED"
        lines.append(f"{c.kind:<11} {c.key:<23} {sl[c.key]:+10.2e}  {status}")
    lines += [
        "",
        "The independent rank is the honest count: dependent constraints are one",
        "constraint wearing two hats, and the rank test finds them instead of trusting",
        "the list.",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    print(summary())
