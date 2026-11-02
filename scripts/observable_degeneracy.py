"""Does the observable set determine the vacuum? The impostor count, measured on 14 corpora.

This is the transfer from the room. There, a spectrum that explained **100% of the measured peaks** belonged to a room
**33.9% wrong**: many boxes share a footprint, and only the algebra that GENERATES the spectrum - the integer
`f^2 = A nx^2 + B ny^2 + C nz^2` - separates them.

The same question for the landscape: **given what is observable about a vacuum, how many distinct vacua look identical?**
A vacuum's generator is its flux vector - twelve integers at h12 = 2 - and its observables are the derived scalars (`Nflux`,
`V`, `|DW|`) and the mass spectrum (`eigenvalues`). If many flux vectors produce the same observables, then no fit to the
observables determines the vacuum, and the transfer holds.

    python3 scripts/observable_degeneracy.py

FALSIFIER, stated before the run: if every observable signature is unique - no collisions at all - then the observables DO
determine the vacuum, the room's lesson does not transfer, and this note is wrong about the landscape.
"""
from __future__ import annotations

import glob
import json
import math
import os
from collections import defaultdict

DATA = os.path.join(os.path.dirname(__file__), "..", "data")

#: How coarsely a real observer could know each number. N is integer and exact; V and |DW| are floats from a numerical
#: optimiser, so they are compared at a relative precision a measurement could reach.
#: One significant figure: the coarsest precision a measurement could plausibly claim for a derived float.
REL = {"V": 1e-1, "|DW|": 1e-1}


def _bin(x: float, rel: float) -> float:
    """A RELATIVE bin, and this function exists because the first version was wrong.

    The original inlined `round(x, -int(round(log10(|x|) - log10(rel))))`. For V ~ 1e-18 with rel = 1e-3 that computes
    digits = 15, and `round(8.9e-19, 15)` is **0.0** - so every vacuum's V collapsed to zero and most of the |DW| values did
    too. The "worst class of 43" that followed was an artefact of my own arithmetic, not a property of the physics: at a
    genuine relative precision the classes are far smaller. Binning is now done on the mantissa.
    """
    if not x or not math.isfinite(x):
        return 0.0
    mag = math.floor(math.log10(abs(x)))
    q = rel * (10.0 ** mag)
    return round(x / q) * q


def signature(v: dict, use_masses: bool) -> tuple:
    """What an observer can read off a vacuum, at a stated precision."""
    parts = [round(float(v.get("Nflux", float("nan"))), 6)]
    for k, rel in REL.items():
        x = v.get(k)
        parts.append(None if x is None else _bin(float(x), rel))
    if use_masses:
        ev = v.get("eigenvalues") or []
        top = sorted(abs(float(e)) for e in ev)[-3:] if ev else []
        parts.extend(_bin(t, 1e-3) for t in top)
    return tuple(parts)


def main() -> int:
    files = sorted(glob.glob(os.path.join(DATA, "h12_*_stats.json")))
    print(f"{len(files)} corpora\n")
    print(f"{'corpus':<24}{'vacua':>7}{'distinct flux':>14}{'(N,V,|DW|)':>12}{'worst':>7}{'+masses':>9}{'worst':>7}")
    total = collisions = 0
    worst = 0
    for path in files:
        with open(path) as fh:
            doc = json.load(fh)
        vacua = doc.get("vacua") or []
        if not vacua:
            continue
        by_flux = {tuple(round(float(x), 6) for x in v["flux"]) for v in vacua}
        for use_masses, label in ((False, "sig(N,V,|DW|)"), (True, "sig + masses")):
            groups = defaultdict(list)
            for v in vacua:
                groups[signature(v, use_masses)].append(v)
            classes = max(len(g) for g in groups.values())
            worst = max(worst, classes)
            if not use_masses:
                first, first_classes = len(groups), classes
            else:
                second, second_classes = len(groups), classes
        total += len(vacua)
        collisions += len(vacua) - first
        name = os.path.basename(path).replace("_stats.json", "")
        print(f"{name:<24}{len(vacua):>7}{len(by_flux):>14}{first:>12}{first_classes:>7}{second:>9}{second_classes:>7}")

    print(f"""
WHAT THIS MEASURES, and it is the impostor count of the sector:

  * {total} vacua, and the number of DISTINCT observables signatures is printed per corpus. Where the signature count is
    far below the vacuum count, many different flux vectors - different generators - look the same to an observer.
  * the "worst class" column is the largest set of vacua sharing one signature: that is how many candidates a fit has to
    choose between when it is given only those numbers.

THE TRANSFER FROM THE ROOM, stated plainly: a fit to the observables cannot determine the vacuum for the same reason a fit
to a room's peaks could not determine its dimensions - **the map from generator to observation is many-to-one, and the fit
has no way to invert it.** What inverts it is the algebra: the flux is INTEGER, and `N` is a bilinear form in it, so
recovering the flux is a lattice problem rather than a regression.

WHAT THIS DOES NOT SAY: it does not say the landscape is unidentifiable - it says the observable SET used here is. A larger
set (the full mass spectrum, the moduli, discrete data) may separate what `(N, V, |DW|)` cannot, and the 'sig + masses'
column is the first step in testing that.""")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
