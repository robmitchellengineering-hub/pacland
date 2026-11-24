# SEXTANT knowledge architecture — one schema, four consumers (priority 2)

Priority 1 gave us the accounting; priority 2 makes it the *single source of truth* the rest of the
machine reads. Today the knowledge is scattered across `sextant.py` (claims), `index.json` (docs),
`research-frontier.json` (the accounting), the Lean tower (proofs), and the session logs (what was
tried and rejected). The architecture collapses them into one node-schema.

## The node-schema

Every research object — a theorem, a claim, a doc, an approach, a rejection — is one node with the
same fields:

| field | meaning | values / example |
|---|---|---|
| `name` | the identifier | `mass_gap_of_radius_bound`, `ym-linked-cluster-contraction` |
| `kind` | what sort of object | `theorem` \| `claim` \| `doc` \| `approach` \| `rejection` |
| `state` | where the proof stands | `proved-lemma` \| `proved-transport` \| `open-obligation` \| `rejected` |
| `tier` | how far the proof goes | `identity` \| `lemma` \| `chain` \| `conditional` \| `result` |
| `proof` | the certificate | the Lean theorem name (kernel-checked) |
| `hypothesis` | the open X (transports only) | `ρ ≤ e^(−A·e^(−cβ))` |
| `falsifier` | what would refute it | a numeric counterexample or a type-inhabitation |
| `evidence` | the run that supports it | `lake build` green @ hash, or the falsifier survived |
| `tasks` | the open work items | the animals bound, the equivalence-collapse |
| `rejected_attempts` | what was tried and failed | the compactness wall, the `∈`/`in` notation, … |
| `source` | where it lives | `Lean` \| `SEXTANT` \| `doc` |

The rule that makes this an architecture and not another registry: **every field has one writer.**
The Lean kernel writes `proof` and `state`; the falsifiers write `evidence`; the engine writes
`tasks` and `rejected_attempts`; the docs write `hypothesis` and the narrative. Nothing is typed by
hand twice.

## The four consumers

1. **Memory** — the cross-session files (`AGENTS.md`, `QUANTUM-READY-MORPHEOS.md`) stop carrying the
   facts and instead carry *pointers* to nodes ("the open obligations are the `open-obligation`
   nodes in `research-frontier.json`"). Memory becomes an index, not a second copy.
2. **Registries** — the SEXTANT CATALOG and the site index are *generated* from the schema, the way
   `index.json` is generated from the repo (and the test fails if they drift).
3. **Evidence** — a falsifier run or a kernel-check writes `evidence` on the node; the verdict and
   the tier are derived, never asserted.
4. **Proof tiers** — the five tiers are a function of the node's `state` + `proof`, not a free-text
   field. A `conditional` with an empty `hypothesis` is a type error in the schema.

## The rejected-approaches registry (what the walls were)

The schema keeps rejections because they are information. The first concrete entries, harvested from
this session's dead-ends (each one a wall that was a lesson, not a mistake):

| rejection | why it failed | the workaround that won |
|---|---|---|
| SU(2) compactness + Haar via Heine–Borel | no `CompactSpace`/`PositiveCompacts` for `specialUnitaryGroup` | `Measure.toSphere` (S³ = SU(2)) |
| `specialUnitaryGroup` as a `Group` | it is a `Submonoid`, not a `Group` | associativity-only (`Monoid`) form |
| `∏ p in s` BigOperators notation | parse error on the `in` binder | `∏ p ∈ s` (`∈`) |
| `Finset.prod_insert` in the subset identity | metavariable / wrong occurrence | `show B = C` + `apply sum_congr rfl` + explicit pointwise |
| `neighborSet` subtype in the walks count | `G.neighborSet : V → Set V` not a type | explicit `{w // w ∈ G.neighborSet u}` + `Fintype.card_coe` |
| the "reduction" milestone framing | re-labelled the same wall as progress | the accounting graph + the three states |

## The concrete next step

Migrate the existing artifacts into the schema: `research-frontier.json` becomes the schema instance,
`sextant.py`'s CATALOG becomes a *view* over it (generated, with a drift test), and the rejected
registry above becomes `web/rejections.json` that the interface renders. That is the infrastructure
the engine (priority 3) loops on and the interface (priority 4) exposes.
