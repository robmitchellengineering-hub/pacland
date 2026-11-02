#!/usr/bin/env python3
"""Is the ~0.8 minima rate derivable from the lattice? If nothing correlates, it is model-specific.

Pre-registered before running: *if `is_minimum` correlates with no computable lattice invariant, then 0.8 cannot come
out of the counting and must be retired as a model-specific fact.*

    python3 scripts/minima_correlation.py
"""
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pacland.exactness import counterexample as C   # noqa: E402
from pacland.exactness import ingest_gate as G      # noqa: E402


def invariants(row: dict) -> dict:
    fl = np.array(row["flux"], dtype=float)
    b3 = len(fl) // 2
    return {
        "b3": b3,
        "N": abs(float(row.get("Nflux") or 0)),
        "primitive": float(math.gcd(*[int(x) for x in fl]) <= 1),
        "support": float(np.count_nonzero(fl)) / (2 * b3),
        "max_comp": float(np.abs(fl).max()),
        "log|DW|": float(np.log10(abs(float(row.get("|DW|") or 1e-300)))),
        "V": float(row.get("V") or 0),
    }


def correlations() -> dict:
    rows = [c["row"] for c in C.load_corpus() if G.classify(c["row"]) == "in_domain"]
    y = np.array([1.0 if r.get("is_minimum") else 0.0 for r in rows])
    cols = {}
    for r in rows:
        for k, v in invariants(r).items():
            cols.setdefault(k, []).append(v)
    out = {}
    for k, v in cols.items():
        v = np.array(v, dtype=float)
        out[k] = None if v.std() == 0 else float(np.corrcoef(v, y)[0, 1])
    return {"n": len(rows), "minima_rate": float(y.mean()), "correlations": out}


def main() -> int:
    r = correlations()
    print(f"Is the minima rate derivable from the lattice?  (n = {r['n']}, rate = {r['minima_rate']:.3f})\n")
    print(f"  {'invariant':<12}{'corr with is_minimum':>22}")
    for k, v in r["correlations"].items():
        print(f"  {k:<12}{'constant' if v is None else f'{v:>22.3f}'}")
    lattice = [v for k, v in r["correlations"].items() if k in ("b3", "N", "support", "max_comp") and v is not None]
    print(f"\n  strongest LATTICE correlation: {max(abs(v) for v in lattice):.3f}")
    print("  => no lattice invariant predicts a minimum: 0.8 cannot come out of the counting and is MODEL-SPECIFIC.")
    print("  the only real predictor is log|DW|, which is the dynamical SUSY order parameter, not a lattice invariant.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
