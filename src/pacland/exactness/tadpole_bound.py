"""`max |N| = b3` is a theorem, not a table of numbers.

The symplectic pairing on the `|component| <= 1` window is

    N(F, H) = sum_{i=1..n} ( F_i H_{i+n} - F_{i+n} H_i ),      n = b3/2

**Proof of the bound.** Each bracket is a difference of two products of components bounded by 1, so each bracket
lies in `[-2, 2]`. There are `n = b3/2` brackets, hence

    |N| <= 2n = b3 .

**Proof that the bound is attained.** Take `F_i = F_{i+n} = 1` and `H_i = -1`, `H_{i+n} = 1` for every `i`. Then
each bracket is `1*1 - 1*(-1) = 2`, so `N = 2n = b3` exactly.

So `max |N| = b3` holds for **every even `b3`**, with no enumeration needed — the earlier ladder (`b3 = 2, 4, 6`)
was three samples of a theorem. Verified numerically at `b3 = 2, 4, 6, 8` in this module's tests.

Run:        python3 scripts/tadpole_bound.py
Guarded by: tests/test_tadpole_bound.py
"""
from __future__ import annotations

import numpy as np


def bound(b3: int) -> int:
    """The theorem's value: `max |N| = b3`."""
    return b3


def attain(b3: int) -> tuple:
    """The explicit pair that attains the bound: `N = b3`."""
    n = b3 // 2
    F = [0] * b3
    H = [0] * b3
    for i in range(n):
        F[i] = F[i + n] = 1
        H[i] = -1
        H[i + n] = 1
    return F, H


def tadpole(F, H) -> int:
    b3 = len(F)
    n = b3 // 2
    return sum(F[i] * H[i + n] - F[i + n] * H[i] for i in range(n))


def measured(b3: int, dtype=np.int32) -> int:
    """Exhaustive max over the window, for the sizes where it is cheap."""
    vals = np.array(np.meshgrid(*[(-1, 0, 1)] * b3, indexing="ij"), dtype=np.int64).reshape(b3, -1).T
    n = b3 // 2
    best = 0
    CH = 2000
    Hp, Hn = vals[:, :n], vals[:, n:]
    for s in range(0, len(vals), CH):
        f = vals[s:s + CH]
        N = f[:, :n] @ Hn.T - f[:, n:] @ Hp.T
        best = max(best, int(np.abs(N).max()))
    return best


__all__ = ["bound", "attain", "tadpole", "measured"]
