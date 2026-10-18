"""Empirical attack on the learnability conjecture — first datum.

Measures the richness of the real flux-vacua class and the structure of the
flux -> observable map, from ``data/vacua_sample.json`` (163 vacua, flux paired
with log|W0| and log(gs) in the same file).

Three tractable, defensible measures:

1. **rank** — linear span dimension of the flux vectors (Gaussian elimination).
2. **coordinate spread / distinctness** — the genotype's diversity.
3. **coordinate-observable correlation** — whether any single flux quantum drives
   an observable (sparse map) or the observable is "mixed" (no single coordinate).

Interpretation (honest): a full-rank flux class with ~zero per-coordinate
correlation means the observables are NOT sparsely determined — consistent with
the known statistical uniformity of W0. That is the "high-complexity" branch of
the learnability question, but it is a *weak* signal: linear correlation misses
nonlinear structure, and two observables cannot resolve the full conjecture.

Honest limits: 163 samples, 2 observables. First datum, not an answer.
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "vacua_sample.json")


def rank_float(vectors) -> int:
    """Rank of a list of integer vectors via Gaussian elimination (float)."""
    m = [list(map(float, v)) for v in vectors]
    rows, cols = len(m), len(m[0]) if m else 0
    rank = 0
    for c in range(cols):
        piv = next((r for r in range(rank, rows) if abs(m[r][c]) > 1e-9), None)
        if piv is None:
            continue
        m[rank], m[piv] = m[piv], m[rank]
        pv = m[rank][c]
        for r in range(rank + 1, rows):
            if abs(m[r][c]) > 1e-9:
                factor = m[r][c] / pv
                for cc in range(c, cols):
                    m[r][cc] -= factor * m[rank][cc]
        rank += 1
        if rank == rows:
            break
    return rank


def pearson(xs, ys) -> float:
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    sx = sum((x - mx) ** 2 for x in xs) ** 0.5
    sy = sum((y - my) ** 2 for y in ys) ** 0.5
    if sx == 0 or sy == 0:
        return 0.0
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (sx * sy)


def main() -> int:
    with open(DATA) as f:
        data = json.load(f)

    rows = []  # (flux, log_W0, log_gs)
    for d in data.values():
        for f, w, g in zip(d["flux"], d["log_W0"], d["log_gs"]):
            rows.append((f, w, g))

    n = len(rows)
    dim = len(rows[0][0])
    fluxes = [r[0] for r in rows]

    r = rank_float(fluxes)
    distinct = len({tuple(f) for f in fluxes})
    coord_spread = [
        max(f[i] for f in fluxes) - min(f[i] for f in fluxes) + 1 for i in range(dim)
    ]

    corr = {}
    for name, idx in [("log_W0", 1), ("log_gs", 2)]:
        ys = [r[idx] for r in rows]
        cs = [pearson([r[0][i] for r in rows], ys) for i in range(dim)]
        corr[name] = {
            "per_coord": [round(c, 3) for c in cs],
            "max_abs": round(max(abs(c) for c in cs), 3),
            "coords_above_0p3": sum(1 for c in cs if abs(c) > 0.3),
        }

    result = {
        "n_flux_vacua": n,
        "flux_dim": dim,
        "distinct_vectors": distinct,
        "rank": r,
        "rank_fraction_of_dim": round(r / dim, 3),
        "coord_spread": coord_spread,
        "correlation": corr,
        "reading": (
            "full-rank flux class + ~zero per-coordinate correlation => observables "
            "are mixed (not sparsely determined); high-complexity branch, weak signal."
        ),
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
