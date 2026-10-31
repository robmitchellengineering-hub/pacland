"""The invariant `I(b3)` — one integer behind classification **and** accessibility.

`docs/plan-bold-claims.md` names the unification-shaped target: a single function of `b3` that predicts both the
*classification* of flux vacua and their *accessibility to sampling*. Two facts make that plausible rather than
sloganeering:

    classification    max|N| = b3 exactly in a |component| <= 1 window
    accessibility     the sampler's per-try success rate falls with h12

Both are governed by the same integer, so the question is whether **one** function fits both — or whether the two
scales are unrelated and the coincidence of `b3` is just the dimension appearing twice.

## The law, stated BEFORE the measurement

    rate(b3) = rate(b3=6) * exp(-c * (b3 - 6)),      c = ln(rate(6)/rate(12)) / 6

With the two existing points — `0.1325` at `h12 = 2` (`b3 = 6`) and `0.00137` at `h12 = 5` (`b3 = 12`) — the fit
gives `c = 0.763`, and the **falsifiable predictions**:

| `h12` | `b3` | predicted rate per try | predicted points per 400-try call |
|---|---|---|---|
| 3 | 8 | 0.0290 | 11.6 |
| 4 | 10 | 0.00637 | 2.6 |

**These were written before the run** (dispatch `2026-10-31T0502Z`, 20 calls each). A law stated after seeing the
data is a description; stated before, it is a test.

**What a confirmation means:** one parameter `c` links dimension to accessibility, and composed with
`max|N| = b3` gives the statement *"the same integer sets what exists and what can be found"* — the closest thing
to a unification-shaped claim this arm has.

**What a refutation means:** the rate does not track `b3` alone, so the two scales are unrelated and `I(b3)` is
not one invariant. That is equally a result and would send the work back to the sampler, not to the lattice.

Run:        python3 scripts/invariant.py
Guarded by: tests/test_invariant.py
"""
from __future__ import annotations

import math

#: The two anchor measurements the law is fitted to (h12, b3, points per try).
ANCHORS = ((2, 6, 0.1325), (5, 12, 0.00137))

#: The measurements that test it.
MEASURED = ((3, 8), (4, 10))

#: What the first run actually produced (dispatch `0511Z-invariant-law2`, 2026-10-31).
#: `h12 = 3`: **20 of 20 calls raised** and the message was swallowed by a `-1` sentinel (the run's own
#: instrumentation defect — a sentinel hid the diagnosis, which the next run must not repeat).
#: `h12 = 4`: 8 and 10 points in the first two calls, against a prediction of 2.5 per call.
OBSERVED = {
    3: {"status": "unmeasurable", "raise_count": 20, "calls": 20,
        "why": "every call raised; the exception text was discarded by a -1 sentinel"},
    4: {"status": "in progress (partial)", "sample": [8, 10], "predicted_per_call": 2.5},
}


def b3_of(h12: int) -> int:
    """`b3 = 2 h12 + 2` for this class of model."""
    return 2 * h12 + 2


def fit_c(anchors=ANCHORS) -> float:
    """The exponential coefficient from the two anchors."""
    (h1, b1, r1), (h2, b2, r2) = anchors
    return math.log(r1 / r2) / (b2 - b1)


def predicted_rate(h12: int, c: float | None = None) -> float:
    """Rate per try predicted at `h12` — computed from the law, not from data."""
    c = fit_c() if c is None else c
    return ANCHORS[0][2] * math.exp(-c * (b3_of(h12) - ANCHORS[0][1]))


def prediction_table() -> list:
    return [{"h12": h, "b3": b3_of(h), "rate_per_try": predicted_rate(h),
             "points_per_400": 400 * predicted_rate(h)} for h, _ in MEASURED]


def verdict(measured: dict | None = None, observed: dict | None = None) -> dict:
    """Compare the law with the measurements when they exist; state the verdict either way."""
    if observed is not None:
        return {"status": "provisional — h12=3 unmeasurable, h12=4 partial", "observed": observed,
                "c": fit_c(),
                "note": ("h12=3 raised on every call with the message discarded; h12=4 gave 8 and 10 points "
                         "in its first two calls against a predicted 2.5, i.e. 3-4x above the law"),
                "composition": ("if h12=4 holds above prediction, the rate does not follow a single "
                                "exponential in b3: the classification and accessibility scales are unrelated "
                                "and I(b3) is not one invariant")}
    measured = measured or {}
    rows = []
    for h in (3, 4):
        pred = predicted_rate(h)
        got = measured.get(h)
        rows.append({"h12": h, "b3": b3_of(h), "predicted": pred, "measured": got,
                     "ratio": (got / pred) if got else None})
    have = all(r["measured"] for r in rows)
    if not have:
        return {"status": "awaiting measurement", "rows": rows, "c": fit_c(),
                "note": "the prediction is on record before the run, which is what makes it a test"}
    ok = all(0.3 <= r["ratio"] <= 3.0 for r in rows)
    return {"status": "confirmed" if ok else "refuted", "rows": rows, "c": fit_c(),
            "note": ("the rate tracks b3 exponentially" if ok else
                     "the rate does not follow the b3 exponential: not one invariant"),
            "composition": ("with max|N| = b3, a confirmed law gives: the same integer sets what exists and "
                            "what can be found" if ok else
                            "the classification and accessibility scales are unrelated: not one invariant")}


__all__ = ["ANCHORS", "MEASURED", "b3_of", "fit_c", "predicted_rate", "prediction_table", "verdict"]
