# What transfers out of this programme, and for what it should not be claimed

Written for a reader from another discipline. The question is narrow and answerable: **which parts of
this work are discipline-independent, what would each need to be used elsewhere, and which parts are
locked to high-energy theory.**

The honest summary: the **method** transfers almost anywhere; the **mathematics** transfers to inverse
problems and to any spectrum; the **physics results** do not transfer at all.

## Tier 1 — the method, which needs no physics

Four practices, each bought with a failure recorded in this repository.

### 1.1 A certificate carries a falsifier and a remedy, or it is not certified

Every claim here is a gate with six fields: **name, result, evidence, producer, falsifier, remedy.**
Regulated industries already have the *shape* — ISO/IEC 17025 uncertainty budgets, FDA software V&V,
SR 11-7 model risk in banking, Goal Structuring Notation safety cases — and **none of them make the
falsifier and the remedy mandatory**.

What that adds is specific: a claim is not certified until someone has written **the sentence that would
make it wrong** and **what they would do about it**. On 2026-10-29 the format caught a mislabel inside one
of its own *verified* certificates, because the falsifier was a checkable sentence and was checked.

**Transfer cost: none.** It is a template and an enforcement hook.

### 1.2 A check that cannot fail in the way you fear is not a check

A test asserting `|control − constant| > 0.05` was true under *either* of the two ensembles it was meant to
distinguish, so it could never catch the mislabel. This is the dominant failure mode of compliance testing
everywhere: **tests that pass by construction.**

The repair is mechanical — for each check, ask *what state of the world would make this red, and is that
state reachable by the defect I am worried about?* — and it is cheap. It is also the single highest-yield
practice in this document.

### 1.3 Compare against a control of the same kind and the same size, never an asymptotic constant

A finite measurement compared against an asymptotic reference measures **the estimator**, not the world.
Transfers directly to:

| field | the same mistake looks like |
|---|---|
| clinical trials | a historical control instead of a matched, contemporaneous one |
| econometrics | an in-sample fit compared to a theoretical asymptotic distribution |
| climate | a model–observation comparison against the wrong baseline period |
| machine learning | a baseline matched on architecture but not on capacity or compute |

### 1.4 Reproducibility is a gate, not an aspiration

A committed certificate that differs by one byte from a fresh run fails the build. Documents that quote a
number are checked against the artefact that produces it. Scripts named in a document must exist in the
repository — a rule added after four runners were cited and never merged.

**Transfer cost: low.** It needs a runner and a committed artefact, not a research programme.

## Tier 2 — the mathematics, for inverse problems and spectra

### 2.1 Identifiability is decided by noise, not by rank

The generalisation with the widest reach. Rank and conditioning say whether a parameter set *could* be
determined; the **Cramér–Rao bound** says whether it *can be*, at the noise level you actually have.

Measured here, on a modal identification problem with 36 parameters: at **−70 dB** of measurement noise
about 23 parameters are identifiable to 10%; at **−60 dB** about **3**; at **−50 dB** **none**, and what
survives is a handful of **combinations**.

| field | the question it answers |
|---|---|
| seismic imaging | how many subsurface parameters are recoverable from N receivers at this SNR? |
| structural health monitoring | how many modes from N accelerometers before the answer is noise? |
| chemical kinetics | how many rate constants from N experiments? |
| medical imaging | how many tissue parameters are separable at this contrast-to-noise? |
| EEG / fMRI source localisation | how many sources from this electrode count? |

**Transfer cost: one day per domain** — the Jacobian and the noise model are discipline-specific, and
nobody should quote our numbers for their domain. The *method* is immediate; the *numbers* never transfer.

### 2.2 Weyl's law with the surface term

Mode counting from volume **and surface area** alone, to 0.02% in the worked case. The surface term is the
part that makes small volumes accurate. Applies to electromagnetic cavities (EMC chamber design, microwave
filters), structural modal density, nuclear level densities, quantum-dot density of states.

### 2.3 Poisson vs GOE as an integrability diagnostic

Level-spacing statistics distinguish an integrable system (Poisson) from a chaotic one (GOE/GUE). Standard
in nuclear spectra, molecular rovibrational levels and microwave billiards. The practical addition from
this programme: **a chaotic spectrum is easier to identify than a degenerate one**, because resolvable
levels are identifiable levels — and a degenerate one has *no* fluctuation statistics to report at all.

### 2.4 Truncation can converge while the observable stays unresolved

A series was converged exactly (`d₂ = d₃` at every point) while the quantity of interest stayed limited by
something else entirely (the sampler's budget). The distinction maps onto lattice-QCD continuum
extrapolation, effective-field-theory truncation, celestial-mechanics perturbation order, and asymptotic
series in fluids:

> **The parameter you varied being converged does not mean the quantity you care about is resolved.**

## Tier 3 — what does not transfer, stated plainly

The following are locked to high-energy theory and should never be presented as products for other fields:

- the **flux invariant ring** (the D3 tadpole as the unique exact structure of a flux pair);
- the **swampland coefficients** on T⁶ (α = 1, z = 1 — exact *there*, and about *that* model);
- **Gopakumar–Vafa integrality** and its defect;
- the **AdS identity** at a supersymmetric vacuum (`V = −3e^K|W|²`);
- **Calabi–Yau** geometric data.

They are strong results and they are not generalisable. **A transfer claim that reaches for these is the
one to distrust.**

## What a transfer actually requires

1. **the domain's Jacobian and noise model** (identifiability), or **its counting function and spectrum**
   (level statistics) — a day, plus a domain expert who can say what the noise floor really is;
2. **a control computed in that domain at that size** — not borrowed;
3. **the falsifier written before the first run**, and kept when the answer is null.

The method is free. The numbers are never free.

## The one-line version

> **The discipline transfers; the numbers do not.** What this programme offers another field is not a
> result about their system, but a way of making their claims fail loudly — including on days when the
> claim is ours.
