"""Economic observable sets for the verification deficit — playbook item #3.

Honest classification, mirroring climate and drugs: a *validation point* needs the
model output O(x) and an independent measurement c*(x) on the **same** state x. On the
observed record that pairing exists (backcast); for the **future** there is no
measurement yet, so every forecast target is computable + not measured = prediction
zone.

Statuses grounded in the 5-angle gap analysis (`docs/economics-gap-analysis.md`) and
the field's own forecast-evaluation record (Meese–Rogoff 1983, Rossi 2013, Gürkaynak
et al. on DSGE-vs-VAR). ``validated`` means the model reproduces the measured series
*in-sample/backcast* — it does NOT mean "validated out-of-sample", which is what a
forecast actually is, and where the field's record is the failure to beat a random walk.
"""
from __future__ import annotations

from ..deficit import DeficitObservable

# name,                        measured, computable, validated
RETROSPECTIVE_OBSERVABLES: tuple[DeficitObservable, ...] = (
    DeficitObservable("real GDP growth",        True, True, True),
    DeficitObservable("CPI inflation",          True, True, True),
    DeficitObservable("unemployment rate",      True, True, True),
    DeficitObservable("short-term policy rate", True, True, True),
    # measured + computable but NOT validated to the same confidence (in-sample fit,
    # and the field's own out-of-sample record is the failure to beat a random walk)
    DeficitObservable("current-account balance",   True, True, False),
    DeficitObservable("wage growth",               True, True, False),
    DeficitObservable("labour-productivity growth",True, True, False),
    DeficitObservable("consumption growth",        True, True, False),
    DeficitObservable("residential investment",    True, True, False),
    DeficitObservable("house-price growth",        True, True, False),
)

# The forecast / policy counterfactual — what a central bank or treasury actually acts
# on. No future state is measured, so every target is computable + NOT measured.
PROSPECTIVE_OBSERVABLES: tuple[DeficitObservable, ...] = (
    DeficitObservable("real GDP growth (t+h)",      False, True, False),
    DeficitObservable("CPI inflation (t+h)",        False, True, False),
    DeficitObservable("unemployment rate (t+h)",    False, True, False),
    DeficitObservable("policy-rate path (t+h)",     False, True, False),
    DeficitObservable("recession probability (t+h)",False, True, False),
)

__all__ = ["RETROSPECTIVE_OBSERVABLES", "PROSPECTIVE_OBSERVABLES"]
