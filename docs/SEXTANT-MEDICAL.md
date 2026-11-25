# SEXTANT — a verified research and discovery tool, for medicine

*One page for a clinician-researcher who is not a programmer.*

## What it is, in one breath

SEXTANT does not guess — it **verifies**. You hand it a research claim ("this treatment works",
"this molecule is a drug candidate", "these two diseases share a mechanism"), and it tells you, with
a machine-checked answer, **what is actually supported by evidence and what is a prediction**. It
also searches *across* disciplines — physics, chemistry, mathematics — for a mechanism that might
explain your medical question.

The name is the point: a sextant doesn't create the stars, it reads your position from them. SEXTANT
doesn't invent medicine — it reads, from the evidence and the proofs, where a claim actually stands.

## What it can do for your research

**1. Check a claim — and get a verdict, not an opinion.**
Every claim is classified into one of four honest boxes:
- **FORCED** — proven (a machine-checked mathematical proof holds),
- **FREE** — a free parameter, not determined by the theory,
- **IMPOSSIBLE** — a no-go (it cannot hold),
- **IRREDUCIBLE** — computable but with no closed-form certificate (still open).

"Does drug X bind target Y?" is a claim. So is "this screening hit is actually a drug candidate."
SEXTANT tells you which box each sits in, and *why*, with the evidence attached.

**2. The verification deficit — the number medicine is missing.**
The single most useful thing SEXTANT gives a clinician is a **number**: how much of a decision is
*measured and validated* versus *predicted*. Concretely, in drug discovery it reports: a screening
decision rests on only ~4 measured endpoints, so the molecule you would actually synthesise is
**0% verified** — it is extrapolation, not verification. That number is what turns "promising" into
"we know exactly how little we know."

**3. Cross-field discovery — the reason a doctor should care about a maths tool.**
The field of medicine has a "silo" problem: a mechanism known in physics or chemistry may be the
exact thing your disease question needs, and no one connects them. SEXTANT's discovery engine finds
those transfers — for example, a *spectral-gap* argument from quantum field theory that applies
directly to *molecular dynamics*, or a *connected-structure* counting technique from lattice physics
that applies to *protein folding*. It proposes the link, then **tests whether it would fail**.

**4. Track the journey, not just the answer.**
When SEXTANT works a problem, the *intermediate* discoveries — the reusable techniques, the dead
ends that taught something — are kept, explained in plain English, and connected in a growing graph.
So a year later you can read back *what the machine actually did*, not just the final answer.

## What it is *not* (the honest limits)

- It does **not** replace a doctor, a trial, or a lab. It verifies claims, proposes hypotheses, and
  measures the gap. **The clinical decision stays yours.**
- It does **not** invent drugs on its own — it *verifies* that a candidate (from any model) is valid,
  drug-like, and synthesizable, and tells you the deficit.
- Its verdict is as good as the evidence you give it. No measured endpoint, no verification — and it
  says so, rather than pretending.

## How to use it (no programming needed)

1. **Read the live explainer** (the same system, in browser form) — the human-readable front page of
   the verdict engine and the discovery map.
2. **Ask a claim.** The tool has a plain question-and-answer surface: type (or click) a claim, and it
   returns the verdict (FORCED / FREE / IMPOSSIBLE / IRREDUCIBLE) plus the evidence and the proof.
3. **Contribute a discovery.** There is a "contribute" flow where you record a research finding, a
   dead end, or an assumption — and the tool files it into the growing knowledge graph.
4. **Point it at your own AI.** If you already use an AI assistant, you can hook it in as the idea
   generator; SEXTANT remains the verifier that checks what it proposes.

## The one-line pitch to give a colleague

> "SEXTANT is a verification tool for research: it tells you which of your claims are proven, which
> are free assumptions, which are impossible, and how much of your decision is measured rather than
> predicted — and it finds mechanisms from other sciences that apply to your problem."
