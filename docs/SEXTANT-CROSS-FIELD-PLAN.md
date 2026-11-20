# SEXTANT — the cross-field verified-discovery system (revision 2)

**Revision 2, dated 2026-11-19.** Revision 1 made four errors that an independent assessment caught, and
this revision corrects them: (1) it treated "an adjunction" as a *discovery*, when the adjoints come free
for every functor; (2) it implied FDM migration is "lossless", when Σ fills gaps and Δ truncates; (3) it
used a trivial known link (diffusion) as the test; (4) it cited "Migration Is a Modality" unverified.
This revision removes those, re-centres on the *encoding* as the thing to check, and adds a **library of
known unifications** so the system recognises "already known" instead of rediscovering it.

## 1. The core insight (unchanged)

Real scientific progress is **holistic synthesis** — jumps that combine *verified* results from several
fields. Sextant's job is to make those jumps **grounded in proofs**, not LLM vibes. The mass gap was the
stress test; the product is the methodology.

**What a "discovery" is, precisely:** a transfer between two fields that (a) was **proposed blind** (the
system did not have the link pre-loaded), (b) reproduces a **non-trivial, checkable property** in the
target field, and (c) is rated **non-trivial and correct** by outside experts. An already-known link is
*not* a discovery — it belongs in the **library**, below.

## 2. Two libraries, not one registry

- **The known-unifications library.** Established cross-field links (heat↔diffusion↔random-walk, gauge↔connection, Markov↔population↔mean-reversion, …) — each with its *encoding* and the *non-trivial property it reproduces*. The system checks new candidates **against this library first**: "already known" is a *recognition*, not a discovery, and the library is the seed that stops reinvention.
- **The open-transfer frontier.** Candidates that are *not* in the library. These are what the discovery criterion (blind proposal + property reproduction + expert rating) is applied to.

## 3. What category theory actually is here (corrected)

Category theory is the **verification substrate**, not the discovery engine:

- a **structure** = an object in a category, with its **encoding** stated explicitly;
- "the same structure" = an **isomorphism** (`Mathlib.Iso` / `IsEquivalence`) — checkable;
- a **transfer** = a **functor** — *naming it is a modeling decision we must make, and the encoding of that functor is the step we check*;
- the adjoint triple `Σ ⊣ Δ ⊣ Π` is **not automatic** for every arbitrary functor: it belongs to the specific **data-migration construction** (Kan extensions over presheaf categories), and it requires suitable conditions (limits/colimits). It is neither free-for-everything nor a discovery criterion — it is one *mechanism*, applicable only where the conditions hold.

**The registry is NOT a bare category.** A bare category of structures permits *mathematically valid but scientifically meaningless* correspondences (a formally correct functor between vacuous encodings). To block that, the registry is a **typed scientific knowledge model, representable categorically** — every registered structure carries, in full:

1. its **formal mathematical definition**;
2. its **assumptions and constraints**;
3. its **domain and interpretation** (what it is a model *of*, in which field);
4. its **proven properties** (tier 1–2 of the classification);
5. its **empirical evidence** (tier 4), where applicable;
6. its **known limitations**;
7. its **permitted mappings** to other structures (which correspondences are allowed).

Category theory then operates on *that* carefully defined information — the functor/isomorphism is checked against the structure's **domain, assumptions, and permitted mappings**, so a correspondence must be both mathematically valid **and** scientifically meaningful. The gate is: *does `F` actually carry the structure's proven property, within its stated domain and permitted mappings, kernel-checked?*

## 4. The epistemic classification — every claim carries exactly one tier

The discipline the mass-gap work forced, now the standing classification for every field. Every structure,
result, and correspondence carries ONE tag, and is promoted up a tier only by a *check*, never by assertion:

1. **Mathematically established** — kernel-checked (Lean).
2. **Follows from established** — derived from tier-1 results by a carried, checked derivation.
3. **Conjecture** — proposed, neither established nor refuted.
4. **Tested numerically** — supported by simulation/data, not proven.
5. **Genuinely unknown** — no evidence either way.

The falsifier-before-believe loop is the machine that moves claims *between* these tiers: a Lean proof
promotes 3→1, a passing experiment promotes 4→2, a refutation drops any tier to 5 or below. No claim is
*reported* above its tier.

## 4a. What a cross-field correspondence must yield

A correspondence between two fields is valuable **only by what it yields** — and exactly one of three things:

1. a **new prediction** — a testable consequence in the target field that was not known;
2. a **new proof technique** — a method that discharges an open target-field claim;
3. a **more efficient experiment** — a cheaper/faster way to test a target-field claim.

A correspondence that yields none of the three is a curiosity, not a discovery. The isomorphism itself is
plumbing; the *yield* is the discovery.

## 5. The models (corrected)

- **Per-field specialists** — one fine-tune per hard-verification field. **Unproven and costly**, so this is a *test before scale* decision: build ONE field end-to-end first and measure whether its specialist beats a baseline before training more.
- **A thin cross-field proposer** — reads the two libraries and *proposes* candidate transfers. It is judged by the §3 gate + §4 experts, not by its own confidence.

## 6. The one honest dependency: an empirical partner

**Resolved for the first field: climate.** The climate module already carries the empirical tier in-tree —
the CMIP6 conservation-drift falsifier (Irving et al. 2021 data), a reference model, the ECS/energy-budget
models, and 19 test files with passing gates. So the first field needs no new partner to start: the dataset
and falsifiers already exist. The cross-field pair for the first real test is then **climate ↔ physics**
(e.g. a statistical-mechanics structure matched to a climate model), which is exactly the §4a yield test.

## 6. The one honest dependency: an empirical partner

The empirical tier cannot run in a container. Before Phases 4–6, the plan must **name one real dataset or
partner** for the first field (the existing climate and economics modules already have real datasets —
those are the natural first field). Without that, most outputs stall at the Lean tier, and we must say so
rather than relabel them "verified."

## 7. Success metric (defined)

**A verified discovery** = a correspondence that (a) was proposed blind, (b) is absent from the known-unifications library, (c) kernel-checks its encoding/iso, (d) **yields at least one of {new prediction, new proof technique, more efficient experiment}**, and (e) is rated non-trivial+correct by an outside expert. **Metric = verified discoveries per unit of total cost** (compute + model + human expert time). Recognitions from the library count as 0 (plumbing); a correspondence that yields none of the three counts as 0 too.

## 8. Build order (packaging moved last)

| phase | what | gate |
|---|---|---|
| 1 | **supervisor daemon** — close the loop | generates → falsifies → kernel-checks one survivor |
| 2 | **known-unifications library** — seed with established links + their encodings + reproduced properties | each entry's encoding + property kernel-checks |
| 3 | **encoding-check gate** — the functor must actually carry the property (not a vacuous iso) | one non-trivial *known* link re-proven by its encoding |
| 4 | **ONE field, end-to-end** — its specialist model + falsifiers + benchmark + a named empirical dataset/partner | that field beats its baseline; the transfer test is *blind proposal* + expert rating |
| 5 | **blind-transfer test harness** — the system proposes transfers with the target hidden | outside experts rate the proposals non-trivial + correct |
| 6 | **container + MorpheOS** — only after phase 4 passes | `pull && run` / boot reproduces phase 4 |

## 9. Prior work we stand beside (added)

- **Applied category theory** — the Topos Institute, the AlgebraicJulia ecosystem, **Catlab** (Spivak's own group) — likely design partners, not just citations.
- **Analogy-finding in AI/cognitive science** — structure-mapping theory (Gentner).
- **Literature-based discovery** — Swanson-style hidden-link mining.
- **Functorial data migration** — Spivak / Wisnesky; `CQL.jl` proves **Σ ⊣ Δ** (not the full triple), and FDM migration is **lossy** (Σ fills gaps, Δ truncates) — stated correctly here.

## 10. The keystone — the five-registry search engine

The registry is **proper scientific infrastructure**, not a list of Lean theorem names. It is **five connected
registries**, each a distinct queryable store, all sharing **stable IDs, versioning, provenance, and
claim↔evidence links**:

1. **Structures** — formal definitions, encodings, types (isomorphism classes), assumptions/constraints.
2. **Domains** — fields, interpretations, terminology (the "meaningful in a field" layer).
3. **Properties** — proven facts + conjectures, each with its **five-tier epistemic status**.
4. **Evidence** — **reproducible computation** (the code), **experimental protocols**, **outcomes**,
   **null results**, and **replication history** (the under-recorded half of science, captured deliberately).
5. **Mappings** — permitted transfers + the **known-unifications library**, separate from the open frontier.

**The architecture that makes it scalable:** the cross-field search engine **queries this structured body**,
and the model **retrieves the underlying evidence on demand** when it investigates a candidate — it does not
read thousands of papers every time it searches for a connection. Search is over a *verified, typed* index;
the evidence is a pointer the model follows only when a candidate needs it.

This is the foundation the whole system turns on: a cross-field discovery is a query across all five
registries — *"a structure in domain A whose type matches an open problem in domain B, whose properties
transfer through a permitted mapping, and whose evidence holds"* — assembled from linked entries, each
carrying its real scientific body. Breadth is then a side-effect of adding fields to the registries, and
the honesty is the encoding-check + the blind-proposal rating.

## 11. Honest status — what is built vs missing (reconciled, 2026-11-19)

The earlier plan (TOOL-SEXTANT-PLAN.md, Nov 19) listed the problem finder, memory, budget control and the
LLM generator as missing. This is the reconciled, audited status against the actual code:

| component | status |
|---|---|
| generate (6 strategies) | built — deterministic + `generate_llm` (P1) |
| falsify (SEXTANT + `run()`) | built |
| record (ledger + `record()`) | built |
| rank / promote (EIG) | built |
| prove (Lean, `prove()`) | built |
| the loop driver (`run_autonomous`) | built |
| radar (problem finder) | **built — minimal** (`radar()` surfaces the top-EIG open problem; `run_autonomous()` is self-starting) |
| memory / learn | **built — minimal** (`memory.py`: append-only search history + per-strategy success, wired into the loop) |
| budget control | partial — a `budget` argument, no dedicated module |
| the five registries | **not built** — planned (§10) |
| cross-field transfer layer | **not built** — planned (§3) |
| empirical tier + partner | **not built** — needs a partner (§6) |

So "the universal core is built" was **over-stated**: the *loop* (generate→falsify→record→rank→prove) is
built and runs, but the **radar** (finding its own problems) and the **memory/learn** layer are missing,
and the cross-field layer is entirely unbuilt. The honest first field is the existing climate/economics
modules (real data, real falsifiers already in-tree).
