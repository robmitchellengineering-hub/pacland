"""synthesis_bounds.py — the M3 synthesis step: combine harvested tier-1 lemmas into candidate bounds.

This is the bridge between "a big library" and "a new bound". Each harvested lemma maps to a bound
SHAPE (a parameterized c(β)); single shapes and pairwise products become candidate bounds that the
referee (bound_search.check_bound) then tests. The honest result is what matters: generic analysis
lemmas rarely reach the specific mass-gap scale m(β)=25.28·e^(−1.182β) — but the mechanism is the
thing a real mathematical insight plugs into, and every candidate (survivor or failure) is recorded.
"""
from __future__ import annotations

import math

from pacland import registry
from pacland import bound_search as bs


def _shape(name: str):
    """Map a lemma (name + statement) to a candidate bound SHAPE c(β), or (None, None)."""
    low = name.lower()
    if any(k in low for k in ("spectral", "eigen", "gap")):
        return "spectral-gap", lambda b: 1.0
    if any(k in low for k in ("decay", "exponential", "superexponential")):
        return "exponential-decay", lambda b: math.exp(-b)
    if any(k in low for k in ("contraction", "mixing", "ergodic", "measure")):
        return "contraction", lambda b: math.exp(-b)
    return None, None


def synthesize_candidates(properties=None, max_candidates: int = 40) -> list[dict]:
    """Emit candidate bounds from the harvested tier-1 lemmas: single shapes + pairwise products."""
    props = properties or registry.query("property", lambda d: d.get("payload", {}).get("tier") == 1)
    shapes = []
    for p in props:
        name = p.get("payload", {}).get("name", "") + " " + p.get("payload", {}).get("statement", "")
        kind, fn = _shape(name)
        if fn is not None:
            shapes.append((kind, fn, p.get("payload", {}).get("name", "")))
    candidates: list[dict] = []
    for kind, fn, nm in shapes:
        candidates.append({"source": f"single:{nm}", "shape": kind, "bound": fn})
    for i in range(len(shapes)):
        for j in range(i + 1, len(shapes)):
            ki, fi, ni = shapes[i]
            kj, fj, nj = shapes[j]
            candidates.append({
                "source": f"product:{ni}x{nj}",
                "shape": f"{ki}*{kj}",
                "bound": (lambda fi=fi, fj=fj: (lambda b: fi(b) * fj(b)))(),
            })
    return candidates[:max_candidates]


def run_synthesis(properties=None, max_candidates: int = 40) -> dict:
    """Synthesize candidate bounds, test each against the referee, and record the honest result."""
    candidates = synthesize_candidates(properties, max_candidates)
    survivors: list[dict] = []
    failures: list[dict] = []
    for c in candidates:
        r = bs.check_bound(c["bound"])
        entry = {"source": c["source"], "shape": c["shape"], **r}
        (survivors if r["survived"] else failures).append(entry)
        registry.record_claim(
            f"claim-synth-{c['source'][:60]}",
            f"synthesized bound {c['source']} ({c['shape']})",
            "survived" if r["survived"] else "failed",
            problem="ym-mass-gap",
            reason=(c["shape"] + " reaches the scale" if r["survived"]
                    else "does not reach the mass-gap scale"),
            produced_by="synthesis",
        )
    return {"n_candidates": len(candidates), "n_survivors": len(survivors),
            "n_failures": len(failures), "survivors": survivors, "failures": failures}
