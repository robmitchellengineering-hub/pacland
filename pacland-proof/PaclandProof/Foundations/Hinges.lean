import Mathlib

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# The four hinges — the assumptions every quantum-gravity framework leans on

QF-0: the hinge ledger. Each hinge below is a **type** (a `structure`) whose
fields are its **named hypotheses** plus its **conclusion**, with its source in
the doc comment.

**Honesty contract (rule 67 — absent green is not green):** this file *states*
the hinges; it does **not** assert any of them. No term of any `structure` below
is constructed here, and no `instance` is declared. Constructing the terms — with
the real mathematical content — is the work of QF-1 … QF-5. A hinge is OPEN until
a term is built and kernel-checked.

**Structural gate:** every hinge must name at least one hypothesis (a field
prefixed `h_`) and cite a source. A `structure` with zero `h_` fields fails this
gate; a planted blank-hypothesis hinge is caught by the schema, not by Lean's
type-checker.

Source plan: `PLANS/PLAN-quantum-foundations.md` §2, and the consolidated
synthesis `QUANTUM-BEDROCK-AND-QG-SYNTHESIS.md` §5.
-/

noncomputable section

namespace Hinges

/-- F1 — QM reconstruction.
Source: Hardy 2001, arXiv:quant-ph/0101012 (also Chiribella–D'Ariano–Perinotti
arXiv:1011.6451; Masanes–Müller arXiv:1004.1483).
Named hypotheses:
- `h_probability_structure` — outcomes carry a probability calculus.
- `h_operational_composition` — preparations/transformations/measurements compose.
- `h_nonclassical_primitive` — ONE of {continuity of reversible transformations,
  purification, self-duality}.
Conclusion: finite-dimensional complex-Hilbert-space quantum mechanics. -/
structure F1 where
  h_probability_structure : Prop
  h_operational_composition : Prop
  h_nonclassical_primitive : Prop
  conclusion_finite_dim_qm : Prop

/-- F2 — the correlation-set principle (what singles out the quantum set).
Source: Popescu–Rohrlich 1994 (PR-box); Navascués–Pironio–Acín 2007
(almost-quantum, arXiv:0704.1897).
Named hypotheses:
- `h_no_signaling`
- `h_information_causality`
Conclusion: these single out the quantum correlation set (the Tsirelson bound).
**OPEN** — both hypotheses are known to be too weak (PR-boxes, almost-quantum). -/
structure F2 where
  h_no_signaling : Prop
  h_information_causality : Prop
  conclusion_singles_out_quantum : Prop

/-- F3 — the Born rule / definite outcome.
Source: Gleason 1957, Ann. Math. 66:543; Zurek envariance 2003/2005.
Named hypotheses:
- `h_additivity` — probability adds over orthogonal projectors.
- `h_noncontextuality` — the measure depends only on the projector, not the frame.
- `h_dim_ge_three` — the Hilbert-space dimension is at least 3. (Gleason's theorem
  is FALSE in dimension 2: there are additive frame functions not induced by any
  density matrix, so this hypothesis is load-bearing, not decoration.)
Conclusion: the only such measure is `Tr(ρP)` (the Born rule). -/
structure F3 where
  h_additivity : Prop
  h_noncontextuality : Prop
  h_dim_ge_three : Prop
  conclusion_born_rule : Prop

/-- F4 — Lorentz-invariant deterministic guidance no-go.
Source: Berndl–Dürr–Goldstein–Zanghì 1996.
Named hypotheses:
- `h_deterministic_guidance`
- `h_lorentz_invariance`
- `h_foliation_free`
Conclusion: no such guidance law exists (the no-go). -/
structure F4 where
  h_deterministic_guidance : Prop
  h_lorentz_invariance : Prop
  h_foliation_free : Prop
  conclusion_no_go : Prop

end Hinges

end
