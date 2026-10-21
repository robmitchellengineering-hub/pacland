"""Drug-discovery verification-deficit report — playbook item #2.

Reuses the pacland certificate machinery unchanged. The result is two-tier:

  retrospective — benchmark-validated endpoints; m = 4, radius ~68%.
  prospective   — the novel molecule; m = 0 (no assay yet) → total.

Headline: a screening campaign's decision surface is validated over only ~4
retrospective assay endpoints, and the prospective hit — the molecule you would
actually synthesize — is extrapolation, not verification (Zhu et al. 2013: the
field's own census found ~18% PAINS and ~52% REOS failure among reported hits).
"""
from __future__ import annotations

from ..deficit import DeficitReport, deficit_report
from .observables import PROSPECTIVE_OBSERVABLES, RETROSPECTIVE_OBSERVABLES


def drug_deficit_report(delta_e: float = 0.025) -> tuple[DeficitReport, DeficitReport]:
    """Return ``(retrospective, prospective)`` deficit reports at budget ``delta_e``."""
    return (
        deficit_report(RETROSPECTIVE_OBSERVABLES, delta_e),
        deficit_report(PROSPECTIVE_OBSERVABLES, delta_e),
    )


def summary(delta_e: float = 0.025) -> str:
    """One plain-text block for the record (and the doc's headline)."""
    ret, pro = drug_deficit_report(delta_e)
    lines = [
        "DRUG-DISCOVERY VERIFICATION DEFICIT (playbook item #2)",
        "=" * 56,
        f"retrospective benchmark  m = {ret.n_validation} of {ret.n_observables} endpoints "
        f"measured+computable+validated",
        f"  -> certificate radius {ret.radius:.3f} (delta_e = {delta_e})",
        f"prospective novel molecule  m = {pro.n_validation} of {pro.n_observables} "
        f"(prediction zone: {pro.n_prediction_zone})",
        f"  -> {'VACUOUS (radius = inf)' if pro.vacuous else f'radius {pro.radius:.3f}'}",
        "",
        "A hit's decision surface is validated only over ~4 retrospective endpoints;",
        "the novel molecule you would synthesize is extrapolation, not verification.",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    print(summary())
