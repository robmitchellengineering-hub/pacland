"""The counterexample engine — the falsifier pointed the other way (D17, second instrument).

A falsifier waits to be pointed at a claim. This **searches**: enumerate an exactly-defined finite window,
apply a conjecture, and either produce the object that breaks it or state precisely what was ruled out.

**The statement it is allowed to make is narrow, and that is the point.** An exhaustive window search
proves *"no counterexample in window W"* — never *"the conjecture is true"*. Every verdict therefore
carries the window it searched and the scope it does not cover. A search whose output cannot be turned into
a counterexample is decoration, so each shipped conjecture is paired with a **known-answer control**: a
predicate that is false in the window and *must* return a counterexample.

Built on `exactness/windows.py` — the enumeration is shared, not re-implemented, so a fix to the window
machinery moves both.

Run:        python3 scripts/counterexample.py
Guarded by: tests/test_counterexample.py
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from . import windows


@dataclass
class Verdict:
    """What an exhaustive search in a finite window establishes — and what it does not."""
    conjecture: str
    window: str
    searched: int
    counterexample: dict | None
    scope: str

    @property
    def verdict(self) -> str:
        return "BROKEN" if self.counterexample is not None else "no counterexample"

    @property
    def proves(self) -> str:
        if self.counterexample is not None:
            return (f"the conjecture is FALSE: {self.counterexample['what']} at "
                    f"(F,H) = {self.counterexample['flux']}")
        return (f"no counterexample among {self.searched} objects in {self.window}. That is a statement "
                f"about this window and nothing outside it.")


def _flux_row(row) -> list:
    return [int(x) for x in row]


def search(predicate, name: str, b3: int = 6, max_abs: int = 1, limit: int = 1) -> Verdict:
    """Exhaustively apply `predicate` to every integral `(F, H)` pair in the window.

    `predicate(flux, tadpole)` returns `True` when the conjecture *holds*. The first `limit` rows where it
    returns `False` are counterexamples.
    """
    fluxes = windows.enumerate_window(b3, max_abs)
    n = windows.tadpoles(fluxes)
    window = f"b3={b3}, |component| <= {max_abs} ({len(fluxes)} flux pairs)"
    found = []
    for row, t in zip(fluxes, n):
        f = _flux_row(row)
        if not predicate(f, int(t)):
            found.append({"flux": f, "tadpole": int(t),
                          "what": f"{name} fails (N = {int(t)})"})
            if len(found) >= limit:
                break
    return Verdict(conjecture=name, window=window, searched=int(len(fluxes)),
                   counterexample=(found[0] if found else None),
                   scope=("exhaustive over the window; it does NOT prove the conjecture outside it, and it "
                          "does not prove the negation either — one counterexample is required to do that"))


# ---------------------------------------------------------------------------------------
# the shipped conjectures
# ---------------------------------------------------------------------------------------
def tadpole_positive(flux, t) -> bool:
    return t > 0


def tadpole_bounded(limit: int):
    def predicate(flux, t) -> bool:
        return t <= limit
    predicate.__name__ = f"tadpole_bounded({limit})"
    return predicate


def tadpole_nonzero(flux, t) -> bool:
    return t != 0


#: The three shipped searches. Two are **known-answer controls** — they must find a counterexample, or the
#: engine cannot be trusted to report a clean one. The third rules something out in its window.
SHIPPED = (
    ("tadpole is always positive", tadpole_positive),
    ("tadpole is never zero", tadpole_nonzero),
    ("tadpole N <= 3", tadpole_bounded(3)),
    ("tadpole N <= 6", tadpole_bounded(6)),
)


def run_all(b3: int = 6, max_abs: int = 1) -> list:
    return [search(p, name, b3=b3, max_abs=max_abs) for name, p in SHIPPED]


__all__ = ["Verdict", "search", "tadpole_positive", "tadpole_bounded", "tadpole_nonzero",
           "SHIPPED", "run_all"]
