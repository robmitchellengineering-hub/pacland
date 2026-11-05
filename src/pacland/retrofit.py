"""Retro-fit the estate's qualitative confidence labels into numeric priors and score them.

Build 2 of the belief layer (``PLANS/PLAN-subjective-probability-belief-layer.md``).
The research arm (``docs/plan-bold-claims.md``) attached words — "High", "Medium-high",
"Medium" — to its hypotheses, and ``docs/falsifiable-predictions.md`` recorded real
outcomes. Neither was a number. This module turns the words into priors and scores the
priors that also have an outcome, producing the estate's FIRST calibration number.

The moment of truth the plan names: if that number shows the confidence was uncalibrated,
the ledger is the fix, not a decoration — and the direction matches Tetlock.
"""
from __future__ import annotations

from dataclasses import dataclass

from .belief import brier_score, log_score

#: Confidence label -> numeric prior. Fixed and documented so the retro-fit is
#: reproducible rather than a fresh judgement each run.
CONFIDENCE_PRIOR = {
    "high": 0.85,
    "medium-high": 0.70,
    "medium": 0.50,
    "low": 0.25,
}


@dataclass(frozen=True)
class Forecast:
    """One scored claim: a numeric prior and whether it held."""

    name: str
    prior: float
    held: bool  # True = held (confirmed/proven); False = refuted/falsified


#: The scoreable set: claims that carried a stated confidence AND have a recorded
#: outcome. n is small on purpose — before this layer, nothing else had both.
LEDGER = (
    Forecast("B1 landscape statistics depend on the tadpole alone", 0.85, False),
    Forecast("prediction #11 GDPNow edge shrinks on the revised value", 0.70, False),
    Forecast("prediction #8 NK3 domain is zero net inflation", 0.85, True),
)


def prior_from_label(label: str) -> float:
    """Map a qualitative confidence label to its numeric prior."""
    key = label.strip().lower()
    if key not in CONFIDENCE_PRIOR:
        raise ValueError(
            f"unknown confidence label {label!r}; known: {sorted(CONFIDENCE_PRIOR)}"
        )
    return CONFIDENCE_PRIOR[key]


def calibrate(forecasts: list[Forecast]) -> dict:
    """Mean Brier and log score over a ledger; lower is better.

    A forecaster that always reports the base rate scores a Brier near 0.25 for a
    balanced record, so that is the calibration watermark.
    """
    if not forecasts:
        raise ValueError("no forecasts to score")
    n = len(forecasts)
    brier = sum(brier_score(f.prior, f.held) for f in forecasts) / n
    log = sum(log_score(f.prior, f.held) for f in forecasts) / n
    return {"n": n, "brier": brier, "log": log}


def report() -> str:
    """The first calibration number, as one sentence a person can read."""
    c = calibrate(list(LEDGER))
    verdict = "miscalibrated (overconfident)" if c["brier"] > 0.25 else "within range"
    return (
        f"{c['n']} scored claims — mean Brier {c['brier']:.3f}, log {c['log']:.3f}. "
        f"A base-rate forecaster sits near Brier 0.25, so this is {verdict} on "
        f"n={c['n']} — preliminary, and the direction matches Tetlock."
    )


__all__ = ["CONFIDENCE_PRIOR", "Forecast", "LEDGER", "calibrate", "prior_from_label", "report"]
