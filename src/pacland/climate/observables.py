"""Climate observable sets for the verification deficit — playbook item #1.

Honest classification, mirroring pacland's own V2 correction: a *validation
point* needs the model output O(x) and an independent observation c*(x) on the
**same** state x. For the future that never exists — so the projection target
is in the *prediction zone* (computable + not measured) and earns no certificate
term. Validation exists only on the historical record, and even there it is thin.

Statuses grounded in the 5-angle gap analysis (`docs/climate-gap-analysis.md`)
and the canonical measurement systems (CERES, Argo, satellite altimetry,
HadCRUT/GISTEMP/Berkeley; IPCC AR6 WG1). ``validated`` means the CMIP-class
ensemble reproduces the observed record within the observed/ensemble spread —
it does NOT mean "validated for the future."
"""
from __future__ import annotations

from ..deficit import DeficitObservable

# name,                measured, computable, validated
HISTORICAL_OBSERVABLES: tuple[DeficitObservable, ...] = (
    DeficitObservable("GMST (global-mean surface temperature)",        True, True, True),
    DeficitObservable("EEI (top-of-atmosphere energy imbalance)",      True, True, True),
    DeficitObservable("OHC (ocean heat content 0-2000 m)",             True, True, True),
    DeficitObservable("GMSL (global-mean sea level)",                  True, True, True),
    # everything below is measured + computable but NOT validated on the record
    DeficitObservable("Arctic sea-ice extent",              True, True, False),  # models underestimate decline
    DeficitObservable("AMOC strength",                      True, True, False),  # short record, wide spread
    DeficitObservable("ENSO amplitude",                     True, True, False),  # realism varies widely
    DeficitObservable("global precipitation pattern",       True, True, False),  # known tropical biases
    DeficitObservable("ice-sheet mass balance (GrIS/AIS)",  True, True, False),  # models lag observed acceleration
    DeficitObservable("heat-wave frequency/intensity",      True, True, False),  # attribution, not projection
    DeficitObservable("extreme precipitation",              True, True, False),  # coarse resolution
    DeficitObservable("tropical-cyclone intensity",         True, True, False),  # needs high-res; very weak
)

# The projection targets — what policy actually consumes. No future state is
# measured, so every one is computable + NOT measured = prediction zone.
PROJECTION_OBSERVABLES: tuple[DeficitObservable, ...] = (
    DeficitObservable("GMST(2100)",                    False, True, False),
    DeficitObservable("GMSL(2100)",                    False, True, False),
    DeficitObservable("Arctic sea-ice extent(2100)",   False, True, False),
    DeficitObservable("extreme-event frequency(2100)", False, True, False),
    DeficitObservable("regional precipitation(2100)",  False, True, False),
)

__all__ = ["HISTORICAL_OBSERVABLES", "PROJECTION_OBSERVABLES"]
