"""Economics falsification guards — the accounting guard-suite (item #3).

Mirrors ``pacland.climate.guards`` and ``pacland.drugs.guards``: each guard asserts one
accounting invariant a macroeconomic model's output must satisfy, under the Valiant
Verification discipline — a violation fails LOUDLY, and each guard has a seeded-fault
mutation test proving it goes red on the fault it exists to catch.

These are the *constraint-first* half: national-accounting identities hold by
construction (double-entry bookkeeping), so they are the reliable content a model
FORBIDS being violated — as opposed to the free values it forecasts. The field already
imposes accounting consistency informally (national accounts, Godley–Lavoie stock-flow
consistency); this wraps it as a pass/fail, mutation-tested guard-suite.

Pure stdlib; no data, no estimation.
"""
from __future__ import annotations


def guard_circular_flow(
    income: float, expenditure: float, output: float, tol: float = 1e-6
) -> tuple[bool, str]:
    """National-accounts identity: total income ≡ total expenditure ≡ total output
    (GDP measured three ways must agree — the circular flow). Fails on a model that
    leaks flow (value appears or vanishes)."""
    resid = max(
        abs(income - expenditure),
        abs(income - output),
        abs(expenditure - output),
    )
    ok = resid <= tol
    return ok, f"circular-flow max-residual={resid:+.3e} (tol {tol})"


def guard_sectoral_balances(
    private_balance: float, government_balance: float, foreign_balance: float,
    tol: float = 1e-6,
) -> tuple[bool, str]:
    """Sectoral-balances identity: (S−I) + (T−G) + (M−X) = 0. The private, government
    and foreign sector balances must sum to zero — a surplus in one sector is, by
    construction, a deficit elsewhere. Fails on a model whose sectors do not sum."""
    resid = private_balance + government_balance + foreign_balance
    ok = abs(resid) <= tol
    return ok, f"sectoral-balance residual={resid:+.3e} (tol {tol})"


def guard_stock_flow(
    d_stock: float, flow: float, tol: float = 1e-6
) -> tuple[bool, str]:
    """Stock-flow consistency: the change in every stock equals the matching flow
    (ΔDebt = deficit, ΔWealth = saving, ΔMoney = money issuance). Fails on a model
    that moves a stock without the flow that produces it — the Godley–Lavoie criterion."""
    resid = d_stock - flow
    ok = abs(resid) <= tol
    return ok, f"stock-flow residual={resid:+.3e} (tol {tol})"


def guard_budget_constraint(
    expenditure: float, income: float, net_borrowing: float, tol: float = 1e-6
) -> tuple[bool, str]:
    """Forbidden-state guard: an agent cannot spend more than its income plus net
    borrowing (expenditure ≤ income + net_borrowing). Fails on a model that lets an
    agent spend money it does not have — the single-agent budget constraint."""
    excess = expenditure - income - net_borrowing
    ok = excess <= tol
    return ok, f"budget excess={excess:+.3e} (tol {tol})"


def guard_nonnegative_price(prices, tol: float = 0.0) -> tuple[bool, str]:
    """Forbidden-state guard: prices and quantities cannot be negative. The
    constraint-first analogue of ``guard_integer_flux`` / ``guard_nonnegative_specific_humidity``."""
    bad = [v for v in prices if v < -tol]
    return not bad, f"negative price/quantity at {len(bad)} point(s): {bad[:5]}"


__all__ = [
    "guard_circular_flow",
    "guard_sectoral_balances",
    "guard_stock_flow",
    "guard_budget_constraint",
    "guard_nonnegative_price",
]
