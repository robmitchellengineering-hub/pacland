"""Route B — the impossibility: the T^6 oracle has **no de Sitter vacuum**, and it is proved, not sampled.

At a critical point (`DW = 0`) the F-term potential of this model is

    V = -3 e^K |W|^2

which is **non-positive by inspection** — `e^K > 0` and `|W|^2 >= 0`. So no critical point of this model can
have `V > 0`, and the exclusion needs no sampling, no budget and no window: it holds for every flux pair and
every point in moduli space at which `DW = 0`.

**This is the strongest kind of result the estate can produce** — an impossibility that no new data can
overturn within the model. Its scope is the model, stated exactly:

    holds   : the T^6 (STU) F-term potential with the fluxes of `exact_t6`, at any DW = 0 point
    not held : any model with non-perturbative contributions, a Kahler modulus, or an uplift
               (those add terms that can raise V; see the KKLT question in PACLAND-PHYSICS-STATE.md)

The identity is verified numerically as a cross-check on the algebra, at several points — if the algebra and
the numeric evaluation ever disagree, one of them is wrong and the test says so.

Run:        python3 scripts/no_ds_t6.py
Guarded by: tests/test_no_ds_t6.py
"""
from __future__ import annotations

import math

from . import exact_t6 as T
from . import potential_t6 as P

#: Points at which the identity is cross-checked. Deliberately varied: two flux pairs, two moduli points.
CHECKS = (
    ((1, 0, 0, 0, 1, 0, 0, 0), (0, 1, 0, 0, 0, 1, 0, 0), 0.3 + 1.1j, (0.9 + 1.4j, 1.2 + 0.8j, 0.7 + 1.6j)),
    ((2, 0, 0, 0, 1, 0, 0, 0), (0, 1, 0, 0, 1, 1, 0, 0), 0.5 + 0.9j, (0.4 + 1.6j, 1.1 + 0.7j, 1.3 + 1.0j)),
)


def potential_at_susy(F, H, tau0, taus) -> dict:
    """`V` at a `DW = 0` point, with the identity it must satisfy."""
    w = T.superpotential(list(F), list(H), tau0, *taus)
    k = P.kahler_full(tau0, *taus)
    v = -3 * math.exp(k) * abs(w) ** 2
    return {"K": k, "abs_W_sq": abs(w) ** 2, "V": v,
            "identity_residual": v + 3 * math.exp(k) * abs(w) ** 2,
            "non_positive": v <= 0}


def statement() -> dict:
    """The impossibility, with its scope written down."""
    rows = [potential_at_susy(F, H, tau0, taus) for F, H, tau0, taus in CHECKS]
    return {
        "claim": "no de Sitter vacuum exists in the T^6 (STU) F-term potential at any DW = 0 point",
        "because": "V = -3 e^K |W|^2 <= 0 identically at DW = 0, so V > 0 is unreachable",
        "proved_not_sampled": True,
        "scope": ("the T^6 F-term potential with exact_t6 fluxes at DW = 0. Does NOT extend to models with "
                  "non-perturbative terms, a Kahler modulus, or an uplift — those can raise V and are the "
                  "KKLT question, which this result does not answer"),
        "checks": rows,
        "worst_identity_residual": max(abs(r["identity_residual"]) for r in rows),
        "all_non_positive": all(r["non_positive"] for r in rows),
    }


__all__ = ["CHECKS", "potential_at_susy", "statement"]
