"""humor_info.py — humor ↔ information theory: funniness is a function of the punchline's Shannon surprise.

The correspondence: a joke's setup induces a probability distribution over continuations; the punchline is
one continuation with probability p = P(punchline | setup). Its Shannon surprise is s = −log₂ p. The claim:
funniness is a QUANTITATIVE function of s — rising with s (incongruity), peaking at an optimal s (the
resolution), then falling for incoherent/random surprise. A testable law, not the usual qualitative
'incongruity-resolution' story.
"""
from __future__ import annotations

import math


def surprise(p: float) -> float:
    """The Shannon surprise (bits) of a punchline with prior probability p."""
    return -math.log2(p)


def funniness(s: float, s_star: float = 4.0, width: float = 2.0) -> float:
    """The inverted-U: funniness peaks at the optimal surprise s_star (resolved incongruity)."""
    return math.exp(-((s - s_star) ** 2) / (2 * width ** 2))


def prediction() -> dict:
    # three jokes: predictable (high p), optimal (intermediate p), random (tiny p)
    predictable = surprise(0.5)          # 1 bit — too obvious
    optimal = surprise(0.0625)           # 4 bits — the "aha" surprise
    random = surprise(0.001)             # ~10 bits — incoherent
    return {
        "prediction": "funniness is a measurable, inverted-U function of the punchline's Shannon surprise "
                      "−log₂ p — peaking at an optimal surprise, not monotone",
        "predictable_joke_surprise_bits": round(predictable, 1),
        "optimal_joke_surprise_bits": round(optimal, 1),
        "random_joke_surprise_bits": round(random, 1),
        "funniness_predictable": round(funniness(predictable), 3),
        "funniness_optimal": round(funniness(optimal), 3),
        "funniness_random": round(funniness(random), 3),
        "novelty": "the incongruity-resolution theory of humor is QUALITATIVE (Suls 1972); a QUANTITATIVE "
                   "funniness(surprise) law with a measured optimal point is the unclaimed claim",
        "confirming_data": "rate jokes: compute each punchline's −log₂ p from a language model, then "
                           "correlate with human funniness ratings — is the inverted-U there?",
    }
