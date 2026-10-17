"""VC-dimension tools for the learnability rig (build #4).

The governing question of the whole system (``docs/evolvability.md`` §6, §7) is
whether the class ``C`` of vacuum-induced prediction functions has polynomial
VC/SQ dimension. This module provides the finite-class tools to measure a lower
bound on VC dimension from data, plus the sample-complexity planning formulas.

Exponential in the number of points — use toy sizes. The real SQ/VC measurement on
continuous flux data is a later, heavier step.
"""
from __future__ import annotations

from itertools import combinations
from math import log, sqrt


def shatters(hypotheses, points) -> bool:
    """Does the (finite) hypothesis class shatter the given points?

    ``hypotheses``: iterable of callables, each mapping a point to ``{0, 1}``.
    ``points``: iterable of point objects.

    A class shatters a point set iff it realizes all ``2^k`` binary labelings.
    """
    points = list(points)
    hypotheses = list(hypotheses)
    k = len(points)
    labelings = {tuple(h(p) for p in points) for h in hypotheses}
    return len(labelings) == 2 ** k


def vc_lower_bound(hypotheses, points) -> int:
    """Largest ``k`` such that some ``k``-subset of ``points`` is shattered.

    Shattering is downward-closed (a shattered set's subsets are shattered), so
    "some k-set is shattered" is monotone in ``k`` and we can stop at the first
    ``k`` with none. Exponential in ``len(points)``; toy sizes only.
    """
    points = list(points)
    hypotheses = list(hypotheses)
    n = len(points)
    for k in range(1, n + 1):
        if any(shatters(hypotheses, subset) for subset in combinations(points, k)):
            continue
        return k - 1
    return n


def sample_complexity(vc_dim: int, epsilon: float, delta: float, c: float = 1.0) -> float:
    """Uniform-convergence sample complexity, up to a constant.

        n >= c * (vc_dim * ln(1/eps) + ln(1/delta)) / eps^2

    ``c`` is a model-dependent constant; ``1.0`` is an illustrative default. This
    is the planning formula that decides whether L4 search is feasible at all
    (``docs/evolvability.md`` §6).
    """
    if epsilon <= 0.0 or delta <= 0.0:
        raise ValueError("epsilon and delta must be positive")
    return c * (vc_dim * log(1.0 / epsilon) + log(1.0 / delta)) / (epsilon ** 2)


def finite_class_radius(class_size: int, n: int, delta: float) -> float:
    """Union-bound confidence radius for a finite class of size ``|C|``.

        sqrt( ln(|C| / delta) / (2n) )

    ``docs/verification-formal.md`` §6: the cost of *search* over a finite class,
    as opposed to verifying a single candidate.
    """
    if n <= 0:
        raise ValueError("n must be positive")
    if not (0.0 < delta < 1.0):
        raise ValueError("delta must be in (0, 1)")
    if class_size <= 0:
        raise ValueError("class_size must be positive")
    return sqrt(log(class_size / delta) / (2.0 * n))
