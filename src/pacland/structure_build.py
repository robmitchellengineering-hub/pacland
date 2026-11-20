"""structure_build.py — how the structure layer gets built: LINKING, not writing.

The 675 machine-checked theorems already exist (they are the properties). A structure is NOT a
hand-written one-liner — it is an INDEX: a type + domain + definition, with LINKS to the theorems that
prove its properties and the tests that evidence it. This module groups the Lean theorems into typed
structures, so the structure layer grows by linking verified knowledge into cross-referenceable units.

Method (the "how"):
  1. group the Lean theorems by topic (a keyword in the theorem name);
  2. each group becomes a structure with a type + domain + a link to every theorem in it;
  3. the cross-field model proposes the TYPE and the permitted mappings; the verification (transfer_verify)
     then checks the property actually carries.
"""
from __future__ import annotations

import re
import time
from pathlib import Path

from pacland import registry

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

# topic → (structure id, type, domain). Each structure links to the theorems whose names match.
STRUCTURE_GROUPS: list[tuple[str, str, str, tuple[str, ...]]] = [
    ("quantum-correlation", "quantum-correlation", "physics",
     ("bell", "mermin", "kron", "pauli")),
    ("hyperbolic-geometry", "hyperbolic", "mathematics",
     ("hyperbolic", "hyperboloid", "gram", "pathangle")),
    ("cayley-tree", "tree", "mathematics",
     ("commonprefix", "lcp", "dyadicbits", "cayley", "tree")),
    ("spectral-gap", "spectral-gap", "mathematics",
     ("contraction", "dirichlet", "ricci", "covfirst", "gap")),
    ("yang-mills", "gauge-theory", "physics",
     ("mass", "confinement", "plaquette", "glueball", "lgt")),
]


def _theorem_names() -> list[str]:
    proof_dir = REPO_ROOT / "pacland-proof" / "PaclandProof"
    names: list[str] = []
    for lean in proof_dir.rglob("*.lean"):
        for m in re.finditer(r"^\s*(?:theorem|lemma)\s+([a-zA-Z0-9_']+)", lean.read_text(), re.M):
            names.append(m.group(1))
    return names


def build_structures() -> int:
    """Group the Lean theorems into typed structures, each linking to its theorems. Returns the count."""
    names = _theorem_names()
    n = 0
    for sid, typ, domain, keywords in STRUCTURE_GROUPS:
        members = [nm for nm in names if any(k in nm.lower() for k in keywords)]
        if not members:
            continue
        registry.add(registry.Entry(
            id=f"structure-{sid}",
            kind="structure",
            payload={"definition": f"the {sid} structure ({len(members)} machine-checked theorems)",
                     "type": typ, "domain": domain,
                     "theorem_count": len(members),
                     "theorems": members},
            provenance={"produced_by": "structure-build", "method": "theorem-grouping",
                        "ts": time.time()},
            links=[f"lean-{m}" for m in members]))
        n += 1
    return n
