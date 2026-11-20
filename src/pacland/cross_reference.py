"""cross_reference.py — the cross-field search: match a type across fields.

The seed of the search engine. Given a type (and optionally the open problem's field), return the
structures in OTHER fields of that type. This is a TYPE-LEVEL match (syntactic) — it does NOT verify the
transfer; that is the functor/encoding-check, a separate step (phase 3 of the plan). A match here is a
CANDIDATE correspondence, nothing more.
"""
from __future__ import annotations

from pacland import registry


def by_type(type_str: str) -> list[dict]:
    """All structures whose type matches (case-insensitive substring)."""
    out = []
    for s in registry.query("structure", lambda d: True):
        p = s["payload"]
        if type_str.lower() in p["type"].lower():
            out.append(s)
    return out


def _domains(payload: dict) -> list[str]:
    """A structure's fields — 'domain' (string) or 'domains' (list), normalised to a list."""
    d = payload.get("domain") or payload.get("domains") or []
    if isinstance(d, str):
        return [d]
    return list(d)


def cross_field(type_str: str, exclude_domain: str) -> list[dict]:
    """Structures of a type in fields OTHER than the open problem's field."""
    return [s for s in by_type(type_str) if exclude_domain not in _domains(s["payload"])]


def propose_transfers(problem: dict) -> list[dict]:
    """Given an open problem {type, domain, name?}, return candidate transfers from OTHER fields of the
    same type. Each candidate carries the source structure's reproduced property (the thing that might
    transfer) and its tier. The three-yield question (§4a) is answered later, at the verification step —
    here we only propose candidates."""
    out = []
    for s in cross_field(problem["type"], problem.get("domain", "")):
        p = s["payload"]
        out.append({
            "from_structure": s["id"],
            "from_domain": _domains(p)[0] if _domains(p) else "?",
            "definition": p.get("definition", ""),
            "reproduces": p.get("reproduces", ""),
            "tier": p.get("tier", 5),
            "permitted_mappings": p.get("permitted_mappings", p.get("maps", [])),
            "problem": problem.get("name", ""),
            "problem_domain": problem.get("domain", ""),
        })
    return out


def type_index() -> dict[str, list[str]]:
    """The cross-reference index: type → the fields that hold it."""
    from collections import defaultdict
    idx: dict[str, set[str]] = defaultdict(set)
    for s in registry.query("structure", lambda d: True):
        idx[s["payload"]["type"]].add(s["payload"]["domain"])
    return {t: sorted(doms) for t, doms in idx.items()}
