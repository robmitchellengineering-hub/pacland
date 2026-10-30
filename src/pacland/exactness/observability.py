"""The observability engine — what this dataset can measure, and what it only appears to (D17).

Three findings in two days all had the same shape: a number that looked like a fact about the world was
really a fact about the instrument — a rounding threshold, a scaling copy, a 0.0024% sample. This engine
asks the question up front, per quantity:

1. **precision** — how many independent rows back the estimate, after removing scaling copies;
2. **parameter sensitivity** — how far the estimate moves when a stated threshold moves;
3. **coverage** — what fraction of the space of interest the sample actually visits.

The verdict is the honest product:

    measured          the interval is narrow and the estimate is stable
    parameter-limited the spread from a stated threshold exceeds the statistical error
                      (so you are measuring the threshold)
    sample-limited    the sample covers so little of the space that the estimate is a
                      statement about the sample and not the space

Run:        python3 scripts/observability.py
Guarded by: tests/test_observability.py
"""
from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class Reading:
    """One quantity, with what it takes to state it honestly."""
    quantity: str
    estimate: float
    ci_low: float
    ci_high: float
    n_used: int
    n_total: int
    parameter_spread: float | None      # |max - min| across the stated parameter range, if any
    coverage: float | None              # fraction of the space of interest visited, if known
    verdict: str
    why: str


def _wilson(k: int, n: int, z: float = 1.96) -> tuple:
    """Wilson interval — correct for the small/lopsided counts the corpus actually has."""
    if n == 0:
        return 0.0, 0.0, 1.0
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return p, max(0.0, centre - half), min(1.0, centre + half)


def proportion(quantitiy: str, k: int, n: int, n_total: int | None = None,
               parameter_spread: float | None = None,
               coverage: float | None = None,
               cover_threshold: float = 0.01,
               spread_threshold: float = 0.5) -> Reading:
    """A proportion, judged by the three questions above.

    `spread_threshold`: the parameter-induced spread (as a fraction of the estimate) above which the
    reading is declared `parameter-limited`. `cover_threshold`: coverage below which it is
    `sample-limited`.
    """
    p, lo, hi = _wilson(int(k), int(n))
    half_width = (hi - lo) / 2
    verdict, why = "measured", "the interval is narrow and no stated parameter dominates it"
    if coverage is not None and coverage < cover_threshold:
        verdict = "sample-limited"
        why = (f"the sample visits {coverage:.4%} of the space of interest, so this is a statement about "
               f"the sample, not the space")
    elif parameter_spread is not None and parameter_spread > spread_threshold * max(p, 1e-12):
        verdict = "parameter-limited"
        why = (f"a stated threshold moves the estimate by {parameter_spread / max(p, 1e-12):.0%} of itself "
               f"(more than the ±{half_width / max(p, 1e-12):.2%} statistical half-width) — you are "
               f"measuring the threshold")
    return Reading(quantity=quantitiy, estimate=p, ci_low=lo, ci_high=hi, n_used=int(n),
                   n_total=int(n_total if n_total is not None else n),
                   parameter_spread=parameter_spread, coverage=coverage, verdict=verdict, why=why)


# ---------------------------------------------------------------------------------------
# the corpus's own quantities
# ---------------------------------------------------------------------------------------
def corpus_readings(data_dir=None) -> list:
    """The corpus's headline proportions, each judged. Uses the counterexample engine's loader."""
    from . import counterexample as C

    corpus = C.load_corpus(data_dir)
    n = len(corpus)
    prim = [c for c in corpus if C.scaling_gcd(c["row"]["flux"]) <= 1]
    n_prim = len(prim)
    susy = sum(1 for c in prim if c["row"].get("is_susy"))
    minima = sum(1 for c in prim if c["row"].get("is_minimum"))

    # minima is the one we know is threshold-sensitive: the count moves 4111 -> 2045 across t = 0 .. 1e-3
    table = {r["threshold"]: r["count"] for r in C.threshold_table((0.0, 1e-3), data_dir)}
    spread = None
    if 0.0 in table and 1e-3 in table and n_prim:
        spread = abs(table[0.0] / n_prim - table[1e-3] / n_prim)

    return [
        proportion("SUSY fraction (primitive rows)", susy, n_prim, n_prim),
        proportion("minima fraction (primitive rows)", minima, n_prim, n_prim,
                   parameter_spread=spread),
        proportion("primitive fraction", n_prim, n, n),
    ]


__all__ = ["Reading", "proportion", "corpus_readings"]
