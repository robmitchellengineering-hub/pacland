"""Structure mining — which observables carry geometric information?

The new approach (``docs/new-approach.md``) is constraint-first: find the observables
whose values are *structured* (dependent on the flux / geometry) as opposed to *random*
(uniform, like W0 — the negative result). The tool here is **non-linear**: mutual
information, not Pearson correlation, so it catches structure that linear correlation
misses. Significance is judged by a permutation test against the null "observable is
independent of flux".

Pure stdlib. Finite-sample mutual information is biased; the permutation test is what
separates real structure from that bias.
"""
from __future__ import annotations

import random
from math import log2


def _bin_indices(vals, bins):
    lo, hi = min(vals), max(vals)
    if hi == lo:
        return [0] * len(vals)
    return [min(int((v - lo) / (hi - lo) * bins), bins - 1) for v in vals]


def _entropy(counts) -> float:
    total = sum(counts.values())
    if total == 0:
        return 0.0
    return -sum((c / total) * log2(c / total) for c in counts.values() if c > 0)


def mutual_information(xs, ys, bins: int = 8) -> float:
    """Estimated mutual information I(X;Y) via 2D binning (naive estimator).

    Returns bits. A naive estimator is biased upward for small samples; use
    ``mi_significance`` to judge whether a value is above that bias.
    """
    n = len(xs)
    if n < 2 or len(xs) != len(ys):
        raise ValueError("need equal-length inputs of length >= 2")
    bx = _bin_indices(list(xs), bins)
    by = _bin_indices(list(ys), bins)
    joint: dict = {}
    mx: dict = {}
    my: dict = {}
    for i in range(n):
        joint[(bx[i], by[i])] = joint.get((bx[i], by[i]), 0) + 1
        mx[bx[i]] = mx.get(bx[i], 0) + 1
        my[by[i]] = my.get(by[i], 0) + 1
    return _entropy(mx) + _entropy(my) - _entropy(joint)


def mi_significance(
    xs, ys, bins: int = 8, permutations: int = 200, seed: int = 0
) -> dict:
    """Permutation test: is I(X;Y) larger than chance?

    Shuffles y, recomputes MI, and reports the z-score of the true MI against the
    null distribution. ``|z| >= 3`` is the usual "real structure" threshold.
    """
    rng = random.Random(seed)
    true = mutual_information(xs, ys, bins)
    ys_list = list(ys)
    null = []
    for _ in range(permutations):
        rng.shuffle(ys_list)
        null.append(mutual_information(xs, ys_list, bins))
    mean = sum(null) / len(null)
    var = sum((v - mean) ** 2 for v in null) / len(null)
    std = var ** 0.5
    z = (true - mean) / std if std > 0 else 0.0
    return {"mi": true, "null_mean": mean, "z": z}


def classify_observable(
    flux_cols, y, bins: int = 8, permutations: int = 200, z_threshold: float = 3.0
) -> dict:
    """Classify one observable as ``structured`` or ``random``.

    ``flux_cols`` is a list of lists — one per flux coordinate, each the same length
    as ``y``. Returns the max MI over coordinates, its z-score, and the verdict.
    """
    best = {"mi": 0.0, "z": 0.0, "coord": -1}
    for i, col in enumerate(flux_cols):
        r = mi_significance(col, y, bins=bins, permutations=permutations)
        if r["mi"] > best["mi"]:
            best = {"mi": r["mi"], "z": r["z"], "coord": i}
    verdict = "structured" if best["z"] >= z_threshold else "random"
    return {
        "verdict": verdict,
        "max_mi": best["mi"],
        "max_z": best["z"],
        "coord": best["coord"],
    }
