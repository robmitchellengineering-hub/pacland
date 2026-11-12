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

def wilsonLoopFund (g A : ℝ) (N : ℕ) : ℝ :=
  (N : ℝ) * Real.exp (-(g^2 * A / 2) * casimirFund N)

/-- **The area law / string tension**: the coefficient of area `A` in `−log(⟨W_F⟩/dim F)` is
`g²C₂(F)/2` — the string tension is the fundamental Casimir (halved), the exact 2D result. -/
theorem wilsonLoop_area_law (g A : ℝ) (N : ℕ) (hN : 1 ≤ N) :
    -Real.log (wilsonLoopFund g A N / (N : ℝ)) = (g^2 * A / 2) * casimirFund N := by
  dsimp [wilsonLoopFund]
  have hN0 : (N : ℝ) ≠ 0 := by exact_mod_cast (ne_of_gt (lt_of_lt_of_le (by norm_num : (0:ℕ) < 1) hN))
  field_simp [hN0]
  rw [Real.log_exp]
  ring

/-- The string tension from the Wilson-loop area law equals the general `stringTension` formula:
`g²C₂(F)/2 = g²(N²−1)/(4N)`. -/
theorem stringTension_eq_casimir (g : ℝ) (N : ℕ) :
    g^2 * casimirFund N / 2 = stringTension g N := by
  dsimp [casimirFund, stringTension]
  ring
def su2_casimir_n (n : ℕ) : ℚ := (n : ℚ) * ((n : ℚ) + 2) / 4

/-- The spin-(n/2) dimension of SU(2): `n+1`. -/
def su2_dim_n (n : ℕ) : ℕ := n + 1

/-- **The mass gap is the smallest positive Casimir**: for n ≥ 1 the Casimir `n(n+2)/4 ≥ 3/4`,
attained at the fundamental (n=1). So the exact 2D SU(2) mass gap is the fundamental Casimir 3/4
(in units of g²A/2). -/
theorem su2_casimir_n_minimal {n : ℕ} (hn : 1 ≤ n) : (3 : ℚ) / 4 ≤ su2_casimir_n n := by
  dsimp [su2_casimir_n]
  have hn1 : (1 : ℚ) ≤ (n : ℚ) := by exact_mod_cast hn
  have hn0 : (0 : ℚ) ≤ (n : ℚ) := le_trans (by norm_num : (0 : ℚ) ≤ 1) hn1
  have hnp : (3 : ℚ) ≤ (n : ℚ) + 2 := by linarith [hn1]
  have hprod : (3 : ℚ) ≤ (n : ℚ) * ((n : ℚ) + 2) := by
    simpa using (mul_le_mul hn1 hnp (by norm_num : (0 : ℚ) ≤ 3) hn0 : (1 : ℚ) * 3 ≤ (n : ℚ) * ((n : ℚ) + 2))
  linarith

/-- The fundamental (n=1) Casimir is exactly 3/4 — the value the mass gap attains. -/
theorem su2_casimir_n_one : su2_casimir_n 1 = (3 : ℚ) / 4 := by
  norm_num [su2_casimir_n]
def su2_boltzmann (g A : ℝ) (n : ℕ) : ℝ :=
  Real.exp (-(g^2 * A / 2) * ((n : ℝ) * ((n : ℝ) + 2) / 4))

/-- The vacuum (n = 0) has weight 1 — it is the ground state. -/
theorem su2_boltzmann_zero (g A : ℝ) : su2_boltzmann g A 0 = 1 := by
  simp [su2_boltzmann]

/-- **The fundamental (n = 1) dominates the excited sectors**: for n ≥ 1, the Boltzmann weight is at
most `exp(−3g²A/8)`. So the mass gap is exactly the fundamental's exponential — the smallest positive
Casimir 3/4, halved. This is the Peter–Weyl / heat-kernel statement of the exact 2D mass gap. -/
theorem su2_boltzmann_fundamental_max {g A : ℝ} (hA : 0 ≤ A) {n : ℕ} (hn : 1 ≤ n) :
    su2_boltzmann g A n ≤ su2_boltzmann g A 1 := by
  dsimp [su2_boltzmann]
  have hgA : 0 ≤ g^2 * A / 2 := by positivity
  have hn1 : (1 : ℝ) ≤ (n : ℝ) := by exact_mod_cast hn
  have hn0 : (0 : ℝ) ≤ (n : ℝ) := le_trans (by norm_num : (0 : ℝ) ≤ 1) hn1
  have hnp : (3 : ℝ) ≤ (n : ℝ) + 2 := by linarith [hn1]
  have hcas : (3 : ℝ) / 4 ≤ (n : ℝ) * ((n : ℝ) + 2) / 4 := by
    have hprod : (3 : ℝ) ≤ (n : ℝ) * ((n : ℝ) + 2) := by
      simpa using (mul_le_mul hn1 hnp (by norm_num : (0 : ℝ) ≤ 3) hn0 : (1 : ℝ) * 3 ≤ (n : ℝ) * ((n : ℝ) + 2))
    linarith
  have harg : -(g^2 * A / 2) * ((n : ℝ) * ((n : ℝ) + 2) / 4) ≤ -(g^2 * A / 2) * (1 * (1 + 2) / 4) := by
    nlinarith [mul_le_mul_of_nonneg_left hcas hgA]
  norm_num
  nlinarith [harg]
/-- The truncated genus-0 SU(2) partition function (the Peter–Weyl sum over the spin-k/2 sectors):
`Z = Σ_{k=0}^{n} (k+1)² · exp(−t·k(k+2)/4)`, with `t = g²A/2`. The dimension is (k+1)² and the
heat-kernel weight is exp(−t·k(k+2)/4) (the Casimir k(k+2)/4). -/
def su2_partition (t : ℝ) (n : ℕ) : ℝ :=
  ∑ k ∈ Finset.range (n+1), ((k : ℝ) + 1)^2 * Real.exp (-t * (k : ℝ) * ((k : ℝ) + 2) / 4)

theorem su2_partition_ge_one (t : ℝ) (n : ℕ) :
    1 ≤ su2_partition t n := by
  dsimp [su2_partition]
  rw [Finset.sum_range_succ']
  norm_num [Real.exp_zero]
  have hrest : 0 ≤ ∑ k ∈ Finset.range n, (((k : ℝ) + 1) + 1)^2 * Real.exp (-(t * ((k : ℝ) + 1) * (((k : ℝ) + 1) + 2)) / 4) := by
    exact Finset.sum_nonneg (by intro k hk; exact mul_nonneg (sq_nonneg (((k : ℝ) + 1) + 1)) (le_of_lt (Real.exp_pos (-(t * ((k : ℝ) + 1) * (((k : ℝ) + 1) + 2)) / 4))))
  nlinarith
/-- **The fundamental sector's contribution**: the k=1 (fundamental) term of the partition function
is exactly `4·exp(−3t/4)` — the fundamental dimension squared times its heat-kernel weight. -/
theorem su2_partition_fundamental_term (t : ℝ) :
    ((1 : ℝ) + 1)^2 * Real.exp (-t * (1 : ℝ) * ((1 : ℝ) + 2) / 4) = 4 * Real.exp (-3 * t / 4) := by
  norm_num
  ring_nf

/-- **The mass gap extracted from the partition function**: the negative log of the fundamental's
Boltzmann weight is the mass gap `3g²A/8` — the vacuum-to-fundamental energy difference. -/
theorem su2_mass_gap_from_boltzmann (g A : ℝ) :
    -Real.log (su2_boltzmann g A 1) = 3 * g^2 * A / 8 := by
  dsimp [su2_boltzmann]
  rw [Real.log_exp]
  ring
/-- **The subleading correction**: for n ≥ 1, the partition function is at least the vacuum plus
the fundamental — `1 + 4·exp(−3t/4) ≤ Z`. The vacuum dominates and the fundamental is the first
excited (subleading) sector. -/
theorem su2_partition_ge_fundamental {t : ℝ} (n : ℕ) (hn : 1 ≤ n) :
    1 + 4 * Real.exp (-3 * t / 4) ≤ su2_partition t n := by
  dsimp [su2_partition]
  have hsubset : Finset.range 2 ⊆ Finset.range (n+1) := by
    intro k hk
    rw [Finset.mem_range] at hk ⊢
    omega
  have hsum : (∑ k ∈ Finset.range 2, ((k : ℝ) + 1)^2 * Real.exp (-t * (k : ℝ) * ((k : ℝ) + 2) / 4))
      ≤ ∑ k ∈ Finset.range (n+1), ((k : ℝ) + 1)^2 * Real.exp (-t * (k : ℝ) * ((k : ℝ) + 2) / 4) := by
    exact Finset.sum_le_sum_of_subset_of_nonneg hsubset (by
      intro k hk hk'
      exact mul_nonneg (sq_nonneg ((k : ℝ) + 1)) (le_of_lt (Real.exp_pos (-t * (k : ℝ) * ((k : ℝ) + 2) / 4))))
  have h2 : (∑ k ∈ Finset.range 2, ((k : ℝ) + 1)^2 * Real.exp (-t * (k : ℝ) * ((k : ℝ) + 2) / 4)) = 1 + 4 * Real.exp (-3 * t / 4) := by
    norm_num [Real.exp_zero, Finset.sum_range_succ, Finset.sum_range_succ]
    ring_nf
  rwa [h2] at hsum
end QM
