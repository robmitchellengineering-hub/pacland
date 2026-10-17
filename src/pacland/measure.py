"""The observable measure D (``docs/observable-measure.md``).

Finite support, log-space convention. Provides i.i.d. sampling (with replacement)
and the exact finite-set disagreement rate used by ``finite_d_certificate``.
"""
from __future__ import annotations

import random
from dataclasses import dataclass


@dataclass(frozen=True)
class Observable:
    """One dimensionless observable, in log space (``docs/observable-measure.md`` §2)."""

    name: str
    target_log: float | None  # ln(c*); None = unmeasured (prediction zone)
    computable: bool          # can the oracle compute h(x) for this observable?

    @property
    def measured(self) -> bool:
        """True when the true target is known (verification zone)."""
        return self.target_log is not None


@dataclass(frozen=True)
class Measure:
    """A finite, weighted observable measure D.

    ``weights`` must be non-negative and sum to 1. The weight vector *is* the
    scientific commitment about which observables matter (``docs/observable-measure.md``
    §4); every certificate is conditional on it.
    """

    observables: tuple[Observable, ...]
    weights: tuple[float, ...]

    def __post_init__(self) -> None:
        if not self.observables:
            raise ValueError("at least one observable is required")
        if len(self.observables) != len(self.weights):
            raise ValueError("one weight per observable")
        if any(w < 0 for w in self.weights):
            raise ValueError("weights must be non-negative")
        if abs(sum(self.weights) - 1.0) > 1e-9:
            raise ValueError("weights must sum to 1")

    @classmethod
    def uniform(cls, observables: tuple[Observable, ...]) -> "Measure":
        """Uniform weights — the placeholder default, stated explicitly."""
        w = 1.0 / len(observables)
        return cls(observables, tuple(w for _ in observables))

    def sample_indices(self, n: int, rng: random.Random | None = None) -> list[int]:
        """i.i.d. sample of ``n`` observable indices, with replacement, per weights."""
        rng = rng or random.Random()
        return rng.choices(range(len(self.observables)), weights=self.weights, k=n)

    def exact_disagreement(
        self,
        h_logs: dict[str, float],
        oracle_logs: dict[str, float],
        threshold: float,
    ) -> float:
        """Finite-set exact ``p_g(threshold) = sum_i w_i * 1[ |ln(h/o)| > threshold ]``.

        ``docs/observable-measure.md`` §5. Requires a log-space value for every
        observable in the measure.
        """
        total = 0.0
        for obs, w in zip(self.observables, self.weights):
            if obs.name not in h_logs or obs.name not in oracle_logs:
                raise KeyError(f"missing value for observable {obs.name!r}")
            if abs(h_logs[obs.name] - oracle_logs[obs.name]) > threshold:
                total += w
        return total
