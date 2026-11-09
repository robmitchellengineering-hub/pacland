import Mathlib

/-!
# Quasi-surjectivity of the tree-to-H² map (the density half of the quasi-isometry)

Self-contained companion to `HyperbolicPlane.lean` (which a concurrent session owns). It
redeclares the hyperboloid model pieces it needs under the distinct namespace `QMTreeDensity` so it
builds independently, and proves the *quasi-surjectivity* rung: every hyperboloid point is within a
bounded hyperbolic distance of the tree's image.

The argument is dyadic density. A point `(cosh r, sinh r · cos θ, sinh r · sin θ)` is approximated by
a vertex at depth `d` with `ln 2 · d ≈ r` (radial error ≤ `ln 2`) and angle `2π · k/2^d ≈ θ`
(angular error ≤ `2π/2^d`, since dyadic rationals are dense in `[0, 1)`). The hyperbolic distance
then satisfies `d ≤ arcosh(cosh(ln 2) + 4π²)`, a constant. The proof uses the parametrisation of the
hyperboloid via `Complex.arg`, the `ℕ`-floor density lemmas, and the identity
`cosh r cosh r' − sinh r sinh r' cos Δ = cosh(r − r') + sinh r sinh r' (1 − cos Δ)`.
-/

namespace QMTreeDensity

/-- The hyperboloid model of H²: points `(t, x, y)` on the upper sheet of `-t² + x² + y² = -1`. -/
def Hyperboloid : Type := { p : ℝ × ℝ × ℝ // -p.1 ^ 2 + p.2.1 ^ 2 + p.2.2 ^ 2 = -1 ∧ 0 < p.1 }

/-- The Minkowski inner product `⟨p, q⟩_M = -t_p t_q + x_p x_q + y_p y_q`. -/
def minkowski (p q : ℝ × ℝ × ℝ) : ℝ :=
  -p.1 * q.1 + p.2.1 * q.2.1 + p.2.2 * q.2.2

/-- The hyperbolic distance on the hyperboloid model: `d(p, q) = arcosh(−⟨p, q⟩_M)`. -/
noncomputable def hyperbolicDist (p q : Hyperboloid) : ℝ :=
  Real.arcosh (-minkowski p.1 q.1)

/-- The angle of a tree path — its binary expansion in `[0,1)`, computed recursively. -/
noncomputable def pathAngle : List Bool → ℝ
  | [] => 0
  | b :: t => (if b then (1 : ℝ) else 0) / 2 + pathAngle t / 2

/-- **The quasi-isometry map.** A tree vertex `s` maps to a hyperboloid point at hyperbolic distance
`ln 2 · |s|` from the base and angle `pathAngle s`. -/
noncomputable def treeToH2 (s : List Bool) : Hyperboloid :=
  ⟨(Real.cosh ((Real.log 2) * (s.length : ℝ)),
     Real.sinh ((Real.log 2) * (s.length : ℝ)) * Real.cos (2 * Real.pi * pathAngle s),
     Real.sinh ((Real.log 2) * (s.length : ℝ)) * Real.sin (2 * Real.pi * pathAngle s)), by
     constructor
     · calc
          -(Real.cosh ((Real.log 2) * (s.length : ℝ))) ^ 2
            + (Real.sinh ((Real.log 2) * (s.length : ℝ)) * Real.cos (2 * Real.pi * pathAngle s)) ^ 2
            + (Real.sinh ((Real.log 2) * (s.length : ℝ)) * Real.sin (2 * Real.pi * pathAngle s)) ^ 2
            = -(Real.cosh ((Real.log 2) * (s.length : ℝ))) ^ 2
              + (Real.sinh ((Real.log 2) * (s.length : ℝ))) ^ 2
                * ((Real.cos (2 * Real.pi * pathAngle s)) ^ 2
                  + (Real.sin (2 * Real.pi * pathAngle s)) ^ 2) := by ring
          _ = -(Real.cosh ((Real.log 2) * (s.length : ℝ))) ^ 2
              + (Real.sinh ((Real.log 2) * (s.length : ℝ))) ^ 2 := by
                rw [Real.cos_sq_add_sin_sq]
                ring
          _ = -1 := by
                have h := Real.cosh_sq_sub_sinh_sq ((Real.log 2) * (s.length : ℝ))
                nlinarith
     · exact Real.cosh_pos ((Real.log 2) * (s.length : ℝ))⟩

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

/-- `sinh r ≤ exp r` for `r ≥ 0`. -/
lemma sinh_le_exp {r : ℝ} (hr : 0 ≤ r) : Real.sinh r ≤ Real.exp r := by
  rw [Real.sinh_eq]
  have h1 : 0 ≤ Real.exp r := Real.exp_nonneg r
  have h2 : 0 ≤ Real.exp (-r) := Real.exp_nonneg (-r)
  nlinarith

/-- `sinh(ln 2 · d) ≤ 2^d`. -/
lemma sinh_ln2_mul_le_two_pow (d : ℕ) :
    Real.sinh (Real.log 2 * (d : ℝ)) ≤ (2 : ℝ) ^ d := by
  have h := sinh_le_exp (by positivity : 0 ≤ Real.log 2 * (d : ℝ))
  rwa [exp_ln2_mul_eq_two_pow d] at h

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

end QMTreeDensity
