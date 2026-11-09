import Mathlib
import PaclandProof.QM.HyperbolicPlane
import PaclandProof.QM.HyperbolicMetric
import PaclandProof.QM.Hyperbolic

/-!
# Quasi-surjectivity of the tree-to-H² map (the density half of the quasi-isometry)

Proves the *quasi-surjectivity* rung: every hyperboloid point is within a bounded hyperbolic distance
of the tree's image.

The hyperboloid model (`Hyperboloid`, `minkowski`, `hyperbolicDist`, `pathAngle`, `treeToH2`) is
imported from `PaclandProof.QM.HyperbolicPlane` (namespace `QM`, `open QM` below) — this file no
longer carries a private copy. The argument is dyadic density. A point
`(cosh r, sinh r · cos θ, sinh r · sin θ)` is approximated by a vertex at depth `d` with
`ln 2 · d ≈ r` (radial error ≤ `ln 2`) and angle `2π · k/2^d ≈ θ` (angular error ≤ `2π/2^d`, since
dyadic rationals are dense in `[0, 1)`). The hyperbolic distance then satisfies
`d ≤ arcosh(cosh(ln 2) + 4π²)`, a constant. The proof uses the parametrisation of the hyperboloid via
`Complex.arg`, the `ℕ`-floor density lemmas, and the identity
`cosh r cosh r' − sinh r sinh r' cos Δ = cosh(r − r') + sinh r sinh r' (1 − cos Δ)`.
-/

open QM

namespace QMTreeDensity

/-- A hyperboloid point in `(r, θ)` coordinates — `(cosh r, sinh r · cos θ, sinh r · sin θ)`. -/
noncomputable def h2point (r θ : ℝ) : Hyperboloid :=
  ⟨(Real.cosh r, Real.sinh r * Real.cos θ, Real.sinh r * Real.sin θ), by
    constructor
    · calc
        -(Real.cosh r) ^ 2 + (Real.sinh r * Real.cos θ) ^ 2 + (Real.sinh r * Real.sin θ) ^ 2
          = -(Real.cosh r) ^ 2 + (Real.sinh r) ^ 2 * ((Real.cos θ) ^ 2 + (Real.sin θ) ^ 2) := by ring
        _ = -(Real.cosh r) ^ 2 + (Real.sinh r) ^ 2 := by
              rw [Real.cos_sq_add_sin_sq]
              ring
        _ = -1 := by
              have h := Real.cosh_sq_sub_sinh_sq r
              nlinarith
    · exact Real.cosh_pos r⟩

/-- `treeToH2 s` is exactly `h2point (ln 2 · |s|) (2π · pathAngle s)`. -/
lemma treeToH2_eq_h2point (s : List Bool) :
    treeToH2 s = h2point ((Real.log 2) * (s.length : ℝ)) (2 * Real.pi * pathAngle s) := by
  apply Subtype.ext
  rfl

/-- The hyperbolic distance between two `(r, θ)`-coordinates:
`arcosh(cosh r cosh r' − sinh r sinh r' cos(θ − θ'))`. -/
lemma hyperbolicDist_h2point (r r' θ θ' : ℝ) :
    hyperbolicDist (h2point r θ) (h2point r' θ') =
      Real.arcosh (Real.cosh r * Real.cosh r' - Real.sinh r * Real.sinh r' * Real.cos (θ - θ')) := by
  dsimp [hyperbolicDist, minkowski, h2point]
  congr 1
  rw [Real.cos_sub]
  ring

/-- The hyperbolic distance is symmetric (the Minkowski product is). -/
lemma hyperbolicDist_comm (p q : Hyperboloid) : hyperbolicDist p q = hyperbolicDist q p := by
  dsimp [hyperbolicDist]
  congr 1
  dsimp [minkowski]
  ring

/-- **Parametrisation.** Every hyperboloid point is `(cosh r, sinh r · cos θ, sinh r · sin θ)` for a
radius `r ≥ 0` and an angle `θ ∈ [0, 2π)`. The angle is `Complex.arg` of `x + y·I` (reduced into
`[0, 2π)`), the radius is `arcosh t`. -/
lemma hyperboloid_param (p : Hyperboloid) :
    ∃ r θ, 0 ≤ r ∧ θ ∈ Set.Ico 0 (2 * Real.pi) ∧
      p.1.1 = Real.cosh r ∧
      p.1.2.1 = Real.sinh r * Real.cos θ ∧
      p.1.2.2 = Real.sinh r * Real.sin θ := by
  let t := p.1.1
  let x := p.1.2.1
  let y := p.1.2.2
  have ht_pos : 0 < t := p.2.2
  have hquad : -t ^ 2 + x ^ 2 + y ^ 2 = -1 := p.2.1
  have ht_ge_one : 1 ≤ t := by
    have hsq : 1 ≤ t ^ 2 := by
      nlinarith [hquad]
    have h : 1 ≤ |t| := (one_le_sq_iff_one_le_abs (a := t)).mp hsq
    rwa [abs_of_pos ht_pos] at h
  let r := Real.arcosh t
  let z : ℂ := x + y * Complex.I
  let θ := if 0 ≤ Complex.arg z then Complex.arg z else Complex.arg z + 2 * Real.pi
  have hsq : t ^ 2 - 1 = x ^ 2 + y ^ 2 := by nlinarith [hquad]
  have hsinh : Real.sinh r = Real.sqrt (t ^ 2 - 1) := by
    dsimp [r]
    exact Real.sinh_arcosh ht_ge_one
  have hnorm_sq : Complex.normSq z = x ^ 2 + y ^ 2 := by
    dsimp [z]
    rw [Complex.normSq_apply]
    simp
    ring
  have hnorm : ‖z‖ = Real.sinh r := by
    have h1 : Real.sqrt (Complex.normSq z) = ‖z‖ := by
      rw [Complex.normSq_eq_norm_sq]
      exact Real.sqrt_sq (norm_nonneg z)
    calc
      ‖z‖ = Real.sqrt (Complex.normSq z) := h1.symm
      _ = Real.sqrt (x ^ 2 + y ^ 2) := by rw [hnorm_sq]
      _ = Real.sqrt (t ^ 2 - 1) := by rw [← hsq]
      _ = Real.sinh r := hsinh.symm
  have hcosθ : Real.cos θ = Real.cos (Complex.arg z) := by
    dsimp [θ]
    by_cases h : 0 ≤ Complex.arg z
    · simp [h]
    · simp [h, Real.cos_add_two_pi]
  have hsinθ : Real.sin θ = Real.sin (Complex.arg z) := by
    dsimp [θ]
    by_cases h : 0 ≤ Complex.arg z
    · simp [h]
    · simp [h, Real.sin_add_two_pi]
  refine ⟨r, θ, ?_, ?_, ?_, ?_, ?_⟩
  · exact Real.arcosh_nonneg ht_ge_one
  · constructor
    · dsimp [θ]
      by_cases h : 0 ≤ Complex.arg z
      · rw [ite_eq_left h]
        exact h
      · rw [ite_eq_right h]
        have harggt : -Real.pi < Complex.arg z := Complex.neg_pi_lt_arg z
        have hpos : 0 < Complex.arg z + 2 * Real.pi := by nlinarith [harggt, Real.pi_pos]
        exact le_of_lt hpos
    · dsimp [θ]
      by_cases h : 0 ≤ Complex.arg z
      · rw [ite_eq_left h]
        have hargle : Complex.arg z ≤ Real.pi := Complex.arg_le_pi z
        nlinarith [hargle, Real.pi_pos]
      · rw [ite_eq_right h]
        have hneg : Complex.arg z < 0 := lt_of_not_ge h
        nlinarith [hneg]
  · dsimp [r]
    exact (Real.cosh_arcosh ht_ge_one).symm
  · have hx_eq : x = Real.sinh r * Real.cos θ := by
      calc
        x = ‖z‖ * Real.cos (Complex.arg z) := by
          have h := Complex.norm_mul_cos_arg z
          simpa [z] using h.symm
        _ = ‖z‖ * Real.cos θ := by rw [hcosθ]
        _ = Real.sinh r * Real.cos θ := by rw [hnorm]
    simpa [x] using hx_eq
  · have hy_eq : y = Real.sinh r * Real.sin θ := by
      calc
        y = ‖z‖ * Real.sin (Complex.arg z) := by
          have h := Complex.norm_mul_sin_arg z
          simpa [z] using h.symm
        _ = ‖z‖ * Real.sin θ := by rw [hsinθ]
        _ = Real.sinh r * Real.sin θ := by rw [hnorm]
    simpa [y] using hy_eq

/-- `exp (ln 2 · d) = 2^d`. -/
lemma exp_ln2_mul_eq_two_pow (d : ℕ) : Real.exp ((Real.log 2) * (d : ℝ)) = (2 : ℝ) ^ d := by
  rw [Real.exp_mul, Real.exp_log (by norm_num : 0 < (2 : ℝ)), Real.rpow_natCast]

/-- `1 - cos x ≤ x²/2` for all real `x`. -/
lemma one_sub_cos_le_sq_div_two_general (x : ℝ) : 1 - Real.cos x ≤ x ^ 2 / 2 := by
  have hcos : 1 - Real.cos x = 2 * Real.sin (x / 2) ^ 2 := by
    have h := Real.cos_two_mul (x / 2)
    rw [show 2 * (x / 2) = x by ring] at h
    have hsq := Real.cos_sq_add_sin_sq (x / 2)
    nlinarith [h, hsq]
  have hsin : Real.sin (x / 2) ^ 2 ≤ (x / 2) ^ 2 := Real.sin_sq_le_sq
  nlinarith [hcos, hsin]

/-- **Radial density.** Every radius `r ≥ 0` is within `ln 2` of some `ln 2 · d`. -/
lemma radial_approx (r : ℝ) (hr : 0 ≤ r) :
    ∃ d : ℕ, |r - (Real.log 2) * (d : ℝ)| ≤ Real.log 2 := by
  let d := Nat.floor (r / (Real.log 2))
  refine ⟨d, ?_⟩
  have hlog : 0 < Real.log 2 := Real.log_pos (by norm_num : (1 : ℝ) < 2)
  have hle : 0 ≤ r / (Real.log 2) - (d : ℝ) := by
    have := Nat.floor_le (a := r / (Real.log 2)) (by positivity : 0 ≤ r / (Real.log 2))
    simpa [d] using sub_nonneg.mpr this
  have hlt : r / (Real.log 2) - (d : ℝ) < 1 := by
    have := Nat.lt_floor_add_one (r / (Real.log 2))
    linarith
  have hdiff : r - (Real.log 2) * (d : ℝ) = (Real.log 2) * (r / (Real.log 2) - (d : ℝ)) := by
    field_simp [ne_of_gt hlog]
  have h1 : |r - (Real.log 2) * (d : ℝ)| = (Real.log 2) * |r / (Real.log 2) - (d : ℝ)| := by
    rw [hdiff, abs_mul, abs_of_pos hlog]
  have h2 : (Real.log 2) * |r / (Real.log 2) - (d : ℝ)| ≤ (Real.log 2) * 1 := by
    have hb : |r / (Real.log 2) - (d : ℝ)| ≤ 1 := by
      rw [abs_of_nonneg hle]
      exact le_of_lt hlt
    nlinarith [hlog]
  rw [h1]
  simpa using h2

/-- **Dyadic density in angle.** For `x ∈ [0, 1)` and any depth `d`, some `k < 2^d` has
`|x - k/2^d| ≤ 1/2^d`. -/
lemma dyadic_approx (x : ℝ) (hx0 : 0 ≤ x) (hx1 : x < 1) (d : ℕ) :
    ∃ k : ℕ, k < 2 ^ d ∧ |x - (k : ℝ) / (2 ^ d : ℝ)| ≤ 1 / (2 ^ d : ℝ) := by
  let k := Nat.floor (x * (2 ^ d : ℝ))
  refine ⟨k, ?_, ?_⟩
  · have hle : (k : ℝ) ≤ x * (2 ^ d : ℝ) :=
      Nat.floor_le (by positivity : 0 ≤ x * (2 ^ d : ℝ))
    have hlt : x * (2 ^ d : ℝ) < (2 ^ d : ℝ) := by
      have hpow : 0 < (2 ^ d : ℝ) := by positivity
      nlinarith [hx1]
    have hk_lt : (k : ℝ) < (2 ^ d : ℝ) := lt_of_le_of_lt hle hlt
    exact_mod_cast hk_lt
  · have hpow : 0 < (2 ^ d : ℝ) := by positivity
    have h2d : (2 ^ d : ℝ) ≠ 0 := ne_of_gt hpow
    have hle : 0 ≤ x * (2 ^ d : ℝ) - (k : ℝ) := by
      have := Nat.floor_le (by positivity : 0 ≤ x * (2 ^ d : ℝ))
      simpa [k] using sub_nonneg.mpr this
    have hlt1 : x * (2 ^ d : ℝ) - (k : ℝ) < 1 := by
      have := Nat.lt_floor_add_one (x * (2 ^ d : ℝ))
      linarith
    have hnum : x - (k : ℝ) / (2 ^ d : ℝ) = (x * (2 ^ d : ℝ) - (k : ℝ)) / (2 ^ d : ℝ) := by
      field_simp [h2d]
    calc
      |x - (k : ℝ) / (2 ^ d : ℝ)| = |(x * (2 ^ d : ℝ) - (k : ℝ)) / (2 ^ d : ℝ)| := by rw [hnum]
      _ = |x * (2 ^ d : ℝ) - (k : ℝ)| / |(2 ^ d : ℝ)| := by rw [abs_div]
      _ = |x * (2 ^ d : ℝ) - (k : ℝ)| / (2 ^ d : ℝ) := by rw [abs_of_pos hpow]
      _ ≤ 1 / (2 ^ d : ℝ) := by
          rw [abs_of_nonneg hle]
          exact div_le_div_of_nonneg_right (le_of_lt hlt1) (le_of_lt hpow)

/-- The length-`d` binary expansion of `k` (most-significant bit first), so that
`pathAngle (dyadicBits d k) = k / 2^d` when `k < 2^d`. -/
def dyadicBits : ℕ → ℕ → List Bool
  | 0, _ => []
  | d + 1, k => decide (k / 2 ^ d = 1) :: dyadicBits d (k % 2 ^ d)

lemma dyadicBits_length (d k : ℕ) : (dyadicBits d k).length = d := by
  induction d generalizing k with
  | zero => rfl
  | succ d ih => simp [dyadicBits, ih]

lemma if_decide_eq_natCast_of_lt_two {n : ℕ} (hn : n < 2) :
    (if decide (n = 1) then (1 : ℝ) else 0) = (n : ℝ) := by
  interval_cases n <;> norm_num

lemma pathAngle_dyadicBits (d k : ℕ) (hk : k < 2 ^ d) :
    pathAngle (dyadicBits d k) = (k : ℝ) / (2 ^ d : ℝ) := by
  induction d generalizing k with
  | zero =>
    have hk0 : k = 0 := by omega
    simp [dyadicBits, pathAngle, hk0]
  | succ d ih =>
    have hkdiv : k / 2 ^ d < 2 := Nat.div_lt_of_lt_mul (by simpa [pow_succ] using hk)
    have hkmod : k % 2 ^ d < 2 ^ d := Nat.mod_lt _ (by positivity)
    simp only [dyadicBits, pathAngle]
    rw [ih (k % 2 ^ d) hkmod]
    rw [if_decide_eq_natCast_of_lt_two hkdiv]
    rw [show (2 ^ (d + 1) : ℝ) = (2 ^ d : ℝ) * 2 by rw [pow_succ]]
    have hmodadd' : ((k % 2 ^ d : ℕ) : ℝ) + (2 : ℝ) ^ d * ((k / 2 ^ d : ℕ) : ℝ) = (k : ℝ) := by
      rw [show (2 : ℝ) ^ d = ((2 ^ d : ℕ) : ℝ) by norm_num]
      rw [← Nat.cast_mul, ← Nat.cast_add, Nat.mod_add_div k (2 ^ d)]
    rw [← hmodadd']
    field_simp [show (2 ^ d : ℝ) ≠ 0 by positivity]
    ring_nf

/-- Every `k < 2^d` is realised as the angle of a length-`d` tree path. -/
lemma dyadicBits_exists (d k : ℕ) (hk : k < 2 ^ d) :
    ∃ s : List Bool, s.length = d ∧ pathAngle s = (k : ℝ) / (2 ^ d : ℝ) :=
  ⟨dyadicBits d k, dyadicBits_length d k, pathAngle_dyadicBits d k hk⟩

/-- **The distance bound from coordinate approximation.** If a point `(r, θ)` is radially within
`ln 2` of `(ln 2 · d, θ')` and angularly within `2π/2^d`, then its hyperbolic distance to
`(ln 2 · d, θ')` is at most the constant `arcosh(cosh(ln 2) + 4π²)`. -/
lemma hyperbolicDist_bound_of_approx (r θ θ' : ℝ) (d : ℕ)
    (hr : 0 ≤ r)
    (hrdiff : |r - (Real.log 2) * (d : ℝ)| ≤ Real.log 2)
    (hthdiff : |θ - θ'| ≤ 2 * Real.pi / (2 ^ d : ℝ)) :
    hyperbolicDist (h2point r θ) (h2point ((Real.log 2) * (d : ℝ)) θ') ≤
      Real.arcosh (Real.cosh (Real.log 2) + 4 * Real.pi ^ 2) := by
  rw [hyperbolicDist_h2point]
  have harg : Real.cosh r * Real.cosh ((Real.log 2) * (d : ℝ))
        - Real.sinh r * Real.sinh ((Real.log 2) * (d : ℝ)) * Real.cos (θ - θ')
      = Real.cosh (r - (Real.log 2) * (d : ℝ))
        + Real.sinh r * Real.sinh ((Real.log 2) * (d : ℝ)) * (1 - Real.cos (θ - θ')) := by
    calc
      Real.cosh r * Real.cosh ((Real.log 2) * (d : ℝ))
          - Real.sinh r * Real.sinh ((Real.log 2) * (d : ℝ)) * Real.cos (θ - θ')
        = (Real.cosh r * Real.cosh ((Real.log 2) * (d : ℝ))
              - Real.sinh r * Real.sinh ((Real.log 2) * (d : ℝ)))
            + Real.sinh r * Real.sinh ((Real.log 2) * (d : ℝ)) * (1 - Real.cos (θ - θ')) := by ring
      _ = Real.cosh (r - (Real.log 2) * (d : ℝ))
            + Real.sinh r * Real.sinh ((Real.log 2) * (d : ℝ)) * (1 - Real.cos (θ - θ')) := by
            rw [Real.cosh_sub]
  rw [harg]
  refine (Real.arcosh_le_arcosh ?_ ?_).2 ?_
  · have hcosh : 0 < Real.cosh (r - (Real.log 2) * (d : ℝ)) := Real.cosh_pos _
    have hs1 : 0 ≤ Real.sinh r := Real.sinh_nonneg_iff.mpr hr
    have hs2 : 0 ≤ Real.sinh ((Real.log 2) * (d : ℝ)) :=
      Real.sinh_nonneg_iff.mpr (by positivity)
    have hc : 0 ≤ 1 - Real.cos (θ - θ') := sub_nonneg.mpr (Real.cos_le_one _)
    have hprod : 0 ≤ Real.sinh r * Real.sinh ((Real.log 2) * (d : ℝ)) * (1 - Real.cos (θ - θ')) := by
      positivity
    nlinarith [hcosh, hprod]
  · positivity
  · have hcosh_le : Real.cosh (r - (Real.log 2) * (d : ℝ)) ≤ Real.cosh (Real.log 2) := by
      rw [Real.cosh_le_cosh]
      rw [abs_of_pos (Real.log_pos (by norm_num : (1 : ℝ) < 2))]
      exact hrdiff
    have hsinh1_le : Real.sinh r ≤ 2 * (2 : ℝ) ^ d := by
      have hrle : r ≤ (Real.log 2) * (d : ℝ) + Real.log 2 := by
        rw [abs_le] at hrdiff
        nlinarith [hrdiff.2]
      have h1 : Real.sinh r ≤ Real.exp r := sinh_le_exp hr
      have h2 : Real.exp r ≤ Real.exp ((Real.log 2) * (d : ℝ) + Real.log 2) :=
        (Real.exp_le_exp).2 hrle
      have h3 : Real.exp ((Real.log 2) * (d : ℝ) + Real.log 2) = 2 * (2 : ℝ) ^ d := by
        rw [Real.exp_add, exp_ln2_mul_eq_two_pow, Real.exp_log (by norm_num : 0 < (2 : ℝ))]
        ring
      calc
        Real.sinh r ≤ Real.exp r := h1
        _ ≤ Real.exp ((Real.log 2) * (d : ℝ) + Real.log 2) := h2
        _ = 2 * (2 : ℝ) ^ d := h3
    have hsinh2_le : Real.sinh ((Real.log 2) * (d : ℝ)) ≤ (2 : ℝ) ^ d :=
      sinh_ln2_mul_le_two_pow d
    have hcos_le : 1 - Real.cos (θ - θ') ≤ (2 * Real.pi / (2 ^ d : ℝ)) ^ 2 / 2 := by
      have h1 : 1 - Real.cos (θ - θ') ≤ (θ - θ') ^ 2 / 2 := one_sub_cos_le_sq_div_two_general (θ - θ')
      have h2 : (θ - θ') ^ 2 ≤ (2 * Real.pi / (2 ^ d : ℝ)) ^ 2 := by
        rw [sq_le_sq]
        rw [abs_of_nonneg (by positivity : 0 ≤ 2 * Real.pi / (2 ^ d : ℝ))]
        exact hthdiff
      nlinarith [h1, h2]
    have h1 : Real.sinh ((Real.log 2) * (d : ℝ)) * (1 - Real.cos (θ - θ'))
        ≤ (2 : ℝ) ^ d * ((2 * Real.pi / (2 ^ d : ℝ)) ^ 2 / 2) := by
      exact mul_le_mul hsinh2_le hcos_le
        (sub_nonneg.mpr (Real.cos_le_one _) : 0 ≤ 1 - Real.cos (θ - θ'))
        (by positivity : 0 ≤ (2 : ℝ) ^ d)
    have h1' : (2 : ℝ) ^ d * ((2 * Real.pi / (2 ^ d : ℝ)) ^ 2 / 2) =
        2 * Real.pi ^ 2 / (2 ^ d : ℝ) := by
      field_simp [show (2 ^ d : ℝ) ≠ 0 by positivity]
    have h1'' : Real.sinh ((Real.log 2) * (d : ℝ)) * (1 - Real.cos (θ - θ'))
        ≤ 2 * Real.pi ^ 2 / (2 ^ d : ℝ) := by
      rwa [h1'] at h1
    have h2 : Real.sinh r * (Real.sinh ((Real.log 2) * (d : ℝ)) * (1 - Real.cos (θ - θ')))
        ≤ (2 * (2 : ℝ) ^ d) * (2 * Real.pi ^ 2 / (2 ^ d : ℝ)) := by
      exact mul_le_mul hsinh1_le h1''
        (mul_nonneg (Real.sinh_nonneg_iff.mpr (by positivity))
          (sub_nonneg.mpr (Real.cos_le_one _)) :
          0 ≤ Real.sinh ((Real.log 2) * (d : ℝ)) * (1 - Real.cos (θ - θ')))
        (by positivity : 0 ≤ 2 * (2 : ℝ) ^ d)
    have h2' : (2 * (2 : ℝ) ^ d) * (2 * Real.pi ^ 2 / (2 ^ d : ℝ)) = 4 * Real.pi ^ 2 := by
      field_simp [show (2 ^ d : ℝ) ≠ 0 by positivity]
      ring
    have hprod_le : Real.sinh r * Real.sinh ((Real.log 2) * (d : ℝ)) * (1 - Real.cos (θ - θ'))
        ≤ 4 * Real.pi ^ 2 := by
      rw [show Real.sinh r * Real.sinh ((Real.log 2) * (d : ℝ)) * (1 - Real.cos (θ - θ'))
            = Real.sinh r * (Real.sinh ((Real.log 2) * (d : ℝ)) * (1 - Real.cos (θ - θ'))) by ring]
      rwa [h2'] at h2
    nlinarith [hcosh_le, hprod_le]

/-- **Quasi-surjectivity.** Every hyperboloid point is within the constant
`arcosh(cosh(ln 2) + 4π²)` of the tree's image. -/
theorem treeToH2_quasiSurjective :
    ∃ R : ℝ, ∀ p : Hyperboloid, ∃ s : List Bool, hyperbolicDist (treeToH2 s) p ≤ R := by
  refine ⟨Real.arcosh (Real.cosh (Real.log 2) + 4 * Real.pi ^ 2), ?_⟩
  intro p
  rcases hyperboloid_param p with ⟨r, θ, hr0, hθrange, hpt, hpx, hpy⟩
  rcases radial_approx r hr0 with ⟨d, hrdiff⟩
  have hx0 : 0 ≤ θ / (2 * Real.pi) := div_nonneg hθrange.1 (le_of_lt Real.two_pi_pos)
  have hx1 : θ / (2 * Real.pi) < 1 := (div_lt_iff₀ Real.two_pi_pos).2 (by simpa using hθrange.2)
  rcases dyadic_approx (θ / (2 * Real.pi)) hx0 hx1 d with ⟨k, hk_lt, hk_close⟩
  rcases dyadicBits_exists d k hk_lt with ⟨s, hslen, hsang⟩
  refine ⟨s, ?_⟩
  have hp_eq : p = h2point r θ := by
    apply Subtype.ext
    apply Prod.ext
    · simpa [h2point] using hpt
    · apply Prod.ext
      · simpa [h2point] using hpx
      · simpa [h2point] using hpy
  have hthdiff : |θ - 2 * Real.pi * pathAngle s| ≤ 2 * Real.pi / (2 ^ d : ℝ) := by
    have hinside : θ - 2 * Real.pi * ((k : ℝ) / (2 ^ d : ℝ)) =
        2 * Real.pi * (θ / (2 * Real.pi) - (k : ℝ) / (2 ^ d : ℝ)) := by
      field_simp [ne_of_gt Real.two_pi_pos]
    calc
      |θ - 2 * Real.pi * pathAngle s| = |θ - 2 * Real.pi * ((k : ℝ) / (2 ^ d : ℝ))| := by rw [hsang]
      _ = |2 * Real.pi * (θ / (2 * Real.pi) - (k : ℝ) / (2 ^ d : ℝ))| := by rw [hinside]
      _ = (2 * Real.pi) * |θ / (2 * Real.pi) - (k : ℝ) / (2 ^ d : ℝ)| := by
          rw [abs_mul, abs_of_pos Real.two_pi_pos]
      _ ≤ (2 * Real.pi) * (1 / (2 ^ d : ℝ)) := by
          exact mul_le_mul_of_nonneg_left hk_close (le_of_lt Real.two_pi_pos)
      _ = 2 * Real.pi / (2 ^ d : ℝ) := by ring
  have hdist_eq : hyperbolicDist (treeToH2 s) p =
      hyperbolicDist (h2point ((Real.log 2) * (s.length : ℝ)) (2 * Real.pi * pathAngle s)) (h2point r θ) := by
    rw [treeToH2_eq_h2point, hp_eq]
  rw [hdist_eq, hyperbolicDist_comm]
  exact hyperbolicDist_bound_of_approx r θ (2 * Real.pi * pathAngle s) s.length hr0
    (by simpa [← hslen] using hrdiff)
    (by simpa [← hslen] using hthdiff)

/-! ## Distortion (the *true* direction) and the honest boundary of the quasi-isometry

`treeToH2` is **coarsely Lipschitz** (below) and **coarsely surjective**
(`treeToH2_quasiSurjective` above), but it is **not** coarsely injective — the binary-expansion
angle collapses the two boundary branches `0.0111…₂` and `0.1000…₂` to the same ideal point. The
lower bound of a quasi-isometry therefore fails; see `treeToH2_not_coarsely_injective` below. -/

/-- The edge upper-bound constant of the tree→H² embedding: `arcosh(cosh(ln 2) + 2π²)` — the
largest hyperbolic length of a single parent–child edge (`hyperbolicDist_edge_le`). -/
noncomputable def edgeBound : ℝ := Real.arcosh (Real.cosh (Real.log 2) + 2 * Real.pi ^ 2)

/-- The hyperbolic distance from a point to itself is zero. -/
lemma hyperbolicDist_self (p : Hyperboloid) : hyperbolicDist p p = 0 := by
  dsimp [hyperbolicDist]
  rw [HyperbolicMetric.minkowski_self p]
  simpa using (Real.arcosh_zero : Real.arcosh 1 = 0)

/-- **Edge-chain upper bound.** Appending a suffix `r` to a tree path moves its image by at most
`edgeBound` per appended bit: the hyperbolic distance from `treeToH2 s` to `treeToH2 (s ++ r)` is at
most `edgeBound · r.length`. This is the chaining lemma behind the coarse-Lipschitz (upper) half of
the quasi-isometry. -/
lemma treeToH2_append_dist_le (s r : List Bool) :
    hyperbolicDist (treeToH2 (s ++ r)) (treeToH2 s) ≤ edgeBound * (r.length : ℝ) := by
  induction r generalizing s with
  | nil => simp [hyperbolicDist_self]
  | cons b r' ih =>
      have hstep : hyperbolicDist (treeToH2 (s ++ [b])) (treeToH2 s) ≤ edgeBound :=
        hyperbolicDist_edge_le s b
      have hrec : hyperbolicDist (treeToH2 ((s ++ [b]) ++ r')) (treeToH2 (s ++ [b])) ≤
          edgeBound * (r'.length : ℝ) := ih (s ++ [b])
      have htri := HyperbolicMetric.hyperbolicDist_triangle
        (treeToH2 ((s ++ [b]) ++ r')) (treeToH2 (s ++ [b])) (treeToH2 s)
      have hmain : hyperbolicDist (treeToH2 (s ++ (b :: r'))) (treeToH2 s) ≤
            hyperbolicDist (treeToH2 ((s ++ [b]) ++ r')) (treeToH2 (s ++ [b]))
              + hyperbolicDist (treeToH2 (s ++ [b])) (treeToH2 s) := by
        simpa [List.append_assoc] using htri
      rw [List.length_cons]
      push_cast
      rw [show edgeBound * ((r'.length : ℝ) + 1) = edgeBound * (r'.length : ℝ) + edgeBound by ring]
      nlinarith

/-- **Coarse Lipschitz (the true upper half of the quasi-isometry).** The hyperbolic distance of two
tree images is at most `edgeBound` times the tree distance: the tree path from `s` to `t` passes
through the lowest common ancestor (depth `commonPrefixLength s t`), and each of its
`treeDist s t` edges contributes at most `edgeBound`. -/
lemma hyperbolicDist_le_edge_mul_treeDistR (s t : List Bool) :
    hyperbolicDist (treeToH2 s) (treeToH2 t) ≤ edgeBound * treeDistR s t := by
  let l := commonPrefixLength s t
  let p := s.take l
  have hup : hyperbolicDist (treeToH2 s) (treeToH2 p) ≤ edgeBound * ((s.drop l).length : ℝ) := by
    have hsp : p ++ s.drop l = s := by
      simpa [p] using (List.take_append_drop l s)
    have hrec := treeToH2_append_dist_le p (s.drop l)
    simpa [hsp] using hrec
  have hdown : hyperbolicDist (treeToH2 p) (treeToH2 t) ≤ edgeBound * ((t.drop l).length : ℝ) := by
    have hst : s.take l = t.take l := take_eq_of_le_lcp (s := s) (t := t) (le_refl l)
    have ht : t.take l = p := by
      simpa [p] using hst.symm
    have hpt : p ++ t.drop l = t := by
      rw [← ht]
      exact (List.take_append_drop l t)
    have hrec := treeToH2_append_dist_le p (t.drop l)
    rw [hyperbolicDist_comm]
    simpa [hpt] using hrec
  have htri := HyperbolicMetric.hyperbolicDist_triangle (treeToH2 s) (treeToH2 p) (treeToH2 t)
  have hdrop_nat : (s.drop l).length + (t.drop l).length = treeDist s t := by
    rw [List.length_drop, List.length_drop]
    have hs : l ≤ s.length := by dsimp [l]; exact (commonPrefix_length_le (s := s) (t := t)).1
    have ht : l ≤ t.length := by dsimp [l]; exact (commonPrefix_length_le (s := s) (t := t)).2
    dsimp [l, treeDist]
    omega
  have hcast : ((s.drop l).length : ℝ) + ((t.drop l).length : ℝ) = treeDistR s t := by
    dsimp [treeDistR]
    exact_mod_cast hdrop_nat
  have hsum : hyperbolicDist (treeToH2 s) (treeToH2 t) ≤
      edgeBound * ((s.drop l).length : ℝ) + edgeBound * ((t.drop l).length : ℝ) := by
    nlinarith [htri, hup, hdown]
  have hdist : edgeBound * ((s.drop l).length : ℝ) + edgeBound * ((t.drop l).length : ℝ)
      = edgeBound * treeDistR s t := by
    rw [← mul_add, hcast]
  rw [← hdist]
  exact hsum

/-- **The map is coarsely Lipschitz.** The (true) upper bound packaged as an existential: there is a
constant `E = edgeBound` with `hyperbolicDist (treeToH2 s) (treeToH2 t) ≤ E · treeDistR s t`. -/
theorem treeToH2_coarseLipschitz :
    ∃ E : ℝ, ∀ s t : List Bool, hyperbolicDist (treeToH2 s) (treeToH2 t) ≤ E * treeDistR s t :=
  ⟨edgeBound, fun s t => hyperbolicDist_le_edge_mul_treeDistR s t⟩

/-! ## The honest boundary: `treeToH2` is *not* coarsely injective

The binary-expansion angle `2π · pathAngle` identifies `0.0111…₂` with `0.1000…₂`: the two branch
vertices `[true, false, …, false]` and `[false, true, …, true]` have `pathAngle` `1/2` and
`1/2 − 2^−(k+1)`, so their images sit at the same radius `ln 2 · (k+1)` with angle difference
`2π · 2^−(k+1) → 0`. Their hyperbolic distance therefore converges to a **constant**
(`arcosh(cosh(ln 2) + 4π²)`), while their tree distance `2(k+1)` grows without bound. Hence no `K, C`
can satisfy `treeDistR ≤ K · hyperbolicDist + C`: the lower half of a quasi-isometry fails, and the
map `treeToH2` is **not** a quasi-isometry (it is only coarsely Lipschitz + coarsely surjective). -/

/-- The "true, then all-false" branch vertex `[true, false, …, false]` (length `k + 1`); its
`pathAngle` is exactly `1/2` (`0.1000…₂`). -/
def antipodalS (k : ℕ) : List Bool := true :: List.replicate k false

/-- The "false, then all-true" branch vertex `[false, true, …, true]` (length `k + 1`); its
`pathAngle` is `1/2 − 2^−(k+1)` (`0.0111…₂`), approaching `1/2` from below. -/
def antipodalT (k : ℕ) : List Bool := false :: List.replicate k true

lemma pathAngle_replicate_false (k : ℕ) : pathAngle (List.replicate k false) = 0 := by
  induction k with
  | zero => simp [pathAngle]
  | succ k ih => simp [pathAngle, List.replicate_succ, ih]

lemma pathAngle_antipodalS (k : ℕ) : pathAngle (antipodalS k) = 1 / 2 := by
  simp [antipodalS, pathAngle, pathAngle_replicate_false]

lemma pathAngle_replicate_true (k : ℕ) :
    pathAngle (List.replicate k true) = 1 - 1 / (2 : ℝ) ^ k := by
  induction k with
  | zero => simp [pathAngle]
  | succ k ih =>
      simp [pathAngle, List.replicate_succ, ih]
      rw [pow_succ]
      field_simp
      ring

lemma pathAngle_antipodalT (k : ℕ) :
    pathAngle (antipodalT k) = 1 / 2 - 1 / (2 : ℝ) ^ (k + 1) := by
  simp [antipodalT, pathAngle, pathAngle_replicate_true]
  rw [pow_succ]
  field_simp

/-- The two antipodal branch vertices of the same depth have tree distance `2(k+1)`. -/
lemma treeDist_antipodal (k : ℕ) :
    treeDist (antipodalS k) (antipodalT k) = 2 * (k + 1) := by
  simp [antipodalS, antipodalT, treeDist, commonPrefixLength, List.length_replicate]
  omega

lemma treeDistR_antipodal (k : ℕ) :
    treeDistR (antipodalS k) (antipodalT k) = ((2 * (k + 1) : ℕ) : ℝ) := by
  rw [treeDistR, treeDist_antipodal]

/-- **The collapse.** The images of the two antipodal branch vertices are within the constant
`arcosh(cosh(ln 2) + 4π²)` of each other, uniformly in `k` — they are the *same* radius and an angle
`2π · 2^−(k+1)` apart, so `hyperbolicDist_bound_of_approx` (radial error `0`, angular error
`2π/2^(k+1)`) applies. -/
lemma hyperbolicDist_antipodal_bounded (k : ℕ) :
    hyperbolicDist (treeToH2 (antipodalS k)) (treeToH2 (antipodalT k)) ≤
      Real.arcosh (Real.cosh (Real.log 2) + 4 * Real.pi ^ 2) := by
  rw [treeToH2_eq_h2point, treeToH2_eq_h2point]
  have hlenS : (antipodalS k).length = k + 1 := by simp [antipodalS]
  have hlenT : (antipodalT k).length = k + 1 := by simp [antipodalT]
  rw [hlenS, hlenT]
  have hthdiff : |2 * Real.pi * pathAngle (antipodalS k) - 2 * Real.pi * pathAngle (antipodalT k)|
      ≤ 2 * Real.pi / (2 ^ (k + 1) : ℝ) := by
    rw [← mul_sub]
    have hdiff : pathAngle (antipodalS k) - pathAngle (antipodalT k) = 1 / (2 : ℝ) ^ (k + 1) := by
      rw [pathAngle_antipodalS, pathAngle_antipodalT]
      ring
    rw [hdiff]
    rw [abs_of_nonneg (by positivity : 0 ≤ 2 * Real.pi * (1 / (2 : ℝ) ^ (k + 1)))]
    rw [show 2 * Real.pi * (1 / (2 : ℝ) ^ (k + 1)) = 2 * Real.pi / (2 : ℝ) ^ (k + 1) by ring]
  exact hyperbolicDist_bound_of_approx
    (Real.log 2 * ((k + 1 : ℕ) : ℝ))
    (2 * Real.pi * pathAngle (antipodalS k))
    (2 * Real.pi * pathAngle (antipodalT k))
    (k + 1)
    (by positivity)
    (by
      rw [show Real.log 2 * ((k + 1 : ℕ) : ℝ) - Real.log 2 * ((k + 1 : ℕ) : ℝ) = 0 by ring]
      rw [abs_zero]
      exact le_of_lt (Real.log_pos (by norm_num : (1 : ℝ) < 2)))
    hthdiff

/-- The tree distance of the antipodal pair is unbounded as a function of the additive constant. -/
lemma treeDistR_antipodal_unbounded (B : ℝ) :
    ∃ k : ℕ, B < treeDistR (antipodalS k) (antipodalT k) := by
  rcases exists_nat_gt B with ⟨n, hn⟩
  refine ⟨n, ?_⟩
  rw [treeDistR_antipodal]
  push_cast
  have hn0 : 0 ≤ (n : ℝ) := by positivity
  nlinarith [hn, hn0]

/-- **`treeToH2` is not coarsely injective.** No constants `K, C` make
`treeDistR s t ≤ K · hyperbolicDist (treeToH2 s) (treeToH2 t) + C` hold for all `s, t`: along the
antipodal family the left side is `2(k+1) → ∞` while the right side stays bounded (the hyperbolic
distance is `≤ arcosh(cosh(ln 2) + 4π²)`). -/
theorem treeToH2_not_coarsely_injective :
    ¬ ∃ K C : ℝ, 0 < K ∧ ∀ s t : List Bool,
      treeDistR s t ≤ K * hyperbolicDist (treeToH2 s) (treeToH2 t) + C := by
  rintro ⟨K, C, hK, h⟩
  let B : ℝ := Real.arcosh (Real.cosh (Real.log 2) + 4 * Real.pi ^ 2)
  have hbounded : ∀ k : ℕ, hyperbolicDist (treeToH2 (antipodalS k)) (treeToH2 (antipodalT k)) ≤ B := by
    intro k
    exact hyperbolicDist_antipodal_bounded k
  have hle : ∀ k : ℕ, treeDistR (antipodalS k) (antipodalT k) ≤ K * B + C := by
    intro k
    have hk := h (antipodalS k) (antipodalT k)
    have hmul : K * hyperbolicDist (treeToH2 (antipodalS k)) (treeToH2 (antipodalT k)) ≤ K * B :=
      mul_le_mul_of_nonneg_left (hbounded k) (le_of_lt hK)
    nlinarith
  rcases treeDistR_antipodal_unbounded (K * B + C) with ⟨k, hbig⟩
  have hle' := hle k
  nlinarith

/-- **`treeToH2` is not a quasi-isometry.** It is coarsely Lipschitz (`treeToH2_coarseLipschitz`)
and coarsely surjective (`treeToH2_quasiSurjective`), but not coarsely injective
(`treeToH2_not_coarsely_injective`), so `quasiIsometricReal treeDistR hyperbolicDist treeToH2` is
false. -/
theorem treeToH2_not_quasiIsometric :
    ¬ quasiIsometricReal treeDistR hyperbolicDist treeToH2 := by
  rintro ⟨K, C, R, hK, hdist, hsurj⟩
  exact treeToH2_not_coarsely_injective ⟨K, C, hK, fun s t => (hdist s t).1⟩

end QMTreeDensity
