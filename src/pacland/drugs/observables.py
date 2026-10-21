"""Drug observable sets for the verification deficit — playbook item #2.

Honest classification, mirroring climate (and pacland's own V2 correction): a
*validation point* needs the model output O(x) and an independent measurement
c*(x) on the **same** compound. On a benchmark that pairing exists (retrospective);
for a **novel molecule there is no assay yet**, so every predicted endpoint is
computable + not measured = prediction zone.

Statuses grounded in the 5-angle gap analysis (`docs/drugs-gap-analysis.md`):
PDBbind / TDC / ChEMBL are the measured yardsticks. ``validated`` means the model
reproduces the measured endpoint within the benchmark tolerance — it does NOT mean
"validated for a novel scaffold."
"""
from __future__ import annotations

from ..deficit import DeficitObservable

# name,                    measured, computable, validated
RETROSPECTIVE_OBSERVABLES: tuple[DeficitObservable, ...] = (
    DeficitObservable("binding affinity (PDBbind)",        True, True, True),
    DeficitObservable("aqueous solubility (TDC)",          True, True, True),
    DeficitObservable("hERG liability (TDC)",              True, True, True),
    DeficitObservable("hepatic clearance (TDC)",           True, True, True),
    # measured + computable but NOT benchmark-validated to the same confidence
    DeficitObservable("plasma protein binding",            True, True, False),
    DeficitObservable("blood-brain barrier penetration",   True, True, False),
    DeficitObservable("metabolic stability",               True, True, False),
    DeficitObservable("mutagenicity / toxicity",           True, True, False),
    DeficitObservable("synthesizability (RAScore)",        True, True, False),
    DeficitObservable("cytotoxicity",                      True, True, False),
)

# The prospective hit — the novel molecule you would actually synthesize.
# No assay value exists, so every endpoint is computable + NOT measured.
PROSPECTIVE_OBSERVABLES: tuple[DeficitObservable, ...] = (
    DeficitObservable("binding affinity (novel molecule)",  False, True, False),
    DeficitObservable("solubility (novel molecule)",        False, True, False),
    DeficitObservable("hERG (novel molecule)",              False, True, False),
    DeficitObservable("clearance (novel molecule)",         False, True, False),
    DeficitObservable("toxicity (novel molecule)",          False, True, False),
)

__all__ = ["RETROSPECTIVE_OBSERVABLES", "PROSPECTIVE_OBSERVABLES"]
