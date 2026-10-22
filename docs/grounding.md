# The grounding — what transfers to every discipline, and what was physics-specific

The question: *how do we know we are measuring the right things?* The honest answer
is that only **part** of the string-theory verification kit transfers. The rest was
built for one physics question and must not be assumed to generalize.

## What genuinely transfers (discipline-independent)

1. **Constraints are necessary conditions.** Every field has things that *must* hold —
   conservation (climate), valency/charge (chemistry), a gate passing by name
   (software). Verify what is forbidden, not what is predicted. This is logic, not
   physics, so it transfers unchanged.
2. **The deficit is a conservative lower bound.** Count only what is simultaneously
   measured + computable + validated; `m` is then a floor and the certificate radius a
   ceiling. (The word *validated* is discipline-specific — what counts as validation
   has to be defined per field.)
3. **Mutation-tested guards (falsification).** A check must be able to fail, with a
   seeded fault proving it does. This is the Valiant Verification SDK — software
   engineering, not physics — and it transfers unchanged.

## What was physics-specific (do NOT assume it generalizes)

- **The Rule of Three's specific tests** — mutual information, ridge cross-validation,
  and a permutation null — were built to answer one question: *is this flux observable
  structured or random?* The general idea (get independent agreement) is a heuristic,
  not a method; the specific trio is physics.
- **Known-answer oracles** — mirror symmetry, the exact tadpole — exist because
  Calabi-Yau geometry has exact dualities. Most fields have no such free known-answer,
  so this does not transfer automatically.

## The open question

For each new discipline, *what makes a measurement trustworthy there* is an **open
question to be worked out per field**, not imported from string theory. The three
transferable pieces above are the honest floor; everything else is still to be
established discipline by discipline.

## Worked example — climate's own safeguards (worked out 2026-10-22)

- **Climate's oracle:** `piControl → zero drift`. A pre-industrial control has no
  forcing, so a conserving model *must* be stationary. This is an always-true answer
  from the model's own setup — no external dataset — and the drift data measures the
  violation of it.
- **Climate's Rule of Three:** the **three conservation ledgers** — energy, mass, salt.
  Three independent physics (radiative, mass, and a source-free tracer), all of which a
  conserving model must close. The measured result: 12/19 models leak energy, 6/19 leak
  mass, but only 2/19 leak salt — so the leak lives in the atmosphere-ocean coupling,
  not the ocean model. That is a discipline-specific three-way check, not the physics
  trio (MI/ridge/permutation) borrowed out of place.

## Worked example — drug discovery's own safeguards

- **Drugs' oracle:** **chemical validity** — a molecule must be valency/charge/tautomer-
  consistent (the RDKit-sanitisation standard). A "molecule" with a pentavalent carbon is
  not a molecule; validity is an always-true answer, no opinion required.
- **Drugs' Rule of Three:** three independent checks a candidate must all pass —
  **validity** (well-formed), **drug-likeness** (Lipinski / PAINS / REOS forbidden-state
  filters), **synthesizability** (RAScore accessibility floor). Three different axes
  (structure, medicinal chemistry, synthetic feasibility), each able to rule the
  candidate out on its own.

## Worked example — economics' own safeguards

- **Economics' oracle:** **accounting consistency** — double-entry identities hold *by
  construction*. Income equals expenditure equals output; every financial asset is
  someone's liability. A model that breaks a national-accounts identity is wrong without
  any data — the analogue of a pentavalent carbon (drugs) and piControl → zero drift
  (climate).
- **Economics' Rule of Three:** three independent axes, each from a different
  direction, all pointing at the one claim *"a macro model predicts relations, never
  values"* — **empirical** (out-of-sample forecast failure: Meese–Rogoff / Rossi /
  Gürkaynak), **theoretical** (set-identification: Sonnenschein–Mantel–Debreu / Gorman —
  aggregates never identify the model), and **structural** (the accounting identities —
  double-entry, the only exact content). The three ledgers (circular flow, sectoral
  balances, stock-flow) are three facets of the *structural* axis, not three axes.

The principle each discipline must satisfy: **name its own oracle (the always-true
answer) and its own set of N independent checks (one per failure mode, all must agree).**
Climate, drugs and economics have theirs; each future discipline must work out its own before its
results count as grounded. The *how* — the machine that turns a claim's failure modes
into the minimal check-set, and the sweep that finds it automatically — is
`docs/verification-config.md`.
