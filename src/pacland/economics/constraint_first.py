"""Constraint-first structure of an economy — the provable half, plus its honest limit.

This is the economics analog of the Standard-Model frontier (`docs/sm-frontier.md`), and
it follows the expansion recipe (`docs/expansion-map.md`): the *exact* statements are the
accounting identities, and everything beyond them is heuristic. Unlike the flux sector
(where Sp + the First Fundamental Theorem made "the tadpole is the unique invariant" a
theorem), economics has **no clean symmetry group**, so the parts are carefully split:

    PROVABLE (exact, by construction — no symmetry group needed):
      E1   double-entry conservation — for any flow-of-funds matrix, Σᵢ bᵢ = 0.
      E1'  uniqueness — the only value-free *linear* conservation law is total conservation.
      E2   Walras' law → relative prices only (numéraire invariance) — p·z ≡ 0 forces
           N−1 independent market-clearing conditions for N prices.

    CITED (not proved here):
      E3   Sonnenschein–Mantel–Debreu — the only restrictions on aggregate excess demand
           are Walras' law + degree-0 homogeneity, so aggregates can never *select* an
           equilibrium; the micro parameters are always needed.

    HEURISTIC (said so — expansion-map.md's caveat):
      The generalization "constraint + label exhausts the exact structure" is *not* a
      theorem for economics, exactly as "unpredicable in any UV completion" is conjectured
      (not proven) for the SM.

Everything below is exact rational arithmetic (Python ``Fraction``, zero floating point),
mirroring ``scripts/validate_sm_anomaly.py``.
"""
from __future__ import annotations

from fractions import Fraction as F


def net_balances(flows):
    """Net balance per sector from a flow-of-funds matrix.

    ``flows[i][j]`` = value paid from sector ``i`` to sector ``j`` (n×n, zero diagonal).
    Returns ``b[i] = Σⱼ flows[i][j] − Σⱼ flows[j][i]`` (total outflow − total inflow).
    """
    n = len(flows)
    b = []
    for i in range(n):
        out = sum(F(x) for x in flows[i])
        inn = sum(F(flows[j][i]) for j in range(n))
        b.append(out - inn)
    return b


def total_balance(balances):
    """Σᵢ bᵢ — identically zero for any double-entry flow matrix (E1)."""
    return sum(F(x) for x in balances)


def realize(balances):
    """Construct a flow matrix realizing a given balance vector with Σ b = 0.

    Uses a single "hub" (sector 0): surplus sectors pay the hub, deficit sectors are
    paid by the hub. Proves the realizable set of balances is *exactly* the hyperplane
    {Σ b = 0}, which is the premise of the uniqueness theorem (E1′).
    """
    n = len(balances)
    b = [F(x) for x in balances]
    flows = [[F(0)] * n for _ in range(n)]
    for i in range(1, n):
        if b[i] >= 0:
            flows[i][0] = b[i]        # i's surplus flows out to the hub
        else:
            flows[0][i] = -b[i]       # the hub covers i's deficit
    return flows


def _rref_nullspace(matrix):
    """Rational RREF and a nullspace basis of ``matrix`` (rows of Fractions).

    Returns ``(rank, basis)`` where ``basis`` is a list of nullspace vectors.
    """
    A = [[F(x) for x in row] for row in matrix]
    m = len(A)
    n = len(A[0]) if m else 0
    pivots = []
    r = 0
    for c in range(n):
        piv = next((i for i in range(r, m) if A[i][c] != 0), None)
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        inv = F(1) / A[r][c]
        A[r] = [x * inv for x in A[r]]
        for i in range(m):
            if i != r and A[i][c] != 0:
                fac = A[i][c]
                A[i] = [a - fac * b for a, b in zip(A[i], A[r])]
        pivots.append(c)
        r += 1
        if r == m:
            break
    pivot_cols = set(pivots)
    free_cols = [c for c in range(n) if c not in pivot_cols]
    basis = []
    for fc in free_cols:
        v = [F(0)] * n
        v[fc] = F(1)
        for i, pc in enumerate(pivots):
            v[pc] = -A[i][fc]
        basis.append(v)
    return len(pivots), basis


def conservation_laws(n):
    """The conservation laws of double-entry flows (E1′).

    A conservation law is a linear functional ``c`` with ``c·b = 0`` for *every*
    realizable balance vector ``b`` (every ``b`` with ``Σ b = 0``). The realizable set
    is the hyperplane spanned by ``eᵢ − eᵢ₊₁``, so the conservation laws are the
    (right) nullspace of that (n−1)×n matrix. Returns ``(rank, basis)``; the theorem is
    that the basis is exactly ``span{(1,…,1)}`` (dimension 1).
    """
    rows = []
    for i in range(n - 1):
        row = [F(0)] * n
        row[i] = F(1)
        row[i + 1] = F(-1)
        rows.append(row)
    return _rref_nullspace(rows)


def walras_law(excess_demand, prices):
    """Walras' law check: ``Σₖ pₖ zₖ`` — identically zero (E2)."""
    return sum(F(p) * F(z) for p, z in zip(prices, excess_demand))


def cobb_douglas_exchange(ratio):
    """The 2-good × 2-agent symmetric Cobb–Douglas exchange economy, exactly (E2/E3).

    Agents have identical Cobb–Douglas tastes (each spends half of income on each good)
    and endowments e₁=(1,0), e₂=(0,1). With ``r = p₂/p₁`` the excess demands are

        z₁(r) = r/2 − 1/2 ,   z₂(r) = 1/(2r) − 1/2

    Returns ``(z, walras_residual)`` where ``walras_residual = z₁ + r·z₂`` (the p₁ factor
    is free). Walras' law holds identically in ``r``; the market clears iff ``r = 1`` —
    only the *relative* price is fixed, the price level is a free ray (numéraire).
    """
    r = F(ratio)
    z1 = r / 2 - F(1, 2)
    z2 = F(1) / (2 * r) - F(1, 2)
    walras = z1 + r * z2
    return [z1, z2], walras


__all__ = [
    "net_balances",
    "total_balance",
    "realize",
    "conservation_laws",
    "walras_law",
    "cobb_douglas_exchange",
]
