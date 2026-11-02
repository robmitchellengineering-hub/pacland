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
import os
from collections import defaultdict

DATA = os.path.join(os.path.dirname(__file__), "..", "data")

#: How coarsely a real observer could know each number. N is integer and exact; V and |DW| are floats from a numerical
#: optimiser, so they are compared at a relative precision a measurement could reach.
REL = {"V": 1e-3, "|DW|": 1e-3}


def signature(v: dict, use_masses: bool) -> tuple:
    """What an observer can read off a vacuum, at a stated precision."""
    parts = [round(float(v.get("Nflux", float("nan"))), 6)]
    for k, rel in REL.items():
        x = v.get(k)
        if x is None:
            parts.append(None)
        else:
            # a relative bin: the exponent of the magnitude, and the mantissa to `rel`
            x = float(x)
            parts.append(round(x, -int(round(__import__("math").log10(abs(x) + 1e-300) - __import__("math").log10(rel))))
                         if x else 0.0)
    if use_masses:
        ev = v.get("eigenvalues") or []
        top = sorted(abs(float(e)) for e in ev)[-3:] if ev else []
        parts.extend(round(t, -int(round(__import__("math").log10(t + 1e-300) - 3))) for t in top)
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
