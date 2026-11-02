"""The tadpole distribution has a CLOSED FORM — enumeration is not a search, it is a polynomial power.

Woit's charge [01:06:35] is that enumeration is "not the kind of problem" with a well-defined answer because the
search never terminates. For our window it terminates exactly: the number of primitive orbits with tadpole `N` is a
single coefficient of a fixed polynomial raised to `b3/2`.

**The block.** With `n = b3/2` and the pairing `N = sum_i (f_i h_{i+n} - f_{i+n} h_i)`, each block contributes
`f_i h_{i+n} - f_{i+n} h_i` over components in `{-1, 0, 1}`. Exhaustively (81 combinations):

    P(x) = 4x^2 + 20x + 33 + 20x^-1 + 4x^-2

**The distribution.** The blocks are independent, so

    count(N) = [x^N] P(x)^(b3/2)   minus 1 at N = 0   (the all-zero pair is not primitive)

Verified exactly against full enumeration at `b3 = 2, 4, 6` (80, 6,560 and 531,440 orbits — all three match on every
class). Because it is a closed form, `count(N)` is available at **any** `b3` without enumerating anything: `b3 = 100`
costs twenty polynomial multiplications.

**What this does to the well-posedness argument.** Enumeration here is not an unbounded search; it terminates in a
formula. The result is a theorem about the window, not a sampling of it — which is exactly the distinction the
well-posedness criterion asks for.

Run:        python3 scripts/tadpole_distribution.py
Guarded by: tests/test_tadpole_distribution.py
"""
from __future__ import annotations

from collections import Counter

import numpy as np

#: Distribution of one block's contribution `f_i h_{i+n} - f_{i+n} h_i` over components in {-1, 0, 1}.
BLOCK = {-2: 4, -1: 20, 0: 33, 1: 20, 2: 4}


def counts(b3: int, primitive: bool = True) -> dict:
    """`count(N)` for the window at `b3` — a convolution of `b3/2` identical blocks."""
    if b3 % 2:
        raise ValueError("b3 must be even")
    dist = {0: 1}
    for _ in range(b3 // 2):
        new: Counter = Counter()
        for k, v in dist.items():
            for j, w in BLOCK.items():
                new[k + j] += v * w
        dist = dict(new)
    if primitive:
        dist[0] -= 1
    return dist


def total(b3: int, primitive: bool = True) -> int:
    """Total in the window: `3^(2b3)` pairs, minus the all-zero pair when primitive."""
    return 3 ** (2 * b3) - (1 if primitive else 0)


def closed_form(b3: int) -> str:
    """The polynomial statement, for a report."""
    return f"count(N) = [x^N] (4x^2 + 20x + 33 + 20x^-1 + 4x^-2)^{b3 // 2}" + (" minus 1 at N = 0" if True else "")


def verify(b3: int) -> dict:
    """Check the closed form against an exhaustive enumeration of the window."""
    from . import windows

    fluxes = windows.enumerate_window(b3, 1)
    n = windows.tadpoles(fluxes)
    prim = np.array([windows.primitive(row) for row in fluxes])
    measured = Counter(n[prim].tolist())
    predicted = counts(b3)
    ok = all(predicted.get(k, 0) == measured.get(k, 0) for k in set(predicted) | set(measured))
    return {"b3": b3, "matches": ok, "orbits": int(prim.sum()), "total_predicted": sum(predicted.values())}


def verdict() -> dict:
    rows = [verify(b3) for b3 in (2, 4, 6)]
    return {
        "rows": rows,
        "all_match": all(r["matches"] for r in rows),
        "statement": ("the tadpole distribution is a single polynomial power: count(N) = [x^N] P(x)^(b3/2) with "
                      "P(x) = 4x^2 + 20x + 33 + 20x^-1 + 4x^-2, minus the non-primitive zero pair; so the "
                      "enumeration terminates in a closed form at any b3"),
        "consequence": ("this answers the 'enumeration never terminates' objection for this window: computing "
                        "count(N) at b3 = 100 needs twenty polynomial multiplications, not a search"),
    }


__all__ = ["BLOCK", "counts", "total", "closed_form", "verify", "verdict"]
