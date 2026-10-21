"""Climate verification-deficit report — playbook item #1.

Reuses the pacland certificate machinery unchanged (``..certificate``,
``..deficit``). The result is two-tier:

  historical  — the only place validation is possible; m = 4, radius ~68%.
  projection  — the policy target; m = 0 (no future state is measured) → total.

Headline: a climate model's fit to the observed past is certified only to ~68%
tolerance over 4 observables, and its 2100 projection is — strictly —
extrapolation, not verification.

Pure stdlib + the existing pacland modules.
"""
from __future__ import annotations

from ..deficit import DeficitReport, deficit_report
from .observables import HISTORICAL_OBSERVABLES, PROJECTION_OBSERVABLES


def climate_deficit_report(delta_e: float = 0.025) -> tuple[DeficitReport, DeficitReport]:
    """Return ``(historical, projection)`` deficit reports at confidence budget ``delta_e``."""
    return (
        deficit_report(HISTORICAL_OBSERVABLES, delta_e),
        deficit_report(PROJECTION_OBSERVABLES, delta_e),
    )


def summary(delta_e: float = 0.025) -> str:
    """One plain-text block for the record (and the doc's headline)."""
    hist, proj = climate_deficit_report(delta_e)
    lines = [
        "CLIMATE VERIFICATION DEFICIT (playbook item #1)",
        "=" * 48,
        f"historical record  m = {hist.n_validation} of {hist.n_observables} observables "
        f"measured+computable+validated",
        f"  -> certificate radius {hist.radius:.3f} (delta_e = {delta_e})",
        f"projection targets m = {proj.n_validation} of {proj.n_observables} "
        f"(prediction zone: {proj.n_prediction_zone})",
        f"  -> {'VACUOUS (radius = inf)' if proj.vacuous else f'radius {proj.radius:.3f}'}",
        "",
        "A model's fit to the observed past is certified only to ~68% tolerance;",
        "its 2100 projection is extrapolation, not verification.",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    print(summary())
