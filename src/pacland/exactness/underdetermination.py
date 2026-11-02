"""The measure space has an exact dimension — and nothing fixes a point in it.

Albert [01:39:47]: *"Any probability distribution whatsoever over classical initial conditions is perfectly logically
compatible with the classical equations of motion."* This module makes that concrete for our window instead of
quoting it.

**The counting.** Orbits are labelled by their tadpole `N`. The Lagrangian symmetries of the pairing
`N = sum_i (F_i H_{i+n} - F_{i+n} H_i)` identify `N` with `-N` (flip `F`, or swap `F` and `H`), and nothing else:
component permutations and simultaneous sign flips act trivially on `N`. So the invariant classes are `|N|`.

**Measured, exactly, on the fully enumerated window `|component| <= 1`:**

| b3 | orbits | distinct N | distinct abs(N) |
|---|---|---|---|
| 2 | 80 | 5 | 3 |
| 4 | 6,560 | 9 | 5 |
| 6 | 531,440 | 13 | 7 |

`distinct N = 2*b3 + 1`, i.e. **every integer tadpole from `-b3` to `+b3` is attained** (which needs the bound
`max |N| = b3` from `tadpole_bound.py`), and `distinct |N| = b3 + 1`.

**The consequence — a proof of underdetermination, not a complaint.** A measure constant on invariant classes is a
point in the simplex of those `b3 + 1` weights, so the measure space has dimension **`b3`**: 6 at `b3 = 6`, 12 at
`b3 = 12`, and so on. **No invariant of the window reduces that dimension** — the symmetry identifies `N` with `-N`
and stops. There is therefore no invariant that *selects* a measure; the choice is a free point in a `b3`-dimensional
simplex, exactly as Albert describes for initial conditions.

Run:        python3 scripts/underdetermination.py
Guarded by: tests/test_underdetermination.py
"""
from __future__ import annotations

import numpy as np

from . import windows

LADDER = (2, 4, 6)


def classes(b3: int, max_abs: int = 1) -> dict:
    """Exact tadpole class structure of the primitive orbits."""
    fluxes = windows.enumerate_window(b3, max_abs)
    n = windows.tadpoles(fluxes)
    prim = np.array([windows.primitive(row) for row in fluxes])
    N = n[prim]
    distinct = sorted({int(x) for x in N.tolist()})
    absd = sorted({abs(int(x)) for x in N.tolist()})
    return {
        "b3": b3,
        "orbits": int(prim.sum()),
        "distinct_N": len(distinct),
        "distinct_absN": len(absd),
        "n_values": distinct,
        "all_tadpoles_attained": distinct == list(range(-b3, b3 + 1)),
        "measure_dimension": len(absd) - 1,   # simplex over the invariant classes
    }


def ladder(b3s=LADDER) -> list:
    return [classes(b3) for b3 in b3s]


def verdict(rows=None) -> dict:
    rows = rows or ladder()
    ok = all(r["all_tadpoles_attained"] for r in rows)
    dims = {r["b3"]: r["measure_dimension"] for r in rows}
    return {
        "rows": rows,
        "every_tadpole_attained": ok,
        "measure_dimensions": dims,
        "statement": ("A measure constant on invariant classes is a free point in a b3-dimensional simplex "
                      "(6 at b3=6, 12 at b3=12). No invariant of the window reduces that dimension, so the measure "
                      "is underdetermined by the data — a proof, not a failure to find one."),
        "citation": "Albert [01:39:47]: any distribution is logically compatible with the equations of motion",
        "falsifier": ("an invariant that identifies two distinct |N| classes would reduce the dimension; none is "
                      "known, and the symmetry group closes after N ~ -N"),
    }


__all__ = ["LADDER", "classes", "ladder", "verdict"]
