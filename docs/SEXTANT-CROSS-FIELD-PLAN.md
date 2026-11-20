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
- the adjoints `Σ ⊣ Δ ⊣ Π` are **free** for any functor — so their existence is **not** evidence of anything. They are plumbing, not a discovery.

**The thing we check is the encoding, not the adjunction.** Each library entry ships as: `(field A, structure X, encoding E_X, property P_A(X) that E_X must reproduce)` and `(field B, structure Y, encoding E_Y, property P_B(Y))`, plus the functor `F` claiming `X ≅ Y`. The gate is: *does `F` actually carry `P_A` to `P_B`, kernel-checked?* If the encoding is invented and `F` is vacuous, the check fails — that is the point.

## 4. Verification — three tiers, no fake bar

1. **Lean (the encoding + the isomorphism).** The encoding and the functor kernel-check; the claimed property is actually carried. (This is the only tier an autonomous machine can fully discharge on its own.)
2. **Empirical (the reality-match).** The transferred prediction survives a pre-registered experiment / held-out data / null model. **This tier is only claimable where a dataset or partner exists** — see §6; without one, an output stops at the Lean tier and is *not* called "verified."
3. **Expert rating.** Blind-proposed transfers are rated by outside specialists for *non-triviality and correctness*. A transfer that reproduces a known result is rated trivial; the rating is part of the record.

**Removed:** the "computational irreducibility / emergence bar" (revision 1). It added wording, not a test — "verify by replay" is already what Lean and simulation do. Dropped.

## 5. The models (corrected)

- **Per-field specialists** — one fine-tune per hard-verification field. **Unproven and costly**, so this is a *test before scale* decision: build ONE field end-to-end first and measure whether its specialist beats a baseline before training more.
- **A thin cross-field proposer** — reads the two libraries and *proposes* candidate transfers. It is judged by the §3 gate + §4 experts, not by its own confidence.

## 6. The one honest dependency: an empirical partner

The empirical tier cannot run in a container. Before Phases 4–6, the plan must **name one real dataset or
partner** for the first field (the existing climate and economics modules already have real datasets —
those are the natural first field). Without that, most outputs stall at the Lean tier, and we must say so
rather than relabel them "verified."

## 7. Success metric (defined)

**A verified discovery** = a transfer that (a) was proposed blind, (b) is absent from the known-unifications
library, (c) kernel-checks its encoding/iso, (d) reproduces a non-trivial property, and (e) is rated
non-trivial+correct by an outside expert. **Metric = verified discoveries per unit of total cost** (compute
+ model + human expert time). Recognitions from the library count as *0 discoveries* (they are plumbing).

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

## 10. The keystone (unchanged, but honest)

The two libraries are the keystone: once a field's structures are encoded with their reproduced properties,
every other field's open problems can search them — and the library of *known* links is what stops the
system from mistaking "reinventing heat diffusion" for a discovery. Breadth is a side-effect of adding
fields; the honesty is the encoding-check + the blind-proposal rating.
