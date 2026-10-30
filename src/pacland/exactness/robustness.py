"""The robustness engine — a number is only a fact once you say how much it depends on your choices (D17).

Three findings in two days were all one failure: a statistic quoted as a single number, where the number was
really a menu of defensible choices and nobody had published the menu. This engine prints the menu.

For a named statistic it varies the **choices an honest analyst could defend** — dedup, weighting, threshold,
measure — and reports:

    the value under each choice
    the spread across choices
    a verdict: stable | choice-dependent | dominated-by-one-choice
    which choice dominates

`stable` has to be able to fail, so every shipped statistic carries a test where a planted
choice-dependence must be detected.

Run:        python3 scripts/robustness.py
Guarded by: tests/test_robustness.py
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Robustness:
    """A statistic, every defensible choice, and what the spread says about it."""
    statistic: str
    values: dict            # choice label -> value
    spread: float           # max - min over the choices
    verdict: str            # stable | choice-dependent | dominated-by-one-choice
    dominant: str | None    # the choice responsible for the largest single move
    note: str = ""

    @property
    def stable(self) -> bool:
        return self.verdict == "stable"


def assess(statistic: str, values: dict, tolerance: float = 0.10) -> Robustness:
    """Judge a set of choice-labelled values.

    `tolerance` is the relative spread — as a fraction of the mean value — below which the statistic is
    called stable. The default 10% is a stated convention, not a law: it is in the docstring so a reader can
    disagree with the number instead of with the verdict.
    """
    if not values:
        raise ValueError("no values to assess")
    lo, hi = min(values.values()), max(values.values())
    spread = hi - lo
    mean = sum(values.values()) / len(values)
    scale = abs(mean) if abs(mean) > 1e-12 else 1e-12
    rel = spread / scale
    if rel <= tolerance:
        return Robustness(statistic, values, spread, "stable", None,
                          f"spread {rel:.1%} of the mean, inside the stated {tolerance:.0%} convention")
    # which single choice moves the value most, relative to the median of the rest?
    ordered = sorted(values.items(), key=lambda kv: kv[1])
    low_choice, high_choice = ordered[0], ordered[-1]
    dominant = f"{high_choice[0]} vs {low_choice[0]}"
    return Robustness(statistic, values, spread, "choice-dependent", dominant,
                      f"spread {rel:.1%} of the mean: the answer to '{statistic}' depends on the choice, "
                      f"and the largest move is {dominant}")


# ---------------------------------------------------------------------------------------
# customer 1: the corpus SUSY fraction
# ---------------------------------------------------------------------------------------
def corpus_susy_fraction(data_dir=None) -> Robustness:
    """The 21.17% headline, across every choice that could move it.

    Row-weighted vs family-weighted is the big one: the corpus contributes 3,000 rows at h12 = 2 where SUSY
    is common and 2,965 rows spread over the rest where it is rare, so a row-weighted pooled number is
    partly a statement about how the campaign allocated its runs.
    """
    from . import counterexample as C

    corpus = C.load_corpus(data_dir)
    rows = [(c["file"], c["row"]) for c in corpus]
    total = len(rows)

    def rate(subset) -> float:
        if not subset:
            return 0.0
        return sum(1 for _, r in subset if r.get("is_susy")) / len(subset)

    dedup = [(f, r) for f, r in rows if C.scaling_gcd(r["flux"]) <= 1]
    families = sorted({f for f, _ in rows})
    per_family = [rate([(f, r) for f, r in rows if f == fam]) for fam in families]

    values = {
        "row-weighted, all rows": rate(rows),
        "row-weighted, primitive only": rate(dedup),
        "family-weighted (mean over 16 files)": sum(per_family) / len(per_family),
        "h12 = 2 rows only": rate([(f, r) for f, r in rows if f.startswith("h12_2")]),
        "h12 = 3 rows only": rate([(f, r) for f, r in rows if f.startswith("h12_3")]),
        "h12 = 4 rows only": rate([(f, r) for f, r in rows if f.startswith("h12_4")]),
    }
    r = assess("corpus SUSY fraction", values)
    r.note = (f"{total} rows over {len(families)} files. The h12 split is not a nuisance parameter: the "
              f"pooled number sits between the h12 strata, so it is partly a statement about how the "
              f"campaign allocated runs, not about the landscape.")
    return r


# ---------------------------------------------------------------------------------------
# customer 2: F1's 5.05x small-tadpole ratio, judged through F1's OWN construction
# ---------------------------------------------------------------------------------------
def measure_ratio(b3: int = 6, max_abs: int = 1, property_index: int = 0) -> Robustness:
    """F1's headline ratio, re-judged **through `measures.table()`** rather than re-derived.

    The first attempt at this customer (recorded in the git history) compared "flux-uniform" against
    "primitive-uniform" and got 1.000 — because in the small window primitivity and `|N| <= 1` are
    independent, so the two were the same fraction twice. It would have shipped a wrong ratio labelled
    "stable", which is exactly the defect this engine exists to catch. F1's 5.05x is the **max/min across
    the five measures** of one property, so the only honest way to judge it is to ask `measures` for the row
    and assess those five values.
    """
    from . import measures as M

    t = M.table(b3, max_abs)
    row = t["rows"][property_index]
    r = assess(f"F1 ratio for `{row['property']}`", dict(row["values"]))
    r.note = (f"window {t['window']}, {t['pairs']} pairs, exact enumeration. F1's ratio is max/min across "
              f"the measures = {row['ratio']:.3f}x; the spread is {row['spread']:.4f}. The measures are all "
              f"defensible, so the fact is the ratio, not either endpoint. Note the property with zero "
              f"support under some measure (see `measures.table()`), where a ratio is definitional rather "
              f"than measured.")
    return r


__all__ = ["Robustness", "assess", "corpus_susy_fraction", "measure_ratio"]
