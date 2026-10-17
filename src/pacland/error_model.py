"""Per-observable error model and calibration (L2 contract).

Implements ``docs/oracle.md`` §4 (the error model) and §6 (the calibration
protocol). The error model is the oracle's *claim* about its own error
``e(x) = O(x) - c*(x)``; calibration is what turns that claim into something the
certificate may use.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .certificate import hoeffding_radius


class Kind(str, Enum):
    """Allowed error-model kinds (``docs/oracle.md`` §4)."""

    INTERVAL = "interval"
    EMPIRICAL = "empirical"
    UNKNOWN = "unknown"


class CalibrationVerdict(str, Enum):
    """Outcome of comparing a claimed tail bound against validation data."""

    WELL_CALIBRATED = "well-calibrated"
    MISCALIBRATED = "miscalibrated"
    INSUFFICIENT_DATA = "insufficient-data"


@dataclass(frozen=True)
class ErrorModel:
    """A claim about the oracle error for one observable.

    Fields
    ------
    bias, scale:
        systematic offset and dispersion of ``e(x)``.
    beta:
        tail threshold; the claim is ``|e(x)| <= beta``.
    delta_beta:
        claimed exceedance rate ``Pr[|e(x)| > beta] <= delta_beta``.
    kind:
        one of ``Kind``.
    validated:
        whether this model has been calibrated in the verification zone
        (``docs/oracle.md`` §7). A certificate may only use ``validated=True``
        models; ``False`` means extrapolated (prediction zone).
    """

    bias: float
    scale: float
    beta: float
    delta_beta: float
    kind: Kind
    validated: bool


def calibrate(
    claimed_delta_beta: float,
    p_hat_e: float,
    m: int,
    delta_e: float,
) -> CalibrationVerdict:
    """``docs/oracle.md`` §6 — compare a claimed tail against empirical data.

    The oracle's model is *well-calibrated* iff the empirical exceedance rate, plus
    its one-sided Hoeffding radius, does not exceed the claimed rate:

        p_hat_e + hoeffding_radius(m, delta_e) <= claimed_delta_beta

    ``m == 0`` (no validation points) yields ``INSUFFICIENT_DATA``.
    """
    if m <= 0:
        return CalibrationVerdict.INSUFFICIENT_DATA
    if not (0.0 <= claimed_delta_beta <= 1.0):
        raise ValueError("claimed_delta_beta must be in [0, 1]")
    if not (0.0 <= p_hat_e <= 1.0):
        raise ValueError("p_hat_e must be in [0, 1]")
    radius = hoeffding_radius(m, delta_e)
    if p_hat_e + radius <= claimed_delta_beta:
        return CalibrationVerdict.WELL_CALIBRATED
    return CalibrationVerdict.MISCALIBRATED
