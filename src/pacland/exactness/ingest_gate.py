"""One gate at ingest: a row outside the sampler's own declared domain is not a vacuum this model produces.

`data_sampler`'s default is `moduli_bounds = (1.0, 5.0)`. A corpus row with `|z| = 8.5e29` cannot have been produced by
that sampler, so it is not a point of the theory — it is a runaway. Letting such rows into an aggregate does not add
noise; it changes what the aggregate is about.

This is therefore **a domain check, not a hygiene convention**: the bounds are the model's own statement of where it can
place a modulus, which puts the gate in the same class as `max |N| = b3` rather than in the class of taste.

Two thresholds are reported, always, so the choice is visible rather than baked in:

    IN_DOMAIN   |z| within the sampler's declared bounds   (1.0, 5.0)
    LOOSE       |z| within a generous band                 (1e-3, 1e3)
    RUNAWAY     outside even the loose band

**The gate must fail loudly.** It reports how many rows it rejects; it never filters silently. A gate that quietly
cleans the data is how a corpus always passes.

Run:        python3 scripts/ingest_gate.py
Guarded by: tests/test_ingest_gate.py
"""
from __future__ import annotations

import math

#: The sampler's own declared defaults (jaxvacua `data_sampler`).
MODULI_BOUNDS = (1.0, 5.0)

#: A generous band, reported beside the declared one.
LOOSE_BAND = (1e-3, 1e3)


def _component_abs(x) -> float:
    """One component as `|z|`.

    The corpus stores a complex number as a two-element ``[re, im]`` list, not as a Python complex. Getting that wrong
    once made every row read as runaway -- a parse failure silently promoted to a data verdict, which is the same
    mistake as a ``-1`` sentinel. Unparseable input now raises instead of being classified.
    """
    if isinstance(x, (list, tuple)):
        if len(x) != 2:
            raise ValueError(f"expected [re, im], got {x!r}")
        return abs(complex(float(x[0]), float(x[1])))
    return abs(complex(x))


def modulus_scale(row: dict) -> float:
    """The largest `|z|` over the row's moduli (and `tau` if present). `nan` when the row carries none."""
    vals = []
    for key in ("moduli", "tau"):
        v = row.get(key)
        if v is None:
            continue
        # moduli is a list of [re, im] pairs; tau is a single [re, im]
        if key == "tau":
            vals.append(_component_abs(v))
        else:
            seq = v if isinstance(v, (list, tuple)) else [v]
            for x in seq:
                vals.append(_component_abs(x))
    return max(vals) if vals else float("nan")


def classify(row: dict) -> str:
    """`in_domain`, `loose`, or `runaway`."""
    z = modulus_scale(row)
    if z != z:                       # NaN
        return "runaway"
    lo, hi = MODULI_BOUNDS
    if lo <= z <= hi:
        return "in_domain"
    lo, hi = LOOSE_BAND
    if lo <= z <= hi:
        return "loose"
    return "runaway"


def wilson(k: int, n: int, z: float = 1.96) -> tuple:
    """Wilson interval for a proportion — correct for the small, lopsided counts this corpus has.

    Necessary here because the gated counts are tiny at high `b3` (46 in-domain rows at `b3 = 10`): a point estimate
    on 46 rows cannot support a law, and an interval makes that visible instead of arguable.
    """
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (max(0.0, centre - half), min(1.0, centre + half))


def report(rows: list, b3_of=None) -> dict:
    """Counts and rates, per `b3` when `b3_of` is supplied."""
    b3_of = b3_of or (lambda r: len(r["flux"]) // 2)
    per = {}
    for r in rows:
        b3 = b3_of(r)
        d = per.setdefault(b3, {"rows": 0, "in_domain": 0, "loose": 0, "runaway": 0,
                                "susy_all": 0, "susy_in_domain": 0,
                                "minima_all": 0, "minima_in_domain": 0})
        cls = classify(r)
        d["rows"] += 1
        d[cls] += 1
        susy = bool(r.get("is_susy"))
        d["susy_all"] += susy
        minimum = bool(r.get("is_minimum"))
        d["minima_all"] += minimum
        if cls == "in_domain":
            d["susy_in_domain"] += susy
            d["minima_in_domain"] += minimum
    for d in per.values():
        n = d["rows"]
        k = d["in_domain"]
        d["runaway_share"] = d["runaway"] / n if n else 0.0
        d["susy_rate_all"] = d["susy_all"] / n if n else 0.0
        d["susy_rate_in_domain"] = d["susy_in_domain"] / k if k else 0.0
        d["minima_rate_all"] = d["minima_all"] / n if n else 0.0
        d["minima_rate_in_domain"] = d["minima_in_domain"] / k if k else 0.0
        d["susy_ci"] = wilson(d["susy_in_domain"], k)
        d["minima_ci"] = wilson(d["minima_in_domain"], k)
        d["ci_half_width"] = (d["minima_ci"][1] - d["minima_ci"][0]) / 2
    return per


def verdict(per: dict) -> dict:
    tot = sum(d["rows"] for d in per.values())
    run = sum(d["runaway"] for d in per.values())
    return {
        "rows": tot,
        "runaway": run,
        "runaway_share": run / tot if tot else 0.0,
        "gated": {b3: round(d["runaway_share"], 3) for b3, d in sorted(per.items())},
        "statement": ("rows outside the sampler's declared moduli bounds are not vacua this model produces; on this "
                      "corpus they are a large share, and the SUSY fraction over all rows is not the SUSY fraction "
                      "over the theory"),
        "rule": ("fail loudly: the rejected count is reported, never silently dropped"),
    }


def interval_verdict(per: dict, key: str = "minima_rate_in_domain") -> dict:
    """Do the gated rates' intervals all overlap? That is what 'flat' means, and no more than that."""
    b3s = sorted(per)
    los = [per[b3]["minima_ci"][0] for b3 in b3s]
    his = [per[b3]["minima_ci"][1] for b3 in b3s]
    overlap = max(los) <= min(his)
    thin = [b3 for b3 in b3s if per[b3]["in_domain"] < 200]
    return {
        "b3": b3s,
        "rates": [round(per[b3][key], 3) for b3 in b3s],
        "intervals": [(round(per[b3]["minima_ci"][0], 3), round(per[b3]["minima_ci"][1], 3)) for b3 in b3s],
        "intervals_overlap": overlap,
        "under_two_hundred_rows": thin,
        "statement": ("the intervals overlap, so 'flat' is CONSISTENT with the data but not proven -- "
                      "and the rungs with under 200 in-domain rows cannot carry a law"
                      if overlap else "the intervals do not overlap: the rates are distinguishable"),
    }


__all__ = ["MODULI_BOUNDS", "LOOSE_BAND", "wilson", "modulus_scale", "classify", "report", "verdict",
           "interval_verdict"]
