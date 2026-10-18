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
- ``selection``    -> ``docs/selection.md`` (the measure-verifier / typicality test)
- ``structure``    -> ``docs/new-approach.md`` (structure mining: which observables
  carry geometric information)
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
from .constraints import elimination_certificate, elimination_fraction
from .deficit import DeficitObservable, DeficitReport, deficit_report
from .error_model import CalibrationVerdict, ErrorModel, Kind, calibrate
from .measure import Measure, Observable
from .selection import TypicalityVerdict, ks_uniformity, quantile, typicality_test
from .structure import (
    classify_observable,
    cv_predictability,
    mi_significance,
    mutual_information,
    ridge_cv_predictability,
)

__all__ = [
    "Certificate",
    "empirical_exceedance",
    "finite_d_certificate",
    "hoeffding_radius",
    "two_level_certificate",
    "elimination_certificate",
    "elimination_fraction",
    "CalibrationVerdict",
    "DeficitObservable",
    "DeficitReport",
    "deficit_report",
    "ErrorModel",
    "Kind",
    "calibrate",
    "Measure",
    "Observable",
    "TypicalityVerdict",
    "ks_uniformity",
    "quantile",
    "typicality_test",
    "classify_observable",
    "mi_significance",
    "mutual_information",
    "cv_predictability",
    "ridge_cv_predictability",
]
