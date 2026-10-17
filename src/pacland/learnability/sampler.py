"""Flux-vacuum sampler for the learnability rig (build #4).

Generates synthetic "vacua" (integer flux vectors within a tadpole bound) for
testing. The real physics oracle (build #3) plugs in later: any callable mapping
``Vacuum -> dict[observable_name, log_value]`` is an oracle. Until then, tests use
synthetic concept classes with known VC dimension.
"""
from __future__ import annotations

import random
from dataclasses import dataclass


@dataclass(frozen=True)
class Vacuum:
    """A flux vacuum: an integer flux vector ``F3``/``H3``-like quanta."""

    flux: tuple[int, ...]

    def tadpole(self) -> int:
        """Quadratic tadpole proxy ``sum(f_i^2)``."""
        return sum(f * f for f in self.flux)


def sample_flux_vacua(
    n: int,
    dim: int,
    tadpole_bound: int,
    rng: random.Random | None = None,
) -> list[Vacuum]:
    """Rejection-sample ``n`` distinct flux vacua with ``sum(f_i^2) <= bound``.

    Each coordinate is drawn uniformly in ``[-floor(sqrt(bound)), floor(sqrt(bound))]``
    and the whole vector kept iff it satisfies the tadpole bound. Raises if the
    bound is too small to produce ``n`` distinct vectors.
    """
    if n <= 0:
        raise ValueError("n must be positive")
    if dim <= 0:
        raise ValueError("dim must be positive")
    if tadpole_bound < 0:
        raise ValueError("tadpole_bound must be non-negative")

    rng = rng or random.Random()
    lim = int(tadpole_bound ** 0.5)
    vacua: list[Vacuum] = []
    seen: set[tuple[int, ...]] = set()
    guard = 0
    max_attempts = max(n * 1000, 1000)
    while len(vacua) < n and guard < max_attempts:
        guard += 1
        flux = tuple(rng.randint(-lim, lim) for _ in range(dim))
        if sum(f * f for f in flux) <= tadpole_bound and flux not in seen:
            seen.add(flux)
            vacua.append(Vacuum(flux))
    if len(vacua) < n:
        raise RuntimeError(
            f"could not sample {n} distinct vacua; raise tadpole_bound or dim"
        )
    return vacua
