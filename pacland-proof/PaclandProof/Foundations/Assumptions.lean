import Mathlib
import PaclandProof.Foundations.Hinges
import PaclandProof.Foundations.PRBox

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# QF-6 — the assumption table (the honesty ledger)

One machine-readable row per hinge: which hinge, its source, and its STATUS.
`proved` means a kernel-checked term exists (F2's negative: `PRBox.prbox_nonlocal`);
`stated` means the hinge is a `Hinges.F*` structure with named hypotheses but no
term constructed (rule 67 — a statement is not a proof).

This is the ledger the whole track runs on: a hinge without a `proved` row is
OPEN, whatever prose may claim.
-/

noncomputable section

namespace Hinges

/-- Hinge status: `proved` (a kernel-checked term exists) or `stated`
(type declared, no term constructed). -/
inductive Status where
  | proved
  | stated

/-- One row of the assumption table. -/
structure Assumption where
  hinge : String
  source : String
  status : Status

/-- The assumption table. F2's negative is PROVED; F1, F3, F4 are STATED
(their terms are the work of QF-1, QF-3, QF-5). -/
def assumptionTable : List Assumption :=
  [ { hinge := "F1 QM reconstruction", source := "Hardy 2001, arXiv:quant-ph/0101012", status := Status.stated }
  , { hinge := "F2 correlation-set principle", source := "Popescu-Rohrlich 1994; NPA 2007", status := Status.proved }
  , { hinge := "F3 Born rule", source := "Gleason 1957, Ann. Math. 66:543", status := Status.stated }
  , { hinge := "F4 Lorentz-guidance no-go", source := "Berndl-Durr-Goldstein-Zanghi 1996", status := Status.stated }
  ]

end Hinges

end
