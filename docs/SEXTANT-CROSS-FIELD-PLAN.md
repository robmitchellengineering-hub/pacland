# SEXTANT — the cross-field verified-discovery system (full plan)

**The product is the methodology, not any one problem.** The Yang–Mills mass gap was the stress test —
the hardest unsolved problem we aimed at to force the discipline to be honest (falsifier-before-believe,
"we don't fake the open rung"). It may never fall to a 7B model. That's fine: the deliverable is a
**tool for verified scientific research and discovery**, and its real power is **cross-field synthesis**
— breaking the academic silo where specialists rarely meet, and finding the jumps that live *between*
fields.

## 1. The core insight

Real scientific progress is **holistic synthesis** — a jump that combines *verified* results from
several specialist fields into one. Sextant's job is to make those jumps **grounded in proofs**, not
LLM vibes. A cross-field jump is credited only when it is a *verified isomorphism/transfer* between two
fields' structures — not "the model thinks they look similar."

## 2. Settled foundations (from the research)

| question | answer |
|---|---|
| Formal substrate for "structure" + "transfer" | **Category theory** — structure = object; "same" = isomorphism; transfer = functor; unification = natural transformation / adjunction |
| Is it already machine-checkable? | **Yes — Mathlib's `CategoryTheory`** (Category, Functor, NatTrans, Iso, Equivalence, Adjunction, Prop-valued `IsEquivalence`) — nothing to rebuild |
| Prior art for cross-field transfer | **Spivak's functorial data migration** — a functor `F : C → D` induces `Σ_F ⊣ Δ_F ⊣ Π_F`, the lossless round-trip between domains; already machine-certified (Wisnesky "Migration Is a Modality", `CQL.jl`) |
| Search-space model | **Wolfram's multiway graph** — all derivation paths; the falsifier prunes it (concept, not his closed engine) |
| The "emergence" bar | **Computational irreducibility** — an emergence derivation is *provable but irreducible*: verify by replaying the derivation, never by shortcutting it |
| Wolfram's tooling | **Not reusable** (closed Wolfram Engine, enumerator not a discovery engine) — keep the *concepts*, drop the *tooling* |

## 3. The architecture — three layers

```
UNIVERSAL CORE (domain-agnostic, already built)
   radar → generate (6 strategies) → falsify → record (ledger) → believe (calibration) → learn → repeat
   measured by: verified discoveries per unit of effort

DOMAIN PLUGINS (per hard-verification field)
   each field = its falsifiers + verifier + benchmark + a specialist fine-tuned model

CROSS-FIELD LAYER (the new power)
   the structure registry (a category) + the transfer finder (functors/adjunctions) + the isomorphism verifier
```

## 4. The formal model — the structure registry *is* a category

- **Objects** = the *verified structures* of each field (gauge symmetry, diffusion equation, Markov operator, conservation law, codon map, …), each carrying its **type** (its isomorphism class).
- **Morphisms** = structure-preserving maps.
- **"Same structure in two fields"** = an **isomorphism / equivalence** (`Mathlib.Iso` / `IsEquivalence`).
- **Transfer a structure A → B** = a **functor** `F : C → D` with its adjoint triple `Σ_F ⊣ Δ_F ⊣ Π_F` (Spivak's machinery).
- **A cross-field jump** = an **adjunction / natural transformation** showing two fields' structures coincide.

This is the "import a structure from another discipline" made rigorous, and it sits entirely on Mathlib's
already-proven category theory. We stand on Spivak's certified FDM, not open ground.

## 5. Verification — two tiers, plus the emergence bar

1. **Lean (the algebraic core).** The structure's algebra kernel-checks (single-line algebraic proofs).
2. **Empirical (the reality-match).** "The model matches behaviour" survives pre-registered experiment + statistics + null model — *not* Lean.
3. **The emergence bar.** Algebra → behaviour is a derivation; it is *provable but irreducible* (computational irreducibility), so we **verify by replaying the derivation**, never by claiming a shortcut.

A discovery is "verified" when its **algebra kernel-checks** *and* its **emergence derivation is carried**
*and* its **prediction survives the empirical falsifier**.

## 6. The models — specialists + a thin cross-field reader

- **Per-field specialists** (`qwen2.5-discovery-chem`, `-bio`, `-mat`, …) — depth; a 7B model is deep in one field, shallow in all. The `qwen2.5-discovery` recipe repeated per field.
- **A thin cross-field model** — reads only the **registry** (typed structures, not raw literature) and proposes *isomorphisms/transfers*; the one model that sees multiple fields.

## 7. Delivery — two forms of one tool

1. **Container image** — Python loop + Lean + Mathlib + llama.cpp + the GGUF + a supervisor daemon; `pull && run`, the loop runs autonomously and writes discoveries/proofs to a mounted volume.
2. **MorpheOS image** — the same system baked into the OS; boot-and-run appliance.

## 8. Build order (each gated)

| phase | what | gate |
|---|---|---|
| 1 | **supervisor daemon** — close the loop end-to-end | it generates → falsifies → kernel-checks one survivor, no human |
| 2 | **structure registry** — the category; seed it with the structures we already hold (gauge symmetry, diffusion, Markov, conservation) | each entry's type (isomorphism class) kernel-checks |
| 3 | **cross-field transfer** — the functor/adjunction layer on Mathlib | one real transfer (e.g. diffusion physics↔chemistry) kernel-checks as `Σ⊣Δ⊣Π` |
| 4 | **per-domain rollout** — one field at a time: specialist model + falsifiers + benchmark + typed structures | that field beats its rediscovery baseline |
| 5 | **container + MorpheOS** — bundle the whole system | `pull && run` / boot-and-run reproduces phase 1 |
| 6 | **trained model** — the GGUF drops in when training finishes | discovery uses the bundled model, no remote call |

## 9. The honest boundaries

- **Wolfram gives framing, not machinery** — the ruliad ("space of all structures"), multiway ("all derivation paths"), irreducibility ("emergence is provable but not shortcuttable"). The actual machinery is category theory + Mathlib + Spivak's FDM.
- **"Field A's X *is* field B's Y" is a modeling decision** — category theory *verifies* the functor once you name it; it does not *find* it for you. The cross-field model proposes; Lean discharges.
- **The mass gap stays the honest stress test** — it may never fall. It taught us the discipline; it is not the deliverable.

## 10. The one thing the whole plan turns on

The structure registry is the keystone: once a field's verified results are typed structures in a
category, *every other field's open problems can search it for a transfer*. Breadth is then a
side-effect of adding fields to the registry, not a rewrite. That's the silo-breaker, made formal.
