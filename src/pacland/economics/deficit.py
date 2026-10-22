"""Economics verification-deficit report — playbook item #3.

Reuses the pacland certificate machinery unchanged (``..certificate``, ``..deficit``).
The result is two-tier:

  retrospective — the observed/backcast record; m = 4, radius ~68%.
  prospective   — the forecast / policy counterfactual; m = 0 (no future is measured).

Headline: a macroeconomic model's decision surface is validated over only ~4 backcast
series, and its policy forecast — the object central banks actually act on — is
extrapolation, not verification (Meese–Rogoff 1983; Rossi 2013: the field's own record
is the failure to beat a random walk out of sample).

Pure stdlib + the existing pacland modules.
"""
from __future__ import annotations

from ..deficit import DeficitReport, deficit_report
from .observables import PROSPECTIVE_OBSERVABLES, RETROSPECTIVE_OBSERVABLES


def economics_deficit_report(delta_e: float = 0.025) -> tuple[DeficitReport, DeficitReport]:
    """Return ``(retrospective, prospective)`` deficit reports at budget ``delta_e``."""
    return (
        deficit_report(RETROSPECTIVE_OBSERVABLES, delta_e),
        deficit_report(PROSPECTIVE_OBSERVABLES, delta_e),
    )


def summary(delta_e: float = 0.025) -> str:
    """One plain-text block for the record (and the doc's headline)."""
    ret, pro = economics_deficit_report(delta_e)
    lines = [
        "ECONOMICS VERIFICATION DEFICIT (playbook item #3)",
        "=" * 48,
        f"retrospective backcast  m = {ret.n_validation} of {ret.n_observables} series "
        f"measured+computable+validated",
        f"  -> certificate radius {ret.radius:.3f} (delta_e = {delta_e})",
        f"prospective forecast  m = {pro.n_validation} of {pro.n_observables} "
        f"(prediction zone: {pro.n_prediction_zone})",
        f"  -> {'VACUOUS (radius = inf)' if pro.vacuous else f'radius {pro.radius:.3f}'}",
        "",
        "A model's decision surface is validated only over ~4 backcast series;",
        "its policy forecast is extrapolation, not verification.",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    print(summary())
