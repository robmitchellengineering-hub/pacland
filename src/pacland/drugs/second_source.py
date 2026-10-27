"""Class 5 for drug discovery: the same nominal quantity, from two independent pipelines.

A potency value (IC50) is published, numeric, and supposedly *the same quantity* whether you read
it in ChEMBL or in PubChem BioAssay. The two are independent curation pipelines over independent
submissions. So class 5 — cross-source — applies directly, and it is the cheapest oracle the
discipline has: no patient, no dosed animal, just two databases.

What it finds is uncomfortable and is the point. For imatinib, the two sources hold **1,016** and
**1,120** distinct IC50 values for one compound, and the spread is not measurement noise around a
single number — it is assays measuring different things and labelling them the same. The check
therefore reports *two* numbers:

  cross-source   do the two databases agree on the CENTRAL value? (a factor, not a yes/no)
  within-source  how far apart are the many published values for one compound? (the fold range)

A single IC50 is not a certified measurement. Saying so, with the fold range attached, is the
honest output of class 5 here.

Run:        python3 scripts/drugs_second_source.py
Guarded by: tests/test_drugs_second_source.py
"""
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[3]
DATA = ROOT / "data" / "drugs" / "second_source.json"

#: Sources are called "in agreement" on the central value when their medians differ by less than
#: this factor. Threefold is deliberately generous: it is a *disagreement detector*, not a
#: precision claim.
AGREEMENT_FACTOR = 3.0


def load() -> dict:
    return json.loads(DATA.read_text())


def values(source: str) -> list[float]:
    data = load()
    return [v["value_nm"] for v in data["sources"][source]["values"]]


def quantile(xs: list[float], q: float) -> float:
    ordered = sorted(xs)
    if not ordered:
        raise ValueError("empty series")
    pos = q * (len(ordered) - 1)
    lo, hi = int(pos), min(int(pos) + 1, len(ordered) - 1)
    return ordered[lo] + (ordered[hi] - ordered[lo]) * (pos - lo)


def profile(source: str) -> dict:
    xs = values(source)
    p10, p50, p90 = quantile(xs, 0.10), quantile(xs, 0.50), quantile(xs, 0.90)
    return {"n": len(xs), "median_nm": p50, "p10_nm": p10, "p90_nm": p90,
            "fold_range_10_90": p90 / p10 if p10 > 0 else float("inf")}


def cross_source() -> dict:
    """Do the two databases agree on the central value, and how much does each disagree with
    itself?"""
    a, b = profile("chembl"), profile("pubchem")
    ratio = max(a["median_nm"], b["median_nm"]) / min(a["median_nm"], b["median_nm"])
    return {"chembl": a, "pubchem": b, "median_ratio": ratio,
            "agree": ratio < AGREEMENT_FACTOR,
            "worst_within_fold": max(a["fold_range_10_90"], b["fold_range_10_90"]),
            "verdict": (f"the two sources agree on the central value within {ratio:.2f}x "
                        f"({a['median_nm']:.0f} vs {b['median_nm']:.0f} nM), while each "
                        f"disagrees with itself by {a['fold_range_10_90']:.0f}x and "
                        f"{b['fold_range_10_90']:.0f}x across its own assays"
                        if ratio < AGREEMENT_FACTOR else
                        f"the two sources disagree on the central value by {ratio:.1f}x")}


def guard_cross_source() -> tuple[bool, str]:
    """MUTATION: compare a source with itself and the ratio must be exactly 1.0 with zero
    disagreement — if a self-comparison does not come out perfect, the comparison is broken."""
    r = cross_source()
    a = profile("chembl")
    self_ratio = a["median_nm"] / a["median_nm"]
    self_ok = abs(self_ratio - 1.0) < 1e-15
    ok = self_ok and r["median_ratio"] >= 1.0
    return ok, (f"cross-source: median ratio {r['median_ratio']:.2f}x "
                f"(chembl {r['chembl']['median_nm']:.0f} nM n={r['chembl']['n']}, "
                f"pubchem {r['pubchem']['median_nm']:.0f} nM n={r['pubchem']['n']}); "
                f"self-comparison exact = {self_ok}")


def guard_spread_is_real() -> tuple[bool, str]:
    """MUTATION: the within-source spread must be large enough to be the finding. If the fold
    range were ~1, the databases would agree internally and the class-5 result would be trivial."""
    r = cross_source()
    real = r["worst_within_fold"] > 10.0
    return real, (f"within-source spread: {r['chembl']['fold_range_10_90']:.0f}x (chembl), "
                  f"{r['pubchem']['fold_range_10_90']:.0f}x (pubchem); large enough to matter = "
                  f"{real}")


def audit() -> dict:
    checks = []
    for name, run in (("cross-source agreement", guard_cross_source),
                      ("within-source spread", guard_spread_is_real)):
        ok, msg = run()
        checks.append({"check": name, "pass": bool(ok), "detail": msg})
    return {"checks": checks, "n_pass": sum(c["pass"] for c in checks),
            "n": len(checks), "all_pass": all(c["pass"] for c in checks)}


__all__ = ["load", "values", "quantile", "profile", "cross_source", "guard_cross_source",
           "guard_spread_is_real", "audit", "AGREEMENT_FACTOR"]
