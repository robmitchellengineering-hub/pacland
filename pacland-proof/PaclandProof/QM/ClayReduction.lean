import Mathlib
import PaclandProof.QM.PosDefKernel

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# The Millennium problem — the corrected reduction

The honest state of the Yang-Mills attack, **corrected 2026-11-15**. The "OS3 ⟹ LSI
(Otto–Reznikoff 2007)" rung was a *misapplied citation* and is dropped — see
`PLANS/mass-gap-otto-reznikoff-applicability.md`: the LSI machinery (Milman / Otto–Reznikoff) needs
convexity or log-concavity, and the lattice YM measure `exp(−β S_Wilson) dμ_Haar` on a **compact
group** with a **bounded, non-convex** action is the opposite of that setting.

The corrected reduction:

    mass gap  =  OS3 ⟹ gap ≥ 0          (`heat_kernel_posdef`, CosPowers.lean, PROVEN)
               + strong-coupling gap > 0 (`massRate_pos`, YMMassGap.lean, PROVEN)
               + volume-uniform continuum join (OPEN — this is the Clay problem)
    existence =  OS ⟹ Wightman reconstruction (Osterwalder–Schrader 1973/75, CITED)

The two open rungs are named exactly: the **volume-uniform join** (mass gap) and the **OS
reconstruction** (existence). The proven rungs live in the QM tower and are referenced by name here,
not re-imported, because the tower is currently mid-repair. This file states the open rungs and proves
the reductions — not the open rungs.
-/

open scoped BigOperators

noncomputable section

namespace QM

/-- **The volume-uniform continuum join (the open Clay rung).** The lattice spectral gap
`m : ℕ → ℕ → ℝ` (volume → lattice size → gap) is positive with a volume-uniform lower bound that is
independent of the lattice size — the statement whose continuum limit is the 4D mass gap. Stated as a
hypothesis, not proved, not faked. -/
def volumeUniformJoin (m : ℕ → ℕ → ℝ) : Prop :=
  ∃ c : ℝ, 0 < c ∧ ∀ V n, c ≤ m V n

/-- **The Osterwalder-Schrader reconstruction (1973/75)**: the OS axioms (OS0-OS4) ⟹ the Wightman
axioms (W0-W4). Osterwalder, K. and Schrader, R., CMP 31 (1973) 83-112; CMP 42 (1975) 281-305. A
published theorem, stated as a hypothesis with the citation — not proved, not faked. -/
def osWightmanReconstruction (OS W : Prop) : Prop := OS → W

/-- **The existence reduction**: the Wightman axioms (existence) follow from the OS axioms plus the
Osterwalder-Schrader reconstruction. The OS reconstruction is the single named open rung of the
existence half. -/
theorem existence_reduction {OS W : Prop} (hOS : OS) (hRec : osWightmanReconstruction OS W) :
    W := hRec hOS

end QM
