"""ingest.py — populate the registries from the REAL assets, not hand-written one-liners.

The tool self-populates: the machine-checked Lean theorems become Properties (tier 1), the open
hypotheses become Properties (tier 3, conjectures) with their falsifiers, and the climate module becomes
the climate Domain + its Evidence (tier 4). The cross-field search and the transfer verification then run
on the INGESTED knowledge.
"""
from __future__ import annotations

import re
import time
from pathlib import Path

from pacland import registry

REPO_ROOT = Path(__file__).resolve().parent.parent.parent  # src/pacland/ingest.py → repo root


def ingest_lean_proofs() -> int:
    """Every theorem/lemma in the Lean tower → a tier-1 Property (mathematically established)."""
    proof_dir = REPO_ROOT / "pacland-proof" / "PaclandProof"
    if not proof_dir.exists():
        return 0
    n = 0
    for lean in sorted(proof_dir.rglob("*.lean")):
        text = lean.read_text()
        for m in re.finditer(r"^\s*(?:theorem|lemma)\s+([a-zA-Z0-9_']+)", text, re.M):
            name = m.group(1)
            rel = str(lean.relative_to(REPO_ROOT))
            registry.add(registry.Entry(
                id=f"lean-{name}",
                kind="property",
                payload={"name": name, "statement": f"theorem {name} (machine-checked)",
                         "tier": 1, "domain": "mathematics", "source": rel},
                provenance={"produced_by": "ingest", "method": "lean-proof", "ts": time.time()}))
            n += 1
    return n


def ingest_hypotheses() -> int:
    """Every open question → a tier-3 Property (conjecture); each candidate hypothesis → its own property
    with the falsifier attached."""
    from pacland import hypotheses
    n = 0
    for name, h in hypotheses.HYPOTHESES.items():
        registry.add(registry.Entry(
            id=f"hyp-{name}",
            kind="property",
            payload={"name": name, "statement": h.get("question", ""),
                     "tier": 3, "domain": "physics", "open": h.get("open", ""),
                     "forced": h.get("forced", "")},
            provenance={"produced_by": "ingest", "method": "hypothesis-registry", "ts": time.time()}))
        n += 1
        for i, cand in enumerate(h.get("hypotheses", [])):
            registry.add(registry.Entry(
                id=f"cand-{name}-{i}",
                kind="property",
                payload={"name": name, "statement": cand.get("hypothesis", ""),
                         "falsifier": cand.get("falsifier", ""), "tier": 3, "domain": "physics"},
                provenance={"produced_by": "ingest", "method": "candidate", "ts": time.time()}))
            n += 1
    return n


def ingest_climate() -> int:
    """The climate module → the climate Domain + its empirical Evidence (tier 4)."""
    n = 0
    registry.add(registry.Entry(
        id="domain-climate",
        kind="domain",
        payload={"name": "climate", "interpretation": "Earth-system energy and carbon balance",
                 "models": ["energy_budget", "ecs_model", "cmip6_drift", "reference_model"],
                 "tier": 4},
        provenance={"produced_by": "ingest", "method": "module-scan", "ts": time.time()}))
    n += 1
    registry.add(registry.Entry(
        id="evidence-cmip6-drift",
        kind="evidence",
        payload={"name": "CMIP6 conservation drift", "dataset": "Irving et al. 2021",
                 "what": "three-ledger known-answer tests", "tier": 4, "domain": "climate",
                 "test": "tests/test_climate_cmip6_drift.py"},
        provenance={"produced_by": "ingest", "method": "test-scan", "ts": time.time()},
        links=["domain-climate"]))
    n += 1
    return n


def ingest_disciplines() -> int:
    """Every discipline in disciplines.py → a Domain entry (the canonical field list)."""
    from pacland.disciplines import DISCIPLINES
    n = 0
    for d in DISCIPLINES:
        registry.add(registry.Entry(
            id=f"domain-{d.slug}",
            kind="domain",
            payload={"name": d.slug, "title": d.name, "interpretation": d.blurb,
                     "status": d.status, "package": d.package, "docs": d.docs},
            provenance={"produced_by": "ingest", "method": "discipline-registry", "ts": time.time()}))
        n += 1
    return n


_SLUG_ALIASES = {"econ": "economics", "epi": "epidemiology", "rf": "drugs", "site": "energy"}


def ingest_tests() -> int:
    """Every test file → an Evidence entry (a verified claim in its domain), linked to the domain."""
    tests_dir = REPO_ROOT / "tests"
    if not tests_dir.exists():
        return 0
    n = 0
    for t in sorted(tests_dir.glob("test_*.py")):
        prefix = t.name.replace("test_", "").split("_")[0]
        domain = _SLUG_ALIASES.get(prefix, prefix)
        registry.add(registry.Entry(
            id=f"evidence-{t.stem}",
            kind="evidence",
            payload={"name": t.stem, "domain": domain, "test": str(t.relative_to(REPO_ROOT)),
                     "tier": 4},
            provenance={"produced_by": "ingest", "method": "test-scan", "ts": time.time()},
            links=[f"domain-{domain}"]))
        n += 1
    return n


def ingest_all() -> dict[str, int]:
    """Wipe + repopulate the whole registry from the real assets. Returns per-kind counts."""
    registry.clear()
    from pacland import fields, structure_build
    n_fields = fields.seed_fields()
    registry.seed_known_unifications()
    # the economics↔hard-science unifications (all four batches)
    from pacland import economics_unify, economics_more, economics_batch2, economics_batch3
    economics_unify.record()
    economics_more.record()
    economics_batch2.record()
    economics_batch3.record()
    return {
        "structures": n_fields,
        "lean_proofs": ingest_lean_proofs(),
        "hypotheses": ingest_hypotheses(),
        "disciplines": ingest_disciplines(),
        "tests": ingest_tests(),
        "structure_groups": structure_build.build_structures(),
        "economics_unifications": len(registry.query("mapping", lambda d: True)),
    }
