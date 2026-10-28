"""The known-truth battery for causal estimators.

Every method used to estimate a causal effect — difference-in-differences, two-way fixed effects,
instrumental variables, regression discontinuity — can be scored on data where the true effect is
**known by construction**. Nobody publishes that as a standard. This package does.

The battery asks one question per cell: does the estimator recover the effect that was planted, on
data that looks like the data people actually use?
"""
from __future__ import annotations

__all__ = ["battery"]
