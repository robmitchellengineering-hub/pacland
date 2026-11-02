"""H-B: is measure-invariance the same thing as observability?

The hypothesis (from cross-referencing the measure wall with the rate wall): since the measure space is provably
`b3`-dimensional and no sampler can resolve it, **the only observables are the measure-invariant ones** — so the
invariant set and the "computable without a sampler" set should be the SAME SET.

That prediction is tested here on two axes recorded **independently**:

    INVARIANT   true whatever measure is chosen            (docs/measure-invariance.md)
    EXACT       the answer is an exact object -- a theorem, an integer, or a rational -- rather than a float whose
                accuracy is limited by precision or a budget

**The hypothesis predicts perfect agreement. It fails in two cells, and the failures are the result:**

| cell | example | why it breaks the coincidence |
|---|---|---|
| INVARIANT but not EXACT | the zeta zeros to 6.4e-13 | deterministic and sampler-free, but the output is a **float**, not an exact object |
| DEPENDENT but EXACT | the 5.05x measure spread | computed **exactly** over measures, and still not truth-apt |

So "invariant" and "exact" are **different axes**, and H-B conflated them. What survives is the weaker, true statement:
**invariance implies no sampler is needed** — not that it implies exactness.

Run:        python3 scripts/observability_axes.py
Guarded by: tests/test_observability_axes.py
"""
from __future__ import annotations

#: (name, invariant: bool, exact: bool, why the exactness call was made)
ROWS = (
    ("max |N| = b3", True, True, "a theorem; the bound and its attaining pair are exact"),
    ("conifold coefficients 37/30, 2309/1800", True, True, "exact rationals from the recurrence"),
    ("content law A = 8.554", True, True, "coefficients of P(x)^(b3/2); the 8.554 was a fit of something exact"),
    ("gauge quotient: 1 orbit in 531,441", True, True, "an exact count over the enumerated window"),
    ("tadpole ladder: distinct N = 2b3+1", True, True, "an exact count, verified against enumeration"),
    ("measure dimension = b3", True, True, "a statement about a simplex of invariant classes"),
    ("zeta zeros to 6.4e-13", True, False, "sampler-free and deterministic, but the output is a float"),
    ("arithmetic rigidity 0.617 vs GOE 0.531", True, False, "a statistic over numerically computed zeros"),
    ("measure-dependence 5.05x (21% vs 1%)", False, True, "computed exactly over measures, and still not truth-apt"),
    ("SUSY fraction 0.279 / 0.202 / 0.012", False, False, "corpus fraction; sampler- and selection-dependent"),
    ("the N/b3 collapse and its break", False, False, "corpus-dependent"),
    ("accessibility series", False, False, "sampler observable with a budget"),
)


def crosstab() -> dict:
    out = {(True, True): [], (True, False): [], (False, True): [], (False, False): []}
    for name, inv, ex, why in ROWS:
        out[(inv, ex)].append({"name": name, "why": why})
    return out


def disagreements() -> dict:
    """The cells that break the coincidence."""
    t = crosstab()
    return {"invariant_not_exact": t[(True, False)], "exact_not_invariant": t[(False, True)]}


def verdict() -> dict:
    d = disagreements()
    consistent = not d["invariant_not_exact"] and not d["exact_not_invariant"]
    return {
        "rows": len(ROWS),
        "invariant_not_exact": [r["name"] for r in d["invariant_not_exact"]],
        "exact_not_invariant": [r["name"] for r in d["exact_not_invariant"]],
        "coincide": consistent,
        "verdict": ("H-B SUPPORTED — invariance and exactness are the same axis here" if consistent else
                    "H-B REFUTED AS STATED — invariance and exactness are different axes; the failures are listed"),
        "surviving_weaker_claim": ("invariance implies no sampler is needed: every INVARIANT row is computable without "
                                   "a sampler, even where the output is a float. The converse fails."),
    }


__all__ = ["ROWS", "crosstab", "disagreements", "verdict"]
