# SEXTANT — assessment & correction log

Every external assessment and correction, with its disposition. This is the record we assess together
before making further changes. Dated; newest last.

## Plan assessments (the cross-field plan)

### R1 — the first independent assessment (against plan revision 1)
**Verdict: mostly accepted, all fixed in revision 2.**

| # | point | disposition |
|---|---|---|
| 1 | "a jump = an adjunction" is wrong — adjoints come free for every functor | **accepted** — removed (revision 2); later refined (see R2.2 below) |
| 2 | "lossless round-trip" is wrong — FDM migration is lossy (Σ fills gaps, Δ truncates) | **accepted** — removed |
| 3 | the diffusion↔chemistry test is trivial (known since the 1800s) | **accepted** — replaced with blind-proposal + expert rating |
| 4 | "Migration Is a Modality" citation unverified (may be hallucinated) | **accepted** — removed; CQL.jl narrowed to "proves Σ⊣Δ only" |
| 5 | "emergence / computational irreducibility" adds wording, not a test | **accepted** — dropped |
| 6 | experiment tier has no plan (no datasets/partners/labs) | **accepted** — named the empirical-partner dependency (§6) |
| 7 | status claims contradict earlier plan (core "already built" vs missing pieces) | **accepted** — to reconcile (one honest status table) |
| 8 | one 7B fine-tune per field is unproven + costly | **accepted** — "test one field end-to-end before scale" |
| 9 | packaging (container/MorpheOS) too early | **accepted** — moved after first field passes |
| 10 | success metric undefined | **accepted** — defined (§7) |
| 11 | third SEXTANT strategy doc in ~2 days — settle one | **accepted** — this doc is now the single source; later changes are dated amendments |
| 12 | missing prior work: Topos Institute, AlgebraicJulia, Catlab, structure-mapping, LBD | **accepted** — added (§9) |

### R2 — the product-vision refinements (from Rob)
**Verdict: accepted, incorporated.**

| # | point | disposition |
|---|---|---|
| 1 | the mass gap is the stress test; cross-field discovery is the central product | **accepted** — restated as the core |
| 2 | the 5-tier epistemic classification (established / follows / conjecture / tested-numerically / unknown) | **accepted** — §4 |
| 3 | a correspondence is valuable only by its yield (new prediction / new proof technique / more efficient experiment) | **accepted** — §4a + metric |

### R2.1 — the adjoint-triple correction (from Rob)
**Verdict: accepted.**

| # | point | disposition |
|---|---|---|
| 1 | `Σ ⊣ Δ ⊣ Π` is NOT automatic for every arbitrary functor — it is the data-migration construction (Kan extensions over presheaves) requiring limits/colimits | **accepted** — §3 corrected |
| 2 | do not make the registry a bare category; build a **typed scientific knowledge model** (definition, assumptions, domain, interpretation, proven properties, evidence, limitations, permitted mappings) | **accepted** — §3 rewritten |

## PR assessments (PR #621 — the wiring + benchmark)

### P1 — the generate() gap
**Verdict: accepted, in progress.**

| # | point | disposition |
|---|---|---|
| 1 | the main `generate()` in runner.py is still hard-coded Python branches; the LLM is only in `prove()` and the standalone benchmark | **accepted** — confirmed true |
| 2 | next integration: an explicit LLM-backed candidate generator returning structured hypotheses with **source references, assumptions, proposed mappings, falsifiers** | **accepted — in progress** (the `Candidate` fields added; the `generate_llm` function is next) |
| 3 | keep the deterministic generator as the baseline + fallback | **accepted — planned** |

## Current open items (to assess together)

1. **Finish `generate_llm`** — the LLM-backed candidate generator (structured hypotheses), with the deterministic `generate()` as fallback. Partially built (the `Candidate.assumptions` + `Candidate.proposed_mappings` fields are added and committed).
2. **Reconcile the status table** — one honest "built vs missing" table across the plan docs (R1 #7).
3. **Name the first empirical partner/dataset** before Phase 4–6 (R1 #6) — the climate/economics modules are the candidate.
4. **Decide whether the R1 corrections + R2 refinements are all the right way to go** — this log is the record to assess.

## Disposition convention

- **accepted — fixed** = the change is made + committed.
- **accepted — in progress** = agreed, partly built.
- **accepted — planned** = agreed, not yet started.
- **open** = awaiting a decision.
