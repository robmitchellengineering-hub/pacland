import Mathlib

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# QF-5 (toy) — the no-go's algebraic core, kernel-checked

The BDGZ no-go (Berndl–Dürr–Goldstein–Zanghì 1996) says no foliation-free,
Lorentz-invariant *deterministic* guidance law can reproduce the `|ψ|²`
equilibrium measure. Its algebraic core — in a finite `1+1D` toy where a "frame
boost" is the swap of the two configuration points — is exactly this: a
normalized measure invariant under the frame swap is forced **uniform**, so a
non-uniform `|ψ|²` is not frame-equivariant and can have no frame-independent
deterministic guidance. This is the finite slice of the no-go; the full 4D
relativistic statement remains `Hinges.F4`.
-/

noncomputable section

namespace NoGo

/-- The toy "frame boost": swap which of the two configuration points is which. -/
def swap : Fin 2 → Fin 2
  | 0 => 1
  | 1 => 0

/-- A normalized distribution invariant under the frame swap is forced uniform.
The algebraic core of the no-go: a frame-independent equivariant measure on a
transitive configuration space must be uniform. -/
theorem swap_equivariant_forces_uniform (ρ : Fin 2 → ℝ)
    (hnorm : ρ 0 + ρ 1 = 1) (hequiv : ρ ∘ swap = ρ) :
    ρ 0 = 1 / 2 ∧ ρ 1 = 1 / 2 := by
  have h01 : ρ 1 = ρ 0 := by
    have h := congr_fun hequiv 0
    norm_num [swap] at h
    exact h
  have hsum : ρ 0 + ρ 0 = 1 := by
    simpa [h01] using hnorm
  constructor
  · linarith
  · linarith [h01, hsum]

/-- A non-uniform Born distribution is not frame-equivariant: no frame-independent
deterministic law reproduces it — the no-go's conclusion in the toy. -/
theorem nonuniform_breaks_equivariance (ρ : Fin 2 → ℝ)
    (hnonuniform : ρ 0 ≠ 1 / 2) (hnorm : ρ 0 + ρ 1 = 1) :
    ρ ∘ swap ≠ ρ := by
  intro hequiv
  have h := (swap_equivariant_forces_uniform ρ hnorm hequiv).1
  exact hnonuniform h

end NoGo

end
