"""The existence engine — the other side of the falsifier (D17).

The counterexample engine asks *is this conjecture true* and answers by finding the object that breaks it.
This asks **does an object exist with property P**, and answers by *exhibiting it*. Same enumeration, same
window, opposite direction — and the direction matters, because an exhibited object is a **positive** result:
it settles a question about the lattice and it becomes a resource (a concrete flux pair you can compute
with).

Two outcomes, both full results:

    FOUND   an object with its coordinates, its tadpole and the reason it qualifies
    NONE    no such object in the window — a theorem-in-a-window, stated with the window

Run:        python3 scripts/existence.py
Guarded by: tests/test_existence.py
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from . import windows


@dataclass
class Existence:
    """One existence question, answered."""
    question: str
    why: str                      # why an object would be interesting
    window: str
    searched: int
    found: dict | None            # {"flux": [...], "tadpole": int, "note": str}
    matches: int

    @property
    def verdict(self) -> str:
        return "FOUND" if self.found is not None else "NONE"

    @property
    def states(self) -> str:
        if self.found is not None:
            return (f"an object exists: (F|H) = {self.found['flux']} with N = {self.found['tadpole']} — "
                    f"{self.matches} in the window. {self.found['note']}")
        return (f"no object in {self.window} ({self.searched} pairs). That is a theorem about this window "
                f"and nothing outside it.")


def find(predicate, question: str, why: str, b3: int = 6, max_abs: int = 1,
         smallest_first: bool = True) -> Existence:
    """Exhaustively search the window for an object satisfying `predicate(flux, tadpole)`.

    With `smallest_first`, the returned witness is the one of least Euclidean norm — a canonical choice, so
    two runs report the same object and a reader can check it by hand.
    """
    fluxes = windows.enumerate_window(b3, max_abs)
    n = windows.tadpoles(fluxes)
    window = f"b3={b3}, |component| <= {max_abs} ({len(fluxes)} flux pairs)"
    hits = []
    for row, t in zip(fluxes, n):
        f = [int(x) for x in row]
        if predicate(f, int(t)):
            hits.append((sum(abs(x) for x in f), f, int(t)))
    if not hits:
        return Existence(question=question, why=why, window=window, searched=int(len(fluxes)),
                         found=None, matches=0)
    hits.sort(key=lambda h: h[0]) if smallest_first else None
    norm, flux, t = hits[0]
    return Existence(question=question, why=why, window=window, searched=int(len(fluxes)),
                     found={"flux": flux, "tadpole": t,
                            "note": f"least-norm witness (weight {norm}); {len(hits)} matches in the window"},
                     matches=len(hits))


# ---------------------------------------------------------------------------------------
# the shipped questions — each says why an object would be worth having
# ---------------------------------------------------------------------------------------
def _prim(row) -> bool:
    return windows.primitive(row)


def null_tadpole_no_zero_component(flux, t) -> bool:
    return t == 0 and _prim(flux) and all(x != 0 for x in flux)


def null_tadpole_split(flux, t) -> bool:
    """Both halves non-zero and not proportional — the null cone is not just F = 0 or F ∝ H."""
    if t != 0 or not _prim(flux):
        return False
    F, H = flux[:6], flux[6:]
    if not any(F) or not any(H):
        return False
    # proportional check over the rationals via cross-ratios
    for i in range(6):
        for j in range(i + 1, 6):
            if F[i] * H[j] != F[j] * H[i]:
                return True
    return False


def odd_tadpole_no_zero_component(flux, t) -> bool:
    return t == 1 and _prim(flux) and all(x != 0 for x in flux)


def run_all(b3: int = 6, max_abs: int = 1) -> list:
    return [
        find(null_tadpole_split,
             "a primitive pair with zero tadpole whose halves are non-zero and not proportional",
             "it says the kernel of the symplectic pairing is populated away from its two obvious branches "
             "(F = 0 and F proportional to H), which is a statement about the lattice rather than a claim "
             "about a model", b3, max_abs),
        find(null_tadpole_no_zero_component,
             "a primitive pair with zero tadpole and no zero component",
             "it gives a null-tadpole flux pair you can hand to any computation without a component "
             "dropping out — a resource, not just a fact", b3, max_abs),
        find(odd_tadpole_no_zero_component,
             "a primitive pair with N = 1 and no zero component",
             "the minimal odd tadpole is what a brane-inflation or single-brane construction needs; if it "
             "requires a zero component, that is a structural constraint on those constructions",
             b3, max_abs),
    ]


__all__ = ["Existence", "find", "run_all", "null_tadpole_split", "null_tadpole_no_zero_component",
           "odd_tadpole_no_zero_component"]
