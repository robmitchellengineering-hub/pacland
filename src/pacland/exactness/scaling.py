"""Route A — the scaling study: is a lattice fact a fact about the family, or about one window?

Every headline number in this estate is computed in **one** window (`b3 = 6, |component| <= 1`). A number that
is quoted as a fact about the flux lattice has to survive a change of `b3`; if it moves, it is a fact about the
window and must be labelled so.

The exact ladder is `b3 = 2, 4, 6` at `max_abs = 1` — 81, 6,561 and 531,441 pairs. `b3 = 8` is 3^16 = 43M
pairs (about 5.5 GB) so the ladder **stops at 6**, and that limit is part of the result rather than a footnote.

Run:        python3 scripts/scaling.py
Guarded by: tests/test_scaling.py
"""
from __future__ import annotations

import numpy as np

from . import windows

#: The exact ladder. Do not extend past 6 without a memory plan: b3 = 8 is 43M pairs.
LADDER = (2, 4, 6)


def facts(b3: int, max_abs: int = 1) -> dict:
    """The lattice facts, exactly, in the window `b3, max_abs`."""
    fluxes = windows.enumerate_window(b3, max_abs)
    n = windows.tadpoles(fluxes)
    primitive = np.array([windows.primitive(row) for row in fluxes])
    total = len(fluxes)
    return {
        "b3": b3,
        "pairs": int(total),
        "primitive fraction": float(primitive.mean()),
        "N = 0 fraction": float((n == 0).mean()),
        "N > 0 fraction": float((n > 0).mean()),
        "|N| <= 1 fraction": float((np.abs(n) <= 1).mean()),
        "max |N|": int(np.abs(n).max()),
        "all components non-zero": float(np.all(fluxes != 0, axis=1).mean()),
    }


def _direction(values: list) -> str:
    if all(b >= a for a, b in zip(values, values[1:])):
        return "rising"
    if all(b <= a for a, b in zip(values, values[1:])):
        return "falling"
    return "non-monotone"


def verdicts(ladder=LADDER, tolerance: float = 0.10, max_abs: int = 1) -> dict:
    """For each fact: `scale-invariant` or `scale-dependent` with its direction.

    `scale-invariant` means the value moves by less than `tolerance` relative to its mean across the ladder —
    a stated convention, so a reader can disagree with the number rather than the verdict.
    """
    rows = [facts(b3, max_abs) for b3 in ladder]
    out = {}
    for key in rows[0]:
        if key in ("b3", "pairs"):
            continue
        vals = [r[key] for r in rows]
        lo, hi = min(vals), max(vals)
        mean = sum(vals) / len(vals)
        rel = (hi - lo) / abs(mean) if mean else float("inf")
        direction = _direction(vals)
        monotone = direction in ("rising", "falling")
        # A movement smaller than the tolerance is NOT the same as no movement: primitivity goes
        # 0.9877 -> 1.0000, a monotone 1.2% trend that the 10% rule would call "invariant". Both facts are
        # reported, because "invariant within tolerance, and still trending" is the honest description.
        verdict = "scale-invariant" if rel <= tolerance else "scale-dependent"
        out[key] = {
            "values": vals,
            "movement": rel,
            "verdict": verdict,
            "direction": direction if (rel > tolerance or monotone) else "",
            "trend_within_tolerance": bool(rel <= tolerance and monotone and lo != hi),
        }
    return {"ladder": list(ladder), "max_abs": max_abs, "rows": rows, "facts": out,
            "invariant": [k for k, v in out.items() if v["verdict"] == "scale-invariant"]}


def report() -> dict:
    r = verdicts()
    trending = [k for k, v in r["facts"].items() if v["trend_within_tolerance"]]
    return {**r, "name": "primitive fraction",
            "trend_within_tolerance": trending,
            "note": (f"invariant within the stated 10% tolerance: {r['invariant'] or 'none'}"
                     + (f"; of those, still trending with b3: {trending}" if trending else "")
                     + ". Every OTHER fraction moves by more than the tolerance, so a window fraction must "
                       "carry its b3 with it.")}


__all__ = ["LADDER", "facts", "verdicts", "report"]
