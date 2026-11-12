import Mathlib

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# The exact 2D SU(N) Yang–Mills mass gap (Migdal–Witten–Gross–Taylor)

2D Yang–Mills is exactly solvable: the heat-kernel / Migdal result gives the exact string tension
and mass gap in terms of the fundamental quadratic Casimir. This file records the **exact formulas**
(the algebraic core). The full heat-kernel *derivation* (via the Peter–Weyl decomposition of the
partition function) is the next, larger step.

Key facts (M1 of `docs/ym-mass-gap-plan.md`):
- fundamental Casimir `C₂ = (N²−1)/(2N)`;
- string tension `σ = g²(N²−1)/(4N)`;
- mass gap on a circle of circumference `L`: `m = g²L(N²−1)/(4N)`;
- the gap is strictly positive for N ≥ 2 — the exact non-Abelian mass gap, absent in the Abelian
  U(1) case.
-/

open scoped BigOperators

noncomputable section

namespace QM

/-- The fundamental-representation quadratic Casimir of SU(N): `(N² − 1)/(2N)`. -/
def casimirFund (N : ℕ) : ℝ := ((N : ℝ)^2 - 1) / (2 * (N : ℝ))

/-- The string tension of 2D SU(N) Yang–Mills (the exact Migdal/Witten result):
`σ = g²·(N²−1)/(4N)`. -/
def stringTension (g : ℝ) (N : ℕ) : ℝ := g^2 * ((N : ℝ)^2 - 1) / (4 * (N : ℝ))

/-- The mass gap of 2D SU(N) Yang–Mills on a spatial circle of circumference `L`:
`m = g²L·(N²−1)/(4N)` — the exact heat-kernel spectrum. -/
def massGap2D (g L : ℝ) (N : ℕ) : ℝ := g^2 * L * ((N : ℝ)^2 - 1) / (4 * (N : ℝ))

/-- **The exact 2D SU(2) string tension** is `3g²/8` (fundamental Casimir 3/4, halved). -/
theorem stringTension_su2 (g : ℝ) : stringTension g 2 = 3 * g^2 / 8 := by
  norm_num [stringTension]
  ring

/-- **The 2D mass gap is positive** for nonzero coupling and N ≥ 2 — the exact non-Abelian
mass gap is strictly positive, unlike the Abelian U(1) case (which has no such gap). -/
theorem massGap2D_pos {g L : ℝ} (hg : 0 < g) (hL : 0 < L) {N : ℕ} (hN : 2 ≤ N) :
    0 < massGap2D g L N := by
  dsimp [massGap2D]
  have hg2 : 0 < g^2 := sq_pos_of_ne_zero (ne_of_gt hg)
  have hNpos : 0 < (N : ℝ) := by exact_mod_cast (lt_of_lt_of_le (by norm_num : (0:ℕ) < 2) hN)
  have hnum : 0 < (N : ℝ)^2 - 1 := by
    have hN1 : (1 : ℝ) < (N : ℝ) := by exact_mod_cast hN
    nlinarith [sq_pos_of_ne_zero (ne_of_gt (lt_trans zero_lt_one hN1))]
  positivity

def su2_dim (j : ℚ) : ℚ := 2 * j + 1

/-- The quadratic Casimir of the spin-j representation of SU(2): `j(j+1)`. -/
def su2_casimir (j : ℚ) : ℚ := j * (j + 1)

/-- The 2D SU(2) Yang–Mills Hamiltonian eigenvalues on the spin-j sector:
`E_j = (g²L/2)·j(j+1)` — the heat-kernel spectrum (the Laplacian acts as the Casimir). -/
def su2_energy (g L j : ℝ) : ℝ := (g^2 * L / 2) * (j * (j + 1))

/-- **The exact 2D SU(2) mass gap** = E_{1/2} − E_0 = `3g²L/8` — the fundamental Casimir 3/4,
halved. This is the SU(2) case of `massGap2D g L 2`. -/
theorem su2_mass_gap (g L : ℝ) :
    su2_energy g L (1 / 2) - su2_energy g L 0 = 3 * g^2 * L / 8 := by
  dsimp [su2_energy]
  ring

/-- The spin-j energy is positive for positive g, L and j > 0 (the Casimir j(j+1) > 0). -/
theorem su2_energy_pos {g L j : ℝ} (hg : 0 < g) (hL : 0 < L) (hj : 0 < j) :
    0 < su2_energy g L j := by
  dsimp [su2_energy]
  have hg2 : 0 < g^2 := sq_pos_of_ne_zero (ne_of_gt hg)
  have hjj : 0 < j * (j + 1) := by nlinarith [hj]
  positivity

/-- The SU(2) spin-spectrum mass gap equals the general `massGap2D` formula at N = 2:
both are `3g²L/8`. -/
theorem su2_mass_gap_eq_general (g L : ℝ) :
    3 * g^2 * L / 8 = massGap2D g L 2 := by
  norm_num [massGap2D]
  ring

end QM
