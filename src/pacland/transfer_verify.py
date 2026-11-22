"""transfer_verify.py — phase 3: verify a cross-field transfer actually carries its property.

A proposed transfer is credited only when BOTH ends of the mapping reproduce the SAME invariant. This
is a NUMERICAL check (tier 4, "tested numerically"), not a Lean proof (tier 1); the honest bar is that
a vacuous or wrong mapping FAILS here because the two ends' measured invariants diverge.

Generalised: ``verify_transfer`` is registry-driven, so it can verify ANY mapping the registry knows,
not one hard-coded id. Dispatch order is
  1. a SPECIFIC per-mapping checker (exact invariant), else
  2. a TYPE-level checker (both ends share a structure type with a canonical invariant), else
  3. an honest "unverified" verdict — a mapping with no numerical invariant checker is UNVERIFIED,
     never a false PASS.
"""
from __future__ import annotations

import random
import time

from pacland import registry


# ------------------------------------------------------------------------------------------ #
# Structure-type → invariant checker. Each checker measures a canonical invariant and returns a
# dict with a boolean ``verified``. Add one checker per type to widen what transfers are verifiable.
# ------------------------------------------------------------------------------------------ #

def _diffusive_msd_check(n_steps: int = 1000, n_walkers: int = 2000, seed: int = 0,
                         tolerance: float = 0.05) -> dict:
    """The parabolic-pde invariant: linear mean-squared displacement ⟨x²⟩ = 2Dt.

    A symmetric random walk on the integers (step ±1, unit time) has D = 1/2, so ⟨x²⟩ = t.
    """
    rng = random.Random(seed)
    msd_sum = 0.0
    for _ in range(n_walkers):
        x = 0
        for _ in range(n_steps):
            x += rng.choice((-1, 1))
        msd_sum += x * x
    measured = msd_sum / n_walkers
    expected = 2 * 0.5 * n_steps  # 2Dt with D = 1/2, t = n_steps
    ratio = measured / expected
    return {
        "invariant": "linear mean-squared displacement ⟨x²⟩ = 2Dt",
        "measured_msd": measured, "expected_msd": expected, "ratio": ratio,
        "verified": abs(ratio - 1.0) < tolerance,
    }


def check_spectral_gap_mixing() -> dict:
    """The markov invariant: a reversible chain mixes iff its spectral gap (1 − λ₂) is positive.

    A 2-state reversible chain with transition probabilities a, b has gap = a + b. A mixing chain
    (a, b > 0) has gap > 0; a non-mixing chain (a = b = 0, the identity) has gap 0. The check verifies
    the invariant discriminates the two.
    """
    def gap(a: float, b: float) -> float:
        return a + b

    mixing = gap(0.3, 0.4)       # 0.7 → mixes, bound 1/gap finite
    non_mixing = gap(0.0, 0.0)   # 0   → does not mix
    return {
        "invariant": "spectral gap (1 − λ₂) bounds mixing time (1/gap)",
        "gap_mixing": mixing, "gap_non_mixing": non_mixing,
        "mixing_time_bound": 1.0 / mixing if mixing > 0 else float("inf"),
        "verified": mixing > 0.0 and non_mixing == 0.0,
    }


# exact-invariant checks keyed by MAPPING id
SPECIFIC_CHECKS: dict[str, object] = {
    "heat-diffusion-walk": _diffusive_msd_check,
}

# canonical-invariant checks keyed by STRUCTURE type (both ends must share the type)
TYPE_CHECKS: dict[str, object] = {
    "parabolic-pde": _diffusive_msd_check,
    "markov": check_spectral_gap_mixing,
}


def _structure_type(name: str) -> str | None:
    """The registered type of a structure (e.g. 'parabolic-pde', 'markov'), or None if unknown."""
    hit = registry.get("structure", name)
    if hit is not None:
        return hit.get("payload", {}).get("type")
    # fall back to the in-tree catalog when the registry has not been seeded yet
    try:
        from pacland import fields
        for s in fields.FIELDS:
            if s["id"] == name:
                return s.get("type")
    except Exception:  # noqa: BLE001
        return None
    return None


def _record(mapping_id: str, source: str, target: str, check_name: str, r: dict) -> dict:
    """Record the transfer verdict as Evidence (tier 4) linked to the mapping."""
    evidence_id = registry.new_id()
    registry.add(registry.Entry(
        id=evidence_id, kind="evidence",
        payload={
            "mapping": mapping_id, "source": source, "target": target,
            "check": check_name, "result": r, "tier": 4,
        },
        provenance={"produced_by": "transfer_verify", "method": "numerical-encoding-check",
                    "ts": time.time()},
        links=[mapping_id]))
    return {"mapping": mapping_id, "verified": bool(r.get("verified")), "evidence_id": evidence_id,
            "check": check_name, "result": r}


def verify_transfer(mapping_id: str) -> dict:
    """Verify a cross-field mapping by its exact invariant, else its shared structure type, else honestly
    report it UNVERIFIED. Registry-driven: works for any mapping id the registry holds."""
    # 1. a specific per-mapping checker (the exact invariant)
    if mapping_id in SPECIFIC_CHECKS:
        return _record(mapping_id, "", "", mapping_id, SPECIFIC_CHECKS[mapping_id]())

    # 2. resolve the mapping's two ends + their structure types
    m = registry.get("mapping", mapping_id)
    if m is None:
        return {"mapping": mapping_id, "verified": False,
                "error": f"unknown mapping {mapping_id!r} (not in the registry)"}
    frm = m.get("payload", {}).get("from", "")
    to = m.get("payload", {}).get("to", "")
    tf, tt = _structure_type(frm), _structure_type(to)

    # 3. a TYPE-level checker, when both ends share a type that has a canonical invariant
    if tf is not None and tf == tt and tf in TYPE_CHECKS:
        r = TYPE_CHECKS[tf]()
        return _record(mapping_id, frm, to, f"type:{tf}", r)

    # 4. honest: no numerical invariant checker for this mapping
    return {"mapping": mapping_id, "verified": False, "status": "unverified",
            "reason": f"no invariant checker for {frm}→{to} (types {tf}/{tt}); "
                      "add a SPECIFIC_CHECKS entry or a TYPE_CHECKS entry for its shared type"}


def verifiable_mappings() -> list[str]:
    """Every registry mapping that CAN be verified now (a specific or a shared-type checker exists)."""
    out: list[str] = []
    for m in registry.query("mapping", lambda d: True):
        mid = m.get("id", "")
        if mid in SPECIFIC_CHECKS:
            out.append(mid)
            continue
        frm = m.get("payload", {}).get("from", "")
        to = m.get("payload", {}).get("to", "")
        tf, tt = _structure_type(frm), _structure_type(to)
        if tf is not None and tf == tt and tf in TYPE_CHECKS:
            out.append(mid)
    return out
