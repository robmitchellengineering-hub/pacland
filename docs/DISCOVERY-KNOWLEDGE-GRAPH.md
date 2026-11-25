# The discovery knowledge graph — nodes with relationships, not a notebook

**Why this exists.** A research notebook is a flat list of notes. A knowledge graph is notes
*wired together*. The difference is the difference between "we wrote down what happened" and "the
machine can reason about what it learned and reuse it." This file is the schema for the graph: the
node types, the relationship types, the process that adds them, and the evidence each relationship
requires before it may exist.

The rule that makes it powerful rather than another registry: **an edge is only added when its
evidence requirement is met.** The graph grows by *validated methods*, not by accumulating more
AI-generated hypotheses.

## The node types — the eight stages a discovery walks through

A single mathematical result travels through eight stages. Each stage is a node; each arrow between
stages is a relationship. The stages:

| # | node kind | what it is | example (from the mass-gap work) |
|---|---|---|---|
| 1 | `original-result` | the mathematical result, before proof | "the mass gap is a spectral gap" |
| 2 | `verified-theorem` | the kernel-checked source theorem | `clustering_iff_gap` (Lean, no `sorry`) |
| 3 | `methodology-discovery` | the reusable technique that did the work | "the transfer-matrix spectral bridge" |
| 4 | `reusable-mechanism` | the mechanism, in plain English | "locate a gap in a spectrum via positivity" |
| 5 | `transfer-hypothesis` | "this could apply to X" | "could locate a gap in the Anderson model" |
| 6 | `proposed-application` | the named discipline / field | condensed-matter spectral theory |
| 7 | `destination-verification` | the independent verifier that fired | the Anderson-model spectral gap check |
| 8 | `new-evidence` | the assumptions, limits, and validation | "assumes a compact transfer operator" |

## The relationship types — the edges

| relation | direction | meaning |
|---|---|---|
| `proves` | `verified-theorem` → `original-result` | the checked theorem establishes the result |
| `extracts` | `methodology-discovery` → `reusable-mechanism` | the technique is distilled to its mechanism |
| `transfers-to` | `reusable-mechanism` → `transfer-hypothesis` | the mechanism is hypothesised to transfer |
| `applies-in` | `transfer-hypothesis` → `proposed-application` | the hypothesis targets a named field |
| `verified-in` | `proposed-application` → `destination-verification` | the destination's verifier confirms it |
| `assumes` | `verified-theorem` → `new-evidence` | the theorem's assumptions and limits |
| `generalizes` | `reusable-mechanism` → `verified-theorem` | the mechanism is the general form |
| `refutes` | `new-evidence` → `transfer-hypothesis` | a wall: the hypothesis is falsified |

## The process — the seven steps that add a discovery

When the engine lands a lemma or a technique, it runs this loop — and it adds nodes/edges to the
graph only where the evidence is met:

1. **Check whether the discovery already exists.** Search the graph for the same mechanism. If it is
   already a node, do not duplicate — link to it.
2. **Identify its original provenance.** Find the `verified-theorem` (or the pre-proof
   `original-result`) it came from.
3. **Extract the underlying mechanism.** Write the plain-English `reusable-mechanism` — the part that
   transfers, separated from the part that is specific to this problem.
4. **Generate a formal or computational test where possible.** A falsifier for the mechanism, or a
   kernel-check of the theorem.
5. **Record assumptions and limitations.** The `new-evidence` node: what it assumes, where it breaks.
6. **Create proposed cross-field transfer links.** The `transfer-hypothesis` → `proposed-application`
   edges, each with a named target and a falsifier.
7. **Update the graph only when the relevant evidence requirement is met.** An edge whose evidence
   is absent is *not* added; it is a pending hypothesis, not a fact.

## The evidence requirement per edge (the gate)

| relation | evidence that must exist before the edge is added |
|---|---|
| `proves` | `lake build` green, no `sorry`, the theorem name |
| `extracts` | the mechanism is stated in plain English and tracked to the theorem |
| `transfers-to` | the hypothesis names a target **and** a falsifier |
| `applies-in` | the destination discipline's verifier is named |
| `verified-in` | the destination verifier **fired and passed** |
| `assumes` | the assumption is stated and tracked |
| `generalizes` | the general statement and the theorem-as-special-case are both given |
| `refutes` | the falsifier fired (the counterexample is recorded) |

This is what "the graph grows by validated methods" means concretely: a `transfers-to` edge without a
falsifier, or a `verified-in` edge without a passed run, is rejected at the gate.

## The seed graph — the mass-gap discoveries, wired

The discoveries already catalogued in `METHODOLOGY-DISCOVERIES.md` seed the graph (this is the first
campaign, so every `transfers-to` / `applies-in` / `verified-in` edge below is a *hypothesis*, marked
as pending until the destination verifier fires):

```
clustering_iff_gap (verified-theorem)
    └─proves→  "the mass gap is a spectral gap" (original-result)
    └─extracts→  transfer-matrix spectral bridge (methodology-discovery)
                    └─extracts→  "locate a gap in a spectrum via positivity" (reusable-mechanism)
                        ├─transfers-to→  "Anderson-model spectral gap" (transfer-hypothesis)
                        │                   └─applies-in→  condensed matter (proposed-application)
                        │                                       └─verified-in→  (destination-verification, PENDING)
                        └─assumes→  "compact transfer operator" (new-evidence)

rooted_animals_count_bound_gen (verified-theorem)
    └─extracts→  animal→uniform-cluster bridge (methodology-discovery)
                    └─extracts→  "count connected subgraphs via rooted spanning trees" (reusable-mechanism)
                        ├─transfers-to→  "percolation / polymer expansion" (transfer-hypothesis)
                        └─transfers-to→  "random-cluster model" (transfer-hypothesis)

trace_is_fundamental_character (verified-theorem)
    └─extracts→  "trace = fundamental character" (methodology-discovery)
                    └─extracts→  "reduce a group-average observable per-irrep" (reusable-mechanism)
                        └─transfers-to→  "random-matrix / representation theory" (transfer-hypothesis)
```

Every `verified-in` edge in the seed is **pending** — the destination verifier has not fired. That is
the honest state: the mechanisms and the transfer hypotheses exist; the independent confirmations do
not yet.

## Why this is more than a notebook

- **It deduplicates.** Step 1 means the same mechanism discovered twice becomes one node, not two notes.
- **It separates provenance from promise.** A `verified-theorem` (checked) and a `transfer-hypothesis`
  (unchecked) are different node kinds with different evidence gates — they cannot be confused.
- **It makes the machine *better each campaign*.** The next campaign starts with the existing
  mechanisms, so it does not re-derive them — it *reuses* them. That is the "progressively more
  capable with every campaign" loop, driven by validated methods, not by more hypotheses.

The companion files are `METHODOLOGY-DISCOVERIES.md` (the plain-English catalog of the same
discoveries) and `SEXTANT-KNOWLEDGE-ARCHITECTURE.md` (the node-schema this graph should migrate into).
The runnable form of this schema is `src/pacland/discovery_graph.py`.
