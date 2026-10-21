"""Drug-discovery falsification guards — the constraint guard-suite (item #2).

Mirrors ``pacland.climate.guards`` and ``pacland.guards``: each guard asserts one
chemical invariant a candidate must satisfy, under the Valiant Verification
discipline — a violation fails LOUDLY, and each guard has a seeded-fault mutation
test proving it goes red on the fault it exists to catch.

These are the *constraint-first* half: the field already runs PAINS/Brenk/REOS/
Ro5/RDKit-sanitization as boolean filters, but never as a certified guard-suite.
This wraps the forbidden-state checks (net charge, valence, drug-likeness,
synthesizability) as pass/fail guards. Pure stdlib; no RDKit needed for the contract.
"""
from __future__ import annotations

_MAX_VALENCE: dict[str, int] = {
    "C": 4, "N": 3, "O": 2, "H": 1, "F": 1, "Cl": 1, "Br": 1, "I": 1, "S": 6, "P": 5,
}


def guard_total_charge_neutral(charges, expected: float = 0.0, tol: float = 1e-6) -> tuple[bool, str]:
    """Forbidden-state guard: the molecule's net formal charge must equal its expected
    charge (default neutral). Fails on a non-neutral drug candidate."""
    total = float(sum(charges))
    ok = abs(total - expected) <= tol
    return ok, f"net charge={total:+.3f} (expected {expected}, tol {tol})"


def guard_valence_bounds(pairs, max_valence=None) -> tuple[bool, str]:
    """Forbidden-state guard: each atom's bond-order sum must not exceed the element's
    maximum valence. Fails on over-valent atoms (e.g. pentavalent carbon)."""
    if max_valence is None:
        max_valence = _MAX_VALENCE
    bad = [(sym, b) for sym, b in pairs if b > max_valence.get(sym, 8)]
    return not bad, f"over-valent atoms: {bad[:5]}"


def guard_lipinski(mw: float, logp: float, hbd: int, hba: int, max_violations: int = 1) -> tuple[bool, str]:
    """Drug-likeness guard (Lipinski's rule of five): a candidate may violate at most
    ``max_violations`` of the four thresholds (MW<=500, logP<=5, HBD<=5, HBA<=10).
    The field's own 'what a drug-like molecule forbids', wrapped as a bound."""
    notes = []
    viol = 0
    if mw > 500:
        viol += 1
        notes.append(f"MW={mw:.0f}")
    if logp > 5:
        viol += 1
        notes.append(f"logP={logp:.1f}")
    if hbd > 5:
        viol += 1
        notes.append(f"HBD={hbd}")
    if hba > 10:
        viol += 1
        notes.append(f"HBA={hba}")
    ok = viol <= max_violations
    return ok, f"Ro5 violations={viol} {notes} (max {max_violations})"


def guard_synthesizable(rascore: float, threshold: float = 8.0) -> tuple[bool, str]:
    """Synthesizability floor: a retrosynthetic-accessibility score (RAScore ~1-10,
    higher = harder) must not exceed ``threshold``. Fails on un-synthesizable candidates."""
    ok = rascore <= threshold
    return ok, f"RAScore={rascore:.2f} (threshold {threshold})"


__all__ = [
    "guard_total_charge_neutral",
    "guard_valence_bounds",
    "guard_lipinski",
    "guard_synthesizable",
]
