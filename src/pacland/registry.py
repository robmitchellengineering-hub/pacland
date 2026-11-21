"""registry.py — the five connected registries: the keystone of the cross-field engine.

Five stores (Structures / Domains / Properties / Evidence / Mappings), all sharing stable IDs,
versioning, provenance, and claim↔evidence links. This is the *seed*: append-only JSONL files + a
cross-cutting entry shape. The cross-field search queries these; the model retrieves the underlying
evidence on demand instead of reading papers.

A discovery query (§10 of the plan) is: a structure in domain A whose type matches an open problem in
domain B, whose properties transfer through a permitted mapping, and whose evidence holds.
"""
from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass, field, asdict
from pathlib import Path

REGISTRY_DIR = Path.home() / ".dsh" / "sextant-registry"
KINDS = ("structure", "domain", "property", "evidence", "mapping")


@dataclass
class Entry:
    id: str
    kind: str                      # one of KINDS
    payload: dict                  # the domain-specific body (definition / domain / property / evidence / mapping)
    version: int = 1
    provenance: dict = field(default_factory=dict)   # {produced_by, method, ts}
    links: list[str] = field(default_factory=list)   # stable ids of linked entries (claim ↔ evidence)


def _store(kind: str) -> Path:
    if kind not in KINDS:
        raise ValueError(f"unknown registry kind {kind!r}; expected one of {KINDS}")
    return REGISTRY_DIR / f"{kind}.jsonl"


def add(entry: Entry) -> Entry:
    """Upsert an entry into its store.

    Re-seeding the same id REPLACES it in place (bumping its version) instead of appending a
    duplicate, so re-ingestion is idempotent; an unknown id is appended. This is what makes the
    store safe for long-running campaigns: a seed refresh updates the static entries and leaves every
    accumulated (dynamic) entry — discoveries, negative results, provenance — untouched.
    """
    entry.provenance.setdefault("ts", time.time())
    p = _store(entry.kind)
    p.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    replaced = False
    if p.exists():
        for ln in p.read_text(encoding="utf-8").splitlines():
            if not ln.strip():
                continue
            try:
                d = json.loads(ln)
            except json.JSONDecodeError:
                lines.append(ln)  # preserve an unparseable line verbatim — never silently drop it
                continue
            if d.get("id") == entry.id:
                entry.version = int(d.get("version", 1)) + 1
                lines.append(json.dumps(asdict(entry)))
                replaced = True
            else:
                lines.append(ln)
    if not replaced:
        lines.append(json.dumps(asdict(entry)))
    p.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    return entry


def get(kind: str, entry_id: str) -> dict | None:
    """Retrieve one entry by id."""
    if not _store(kind).exists():
        return None
    for ln in _store(kind).read_text().splitlines():
        try:
            d = json.loads(ln)
        except json.JSONDecodeError:
            continue
        if d.get("id") == entry_id:
            return d
    return None


def query(kind: str, predicate) -> list[dict]:
    """All entries of a kind satisfying predicate(dict)."""
    if not _store(kind).exists():
        return []
    out = []
    for ln in _store(kind).read_text().splitlines():
        try:
            d = json.loads(ln)
        except json.JSONDecodeError:
            continue
        if predicate(d):
            out.append(d)
    return out


def clear() -> None:
    """Wipe every store — the registry is a seed, and reseeding should start clean."""
    for kind in KINDS:
        p = _store(kind)
        if p.exists():
            p.unlink()
    lp = REGISTRY_DIR / "links.jsonl"
    if lp.exists():
        lp.unlink()


def link(id_a: str, id_b: str, kind: str = "structure") -> None:
    """Add a cross-link between two entries (claim ↔ evidence). In-place, by re-writing the store line."""
    # minimal: record the link in a dedicated links store (claim↔evidence, reversible)
    with (REGISTRY_DIR / "links.jsonl").open("a") as f:
        f.write(json.dumps({"a": id_a, "b": id_b, "kind": kind, "ts": time.time()}) + "\n")


def _seed_entry(kind: str, pid: str, payload: dict, **kw) -> Entry:
    return Entry(id=pid, kind=kind, payload=payload,
                 provenance={"produced_by": "seed", "method": "known-unification"}, **kw)


def seed_known_unifications() -> None:
    """Seed the known-unifications library: established cross-field MAPPINGS (links). The structures
    themselves are seeded by ``fields.seed_fields`` — this only adds the known links between them.
    These are RECOGNITIONS, not discoveries (§2 of the plan)."""
    add(_seed_entry("mapping", "heat-diffusion-walk",
        {"from": "heat-equation", "to": "brownian-motion",
         "mapping": "the diffusion equation is the continuum limit of the symmetric random walk",
         "kind_of_yield": "proof-technique"}))
    add(_seed_entry("mapping", "gauge-connection",
        {"from": "gauge-symmetry", "to": "crystal-space-group",
         "mapping": "a gauge field is a connection on a principal bundle; its field strength is curvature — the same local-symmetry structure as a crystal space group",
         "kind_of_yield": "proof-technique"}))
    add(_seed_entry("mapping", "markov-population",
        {"from": "markov-chain-monte-carlo", "to": "wright-fisher",
         "mapping": "a reversible Markov chain's spectral gap bounds mixing time — the same operator as population-genetic drift",
         "kind_of_yield": "proof-technique"}))


def new_id() -> str:
    return uuid.uuid4().hex[:12]
