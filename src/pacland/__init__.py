"""PACLAND: Probably Approximately Correct Landscape.

A Valiant-verification system for the string landscape. This package holds the
verification and learnability tooling (builds #1 and #4); the physics oracle (L2)
plugs in later through the ``Oracle`` interface in ``learnability.sampler``.

The math these modules implement is specified in ``docs/``:

- ``certificate``  -> ``docs/verification-formal.md`` (Theorem 2, and the
  finite-set collapse of ``docs/observable-measure.md`` §5)
- ``error_model``  -> ``docs/oracle.md`` §4 and §6 (calibration)
- ``measure``      -> ``docs/observable-measure.md`` (log-space, weighted, finite)
- ``learnability`` -> ``docs/evolvability.md`` §5-§6 (SQ/VC conjecture)
"""
from __future__ import annotations

__version__ = "0.1.0"

from .certificate import (
    Certificate,
    empirical_exceedance,
    finite_d_certificate,
    hoeffding_radius,
    two_level_certificate,
)
from .error_model import CalibrationVerdict, ErrorModel, Kind, calibrate
from .measure import Measure, Observable

__all__ = [
    "Certificate",
    "empirical_exceedance",
    "finite_d_certificate",
    "hoeffding_radius",
    "two_level_certificate",
    "CalibrationVerdict",
    "ErrorModel",
    "Kind",
    "calibrate",
    "Measure",
    "Observable",
]
