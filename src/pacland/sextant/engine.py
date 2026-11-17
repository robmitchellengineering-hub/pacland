"""SEXTANT — the classifier: question -> simulate -> classify -> certificate."""
from __future__ import annotations

from . import phantom, registry
from .registry import Claim


def classify(claim: Claim) -> dict:
    """Run one claim through Phantom and return its verdict record."""
    number = phantom.compute(claim.id)
    return {
        "claim": claim.id,
        "question": claim.question,
        "value": claim.value,
        "simulate": number,
        "oracle_class": claim.oracle_class,
        "falsifier": claim.falsifier,
        "remedy": claim.remedy,
        "verdict": claim.verdict,
    }


def run(question: str) -> dict:
    """Match a natural-language question to a claim and classify it.

    Returns ``{"verdict": "UNKNOWN", ...}`` when no claim matches — an absence is
    never a pass (rule 67).
    """
    q = (question or "").strip().lower()
    for claim in registry.CLAIMS:
        if any(k in q for k in claim.keywords):
            return classify(claim)
    return {"question": question, "verdict": "UNKNOWN", "error": "no claim matches"}
