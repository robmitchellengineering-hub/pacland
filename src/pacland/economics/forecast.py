"""Forecast failure — the empirical axis (axis 1) of the economics Rule of Three.

Axis 2 (theoretical) is set-identification; axis 3 (structural) is the accounting
guard-suite. This module is axis 1: the empirical claim that a macro forecast does not
beat a naive benchmark out of sample (Meese–Rogoff 1983, Rossi 2013, Gürkaynak et al.),
so it is extrapolation, not verification.

The check is a runnable forecast evaluation: compare a model's one-step-ahead forecast
error against the no-change (random-walk) benchmark. It is mutation-tested both ways —
a model with no skill leaves the axis-1 claim standing, a model with real skill (an
oracle) falsifies it.

Floating-point by nature (RMSE has a square root); the rest of the discipline is exact.
"""
from __future__ import annotations

import math


def rmse(errors):
    """Root-mean-square error of a list of residuals."""
    if not errors:
        return float("nan")
    return math.sqrt(sum(e * e for e in errors) / len(errors))


def forecast_failure(model_forecasts, actuals):
    """Compare one-step-ahead forecasts against the no-change benchmark.

    ``model_forecasts[t]`` is the forecast for ``actuals[t+1]`` (length
    ``len(actuals)-1``). The naive benchmark predicts ``actuals[t+1] = actuals[t]``.
    Returns a dict with ``model_rmse``, ``naive_rmse`` and ``beat``."""
    n = len(actuals)
    if len(model_forecasts) != n - 1:
        raise ValueError("one-step-ahead forecasts must align with actuals")
    model_err = []
    naive_err = []
    for t in range(1, n):
        model_err.append(model_forecasts[t - 1] - actuals[t])
        naive_err.append(actuals[t - 1] - actuals[t])
    m = rmse(model_err)
    k = rmse(naive_err)
    return {"model_rmse": m, "naive_rmse": k, "beat": m < k}


def guard_forecast_is_extrapolation(model_forecasts, actuals):
    """Axis-1 guard: the claim "a macro forecast is extrapolation, not verification"
    holds for this model iff it does NOT beat the no-change benchmark out of sample.

    Fails (red) when the model DOES beat the benchmark — i.e. the model has real
    forecast skill and the axis-1 claim is falsified for it. Returns ``(ok, message)``."""
    r = forecast_failure(model_forecasts, actuals)
    if r["beat"]:
        return (False,
                f"beats no-change (model RMSE {r['model_rmse']:.4f} < naive {r['naive_rmse']:.4f})"
                " — real skill, axis-1 falsified")
    return (True,
            f"no skill (model RMSE {r['model_rmse']:.4f} >= naive {r['naive_rmse']:.4f})"
            " — extrapolation, not verification")


__all__ = ["rmse", "forecast_failure", "guard_forecast_is_extrapolation"]
