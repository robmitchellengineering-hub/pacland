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
| 2 | next integration: an explicit LLM-backed candidate generator returning structured hypotheses with **source references, assumptions, proposed mappings, falsifiers** | **accepted — fixed** (`generate_llm` + `generate_candidates`; verified live against `qwen2.5-discovery`) |
| 3 | keep the deterministic generator as the baseline + fallback | **accepted — fixed** (`generate()` unchanged; `generate_candidates` falls back to it) |

### R2.3 — the five-registry search engine (from Rob)
**Verdict: accepted, incorporated into §10.**

| # | point | disposition |
|---|---|---|
| 1 | the registry must be proper infrastructure (5 connected registries), not Lean theorem names | **accepted** |
| 2 | Evidence must capture: reproducible computation, experimental protocols, outcomes, null results, replication history | **accepted** — §10 |
| 3 | all five share stable IDs, versioning, provenance, claim↔evidence links | **accepted** — §10 |
| 4 | the model must QUERY the structured body + retrieve evidence ON DEMAND (not read thousands of papers per search) — the scalable architecture | **accepted** — §10 |

## Current open items (to assess together)

1. ~~**Finish `generate_llm`**~~ — **done** (`generate_llm` + `generate_candidates`; both paths verified).
2. ~~**Reconcile the status table**~~ — **done** (plan §11). Note: the radar is now built (minimal) — see the new item below.
3. ~~**Name the first empirical partner/dataset**~~ — **done**: climate (CMIP6 drift, Irving et al. 2021 data + reference model, already in-tree with passing gates).
4. **Decide whether the R1 corrections + R2 refinements are all the right way to go** — this log is the record to assess.

## The meta-lesson (why the scrutiny happened, and the fix)

The corrections were earned, not unfair. Almost every one traces to the SAME discipline violations the
system is built to stop: over-asserting conjecture as established, glossing from memory instead of reading
sources, unverified citations, a known-since-1800s link as a test, contradicting the prior status table,
an undefined metric, packaging before validation, and churn (3 strategy docs in 2 days).

**The fix, going forward:** run my own plans through the falsifier before releasing them — every claim a
tier not an assertion, every citation fetched, the metric defined, the test able to fail, the status
reconciled, one plan with dated amendments, validation before delivery. The discipline built for other
people's claims now applies to my own plans first.

### R1.1 — the minimal radar (self-starting loop)
**Verdict: built.**

The radar (problem finder) was the last missing core component. Added `radar()` — ranks the open hypotheses
by EIG and surfaces the top one (currently `ym-mass-gap`), and `run_autonomous(problem=None)` now defaults to
it, so the loop is self-starting. The full cross-field radar (querying the five registries) remains gated on
the registries being built.

### R1.2 — the memory / learn stage
**Verdict: built (minimal).**

Added `memory.py` — an append-only search history (problem → strategy → candidate → verdict) + `strategy_success()`
(which strategies produce survivors vs falsified), wired into `run_autonomous` so every candidate's verdict is
remembered. The full cross-field memory (learning across the five registries) remains gated on the registries.

### R1.3 — the five registries (seed)
**Verdict: started (minimal seed).**

`registry.py` — the five stores (Structures/Domains/Properties/Evidence/Mappings) with a shared `Entry` shape
(id, kind, version, provenance, links), append-only JSONL persistence, `add/get/query/link`, and a
`seed_known_unifications()` with three established links (diffusion↔walk, gauge↔connection, Markov↔population),
each carrying its type + the non-trivial property it reproduces. The full cross-field search + evidence
retrieval is the next step.

### R1.4 — phase-1 gate verified (the loop closes end-to-end)
**Verdict: verified live.**

`run_autonomous(rounds=1, budget=2)` ran the full loop: radar surfaced `ym-mass-gap`, the LLM generated
2 candidates, the falsifiers + 8-stage challenges ran, and both candidates came back **open** (no falsifier
can measure the mass gap yet) — the loop honestly reported "open" instead of faking a survivor. That is the
discipline working. To exercise the "survivor" branch the loop must be pointed at a problem with a runnable
falsifier (e.g. `ou-gap`), which is the next smoke-test step, not a loop defect.

## Disposition convention

- **accepted — fixed** = the change is made + committed.
- **accepted — in progress** = agreed, partly built.
- **accepted — planned** = agreed, not yet started.
- **open** = awaiting a decision.
