"""Route C — the transfer payoff: a period computed where the easy frame cannot go.

`docs/plan-real-answers.md`. The large-complex-structure series converges only for `|z| < z_c = 3.2e-4`. The
conifold coordinate `u = 1 - z/z_c` converges for `|u| < 1`, which covers `0 < z < 2 z_c`.

So the interval **`z_c < z < 2 z_c` is outside the LCS radius and inside the conifold chart**. Translating into
the conifold frame and computing there produces a number the LCS expansion cannot produce — which is the
difference between a dictionary that is bookkeeping and one that is a computing tool.

**Pass marks.** (a) truncation stability: the value moves by less than `1e-10` between conifold orders `N` and
`N + 40`. (b) an independent route agreeing to `1e-12` where both converge — **not yet done**, see below.

**What is NOT claimed.** A single branch value does not fix the fourth-order Picard-Fuchs equation, so a
"PF residual" computed from one point would be circular (it would test the series against the recurrence that
built it). Pass mark (b) therefore needs the LCS series evaluated as an independent estimate of the same
period, which requires an LCS-series adapter the connection module does not currently expose. That is stated
here rather than faked.

Run:        python3 scripts/continuation.py
Guarded by: tests/test_continuation.py
"""
from __future__ import annotations

import mpmath as mp

from . import conifold_recursion, quintic

#: `u = -0.5` is `z = 1.5 z_c`: past the LCS radius, well inside the conifold chart.
OUTSIDE_U = mp.mpf("-1") / 2


def conifold_period(u=OUTSIDE_U, order: int = 160, dps: int = 60):
    """The exponent-2 conifold branch evaluated at `u`, from its own series."""
    mp.mp.dps = dps
    c = conifold_recursion.numeric_series(n_max=order, s0=2, dps=dps)
    u = mp.mpf(u)
    return mp.fsum(c[n] * u ** n for n in range(len(c)))


def truncation_study(u=OUTSIDE_U, orders=(40, 80, 120, 160), dps: int = 60) -> dict:
    """The pass mark: how far does the value move as the truncation order rises?"""
    mp.mp.dps = dps
    vals = {n: conifold_period(u, n, dps) for n in orders}
    top = vals[max(orders)]
    moves = {n: abs(top - vals[n]) / abs(top) for n in orders if n != max(orders)}
    return {
        "u": mp.mpf(u),
        "z_over_zc": 1 - mp.mpf(u),          # u = 1 - z/z_c  =>  z/z_c = 1 - u
        "orders": list(orders),
        "values": {n: mp.nstr(v, 24) for n, v in vals.items()},
        "moves": {n: float(m) for n, m in moves.items()},
        "worst_move": float(max(moves.values())) if moves else 0.0,
        "pass_mark_1e-10": bool(max(moves.values()) < mp.mpf("1e-10")) if moves else False,
        "note": ("a single branch value does not fix the fourth-order Picard-Fuchs equation, so pass mark (b) "
                 "— an independent route agreeing to 1e-12 where both converge — needs the LCS series as a "
                 "second estimate, which is not yet wired"),
    }


def where_both_converge() -> dict:
    """The region where an independent LCS check is possible: `|z| < z_c`."""
    zc = quintic.Z_CONIFOLD
    return {"z_c": mp.nstr(zc, 10),
            "lcs": "|z| < z_c",
            "conifold": "|u| < 1  =>  0 < z < 2 z_c",
            "overlap": "0 < z < z_c",
            "outside_lcs_inside_conifold": "z_c < z < 2 z_c"}


__all__ = ["OUTSIDE_U", "conifold_period", "truncation_study", "where_both_converge"]
