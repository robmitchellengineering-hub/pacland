"""Verification Deficit Report — approach #6 in PACLAND-V2-PLAN.md.

Quantifies how far string theory is from being verifiable, by counting the
observables that are simultaneously *computable* (the oracle can evaluate them),
*measured* (an independent target c* exists), and *validated* (the oracle's error
model is calibrated against c*). Only those count toward the certificate's
oracle-validation term ``m``.

**Correction over v1:** the ~19 measured Standard-Model parameters are *targets*,
not *validation points*. A validation point needs both the oracle's output O(x)
and an independent c*(x) on the *same* x. For our universe we know c* but not O
(the compactification is unknown); for exact/tractable backgrounds we can compute
O but they are not our universe. So ``m`` is the number of exact/tractable cases
with both — today ~0 — which makes the deficit *total*, not the ~31% that the
finite-observable bound naively suggests.

Pure stdlib; no physics tools. The honest product of approach #6 is this report,
not a vacuum.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import inf

from .certificate import hoeffding_radius


@dataclass(frozen=True)
class DeficitObservable:
    """One observable, classified for the deficit report.

    ``measured``  — an independent target c* exists (experimental value).
    ``computable``— the oracle can evaluate O(x) for it (even approximately).
    ``validated`` — the oracle's error model is calibrated in the verification
    zone (``docs/oracle.md`` §7). A certificate may use only validated models.
    """

    name: str
    measured: bool
    computable: bool
    validated: bool


@dataclass(frozen=True)
class DeficitReport:
    """The counted 2x2 plus the resulting certificate radius."""

    n_observables: int
    n_measured: int          # c* known
    n_computable: int        # O can evaluate
    n_validation: int        # measured AND computable AND validated -> the real m
    n_prediction_zone: int   # computable AND NOT measured (falsifiable later)
    n_unverifiable: int      # measured AND NOT computable
    delta_e: float
    radius: float            # Hoeffding radius on the validation set; inf if empty

    @property
    def vacuous(self) -> bool:
        """True when no observable is simultaneously computable+measured+validated."""
        return self.n_validation == 0


def deficit_report(observables, delta_e: float = 0.025) -> DeficitReport:
    """Count the verification zone and compute the honest certificate radius.

    ``n_validation`` (the real ``m``) is the observables where the oracle can
    compute AND the target is known AND the error model is calibrated. Everything
    else contributes nothing to the certificate today (``docs/observable-measure.md``
    §6: only the top-left cell tightens the certificate).
    """
    obs = list(observables)
    n_measured = sum(o.measured for o in obs)
    n_computable = sum(o.computable for o in obs)
    n_validation = sum(o.measured and o.computable and o.validated for o in obs)
    n_prediction = sum(o.computable and not o.measured for o in obs)
    n_unverifiable = sum(o.measured and not o.computable for o in obs)
    radius = hoeffding_radius(n_validation, delta_e) if n_validation > 0 else inf
    return DeficitReport(
        n_observables=len(obs),
        n_measured=n_measured,
        n_computable=n_computable,
        n_validation=n_validation,
        n_prediction_zone=n_prediction,
        n_unverifiable=n_unverifiable,
        delta_e=delta_e,
        radius=radius,
    )
