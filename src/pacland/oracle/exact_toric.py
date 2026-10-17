"""Exact (zero-error) toy oracle on a toric background — build #2 seed.

On a toroidal/orbifold compactification the physics is exactly computable, so the
oracle has no numerical approximation and its error model is trivially calibrated.
This module is the smallest such case: one observable with a closed form, used to
validate the whole certificate loop before any approximate oracle exists.

Illustrative — the observable is a toy closed form, not a physical result.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

from ..error_model import ErrorModel, Kind


@dataclass(frozen=True)
class ToricBackground:
    """A toy toric background. Illustrative, not a physical result."""

    label: str
    flux: tuple[int, ...]

    def tadpole(self) -> int:
        """Quadratic tadpole proxy ``sum(f_i^2)``."""
        return sum(f * f for f in self.flux)


def exact_toric_oracle(background: ToricBackground) -> dict[str, float]:
    """Exact observable for a toy toric background.

    ``gauge_coupling_log = -ln(1 + tadpole)`` — a closed form with *no* numerical
    approximation, so the oracle error is identically zero. This is the build-#2
    premise in miniature: run the certificate loop on a background where the
    oracle has zero systematic error, to validate the pipeline itself.
    """
    return {"gauge_coupling_log": -math.log(1.0 + background.tadpole())}


def zero_error_model(validated: bool = True) -> ErrorModel:
    """The error model of the exact oracle: zero bias, zero scale, zero tail."""
    return ErrorModel(
        bias=0.0,
        scale=0.0,
        beta=0.0,
        delta_beta=0.0,
        kind=Kind.INTERVAL,
        validated=validated,
    )
