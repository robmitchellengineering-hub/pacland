"""The discovery knowledge graph — nodes with relationships, not a notebook.

A discovery is a node; the relationship between discoveries is an edge. The graph grows by
*validated methods*: an edge is added only when (a) its endpoint node kinds are the right ones for
that relationship and (b) its relationship-specific evidence validator passes. So the graph
accumulates reusable science rather than unchecked hypotheses.

The schema and the process are specified in ``docs/DISCOVERY-KNOWLEDGE-GRAPH.md``. This module is
the runnable form.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

#: The canonical on-disk store — SEXTANT reads this on startup and writes it on every validated
#: discovery, so the graph survives across campaigns and sessions (the recursive self-improvement).
GRAPH_FILE = Path.home() / ".dsh" / "sextant-graph.json"

# --- The node kinds: the stages a discovery walks through --------------------------------------
NODE_KINDS = (
    "original-result",
    "verified-theorem",
    "methodology-discovery",
    "reusable-mechanism",
    "open-obligation",        # the frontier: the thing still to prove
    "transfer-hypothesis",
    "proposed-application",
    "destination-verification",
    "new-evidence",
)


# --- Relationship-specific evidence validators -------------------------------------------------
# Each validator takes the structured evidence dict and returns (ok, reason-when-not-ok).

def _v_proves(e: dict[str, Any]) -> tuple[bool, str]:
    ok = bool(e.get("theorem")) and e.get("sorry_free") is True
    return ok, "" if ok else "needs a Lean theorem name + sorry_free=True"


def _v_extracts(e: dict[str, Any]) -> tuple[bool, str]:
    ok = bool(e.get("mechanism")) and bool(e.get("tracked_to"))
    return ok, "" if ok else "needs the mechanism in plain English + tracked_to a theorem"


def _v_transfers(e: dict[str, Any]) -> tuple[bool, str]:
    ok = bool(e.get("target")) and bool(e.get("falsifier"))
    return ok, "" if ok else "needs a named target AND a falsifier"


def _v_applies(e: dict[str, Any]) -> tuple[bool, str]:
    ok = bool(e.get("verifier"))
    return ok, "" if ok else "needs the destination discipline's verifier named"


def _v_verified_in(e: dict[str, Any]) -> tuple[bool, str]:
    ok = e.get("passed") is True
    return ok, "" if ok else "needs the destination verifier to have fired and passed"


def _v_assumes(e: dict[str, Any]) -> tuple[bool, str]:
    ok = bool(e.get("assumption"))
    return ok, "" if ok else "needs the assumption stated and tracked"


def _v_generalizes(e: dict[str, Any]) -> tuple[bool, str]:
    ok = bool(e.get("general")) and bool(e.get("special_case"))
    return ok, "" if ok else "needs the general statement AND the theorem-as-special-case"


def _v_directly_applies(e: dict[str, Any]) -> tuple[bool, str]:
    ok = bool(e.get("mechanism"))
    return ok, "" if ok else "needs the mechanism the frontier's proof runs on"


def _v_refutes(e: dict[str, Any]) -> tuple[bool, str]:
    ok = bool(e.get("counterexample"))
    return ok, "" if ok else "needs the counterexample recorded"


def _v_yields(e: dict[str, Any]) -> tuple[bool, str]:
    ok = bool(e.get("technique"))
    return ok, "" if ok else "needs the technique named"


# --- The relationship kinds: (meaning, src kind, dst kind, validator) ---------------------------
RELATIONS: dict[str, tuple[str, str, str, Callable[[dict[str, Any]], tuple[bool, str]]]] = {
    "proves": ("the checked theorem establishes the result",
               "verified-theorem", "original-result", _v_proves),
    "yields": ("the theorem's proof yields the reusable technique",
               "verified-theorem", "methodology-discovery", _v_yields),
    "extracts": ("the technique is distilled to its mechanism",
                 "methodology-discovery", "reusable-mechanism", _v_extracts),
    "transfers-to": ("the mechanism is hypothesised to transfer",
                     "reusable-mechanism", "transfer-hypothesis", _v_transfers),
    "applies-in": ("the hypothesis targets a named field",
                   "transfer-hypothesis", "proposed-application", _v_applies),
    "verified-in": ("the destination's verifier confirms it",
                    "proposed-application", "destination-verification", _v_verified_in),
    "assumes": ("the theorem's assumptions and limits",
                "verified-theorem", "new-evidence", _v_assumes),
    "generalizes": ("the mechanism is the general form of the theorem",
                    "reusable-mechanism", "verified-theorem", _v_generalizes),
    "directly-applies-to": ("the mechanism directly advances an open obligation",
                            "reusable-mechanism", "open-obligation", _v_directly_applies),
    "refutes": ("a wall: the hypothesis is falsified",
                "new-evidence", "transfer-hypothesis", _v_refutes),
}


_STOPWORDS = {"the", "and", "for", "via", "are", "has", "that", "which", "this", "with",
              "from", "into", "onto", "does", "not", "its", "each", "been", "also", "than"}


def _overlaps(text: str, haystack: str) -> bool:
    """A keyword-overlap match for cross-synthesis. Stronger than a single-word hit: requires at
    least two content words (stopwords excluded) to overlap the mapping, with a light prefix-stem
    (``spectrum``~``spectral``, ``positivity``~``positive``) so a common word like 'the' cannot fake
    a unification. The emitted declaration is still a *hypothesis* gated by its falsifier — this is
    a recall signal, not a verdict."""
    words = {w for w in text.lower().replace("-", " ").split()
             if len(w) >= 3 and w not in _STOPWORDS}
    hay_words = [w for w in haystack.lower().replace("-", " ").split() if len(w) >= 3]
    hits = 0
    for w in words:
        if any(w.startswith(h[:4]) or h.startswith(w[:4]) for h in hay_words):
            hits += 1
    return hits >= 2


@dataclass
class Node:
    """A single discovery. ``kind`` is one of ``NODE_KINDS``; ``evidence`` backs this node's
    *existence* (a theorem name, a falsifier run, a plain-English statement)."""

    node_id: str
    kind: str
    name: str
    what: str = ""
    evidence: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.kind not in NODE_KINDS:
            raise ValueError(f"unknown node kind {self.kind!r}; expected one of {NODE_KINDS}")


@dataclass
class Edge:
    """A directed relationship. It exists only because its type pair and evidence validator both
    passed at ``add_edge`` time."""

    src: str
    dst: str
    relation: str
    evidence: dict[str, Any] = field(default_factory=dict)


class DiscoveryGraph:
    """A growing graph of reusable scientific knowledge.

    Three rules:
    1. ``add_node`` deduplicates by id.
    2. ``add_edge`` enforces the valid (src kind, dst kind) pair for the relation.
    3. ``add_edge`` runs the relation's evidence validator and rejects a failure.
    """

    def __init__(self) -> None:
        self.nodes: dict[str, Node] = {}
        self.edges: list[Edge] = []
        self.rejections: list[dict[str, str]] = []

    def add_node(self, node_id: str, kind: str, name: str,
                 what: str = "", **evidence: Any) -> Node:
        if node_id in self.nodes:
            return self.nodes[node_id]
        node = Node(node_id, kind, name, what, dict(evidence))
        self.nodes[node_id] = node
        return node

    def add_edge(self, src: str, dst: str, relation: str, evidence: dict[str, Any]) -> Edge | None:
        """Add the edge only if (a) the relation is known, (b) the endpoints exist and their kinds
        are the relation's valid pair, and (c) the relation's evidence validator passes."""
        if relation not in RELATIONS:
            raise ValueError(f"unknown relation {relation!r}")
        if src not in self.nodes or dst not in self.nodes:
            raise KeyError(f"edge endpoints must be existing nodes: {src!r} -> {dst!r}")
        _, src_kind, dst_kind, validator = RELATIONS[relation]
        if self.nodes[src].kind != src_kind or self.nodes[dst].kind != dst_kind:
            self.rejections.append({
                "edge": f"{src} -{relation}-> {dst}",
                "reason": (f"invalid type pair: {relation} needs {src_kind} -> {dst_kind}, "
                           f"got {self.nodes[src].kind} -> {self.nodes[dst].kind}"),
            })
            return None
        ok, reason = validator(dict(evidence))
        if not ok:
            self.rejections.append({"edge": f"{src} -{relation}-> {dst}", "reason": reason})
            return None
        edge = Edge(src, dst, relation, dict(evidence))
        self.edges.append(edge)
        return edge

    def verified_hypotheses(self) -> list[str]:
        """Transfer-hypotheses whose full chain closes: transfers-to -> applies-in -> verified-in
        (with the destination verifier passed)."""
        # map transfer-hypothesis id -> its proposed-application id
        applies = {e.src: e.dst for e in self.edges if e.relation == "applies-in"}
        verified_apps = {e.src for e in self.edges if e.relation == "verified-in"}
        out = []
        for e in self.edges:
            if e.relation != "transfers-to":
                continue
            app = applies.get(e.dst)
            if app is not None and app in verified_apps:
                out.append(e.dst)
        return out

    def pending_hypotheses(self) -> list[Edge]:
        """Transfer-hypotheses whose full chain is NOT yet closed — no verified-in edge on their
        proposed-application. These are to verify, not re-propose."""
        verified = set(self.verified_hypotheses())
        return [e for e in self.edges if e.relation == "transfers-to" and e.dst not in verified]

    def reusable_context(self) -> str:
        mechanisms = [n for n in self.nodes.values() if n.kind == "reusable-mechanism"]
        pending = self.pending_hypotheses()
        parts = []
        if mechanisms:
            parts.append("Reusable mechanisms already discovered (reuse, do not re-derive):")
            parts += [f"  - {m.name}: {m.what}" for m in mechanisms]
        if pending:
            parts.append("Transfer hypotheses pending (do not re-propose — verify instead):")
            parts += [f"  - {self.nodes[e.dst].name}: {self.nodes[e.dst].what}" for e in pending]
        return "\n".join(parts)

    def directly_useful_mechanisms(self) -> list[str]:
        return [e.src for e in self.edges if e.relation == "directly-applies-to"]

    def non_directly_useful_mechanisms(self) -> list[str]:
        direct = set(self.directly_useful_mechanisms())
        return [i for i, n in self.nodes.items()
                if n.kind == "reusable-mechanism" and i not in direct]

    def cross_synthesize(self, mappings: list[dict]) -> list[Edge]:
        """Emit unification declarations for the mechanisms that are NOT directly useful."""
        emitted: list[Edge] = []
        for mid in self.non_directly_useful_mechanisms():
            m = self.nodes[mid]
            hay_text = (m.name + " " + m.what).lower()
            for mapping in mappings:
                mapping_text = (f"{mapping.get('from', '')} {mapping.get('to', '')} "
                                f"{mapping.get('mapping', '')}").lower()
                if not _overlaps(hay_text, mapping_text):
                    continue
                hyp_id = f"hyp-{mid}-{mapping.get('to', 'unknown')}"
                self.add_node(hyp_id, "transfer-hypothesis",
                              f"{m.name} -> {mapping.get('to', '')}",
                              f"unification: {mapping.get('mapping', '')}")
                edge = self.add_edge(mid, hyp_id, "transfers-to",
                                     {"target": mapping.get("to", ""),
                                      "falsifier": f"the destination verifier fails to "
                                                   f"reproduce {m.name}"})
                if edge is not None:
                    emitted.append(edge)
        return emitted

    def to_dict(self) -> dict[str, Any]:
        return {
            "nodes": {i: {"kind": n.kind, "name": n.name, "what": n.what,
                          "evidence": n.evidence} for i, n in self.nodes.items()},
            "edges": [{"src": e.src, "dst": e.dst, "relation": e.relation,
                       "evidence": e.evidence} for e in self.edges],
            "rejections": self.rejections,
        }

    def save(self, path: str | Path | None = None) -> Path:
        p = Path(path) if path is not None else GRAPH_FILE
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(self.to_dict(), indent=2), encoding="utf-8")
        return p

    @classmethod
    def load(cls, path: str | Path | None = None) -> "DiscoveryGraph":
        p = Path(path) if path is not None else GRAPH_FILE
        g = cls()
        if not p.exists():
            return g
        d = json.loads(p.read_text(encoding="utf-8"))
        for i, n in d.get("nodes", {}).items():
            g.add_node(i, n["kind"], n["name"], n.get("what", ""), **n.get("evidence", {}))
        for e in d.get("edges", []):
            ev = e.get("evidence", {})
            if not isinstance(ev, dict):
                # a stale pre-validator store had string evidence — skip, the seed regenerates it
                continue
            g.add_edge(e["src"], e["dst"], e["relation"], ev)
        return g


# --- The seed graph: the mass-gap campaign, wired ----------------------------------------------
def seed_mass_gap() -> DiscoveryGraph:
    g = DiscoveryGraph()

    g.add_node("clustering_iff_gap", "verified-theorem", "clustering iff spectral gap",
               "exponential decay <=> second eigenvalue strictly below the first",
               theorem="MassGapDiamond.clustering_iff_gap", sorry_free=True)
    g.add_node("mass_gap_is_spectral", "original-result", "the mass gap is a spectral gap",
               "m = -log(lambda1/lambda0)")
    g.add_node("spectral_bridge", "methodology-discovery", "transfer-matrix spectral bridge",
               "locate a gap in a spectrum, not as an analogy but exactly")
    g.add_node("locate_gap_via_positivity", "reusable-mechanism",
               "locate a gap in a spectrum via positivity",
               "self-adjoint + positive => real spectrum, simple top eigenvalue")
    g.add_node("anderson_hyp", "transfer-hypothesis", "Anderson-model spectral gap",
               "the same positivity bridge should locate the gap in the Anderson model")
    g.add_node("condensed_matter", "proposed-application", "condensed-matter spectral theory",
               "the spectral-gap location, applied to disordered systems")
    g.add_node("compact_operator", "new-evidence", "assumes a compact transfer operator",
               "the bridge needs compactness, which dies in the infinite-volume limit")

    g.add_edge("clustering_iff_gap", "mass_gap_is_spectral", "proves",
               {"theorem": "MassGapDiamond.clustering_iff_gap", "sorry_free": True})
    g.add_edge("spectral_bridge", "locate_gap_via_positivity", "extracts",
               {"mechanism": "locate a gap via positivity", "tracked_to": "clustering_iff_gap"})
    g.add_edge("clustering_iff_gap", "spectral_bridge", "yields",
               {"technique": "transfer-matrix spectral bridge"})
    g.add_edge("locate_gap_via_positivity", "anderson_hyp", "transfers-to",
               {"target": "Anderson model", "falsifier": "a delocalised regime with no gap"})
    g.add_edge("anderson_hyp", "condensed_matter", "applies-in",
               {"verifier": "the Anderson-model spectral-gap check"})
    g.add_edge("clustering_iff_gap", "compact_operator", "assumes",
               {"assumption": "compact transfer operator"})

    g.add_node("rooted_animals_bound", "verified-theorem", "rooted_animals_count_bound_gen",
               "connected clusters of size n <= |V| (2n) (Delta+1)^(2(n-1))",
               theorem="AnimalsBound.rooted_animals_count_bound_gen", sorry_free=True)
    g.add_node("animal_bridge", "methodology-discovery", "animal->uniform-cluster bridge",
               "size-class summability closes the cluster expansion into a uniform bound")
    g.add_node("count_via_rooted_trees", "reusable-mechanism",
               "count connected subgraphs via rooted spanning trees",
               "a rooted tree has an Euler tour of length 2(n-1), each step <= Delta choices")
    g.add_node("percolation_hyp", "transfer-hypothesis", "percolation / polymer expansion",
               "the walks-count bound transfers to counting connected subgraphs elsewhere")
    g.add_node("random_cluster_hyp", "transfer-hypothesis", "random-cluster model",
               "the size-class summability transfers to the random-cluster connectivity")

    g.add_edge("rooted_animals_bound", "animal_bridge", "yields",
               {"technique": "animal->uniform-cluster bridge"})
    g.add_edge("animal_bridge", "count_via_rooted_trees", "extracts",
               {"mechanism": "count via rooted spanning trees", "tracked_to": "rooted_animals_bound"})
    g.add_edge("count_via_rooted_trees", "percolation_hyp", "transfers-to",
               {"target": "percolation", "falsifier": "a lattice where the walks bound fails"})
    g.add_edge("count_via_rooted_trees", "random_cluster_hyp", "transfers-to",
               {"target": "random-cluster", "falsifier": "a phase where the sum diverges"})

    g.add_node("trace_is_character", "verified-theorem", "trace_is_fundamental_character",
               "Tr g = 2 cos theta = sin(2theta)/sin theta",
               theorem="GaussianRigidity.trace_is_fundamental_character", sorry_free=True)
    g.add_node("trace_rigidity", "methodology-discovery", "trace = fundamental character",
               "the non-Abelian trace observable is the spin-1/2 character")
    g.add_node("reduce_per_irrep", "reusable-mechanism",
               "reduce a group-average observable per-irrep",
               "Peter-Weyl: Tr U = sum_r chi_r, so bounds reduce to per-character")
    g.add_node("rmt_hyp", "transfer-hypothesis", "random-matrix / representation theory",
               "the per-character reduction transfers to matrix observables")

    g.add_edge("trace_is_character", "trace_rigidity", "yields",
               {"technique": "trace = fundamental character"})
    g.add_edge("trace_rigidity", "reduce_per_irrep", "extracts",
               {"mechanism": "reduce per-irrep", "tracked_to": "trace_is_character"})
    g.add_edge("reduce_per_irrep", "rmt_hyp", "transfers-to",
               {"target": "random-matrix theory",
                "falsifier": "an observable not per-irrep reducible"})

    g.add_node("animals_bound_rung", "open-obligation", "the volume-uniform cluster bound",
               "the single-cluster expansion must close into a volume-uniform bound")
    g.add_node("gaussian_rigidity_rung", "open-obligation", "the gauge-invariance rigidity",
               "prove the physical YM covariance is the covariant Laplacian")

    g.add_edge("count_via_rooted_trees", "animals_bound_rung", "directly-applies-to",
               {"mechanism": "rooted-tree walk count"})
    g.add_edge("reduce_per_irrep", "gaussian_rigidity_rung", "directly-applies-to",
               {"mechanism": "per-irrep reduction"})

    return g


if __name__ == "__main__":
    g = seed_mass_gap()
    print(f"nodes: {len(g.nodes)}, edges: {len(g.edges)}")
    print(f"directly useful mechanisms: {g.directly_useful_mechanisms()}")
    print(f"non-directly useful: {g.non_directly_useful_mechanisms()}")
    mappings = [
        {"from": "markov-chain-monte-carlo", "to": "wright-fisher",
         "mapping": "a reversible Markov chain's spectral gap bounds mixing time"},
        {"from": "gauge-symmetry", "to": "crystal-space-group",
         "mapping": "a gauge field is a connection on a principal bundle; its field strength is curvature"},
    ]
    emitted = g.cross_synthesize(mappings)
    print(f"unification declarations emitted: {len(emitted)}")
    for e in emitted:
        print(f"  {e.src} -{e.relation}-> {g.nodes[e.dst].name}")
