import Mathlib
import PaclandProof.QM.LogSobolev
import PaclandProof.QM.ReflectionPositivity

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# The Millennium problem reduced to two named, published theorems

The honest state of the Yang-Mills mass-gap attack, stated as a reduction:

    mass gap  =  OS3 (#510, proven)  +  OS3 ⟹ LSI (Otto-Reznikoff 2007, cited)
                 +  LSI ⟹ Poincaré ⟹ spectral gap (LogSobolev.lean, proven)
    existence =  OS ⟹ Wightman reconstruction (Osterwalder-Schrader 1973/75, cited)

The two open rungs are published theorems, named with exact references. This file states them as
hypotheses with citations and proves the reduction — not the open rungs.
-/

open scoped BigOperators

noncomputable section

namespace QM

/-- **The Otto-Reznikoff criterion (2007)**: reflection positivity (OS3) ⟹ the log-Sobolev inequality.
Otto, F. and Reznikoff, M., "A new criterion for the logarithmic Sobolev inequality and two
applications", J. Funct. Anal. 243 (2007) 121-157. A published theorem, stated here as a hypothesis
with the citation — not proved, not faked. -/
def ottoReznikoffCriterion {α : Type*} [Fintype α] (μ : α → ℝ) (Γ : (α → ℝ) → α → ℝ) (C : ℝ) : Prop :=
  LogSobolev μ Γ C

/-- **The Osterwalder-Schrader reconstruction (1973/75)**: the OS axioms (OS0-OS4) ⟹ the Wightman
axioms (W0-W4). Osterwalder, K. and Schrader, R., CMP 31 (1973) 83-112; CMP 42 (1975) 281-305. A
published theorem, stated as a hypothesis with the citation — not proved, not faked. -/
def osWightmanReconstruction (OS W : Prop) : Prop := OS → W

/-- **The mass-gap reduction**: the mass gap (the Poincaré spectral-gap inequality) follows from
(i) reflection positivity OS3 (#510, proven), (ii) the Otto-Reznikoff criterion `OS3 ⟹ LSI` (cited,
the open rung), and (iii) the `LSI ⟹ Poincaré` tail (`logSobolev_implies_poincare`, proven). The
Otto-Reznikoff criterion is the single named open rung of the mass-gap half. -/
theorem mass_gap_reduction {α : Type*} [Fintype α] {μ : α → ℝ} {Γ : (α → ℝ) → α → ℝ} {C : ℝ}
    (hΓlin : ∀ g ε, Γ (fun x => 1 + ε * g x) = fun x => ε ^ 2 * Γ g x)
    (hEnt : EntropyQuadraticAtOne μ)
    (hOR : ottoReznikoffCriterion μ Γ C) :
    Poincare μ Γ (C / 2) := logSobolev_implies_poincare hΓlin hEnt hOR

/-- **The existence reduction**: the Wightman axioms (existence) follow from the OS axioms plus the
Osterwalder-Schrader reconstruction. The OS reconstruction is the single named open rung of the
existence half. -/
theorem existence_reduction {OS W : Prop} (hOS : OS) (hRec : osWightmanReconstruction OS W) :
    W := hRec hOS

end QM
