"""synthesize.py — the cross-field discovery pipeline, end-to-end.

Given a target field + type (an open problem), it runs the full chain: cross-reference (find structures
of that type in OTHER fields) → pull each match's linked theorems/evidence → propose a transfer with a
candidate yield. The yield is a HEURISTIC here — the actual yield is decided at the verification step
(transfer_verify), not here. This is the "find a structure in field A whose type matches an open problem
in field B" query, made concrete.
"""
from __future__ import annotations

from pacland import cross_reference, registry

# a candidate yield, by the matched structure's type → which of the three yields (§4a) it plausibly gives.
_YIELD_BY_TYPE = {
    "spectral-gap": "proof-technique (a bound transfers: gap → mixing time → convergence rate)",
    "parabolic-pde": "prediction (a transport property transfers: ⟨x²⟩ ∝ t → a measurable quantity)",
    "markov": "prediction (a stationary/spectral property transfers to the target process)",
    "conservation": "proof-technique (a conserved quantity constrains the target's dynamics)",
    "symmetry": "proof-technique (a symmetry → a selection rule / conserved charge)",
    "oscillator": "prediction (a period/rate curve transfers to the target's oscillation)",
    "logistic": "prediction (a saturation curve transfers to the target's growth)",
    "gauge-theory": "proof-technique (a gauge/curvature structure constrains the target)",
}


def _classify_yield(type_str: str) -> str:
    for k, v in _YIELD_BY_TYPE.items():
        if k in type_str.lower():
            return v
    return "unknown (needs a checker)"


def _linked_theorems(struct_id: str) -> int:
    s = registry.get("structure", struct_id)
    if not s:
        return 0
    return sum(1 for l in s.get("links", []) if l.startswith("lean-"))


def synthesize(target_domain: str, target_type: str) -> list[dict]:
    """The cross-field discovery pipeline. Returns one entry per candidate transfer."""
    out = []
    for m in cross_reference.propose_transfers({"type": target_type, "domain": target_domain}):
        out.append({
            "from_structure": m["from_structure"],
            "from_domain": m["from_domain"],
            "definition": m["definition"][:70],
            "reproduces": m["reproduces"][:70],
            "tier": m["tier"],
            "linked_theorems": _linked_theorems(m["from_structure"]),
            "candidate_yield": _classify_yield(target_type),
        })
    # rank: prefer the match with the most linked theorems (the richest transfer source)
    out.sort(key=lambda e: -e["linked_theorems"])
    return out
