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
    """Refresh the registry from the real assets WITHOUT wiping accumulated evidence.

    Seeding is idempotent (``registry.add`` upserts by id and bumps the version), so this updates the
    static seed entries in place and leaves every entry a campaign added — discoveries, negative
    results, provenance — untouched. A full destructive reset is ``registry.clear()``, which is
    deliberately NOT called here: re-ingesting must never throw away the evidence a campaign earned.
    """
    from pacland import fields, structure_build
    n_fields = fields.seed_fields()
    registry.seed_known_unifications()
    # the economics↔hard-science unifications (all five batches)
    from pacland import economics_unify, economics_more, economics_batch2, economics_batch3, economics_batch4
    economics_unify.record()
    economics_more.record()
    economics_batch2.record()
    economics_batch3.record()
    economics_batch4.record()
    # the harvested known-unifications library (38 sourced recognitions)
    from pacland import known_unifications
    known_unifications.record()
    # the harvested soft-field unifications (psychology/sociology/linguistics/urban/politics/…)
    from pacland import soft_unifications
    soft_unifications.record()
    # the comprehensive full catalog (220+ sourced unifications across every sub-field)
    from pacland import full_unifications
    full_unifications.record()
    return {
        "structures": n_fields,
        "lean_proofs": ingest_lean_proofs(),
        "hypotheses": ingest_hypotheses(),
        "disciplines": ingest_disciplines(),
        "tests": ingest_tests(),
        "structure_groups": structure_build.build_structures(),
        "economics_unifications": len(registry.query("mapping", lambda d: True)),
    }


# ------------------------------------------------------------------------------------------ #
# External data integration — other people's data and libraries land in the SAME registry.
# ------------------------------------------------------------------------------------------ #

def ingest_external(contribution: dict) -> dict[str, int]:
    """Ingest an EXTERNAL contribution (another person's domain data) into the registry.

    The contribution is a plain dict in the documented shape::

        {
          "source": "a-slug-identifying-the-project-or-person",
          "description": "one line on what this is",
          "domain": "geology",
          "structures": [{"id": "aquifer", "type": "conservation", "definition": "…",
                          "domain": "geology"}],
          "properties": [{"id": "darcy-law", "statement": "…", "tier": 1, "domain": "geology"}],
          "evidence":   [{"id": "well-log", "test": "…", "dataset": "…", "domain": "geology"}],
          "mappings":   [{"from": "aquifer", "to": "heat-equation", "mapping": "…",
                          "kind_of_yield": "proof-technique"}],
        }

    Every entry is namespaced ``ext:<source>:<id>`` so an external contribution can never collide with
    or overwrite the internal catalog, and each is tagged ``produced_by: "external"`` + its source, so
    the scientific record stays auditable. A mapping's ``from``/``to`` may point at the contribution's
    own structures (auto-namespaced) or at an existing internal structure id (left as-is), so external
    data can be linked to the library the engine already knows. Returns per-kind counts.
    """
    source = str(contribution.get("source", "")).strip() or "external"
    description = str(contribution.get("description", ""))
    domain = str(contribution.get("domain", ""))
    prov = {"produced_by": "external", "source": source, "method": "contribution",
            "description": description, "ts": time.time()}

    n = {"structures": 0, "properties": 0, "evidence": 0, "mappings": 0}

    def _ext(entry_id: str) -> str:
        return f"ext:{source}:{entry_id}"

    own_ids: set[str] = set()
    for s in contribution.get("structures", []):
        sid = str(s.get("id", ""))
        if not sid:
            continue
        own_ids.add(sid)
        registry.add(registry.Entry(
            id=_ext(sid), kind="structure",
            payload={"definition": s.get("definition", ""), "type": s.get("type", ""),
                     "domain": s.get("domain", domain), "tier": s.get("tier", 3),
                     "assumptions": s.get("assumptions", []), "reproduces": s.get("reproduces", "")},
            provenance=prov))
        n["structures"] += 1

    for p in contribution.get("properties", []):
        pid = str(p.get("id", ""))
        if not pid:
            continue
        registry.add(registry.Entry(
            id=_ext(pid), kind="property",
            payload={"name": pid, "statement": p.get("statement", ""), "tier": p.get("tier", 3),
                     "domain": p.get("domain", domain), "falsifier": p.get("falsifier", "")},
            provenance=prov))
        n["properties"] += 1

    for e in contribution.get("evidence", []):
        eid = str(e.get("id", ""))
        if not eid:
            continue
        registry.add(registry.Entry(
            id=_ext(eid), kind="evidence",
            payload={"name": eid, "test": e.get("test", ""), "dataset": e.get("dataset", ""),
                     "what": e.get("what", ""), "tier": 4, "domain": e.get("domain", domain)},
            provenance=prov))
        n["evidence"] += 1

    def _resolve(ref: str) -> str:
        """Namespace a mapping endpoint if it is one of the contribution's OWN structures."""
        return _ext(ref) if ref in own_ids else ref

    for m in contribution.get("mappings", []):
        frm = str(m.get("from", ""))
        to = str(m.get("to", ""))
        if not frm or not to:
            continue
        registry.add(registry.Entry(
            id=_ext(f"mapping-{frm}-{to}"), kind="mapping",
            payload={"from": _resolve(frm), "to": _resolve(to),
                     "mapping": m.get("mapping", ""),
                     "kind_of_yield": m.get("kind_of_yield", "connection")},
            provenance=prov))
        n["mappings"] += 1

    return n


def ingest_library(module) -> dict:
    """Register an EXTERNAL Python library so its data AND its falsifiers become usable by the engine.

    A library module follows the same contribution schema, plus an optional ``FALSIFIERS`` dict::

        SOURCE = "my-project"
        DOMAIN = "geology"
        CONTRIBUTION = {"structures": [...], "properties": [...], "mappings": [...]}
        FALSIFIERS = {"my-check": lambda: (True, "evidence")}

    ``CONTRIBUTION`` is ingested via :func:`ingest_external`; each ``FALSIFIERS`` entry is registered
    into the runner's ``FALSIFIERS`` (namespaced ``ext:<source>:<name>``) AND recorded as an evidence
    claim, so the discovery engine can actually RUN the external checks, not just index their names.
    """
    source = str(getattr(module, "SOURCE", "") or getattr(module, "__name__", "external"))
    out: dict = {"source": source, "falsifiers": 0}
    contrib = getattr(module, "CONTRIBUTION", None)
    if contrib is not None:
        c = dict(contrib)
        c["source"] = source
        out["contribution"] = ingest_external(c)
    falsifiers = getattr(module, "FALSIFIERS", None)
    if isinstance(falsifiers, dict):
        from pacland import runner
        for name, fn in falsifiers.items():
            key = f"ext:{source}:{name}"
            runner.FALSIFIERS[key] = fn
            registry.add(registry.Entry(
                id=f"ext:{source}:evidence-{name}", kind="evidence",
                payload={"name": name, "check": key, "tier": 4,
                         "domain": str(getattr(module, "DOMAIN", ""))},
                provenance={"produced_by": "external", "source": source,
                            "method": "library-falsifier", "ts": time.time()}))
            out["falsifiers"] += 1
    return out


def load_module_from_path(path: str):
    """Import a ``.py`` file as a module (for the ``ingest-library`` CLI)."""
    import importlib.util
    from pathlib import Path
    p = Path(path)
    spec = importlib.util.spec_from_file_location(p.stem, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


def ingest_lean_repo(path: str, source: str = "") -> dict:
    """Ingest an EXTERNAL Lean repo's theorems as tier-1 properties (established + machine-checkable).

    Scans every ``.lean`` file under ``path`` for ``theorem``/``lemma`` declarations and registers each
    as a namespaced tier-1 property. This is the external form of ``ingest_lean_proofs`` — another
    project's proven lemmas enter the property store the synthesis and bound-derivation draw on.
    """
    from pathlib import Path
    p = Path(path)
    if not p.exists():
        return {"lean_theorems": 0}
    source = source or p.name
    n = 0
    for lean in sorted(p.rglob("*.lean")):
        text = lean.read_text(errors="ignore")
        for m in re.finditer(r"^\s*(?:theorem|lemma)\s+([a-zA-Z0-9_']+)", text, re.M):
            name = m.group(1)
            registry.add(registry.Entry(
                id=f"ext:{source}:lean-{name}", kind="property",
                payload={"name": name, "statement": f"theorem {name} (machine-checked)",
                         "tier": 1, "domain": "mathematics", "source": str(lean)},
                provenance={"produced_by": "external", "source": source, "method": "lean-repo",
                            "ts": time.time()}))
            n += 1
    return {"lean_theorems": n}


def ingest_csv(path: str, source: str = "", kind: str = "evidence") -> dict:
    """Ingest a CSV: each row becomes a registry entry of ``kind`` (default evidence), columns → payload.

    A project's tabular data (measurements, catalog rows, benchmark results) lands as queryable
    evidence, namespaced + provenance-tracked like every other external contribution.
    """
    import csv
    from pathlib import Path
    p = Path(path)
    if not p.exists():
        return {"rows": 0}
    source = source or p.stem
    n = 0
    with p.open(newline="", encoding="utf-8") as fh:
        for i, row in enumerate(csv.DictReader(fh)):
            payload = {k: v for k, v in row.items() if v not in ("", None)}
            registry.add(registry.Entry(
                id=f"ext:{source}:{kind}-{i}", kind=kind,
                payload=payload,
                provenance={"produced_by": "external", "source": source, "method": "csv",
                            "ts": time.time()}))
            n += 1
    return {"rows": n}
