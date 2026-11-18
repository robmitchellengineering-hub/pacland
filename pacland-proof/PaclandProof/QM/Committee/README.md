# Committee statement files (ported from yang-mills-group/OpenAI-YM-20261028)

These four files are the PUBLIC STATEMENT of the Gross committee's existence claim
(`yang-mills-group/OpenAI-YM-20261028`, commit `3456e5e75cf8`), ported to Mathlib v4.35 with only the
`import` lines adjusted. They are the committee's work, Apache-2.0 licensed; the original license and
attribution remain theirs.

- `PublicTheory.lean` — Wightman axioms W0–W3 (Hilbert space, fields, Poincaré, energy-momentum).
- `PublicWilson.lean` — the Wilson lattice (plaquette action, product Haar, the continuum limit).
- `ChallengeSpec.lean` — the joint target (`JointExistence`).
- `PublicView.lean` — public view (notation/instance audit).

These are imported ONLY as a statement anchor — so `MassGapSpec.lean` can state `HasEnergyGap` /
`HasMassGap` against the committee's real `WightmanTheory`/`Hierarchy` API. We do NOT import the
committee's `Solution.lean` proof (it is unverified and does not cover the mass gap).

Porting status: `PublicTheory.lean` compiles clean on v4.35 (0 errors). The remaining three are
statement-level and are checked individually.
