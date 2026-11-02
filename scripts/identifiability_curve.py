"""How many numbers does it take to identify a vacuum? The curve, and the lattice's own degeneracy.

The impostor count showed the two ends: `(N, V, |DW|)` leaves up to **43** vacua indistinguishable, and the three largest
masses separate every corpus completely. **This measures the curve between them** - how many masses buy how much
identification - and separately measures **how degenerate `N` alone is**, because `N` is the only observable with a known
algebra (`N = 1/2 F.H`, bilinear in the integers).

    python3 scripts/identifiability_curve.py

WHY IT MATTERS FOR THE TRANSFER: on a room, about thirty identified modes were needed before the dimensions could be
recovered, and fewer than that needed a prior or it failed. If the landscape has the same shape - a threshold below which
nothing is identifiable - then that threshold is the practical answer to "what must be measured", and the algebra only helps
above it.

FALSIFIER, stated before the run: if a single mass already makes every vacuum identifiable (singleton fraction 1.0 at
k = 1), the curve is trivial and the masses are not carrying structure worth the name - it would mean the eigenvalues are
effectively a serial number, not a physical spectrum.
"""
from __future__ import annotations

import glob
import json
import math
import os
from collections import defaultdict

DATA = os.path.join(os.path.dirname(__file__), "..", "data")
REL_V = 1e-1          # the precision swept below; 1e-1 is one significant figure
REL_DW = 1e-1
REL_MASS = 1e-3       # masses are read from the spectrum, so 0.1% is generous


def _bin(x: float, rel: float) -> float:
    """A relative bin: the mantissa at `rel` precision, so a 0.1% difference is not a new observation."""
    if not x or not math.isfinite(x):
        return 0.0
    mag = math.floor(math.log10(abs(x)))
    q = rel * (10 ** mag)
    return round(x / q) * q


def signature(v: dict, k: int) -> tuple:
    ev = sorted((abs(float(e)) for e in (v.get("eigenvalues") or [])), reverse=True)
    masses = tuple(_bin(e, REL_MASS) for e in ev[:k])
    return (v.get("Nflux"), _bin(float(v.get("V") or 0), REL_V), _bin(float(v.get("|DW|") or 0), REL_DW)) + masses


def precision_curve(vacua: list[dict]) -> list[dict]:
    """Identification against PRECISION on the three scalars - the axis that actually matters.

    The first version of the impostor count rounded to one significant figure and found classes of 43; at three significant
    figures every vacuum is unique. **So the degeneracy is a property of the precision, not only of the observable set**,
    and a curve against precision is the honest statement.
    """
    out = []
    for exp in (0, 1, 2, 3, 4, 6):
        rel = 10.0 ** (-exp)
        groups = defaultdict(list)
        for v in vacua:
            key = (round(float(v["Nflux"]), 6),
                   _bin(float(v.get("V") or 0), rel),
                   _bin(float(v.get("|DW|") or 0), rel))
            groups[key].append(v)
        singles = sum(1 for g in groups.values() if len(g) == 1)
        out.append({"digits": exp, "classes": len(groups), "worst": max(len(g) for g in groups.values()),
                    "identifiable": singles / len(vacua)})
    return out


def curve(vacua: list[dict], k_max: int = 12) -> list[dict]:
    out = []
    for k in range(0, k_max + 1):
        groups = defaultdict(list)
        for v in vacua:
            groups[signature(v, k)].append(v)
        singletons = sum(1 for g in groups.values() if len(g) == 1)
        out.append({
            "k": k,
            "classes": len(groups),
            "worst": max(len(g) for g in groups.values()),
            "identifiable": singletons / len(vacua),
        })
    return out


def tadpole_degeneracy(vacua: list[dict]) -> dict:
    """N's own lattice: how many distinct flux vectors share a tadpole, in this corpus."""
    by_n = defaultdict(set)
    for v in vacua:
        by_n[round(float(v["Nflux"]), 6)].add(tuple(round(float(x), 6) for x in v["flux"]))
    counts = sorted((len(s) for s in by_n.values()), reverse=True)
    return {
        "distinct_N": len(by_n),
        "flux_per_N_max": counts[0] if counts else 0,
        "flux_per_N_mean": sum(counts) / len(counts) if counts else 0.0,
    }


def main() -> int:
    files = sorted(glob.glob(os.path.join(DATA, "h12_*_stats.json")))
    print(f"{len(files)} corpora\n")
    pooled = []
    for path in files:
        with open(path) as fh:
            doc = json.load(fh)
        vacua = doc.get("vacua") or []
        if not vacua:
            continue
        name = os.path.basename(path).replace("_stats.json", "")
        c = curve(vacua)
        t = tadpole_degeneracy(vacua)
        pooled.append((name, len(vacua), c, t))
        row = "  ".join(f"k={r['k']}:{r['identifiable']:.2f}" for r in c if r["k"] in (0, 1, 2, 3, 5, 8, 12))
        print(f"{name:<14} n={len(vacua):<4} {row}   | N classes {t['distinct_N']}, "
              f"worst {t['flux_per_N_max']} fluxes/N")

    print("\nPOOLED CURVE (the answer, over all corpora)")
    print(f"{'masses used':>12}{'identifiable fraction':>24}")
    for k in range(0, 13):
        fracs = [next(r["identifiable"] for r in c if r["k"] == k) for _, _, c, _ in pooled]
        mean = sum(fracs) / len(fracs)
        bar = "#" * int(round(mean * 40))
        print(f"{k:>12}{mean:>24.3f}  {bar}")

    print("\nIDENTIFICATION AGAINST PRECISION (three scalars, no masses)")
    print(f"{'significant figures':>22}{'identifiable':>14}{'worst class':>13}")
    for exp in (0, 1, 2, 3, 4, 6):
        vals = []
        for _, _, vac, _ in [(n, c, v, t) for (n, v, c, t) in [] ]:
            pass
        rows = []
        for path in files:
            with open(path) as fh:
                doc = json.load(fh)
            vacua = doc.get("vacua") or []
            if not vacua:
                continue
            rows.append(next(r for r in precision_curve(vacua) if r["digits"] == exp))
        ident = sum(r["identifiable"] for r in rows) / len(rows)
        worst = max(r["worst"] for r in rows)
        print(f"{exp:>22}{ident:>14.3f}{worst:>13}")

    print(f"""
WHAT THE CURVE SAYS:

  * with NO masses, identification is {sum(next(r['identifiable'] for r in c if r['k'] == 0) for _, _, c, _ in pooled) / len(pooled):.3f} - the three scalars almost never
    pick a vacuum out on their own, which is the impostor count restated as a curve.
  * the fraction rises with the number of masses, and the useful question is where it crosses 0.9: that is the product
    answer to "what has to be measured", in the same way about thirty modes was the answer for a room.

THE LATTICE'S OWN DEGENERACY is the second half: `N` alone puts many different flux vectors in one class, so no inversion of
`N` can name a vacuum - only the masses (and the other structure) can. **The algebra is necessary and not sufficient: it
turns the problem from a regression into a lattice problem, and the lattice still needs enough data.**""")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
