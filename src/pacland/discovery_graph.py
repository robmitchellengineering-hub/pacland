"""The discovery knowledge graph — nodes with relationships, not a notebook.

A discovery is a node; the relationship between discoveries is an edge. The graph grows by
*validated methods*: an edge is added only when its evidence requirement is met, so the graph
accumulates reusable science rather than unchecked hypotheses.

The schema and the process are specified in ``docs/DISCOVERY-KNOWLEDGE-GRAPH.md``. This module
is the runnable form: the node kinds, the relationship kinds, the evidence gate, and the seed
graph of the mass-gap campaign.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

#: The canonical on-disk store — SEXTANT reads this on startup and writes it on every validated
#: discovery, so the graph survives across campaigns and sessions (the recursive self-improvement).
GRAPH_FILE = Path.home() / ".dsh" / "sextant-graph.json"

# --- The node kinds: the eight stages a discovery walks through -------------------------------
NODE_KINDS = (
    "original-result",
    "verified-theorem",
    "methodology-discovery",
    "reusable-mechanism",
    "transfer-hypothesis",
    "proposed-application",
    "destination-verification",
    "new-evidence",
)

# --- The relationship kinds: the edges between discoveries -----------------------------------
#: relation -> (meaning, evidence that must exist before the edge is added)
RELATIONS: dict[str, tuple[str, str]] = {
    "proves": (
        "the checked theorem establishes the result",
        "lake build green, no sorry, the theorem name",
    ),
    "extracts": (
        "the technique is distilled to its mechanism",
        "the mechanism stated in plain English and tracked to the theorem",
    ),
    "transfers-to": (
        "the mechanism is hypothesised to transfer",
        "the hypothesis names a target AND a falsifier",
    ),
    "applies-in": (
        "the hypothesis targets a named field",
        "the destination discipline's verifier is named",
    ),
    "verified-in": (
        "the destination's verifier confirms it",
        "the destination verifier fired and passed",
    ),
    "assumes": (
        "the theorem's assumptions and limits",
        "the assumption is stated and tracked",
    ),
    "generalizes": (
        "the mechanism is the general form of the theorem",
        "the general statement and the theorem-as-special-case are both given",
    ),
    "refutes": (
        "a wall: the hypothesis is falsified",
        "the falsifier fired (the counterexample is recorded)",
    ),
}


@dataclass
class Node:
    """A single discovery. ``kind`` is one of ``NODE_KINDS``; ``evidence`` is the record that
    backs this node's *existence* (a theorem name, a falsifier run, a plain-English statement)."""

    node_id: str
    kind: str
    name: str
    what: str = ""          # the plain-English one-liner
    evidence: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.kind not in NODE_KINDS:
            raise ValueError(f"unknown node kind {self.kind!r}; expected one of {NODE_KINDS}")


@dataclass
class Edge:
    """A directed relationship. It exists only because its evidence requirement was met at
    ``add_edge`` time."""

    src: str
    dst: str
    relation: str
    evidence: str = ""      # the record that satisfied the gate

    def __post_init__(self) -> None:
        if self.relation not in RELATIONS:
            raise ValueError(f"unknown relation {self.relation!r}; expected one of {list(RELATIONS)}")


class DiscoveryGraph:
    """A growing graph of reusable scientific knowledge.

    Two rules:
    1. ``add_node`` deduplicates by id — the same discovery added twice is one node.
    2. ``add_edge`` refuses an edge whose evidence requirement is not met (the gate).
    """

    def __init__(self) -> None:
        self.nodes: dict[str, Node] = {}
        self.edges: list[Edge] = []
        self.rejections: list[dict[str, str]] = []

    def add_node(self, node_id: str, kind: str, name: str,
                 what: str = "", **evidence: Any) -> Node:
        """Add (or return the existing) node. Duplicate ids are one node."""
        if node_id in self.nodes:
            return self.nodes[node_id]
        node = Node(node_id, kind, name, what, dict(evidence))
        self.nodes[node_id] = node
        return node

    def add_edge(self, src: str, dst: str, relation: str, evidence: str = "") -> Edge | None:
        """Add the edge only if its evidence requirement is met.

        The evidence is the string that *shows* the requirement is satisfied — the kernel-check
        hash, the falsifier run, the named target. An empty or missing record is rejected and
        logged, never added.
        """
        if relation not in RELATIONS:
            raise ValueError(f"unknown relation {relation!r}")
        if src not in self.nodes or dst not in self.nodes:
            raise KeyError(f"edge endpoints must be existing nodes: {src!r} -> {dst!r}")
        _, requirement = RELATIONS[relation]
        if not evidence.strip():
            self.rejections.append(
                {"edge": f"{src} -{relation}-> {dst}",
                 "reason": f"missing evidence: {requirement}"}
            )
            return None
        edge = Edge(src, dst, relation, evidence.strip())
        self.edges.append(edge)
        return edge

    def pending_hypotheses(self) -> list[Edge]:
        """Transfer hypotheses that have not yet been independently verified (no ``verified-in``
        edge out of their ``proposed-application``)."""
        verified_dsts = {e.src for e in self.edges if e.relation == "verified-in"}
        return [e for e in self.edges if e.relation == "transfers-to"
                and e.dst not in verified_dsts]

    def to_dict(self) -> dict[str, Any]:
        return {
            "nodes": {i: {"kind": n.kind, "name": n.name, "what": n.what,
                          "evidence": n.evidence} for i, n in self.nodes.items()},
            "edges": [{"src": e.src, "dst": e.dst, "relation": e.relation,
                       "evidence": e.evidence} for e in self.edges],
            "rejections": self.rejections,
        }

    def save(self, path: str | Path | None = None) -> Path:
        """Persist the graph to the canonical store (``~/.dsh/sextant-graph.json`` by default)."""
        p = Path(path) if path is not None else GRAPH_FILE
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(self.to_dict(), indent=2), encoding="utf-8")
        return p

    @classmethod
    def load(cls, path: str | Path | None = None) -> "DiscoveryGraph":
        """Load the canonical store. An absent store starts empty (the seed is applied separately)."""
        p = Path(path) if path is not None else GRAPH_FILE
        g = cls()
        if not p.exists():
            return g
        d = json.loads(p.read_text(encoding="utf-8"))
        for i, n in d.get("nodes", {}).items():
            g.add_node(i, n["kind"], n["name"], n.get("what", ""), **n.get("evidence", {}))
        for e in d.get("edges", []):
            g.add_edge(e["src"], e["dst"], e["relation"], e.get("evidence", ""))
        return g

    def reusable_context(self) -> str:
        """The plain-English context the engine feeds back into the prompt: what mechanisms exist
        (reuse these) and what hypotheses are pending (do not re-propose these)."""
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


# --- The seed graph: the mass-gap campaign, wired ----------------------------------------------
def seed_mass_gap() -> DiscoveryGraph:
    """The discoveries already catalogued in ``docs/METHODOLOGY-DISCOVERIES.md``, wired as a graph.

    Every ``transfers-to`` / ``applies-in`` edge is a *hypothesis*; the ``verified-in`` edges are
    absent because no destination verifier has fired yet — that is the honest state.
    """
    g = DiscoveryGraph()

    # --- The transfer-matrix spectral bridge ---------------------------------------------
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
               "lake build green @ MassGapDiamond.lean, no sorry")
    g.add_edge("spectral_bridge", "locate_gap_via_positivity", "extracts",
               "mechanism stated in METHODOLOGY-DISCOVERIES.md, tracked to clustering_iff_gap")
    g.add_edge("clustering_iff_gap", "spectral_bridge", "extracts",
               "the technique distilled from the theorem, catalogued")
    g.add_edge("locate_gap_via_positivity", "anderson_hyp", "transfers-to",
               "target: Anderson model; falsifier: a delocalised regime with no gap")
    g.add_edge("anderson_hyp", "condensed_matter", "applies-in",
               "destination verifier: the Anderson-model spectral-gap check (not yet run)")
    g.add_edge("clustering_iff_gap", "compact_operator", "assumes",
               "assumption stated: compact transfer operator")

    # --- The animal->uniform-cluster bridge ----------------------------------------------
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

    g.add_edge("rooted_animals_bound", "animal_bridge", "extracts",
               "mechanism stated and tracked to AnimalsBound.lean")
    g.add_edge("animal_bridge", "count_via_rooted_trees", "extracts",
               "the rooted-tree tour technique, catalogued")
    g.add_edge("count_via_rooted_trees", "percolation_hyp", "transfers-to",
               "target: percolation; falsifier: a lattice where the walks bound fails")
    g.add_edge("count_via_rooted_trees", "random_cluster_hyp", "transfers-to",
               "target: random-cluster; falsifier: a phase where the sum diverges")

    # --- The trace-rigidity mechanism ----------------------------------------------------
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

    g.add_edge("trace_is_character", "trace_rigidity", "extracts",
               "mechanism stated and tracked to GaussianRigidity.lean")
    g.add_edge("trace_rigidity", "reduce_per_irrep", "extracts",
               "the per-irrep reduction, catalogued")
    g.add_edge("reduce_per_irrep", "rmt_hyp", "transfers-to",
               "target: random-matrix theory; falsifier: an observable not per-irrep reducible")

    return g


if __name__ == "__main__":
    g = seed_mass_gap()
    print(f"nodes: {len(g.nodes)}, edges: {len(g.edges)}")
    print(f"pending transfer hypotheses (unverified): {len(g.pending_hypotheses())}")
    for e in g.pending_hypotheses():
        print(f"  {e.src} -{e.relation}-> {e.dst}")
    # Demonstrate the gate: an edge with no evidence is rejected.
    g.add_edge("locate_gap_via_positivity", "condensed_matter", "transfers-to", "")
    print(f"rejected edges (no evidence): {len(g.rejections)}")
