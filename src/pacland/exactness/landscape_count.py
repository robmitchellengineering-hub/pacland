"""The landscape count — does the discrete gauge symmetry shrink the `10^500`?

The claim under test: *"10^500 counts flux vectors, not distinct physics."* If the discrete gauge symmetry
(flux scaling, `(F,H) ~ d(F,H)`) quotients the lattice heavily, the invariant content is far smaller than the
vector count and the `10^500` framing is inflated. If it quotients almost nothing, the framing survives.

**Measured, exactly, on the enumerable ladder (`|component| <= 1`):**

| b3 | flux pairs | primitive orbits | orbits / pairs | `0 < N <= 1` orbits |
|---|---|---|---|---|
| 2 | 81 | 80 | 0.9877 | 20 |
| 4 | 6,561 | 6,560 | 0.9998 | 1,480 |
| 6 | 531,441 | 531,440 | 1.0000 | 107,100 |

**Verdict: the claim is REFUTED, on two independent counts.**

1. **The gauge quotient is negligible.** At `b3 = 6`, 531,440 of 531,441 pairs are primitive — the symmetry
   removes **one** pair. The flux vectors are almost all distinct orbits, so `10^500` is not inflated by gauge
   copies.
2. **The content is not a function of the tadpole alone.** At fixed `0 < N <= 1` the orbit count runs
   20 → 1,480 → 107,100 across `b3 = 2, 4, 6` — it scales with the window, so `L` does not fix the content.

Both are stated with their window, because both are window-dependent facts.

Run:        python3 scripts/landscape_count.py
Guarded by: tests/test_landscape_count.py
"""
from __future__ import annotations

import numpy as np

from . import windows

#: The enumerable ladder. `b3 = 8` would be 43M pairs (~5.5 GB), so it stops at 6.
LADDER = (2, 4, 6)


def content(b3: int, max_abs: int = 1) -> dict:
    """Primitive orbits, per-tadpole-class counts, and the quotient ratio — exactly."""
    fluxes = windows.enumerate_window(b3, max_abs)
    n = windows.tadpoles(fluxes)
    prim = np.array([windows.primitive(row) for row in fluxes])
    N = n[prim]
    return {
        "b3": b3,
        "flux_pairs": int(len(fluxes)),
        "orbits": int(prim.sum()),
        "quotient_ratio": float(prim.mean()),
        "per_tadpole": {int(k): int(v) for k, v in zip(*np.unique(N, return_counts=True))},
        "up_to_1": int(((N > 0) & (N <= 1)).sum()),
        "up_to_2": int(((N > 0) & (N <= 2)).sum()),
        "up_to_3": int(((N > 0) & (N <= 3)).sum()),
    }


def ladder(b3s=LADDER) -> list:
    return [content(b3) for b3 in b3s]


def verdict(rows=None) -> dict:
    rows = rows or ladder()
    ratios = [r["quotient_ratio"] for r in rows]
    ups = [r["up_to_1"] for r in rows]
    monotone = all(b > a for a, b in zip(ups, ups[1:]))
    return {
        "rows": rows,
        "gauge_quotient_negligible": min(ratios) > 0.98,
        "content_scales_with_b3": monotone,
        "claim_tested": "10^500 counts flux vectors, not distinct physics",
        "verdict": ("REFUTED — the gauge quotient removes a negligible fraction, and the content grows with the "
                    "window at fixed tadpole bound" if (min(ratios) > 0.98 and monotone) else
                    "the claim survives in some form — see the table"),
        "window": f"|component| <= 1, b3 = {[r['b3'] for r in rows]}",
    }


__all__ = ["LADDER", "content", "ladder", "verdict"]
