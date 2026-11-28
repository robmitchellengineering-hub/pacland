import Mathlib
import PaclandProof.QM.Bessel
import PaclandProof.QM.BesselRecurrence

/-!
# The integral representation's foundation — the orthogonality of cos on [0, π]

The derivative-free route to the small-field activity bound `1 − I₁/I₀ ≤ C/β` goes through the
integral representation `I_n(x) = (1/π)∫₀^π e^{x cos θ} cos(nθ) dθ`. Its foundation is the
orthogonality of the cosine family on [0, π]: the first harmonic integrates to zero and the squared
cosine normalizes to π/2. These are the first concrete steps of that route (the Jacobi–Anger
expansion and the concentration bound build on them).
-/

open Real intervalIntegral
open scoped BigOperators

namespace QM

/-- `∫₀^π cos θ dθ = 0` — the first harmonic integrates to zero (orthogonality to the constant). -/
theorem integral_cos_zero_pi : (∫ θ in (0 : ℝ)..π, Real.cos θ) = 0 := by
  have hderiv : ∀ x ∈ Set.uIcc (0 : ℝ) π, HasDerivAt (fun y : ℝ => Real.sin y) (Real.cos x) x := by
    intro x hx
    exact Real.hasDerivAt_sin x
  have hint : IntervalIntegrable (fun y : ℝ => Real.cos y) MeasureTheory.volume (0 : ℝ) π :=
    Real.continuous_cos.intervalIntegrable _ _
  rw [intervalIntegral.integral_eq_sub_of_hasDerivAt hderiv hint]
  simp [Real.sin_pi, Real.sin_zero]

/-- `∫₀^π cos² θ dθ = π/2` — the squared-cosine normalization. -/
theorem integral_cos_sq_pi : (∫ θ in (0 : ℝ)..π, Real.cos θ ^ 2) = π / 2 := by
  rw [integral_cos_sq]
  norm_num [Real.sin_pi, Real.sin_zero, Real.cos_pi, Real.cos_zero]

/-- **The Wallis recurrence**: `∫₀^π cos^{2m+2} θ = ((2m+1)/(2m+2))·∫₀^π cos^{2m} θ`. This is mathlib's
`integral_cos_pow` (the reduction formula) specialized to `[0, π]`, where the boundary term vanishes
(`sin π = sin 0 = 0`). The key input to the Jacobi–Anger expansion. -/
theorem wallis_recurrence (m : ℕ) :
    (∫ θ in (0 : ℝ)..π, (Real.cos θ)^(2*m+2)) =
      ((2*m+1 : ℝ)/(2*m+2)) * (∫ θ in (0 : ℝ)..π, (Real.cos θ)^(2*m)) := by
  rw [integral_cos_pow (a := (0 : ℝ)) (b := π) (n := 2*m)]
  simp [Real.sin_pi, Real.sin_zero]

/-- **The closed Wallis form**: `∫₀^π cos^{2m} θ = π(2m)!/(2^{2m}(m!)²)`. Induction on the Wallis
recurrence, base `∫ 1 = π`. This is the term-by-term coefficient the Jacobi–Anger expansion needs. -/
theorem wallis_closed (m : ℕ) :
    (∫ θ in (0 : ℝ)..π, (Real.cos θ)^(2*m)) =
      π * ((2*m).factorial : ℝ) / (2^(2*m) * (m.factorial : ℝ)^2) := by
  induction m with
  | zero => simp [intervalIntegral.integral_const]
  | succ m ih =>
      rw [show 2*(m+1) = 2*m+2 by omega]
      rw [wallis_recurrence m]
      rw [ih]
      have hfact2 : ((2*m+2).factorial : ℝ) = (2*m+2) * (2*m+1) * ((2*m).factorial : ℝ) := by
        norm_num [Nat.factorial_succ]
        ring
      have hfactm : ((m+1).factorial : ℝ) = (m+1) * (m.factorial : ℝ) := by
        norm_num [Nat.factorial_succ]
      field_simp
      rw [hfact2, hfactm]
      ring

/-- **The odd powers integrate to zero**: `∫₀^π cos^{2k+1} θ = 0`. Induction on the reduction formula
(`integral_cos_pow`): the odd recurrence `∫cos^{2k+3} = (2k+2)/(2k+3)·∫cos^{2k+1}` with base `∫cos = 0`.
Together with `wallis_closed`, this is the full term-by-term decomposition of `e^{x cos θ}` the
Jacobi–Anger expansion needs (odd powers vanish, even powers give the `1/(m!)²` series). -/
theorem integral_cos_odd_pow (k : ℕ) :
    (∫ θ in (0 : ℝ)..π, (Real.cos θ)^(2*k+1)) = 0 := by
  induction k with
  | zero => simpa using integral_cos_zero_pi
  | succ k ih =>
      rw [show 2*(k+1)+1 = (2*k+1)+2 by omega]
      rw [integral_cos_pow (a := (0 : ℝ)) (b := π) (n := 2*k+1)]
      simp [Real.sin_pi, Real.sin_zero]
      rw [ih]
      ring
      tauto

/-- **The term-by-term integration of the exp series on [0, π]**: `∫ Σₘ (x cos θ)^m/m! = Σₘ ∫ (x cos θ)^m/m!`.
Dominated convergence with the bound `|x|^m/m!` (since `|cos θ| ≤ 1`), whose tsum is `exp|x|`. This is
the swap that turns the exp series into the Bessel series (the Jacobi–Anger step). -/
theorem integral_tsum_exp_cos (x : ℝ) :
    (∫ θ in (0 : ℝ)..π, ∑' m : ℕ, (x * Real.cos θ)^m / (m.factorial : ℝ)) =
      ∑' m : ℕ, ∫ θ in (0 : ℝ)..π, (x * Real.cos θ)^m / (m.factorial : ℝ) := by
  have hswap := intervalIntegral.hasSum_integral_of_dominated_convergence
    (μ := MeasureTheory.volume) (a := (0 : ℝ)) (b := π)
    (F := fun m θ => (x * Real.cos θ)^m / (m.factorial : ℝ))
    (f := fun θ => ∑' m : ℕ, (x * Real.cos θ)^m / (m.factorial : ℝ))
    (bound := fun m _ => |x|^m / (m.factorial : ℝ))
    (by
      intro m
      exact (((continuous_const.mul Real.continuous_cos).pow m).div_const (m.factorial : ℝ)).aestronglyMeasurable)
    (by
      intro m
      filter_upwards with θ hθ
      dsimp
      have hcos : |Real.cos θ| ≤ 1 := abs_cos_le_one θ
      have hpow : |x * Real.cos θ|^m ≤ |x|^m := by
        rw [abs_mul, mul_pow]
        have h1 : |x|^m * |Real.cos θ|^m ≤ |x|^m * 1 :=
          mul_le_mul_of_nonneg_left (pow_le_one₀ (abs_nonneg _) hcos) (pow_nonneg (abs_nonneg x) m)
        simpa using h1
      rw [abs_div, abs_pow, abs_of_nonneg (show (0 : ℝ) ≤ (m.factorial : ℝ) by exact Nat.cast_nonneg _)]
      exact div_le_div_of_nonneg_right hpow (Nat.cast_nonneg _))
    (by
      filter_upwards with θ hθ
      exact (NormedSpace.expSeries_div_hasSum_exp |x|).summable)
    (by
      have hconst : (fun _ : ℝ => ∑' m : ℕ, |x|^m / (m.factorial : ℝ)) = (fun _ : ℝ => Real.exp |x|) := by
        funext θ
        rw [Real.exp_eq_exp_ℝ]
        exact (NormedSpace.expSeries_div_hasSum_exp |x|).tsum_eq
      rw [hconst]
      exact continuous_const.intervalIntegrable (0 : ℝ) π)
    (by
      filter_upwards with θ hθ
      exact (NormedSpace.expSeries_div_hasSum_exp (x * Real.cos θ)).summable.hasSum)
  exact hswap.tsum_eq.symm

/-- **The even terms give the Bessel series**: `Σₖ x^{2k}/(2k)!·∫₀^π cos^{2k} = π·besselI 0 x`. The
Wallis closed form turns each even integral into `π(2k)!/(2^{2k}(k!)²)`, whose factorial cancellation
leaves exactly the `(x/2)^{2k}/(k!)²` coefficient of `besselI 0`. -/
theorem tsum_even_cos_eq_besselI0 (x : ℝ) :
    (∑' k : ℕ, x^(2*k) / ((2*k).factorial : ℝ) * (∫ θ in (0 : ℝ)..π, (Real.cos θ)^(2*k))) = π * besselI 0 x := by
  rw [show (fun k : ℕ => x^(2*k) / ((2*k).factorial : ℝ) * (∫ θ in (0 : ℝ)..π, (Real.cos θ)^(2*k))) =
      (fun k : ℕ => π * (x/2)^(2*k) / (k.factorial : ℝ)^2) by
    funext k
    rw [wallis_closed k]
    field_simp [div_pow]
    rw [← mul_pow]
    norm_num
    ring_nf]
  rw [show (fun k : ℕ => π*(x/2)^(2*k)/(k.factorial : ℝ)^2) = (fun k : ℕ => π*((x/2)^(2*k)/(k.factorial : ℝ)^2)) by
    funext k; ring]
  rw [tsum_mul_left]
  congr 1
  rw [show (fun k : ℕ => (x/2)^(2*k) / (k.factorial : ℝ)^2) =
      (fun k : ℕ => (x/2)^(2*k+0) / ((k.factorial : ℝ) * (k+0).factorial)) by
    funext k
    simp [pow_two]]
  rfl

/-- **The full coefficient identity**: `Σₘ x^m/m!·∫₀^π cos^m θ = π·besselI 0 x`. The odd powers vanish
and the even powers give `tsum_even_cos_eq_besselI0`, combined by the even/odd split. This is the
Jacobi–Anger n=0 coefficient expansion. -/
theorem tsum_exp_cos_coeff (x : ℝ) :
    (∑' m : ℕ, x^m / (m.factorial : ℝ) * (∫ θ in (0 : ℝ)..π, (Real.cos θ)^m)) = π * besselI 0 x := by
  let f : ℕ → ℝ := fun m => x^m / (m.factorial : ℝ) * (∫ θ in (0 : ℝ)..π, (Real.cos θ)^m)
  have hsum : Summable f := by
    have hnorm : Summable (fun m => |x|^m / (m.factorial : ℝ)) := (NormedSpace.expSeries_div_hasSum_exp |x|).summable
    have hbound : ∀ m, ‖f m‖ ≤ π * (|x|^m / (m.factorial : ℝ)) := by
      intro m
      dsimp [f]
      have hint : ‖∫ θ in (0 : ℝ)..π, (Real.cos θ)^m‖ ≤ π := by
        have hle : ∀ θ ∈ Set.uIoc (0 : ℝ) π, ‖(Real.cos θ)^m‖ ≤ 1 := by
          intro θ hθ
          rw [Real.norm_eq_abs, abs_pow]
          exact pow_le_one₀ (abs_nonneg _) (abs_cos_le_one θ)
        simpa using (intervalIntegral.norm_integral_le_of_norm_le_const (a := (0 : ℝ)) (b := π) (f := fun θ => (Real.cos θ)^m) (C := 1) hle)
      calc
        ‖x^m / (m.factorial : ℝ) * (∫ θ in (0 : ℝ)..π, (Real.cos θ)^m)‖
          = |x|^m / (m.factorial : ℝ) * ‖∫ θ in (0 : ℝ)..π, (Real.cos θ)^m‖ := by
            rw [Real.norm_eq_abs, abs_mul, abs_div, abs_pow]
            rw [abs_of_nonneg (show (0 : ℝ) ≤ (m.factorial : ℝ) by exact Nat.cast_nonneg _)]
            rw [Real.norm_eq_abs]
        _ ≤ π * (|x|^m / (m.factorial : ℝ)) := by
            simpa [mul_comm] using (mul_le_mul_of_nonneg_left hint (div_nonneg (pow_nonneg (abs_nonneg x) m) (Nat.cast_nonneg (m.factorial))))
    exact Summable.of_norm_bounded (hnorm.mul_left π) hbound
  have hsum_even : Summable (fun k => f (2*k)) := hsum.comp_injective (i := fun k : ℕ => 2*k) (by intro a b h; exact Nat.mul_left_cancel (by norm_num : (0 : ℕ) < 2) h)
  have hsum_odd : Summable (fun k => f (2*k+1)) := hsum.comp_injective (i := fun k : ℕ => 2*k+1) (by intro a b h; exact Nat.mul_left_cancel (by norm_num : (0 : ℕ) < 2) (Nat.succ.inj h))
  have hodd : (∑' k, f (2*k+1)) = 0 := by
    dsimp [f]
    have hzero : (fun k : ℕ => x^(2*k+1) / ((2*k+1).factorial : ℝ) * (∫ θ in (0 : ℝ)..π, (Real.cos θ)^(2*k+1))) = (fun _ : ℕ => 0) := by
      funext k
      rw [integral_cos_odd_pow k]
      simp
    rw [hzero, tsum_zero]
  have heven : (∑' k, f (2*k)) = π * besselI 0 x := by
    dsimp [f]
    exact tsum_even_cos_eq_besselI0 x
  have hsplit := tsum_even_add_odd (f := f) hsum_even hsum_odd
  rw [← hsplit]
  rw [hodd, heven]
  simp

/-- **The Jacobi–Anger n=0 projection**: `∫₀^π exp(x cos θ) dθ = π·besselI 0 x`. The exp series
(`expSeries_div_hasSum_exp`), the term-by-term swap (`integral_tsum_exp_cos`), the linearity, and the
coefficient identity (`tsum_exp_cos_coeff`) assemble into the modified Bessel function. -/
theorem integral_exp_cos_eq_besselI0 (x : ℝ) :
    (∫ θ in (0 : ℝ)..π, Real.exp (x * Real.cos θ)) = π * besselI 0 x := by
  have hexp : (∫ θ in (0 : ℝ)..π, Real.exp (x * Real.cos θ)) =
      (∫ θ in (0 : ℝ)..π, ∑' m : ℕ, (x * Real.cos θ)^m / (m.factorial : ℝ)) := by
    apply intervalIntegral.integral_congr
    intro θ hθ
    rw [Real.exp_eq_exp_ℝ]
    exact (NormedSpace.expSeries_div_hasSum_exp (x * Real.cos θ)).tsum_eq.symm
  rw [hexp, integral_tsum_exp_cos x]
  rw [show (∑' m : ℕ, ∫ θ in (0 : ℝ)..π, (x * Real.cos θ)^m / (m.factorial : ℝ)) =
      (∑' m : ℕ, x^m / (m.factorial : ℝ) * (∫ θ in (0 : ℝ)..π, (Real.cos θ)^m)) by
    apply tsum_congr
    intro m
    have hlin : (∫ θ in (0 : ℝ)..π, (x * Real.cos θ)^m / (m.factorial : ℝ)) =
        x^m / (m.factorial : ℝ) * (∫ θ in (0 : ℝ)..π, (Real.cos θ)^m) := by
      rw [show (fun θ : ℝ => (x * Real.cos θ)^m / (m.factorial : ℝ)) = (fun θ : ℝ => (x^m / (m.factorial : ℝ)) * (Real.cos θ)^m) by
        funext θ
        rw [mul_pow]
        ring]
      rw [intervalIntegral.integral_const_mul]
    exact hlin]
  exact tsum_exp_cos_coeff x

/-- **The term-by-term integration of the exp series × cos on [0, π]** (the n=1 companion to
`integral_tsum_exp_cos`): `∫ (Σₘ (x cos θ)^m/m!)·cos θ = Σₘ ∫ (x cos θ)^m/m!·cos θ`, with the same
dominated-convergence bound `|x|^m/m!` (since `|cos θ| ≤ 1`). -/
theorem integral_tsum_exp_cos_mul_cos (x : ℝ) :
    (∫ θ in (0 : ℝ)..π, (∑' m : ℕ, (x * Real.cos θ)^m / (m.factorial : ℝ)) * Real.cos θ) =
      ∑' m : ℕ, ∫ θ in (0 : ℝ)..π, (x * Real.cos θ)^m / (m.factorial : ℝ) * Real.cos θ := by
  have hswap := intervalIntegral.hasSum_integral_of_dominated_convergence
    (μ := MeasureTheory.volume) (a := (0 : ℝ)) (b := π)
    (F := fun m θ => (x * Real.cos θ)^m / (m.factorial : ℝ) * Real.cos θ)
    (f := fun θ => (∑' m : ℕ, (x * Real.cos θ)^m / (m.factorial : ℝ)) * Real.cos θ)
    (bound := fun m _ => |x|^m / (m.factorial : ℝ))
    (by
      intro m
      exact ((((continuous_const.mul Real.continuous_cos).pow m).div_const (m.factorial : ℝ)).mul Real.continuous_cos).aestronglyMeasurable)
    (by
      intro m
      filter_upwards with θ hθ
      have hcos : |Real.cos θ| ≤ 1 := abs_cos_le_one θ
      have hpow : |x * Real.cos θ|^m ≤ |x|^m := by
        rw [abs_mul, mul_pow]
        have h1 : |x|^m * |Real.cos θ|^m ≤ |x|^m * 1 :=
          mul_le_mul_of_nonneg_left (pow_le_one₀ (abs_nonneg _) hcos) (pow_nonneg (abs_nonneg x) m)
        simpa using h1
      rw [Real.norm_eq_abs, abs_mul, abs_div, abs_pow, abs_of_nonneg (show (0 : ℝ) ≤ (m.factorial : ℝ) by exact Nat.cast_nonneg _)]
      have hle : |x * Real.cos θ|^m * |Real.cos θ| ≤ |x|^m := by
        have h1 : |x * Real.cos θ|^m * |Real.cos θ| ≤ |x|^m * |Real.cos θ| :=
          mul_le_mul_of_nonneg_right hpow (abs_nonneg _)
        have h2 : |x|^m * |Real.cos θ| ≤ |x|^m :=
          mul_le_of_le_one_right (pow_nonneg (abs_nonneg x) m) hcos
        exact le_trans h1 h2
      simpa [div_eq_mul_inv, mul_assoc, mul_left_comm, mul_comm] using (div_le_div_of_nonneg_right hle (Nat.cast_nonneg (m.factorial))))
    (by
      filter_upwards with θ hθ
      exact (NormedSpace.expSeries_div_hasSum_exp |x|).summable)
    (by
      have hconst : (fun _ : ℝ => ∑' m : ℕ, |x|^m / (m.factorial : ℝ)) = (fun _ : ℝ => Real.exp |x|) := by
        funext θ
        rw [Real.exp_eq_exp_ℝ]
        exact (NormedSpace.expSeries_div_hasSum_exp |x|).tsum_eq
      rw [hconst]
      exact continuous_const.intervalIntegrable (0 : ℝ) π)
    (by
      filter_upwards with θ hθ
      exact ((NormedSpace.expSeries_div_hasSum_exp (x * Real.cos θ)).summable.hasSum).mul_right (Real.cos θ))
  exact hswap.tsum_eq.symm

/-- **The n=1 coefficient identity**: `Σₘ x^m/m!·∫₀^π cos^{m+1} θ = π·besselI 1 x`. The even m vanish,
the odd m = 2k+1 give the Wallis closed form, whose factorial cancellation leaves the
`(x/2)^{2k+1}/(k!(k+1)!)` coefficient of `besselI 1`. -/
theorem tsum_exp_cos_mul_cos_coeff (x : ℝ) :
    (∑' m : ℕ, x^m / (m.factorial : ℝ) * (∫ θ in (0 : ℝ)..π, (Real.cos θ)^(m+1))) = π * besselI 1 x := by
  let f : ℕ → ℝ := fun m => x^m / (m.factorial : ℝ) * (∫ θ in (0 : ℝ)..π, (Real.cos θ)^(m+1))
  have hsum : Summable f := by
    have hnorm : Summable (fun m => |x|^m / (m.factorial : ℝ)) := (NormedSpace.expSeries_div_hasSum_exp |x|).summable
    have hbound : ∀ m, ‖f m‖ ≤ π * (|x|^m / (m.factorial : ℝ)) := by
      intro m
      dsimp [f]
      have hint : ‖∫ θ in (0 : ℝ)..π, (Real.cos θ)^(m+1)‖ ≤ π := by
        have hle : ∀ θ ∈ Set.uIoc (0 : ℝ) π, ‖(Real.cos θ)^(m+1)‖ ≤ 1 := by
          intro θ hθ
          rw [Real.norm_eq_abs, abs_pow]
          exact pow_le_one₀ (abs_nonneg _) (abs_cos_le_one θ)
        simpa using (intervalIntegral.norm_integral_le_of_norm_le_const (a := (0 : ℝ)) (b := π) (f := fun θ => (Real.cos θ)^(m+1)) (C := 1) hle)
      calc
        ‖x^m / (m.factorial : ℝ) * (∫ θ in (0 : ℝ)..π, (Real.cos θ)^(m+1))‖
          = |x|^m / (m.factorial : ℝ) * ‖∫ θ in (0 : ℝ)..π, (Real.cos θ)^(m+1)‖ := by
            rw [Real.norm_eq_abs, abs_mul, abs_div, abs_pow]
            rw [abs_of_nonneg (show (0 : ℝ) ≤ (m.factorial : ℝ) by exact Nat.cast_nonneg _)]
            rw [Real.norm_eq_abs]
        _ ≤ π * (|x|^m / (m.factorial : ℝ)) := by
            simpa [mul_comm] using (mul_le_mul_of_nonneg_left hint (div_nonneg (pow_nonneg (abs_nonneg x) m) (Nat.cast_nonneg (m.factorial))))
    exact Summable.of_norm_bounded (hnorm.mul_left π) hbound
  have hsum_even : Summable (fun k => f (2*k)) := hsum.comp_injective (i := fun k : ℕ => 2*k) (by intro a b h; exact Nat.mul_left_cancel (by norm_num : (0 : ℕ) < 2) h)
  have hsum_odd : Summable (fun k => f (2*k+1)) := hsum.comp_injective (i := fun k : ℕ => 2*k+1) (by intro a b h; exact Nat.mul_left_cancel (by norm_num : (0 : ℕ) < 2) (Nat.succ.inj h))
  have heven_zero : (∑' k, f (2*k)) = 0 := by
    dsimp [f]
    have hzero : (fun k : ℕ => x^(2*k) / ((2*k).factorial : ℝ) * (∫ θ in (0 : ℝ)..π, (Real.cos θ)^(2*k+1))) = (fun _ : ℕ => 0) := by
      funext k
      rw [integral_cos_odd_pow k]
      simp
    rw [hzero, tsum_zero]
  have hodd : (∑' k, f (2*k+1)) = π * besselI 1 x := by
    dsimp [f]
    rw [show (fun k : ℕ => x^(2*k+1) / ((2*k+1).factorial : ℝ) * (∫ θ in (0 : ℝ)..π, (Real.cos θ)^(2*k+2))) =
        (fun k : ℕ => π * (x/2)^(2*k+1) / ((k.factorial : ℝ) * (k+1).factorial)) by
      funext k
      rw [show 2*k+2 = 2*(k+1) by omega]
      rw [wallis_closed (k+1)]
      rw [show (2*(k+1)).factorial = (2*(k+1)) * (2*k+1).factorial by
        rw [show 2*(k+1) = (2*k+1)+1 by omega]; rw [Nat.factorial_succ]]
      rw [show (2*k+1).factorial = (2*k+1) * (2*k).factorial by
        rw [show 2*k+1 = (2*k)+1 by omega]; rw [Nat.factorial_succ]]
      rw [show (k+1).factorial = (k+1) * k.factorial by rw [Nat.factorial_succ]]
      norm_num
      field_simp
      rw [div_pow]
      have hpow2 : (2 : ℝ)^(2*(k+1)) = 2^(2*k+1) * 2 := by
        rw [show 2*(k+1) = (2*k+1)+1 by omega]
        rw [pow_succ]
      rw [hpow2]
      field_simp]
    rw [show (fun k : ℕ => π * (x/2)^(2*k+1) / ((k.factorial : ℝ) * (k+1).factorial)) =
        (fun k : ℕ => π * ((x/2)^(2*k+1) / ((k.factorial : ℝ) * (k+1).factorial))) by
      funext k; ring]
    rw [tsum_mul_left]
    congr 1
  have hsplit := tsum_even_add_odd (f := f) hsum_even hsum_odd
  rw [← hsplit]
  rw [heven_zero, hodd]
  simp

/-- **The Jacobi–Anger n=1 projection**: `∫₀^π exp(x cos θ)·cos θ dθ = π·besselI 1 x`. The same
assembly as the n=0 case with a `cos θ` factor: exp series → swap → linearity → coefficient identity.
This gives `E[cos θ] = I₁/I₀` under the von-Mises measure, the input to the concentration bound. -/
theorem integral_exp_cos_mul_cos_eq_besselI1 (x : ℝ) :
    (∫ θ in (0 : ℝ)..π, Real.exp (x * Real.cos θ) * Real.cos θ) = π * besselI 1 x := by
  have hexp : (∫ θ in (0 : ℝ)..π, Real.exp (x * Real.cos θ) * Real.cos θ) =
      (∫ θ in (0 : ℝ)..π, (∑' m : ℕ, (x * Real.cos θ)^m / (m.factorial : ℝ)) * Real.cos θ) := by
    apply intervalIntegral.integral_congr
    intro θ hθ
    rw [Real.exp_eq_exp_ℝ]
    exact congrArg (fun y : ℝ => y * Real.cos θ) ((NormedSpace.expSeries_div_hasSum_exp (x * Real.cos θ)).tsum_eq.symm)
  rw [hexp, integral_tsum_exp_cos_mul_cos x]
  rw [show (∑' m : ℕ, ∫ θ in (0 : ℝ)..π, (x * Real.cos θ)^m / (m.factorial : ℝ) * Real.cos θ) =
      (∑' m : ℕ, x^m / (m.factorial : ℝ) * (∫ θ in (0 : ℝ)..π, (Real.cos θ)^(m+1))) by
    apply tsum_congr
    intro m
    have hlin : (∫ θ in (0 : ℝ)..π, (x * Real.cos θ)^m / (m.factorial : ℝ) * Real.cos θ) =
        x^m / (m.factorial : ℝ) * (∫ θ in (0 : ℝ)..π, (Real.cos θ)^(m+1)) := by
      rw [show (fun θ : ℝ => (x * Real.cos θ)^m / (m.factorial : ℝ) * Real.cos θ) = (fun θ : ℝ => (x^m / (m.factorial : ℝ)) * (Real.cos θ)^(m+1)) by
        funext θ
        rw [mul_pow]
        ring]
      rw [intervalIntegral.integral_const_mul]
    exact hlin]
  exact tsum_exp_cos_mul_cos_coeff x

/-- **The derivative recurrence `I₀′ = I₁`** via differentiation under the integral (the parametric
interval-integral derivative, not the tsum derivative). The n=0/n=1 projections give the integrand and
its derivative, and `hasDerivAt_integral_of_dominated_loc_of_deriv_le` commutes them. -/
theorem besselI0_hasDerivAt (β : ℝ) :
    HasDerivAt (fun x : ℝ => besselI 0 x) (besselI 1 β) β := by
  have h := intervalIntegral.hasDerivAt_integral_of_dominated_loc_of_deriv_le
    (𝕜 := ℝ) (μ := MeasureTheory.volume) (a := (0 : ℝ)) (b := π)
    (F := fun x θ => Real.exp (x * Real.cos θ))
    (F' := fun x θ => Real.cos θ * Real.exp (x * Real.cos θ))
    (x₀ := β) (s := Set.Icc (β - 1) (β + 1))
    (bound := fun _ => Real.exp (|β| + 1))
    (Icc_mem_nhds (by linarith) (by linarith))
    (by
      filter_upwards with x
      exact (Real.continuous_exp.comp (continuous_const.mul Real.continuous_cos)).aestronglyMeasurable)
    (by
      exact (Real.continuous_exp.comp (continuous_const.mul Real.continuous_cos)).intervalIntegrable (0 : ℝ) π)
    (by
      exact (Real.continuous_cos.mul (Real.continuous_exp.comp (continuous_const.mul Real.continuous_cos))).aestronglyMeasurable)
    (by
      filter_upwards with θ hθ
      intro x hx
      rw [Real.norm_eq_abs, abs_mul]
      have hcos : |Real.cos θ| ≤ 1 := abs_cos_le_one θ
      have hxle : x * Real.cos θ ≤ |β| + 1 := by
        have hx_abs : |x| ≤ |β| + 1 := by
          rcases Set.mem_Icc.mp hx with ⟨hxl, hxu⟩
          have hx1 : x ≤ |β| + 1 := le_trans hxu (by linarith [le_abs_self β])
          have hx2 : -(|β| + 1) ≤ x := by linarith [hxl, neg_le_abs β]
          exact abs_le.mpr ⟨hx2, hx1⟩
        have h1 : x * Real.cos θ ≤ |x| * |Real.cos θ| := by
          rw [← abs_mul]
          exact le_abs_self _
        have h2 : |x| * |Real.cos θ| ≤ |β| + 1 := by
          have h21 : |x| * |Real.cos θ| ≤ |x| := mul_le_of_le_one_right (abs_nonneg x) hcos
          exact le_trans h21 hx_abs
        exact le_trans h1 h2
      have hexp : Real.exp (x * Real.cos θ) ≤ Real.exp (|β| + 1) :=
        Real.exp_le_exp.mpr hxle
      simpa using (mul_le_mul hcos hexp (by positivity) (by positivity)))
    (by
      exact continuous_const.intervalIntegrable (0 : ℝ) π)
    (by
      filter_upwards with θ hθ
      intro x hx
      have hlin : HasDerivAt (fun x : ℝ => x * Real.cos θ) (Real.cos θ) x := by
        simpa using (hasDerivAt_id x).mul_const (Real.cos θ)
      simpa [Function.comp_def, mul_comm] using (Real.hasDerivAt_exp (x * Real.cos θ)).comp x hlin)
  have h0 : (fun x : ℝ => ∫ θ in (0 : ℝ)..π, Real.exp (x * Real.cos θ) ∂MeasureTheory.volume) =
      (fun x : ℝ => π * besselI 0 x) := by
    funext x
    exact integral_exp_cos_eq_besselI0 x
  have h1 : (∫ θ in (0 : ℝ)..π, Real.cos θ * Real.exp (β * Real.cos θ)) = π * besselI 1 β := by
    simpa [mul_comm] using integral_exp_cos_mul_cos_eq_besselI1 β
  rw [h0] at h
  rw [h1] at h
  simpa using h.2.const_mul (1 / π)

/-- **The second derivative recurrence's key integral**: `∫₀^π sin² θ e^{x cos θ} dθ = π·I₁(x)/x` for
`x > 0`. Integration by parts with `u = sin θ`, `dv = sin θ e^{x cos θ} dθ = −(1/x) d(e^{x cos θ})`:
the boundary term vanishes, and the remainder is the n=1 integrand. This gives `I₁′ = I₀ − I₁/x`. -/
theorem integral_sin_sq_exp_cos {x : ℝ} (hx : x ≠ 0) :
    (∫ θ in (0 : ℝ)..π, (Real.sin θ)^2 * Real.exp (x * Real.cos θ)) =
      (1 / x) * (∫ θ in (0 : ℝ)..π, Real.cos θ * Real.exp (x * Real.cos θ)) := by
  have hderiv : ∀ θ, HasDerivAt (fun t : ℝ => Real.exp (x * Real.cos t)) (-x * Real.sin θ * Real.exp (x * Real.cos θ)) θ := by
    intro θ
    have hcos : HasDerivAt (fun t : ℝ => Real.cos t) (-Real.sin θ) θ := Real.hasDerivAt_cos θ
    have hlin : HasDerivAt (fun t : ℝ => x * Real.cos t) (-x * Real.sin θ) θ := by
      convert (hcos.const_mul x) using 1
      ring
    convert (Real.hasDerivAt_exp (x * Real.cos θ)).comp θ hlin using 1
    · funext t; rfl
    · ring
  have hibp := intervalIntegral.integral_mul_deriv_eq_deriv_mul
    (u := fun θ => Real.sin θ) (v := fun θ => Real.exp (x * Real.cos θ))
    (u' := fun θ => Real.cos θ)
    (v' := fun θ => -x * Real.sin θ * Real.exp (x * Real.cos θ))
    (fun θ hθ => Real.hasDerivAt_sin θ) (fun θ hθ => hderiv θ)
    (Real.continuous_cos.intervalIntegrable (0 : ℝ) π)
    ((by
        simpa [mul_assoc] using ((Real.continuous_sin.mul (Real.continuous_exp.comp (continuous_const.mul Real.continuous_cos))).const_mul (-x)) : Continuous (fun θ : ℝ => -x * Real.sin θ * Real.exp (x * Real.cos θ))).intervalIntegrable (0 : ℝ) π)
  rw [show (fun θ : ℝ => Real.sin θ * (-x * Real.sin θ * Real.exp (x * Real.cos θ))) =
      (fun θ : ℝ => -x * ((Real.sin θ)^2 * Real.exp (x * Real.cos θ))) by
    funext θ; ring] at hibp
  rw [intervalIntegral.integral_const_mul (-x) (fun θ => (Real.sin θ)^2 * Real.exp (x * Real.cos θ))] at hibp
  simp [Real.sin_pi, Real.sin_zero] at hibp
  field_simp [hx]
  exact hibp

/-- **The second derivative recurrence `I₁′ = I₀ − I₁/β`** (for β ≠ 0). Differentiation under the
integral of the n=1 projection gives `∫cos²θ e^{x cos θ}`, which by `integral_sin_sq_exp_cos` and the
n=0 projection equals `π(I₀ − I₁/x)`. -/
theorem besselI1_hasDerivAt (β : ℝ) (hβ : β ≠ 0) :
    HasDerivAt (fun x : ℝ => besselI 1 x) (besselI 0 β - besselI 1 β / β) β := by
  have h := intervalIntegral.hasDerivAt_integral_of_dominated_loc_of_deriv_le
    (𝕜 := ℝ) (μ := MeasureTheory.volume) (a := (0 : ℝ)) (b := π)
    (F := fun x θ => Real.cos θ * Real.exp (x * Real.cos θ))
    (F' := fun x θ => (Real.cos θ)^2 * Real.exp (x * Real.cos θ))
    (x₀ := β) (s := Set.Icc (β - 1) (β + 1))
    (bound := fun _ => Real.exp (|β| + 1))
    (Icc_mem_nhds (by linarith) (by linarith))
    (by
      filter_upwards with x
      exact (Real.continuous_cos.mul (Real.continuous_exp.comp (continuous_const.mul Real.continuous_cos))).aestronglyMeasurable)
    (by
      exact (Real.continuous_cos.mul (Real.continuous_exp.comp (continuous_const.mul Real.continuous_cos))).intervalIntegrable (0 : ℝ) π)
    (by
      exact ((Real.continuous_cos.pow 2).mul (Real.continuous_exp.comp (continuous_const.mul Real.continuous_cos))).aestronglyMeasurable)
    (by
      filter_upwards with θ hθ
      intro x hx
      rw [Real.norm_eq_abs, abs_mul]
      have hcos2 : |(Real.cos θ)^2| ≤ 1 := by
        rw [abs_pow]
        exact pow_le_one₀ (abs_nonneg _) (abs_cos_le_one θ)
      have hxle : x * Real.cos θ ≤ |β| + 1 := by
        have hx_abs : |x| ≤ |β| + 1 := by
          rcases Set.mem_Icc.mp hx with ⟨hxl, hxu⟩
          have hx1 : x ≤ |β| + 1 := le_trans hxu (by linarith [le_abs_self β])
          have hx2 : -(|β| + 1) ≤ x := by linarith [hxl, neg_le_abs β]
          exact abs_le.mpr ⟨hx2, hx1⟩
        have h1 : x * Real.cos θ ≤ |x| * |Real.cos θ| := by
          rw [← abs_mul]; exact le_abs_self _
        have h2 : |x| * |Real.cos θ| ≤ |β| + 1 := by
          have h21 : |x| * |Real.cos θ| ≤ |x| := mul_le_of_le_one_right (abs_nonneg x) (abs_cos_le_one θ)
          exact le_trans h21 hx_abs
        exact le_trans h1 h2
      have hexp : Real.exp (x * Real.cos θ) ≤ Real.exp (|β| + 1) := Real.exp_le_exp.mpr hxle
      simpa using (mul_le_mul hcos2 hexp (by positivity) (by positivity)))
    (by exact continuous_const.intervalIntegrable (0 : ℝ) π)
    (by
      filter_upwards with θ hθ
      intro x hx
      have hlin : HasDerivAt (fun x : ℝ => x * Real.cos θ) (Real.cos θ) x := by
        simpa using (hasDerivAt_id x).mul_const (Real.cos θ)
      have hexp' : HasDerivAt (fun x : ℝ => Real.exp (x * Real.cos θ)) (Real.cos θ * Real.exp (x * Real.cos θ)) x := by
        simpa [Function.comp_def, mul_comm] using (Real.hasDerivAt_exp (x * Real.cos θ)).comp x hlin
      simpa [pow_two, mul_assoc] using hexp'.const_mul (Real.cos θ))
  have h0 : (fun x : ℝ => ∫ θ in (0 : ℝ)..π, Real.cos θ * Real.exp (x * Real.cos θ) ∂MeasureTheory.volume) =
      (fun x : ℝ => π * besselI 1 x) := by
    funext x
    simpa [mul_comm] using integral_exp_cos_mul_cos_eq_besselI1 x
  have hval : (∫ θ in (0 : ℝ)..π, (Real.cos θ)^2 * Real.exp (β * Real.cos θ)) = π * (besselI 0 β - besselI 1 β / β) := by
    have hpoint : (fun θ : ℝ => (Real.cos θ)^2 * Real.exp (β * Real.cos θ)) =
        (fun θ : ℝ => Real.exp (β * Real.cos θ) - (Real.sin θ)^2 * Real.exp (β * Real.cos θ)) := by
      funext θ
      have hsq : (Real.cos θ)^2 + (Real.sin θ)^2 = 1 := Real.cos_sq_add_sin_sq θ
      have hsq' : (Real.cos θ)^2 = 1 - (Real.sin θ)^2 := by linarith [hsq]
      rw [hsq']
      ring
    have hcont_exp : Continuous (fun θ : ℝ => Real.exp (β * Real.cos θ)) :=
      Real.continuous_exp.comp ((continuous_const : Continuous (fun _ : ℝ => β)).mul Real.continuous_cos)
    have hcont_cos2 : Continuous (fun θ : ℝ => (Real.cos θ)^2 * Real.exp (β * Real.cos θ)) :=
      (Real.continuous_cos.pow 2).mul hcont_exp
    have hcont_sin2 : Continuous (fun θ : ℝ => (Real.sin θ)^2 * Real.exp (β * Real.cos θ)) :=
      (Real.continuous_sin.pow 2).mul hcont_exp
    rw [hpoint, intervalIntegral.integral_sub (hcont_exp.intervalIntegrable (μ := MeasureTheory.volume) (0 : ℝ) π) (hcont_sin2.intervalIntegrable (μ := MeasureTheory.volume) (0 : ℝ) π)]
    -- now simplify the RHS
    rw [integral_exp_cos_eq_besselI0 β]
    rw [integral_sin_sq_exp_cos hβ]
    rw [show (∫ θ in (0 : ℝ)..π, Real.cos θ * Real.exp (β * Real.cos θ)) = π * besselI 1 β by
      simpa [mul_comm] using integral_exp_cos_mul_cos_eq_besselI1 β]
    ring
  rw [h0] at h
  rw [hval] at h
  simpa using h.2.const_mul (1 / π)

/-- **The Riccati equation for the Bessel ratio** `r = I₁/I₀`: from `I₀′=I₁` and `I₁′=I₀−I₁/β`,
the quotient rule gives `r′ = 1 − r/β − r²`. Its fixed point is `1 − 1/(2β)`, which is the
concentration `1 − r ≤ C/β` — the ym-bakry-ceiling antipode-suppression bound. -/
theorem bessel_ratio_hasDerivAt (β : ℝ) (hβ : 0 < β) :
    HasDerivAt (fun x : ℝ => besselI 1 x / besselI 0 x)
      (1 - (besselI 1 β / besselI 0 β) / β - (besselI 1 β / besselI 0 β)^2) β := by
  have hI0 : besselI 0 β ≠ 0 := ne_of_gt (besselI_pos hβ)
  have hd0 : HasDerivAt (fun x : ℝ => besselI 0 x) (besselI 1 β) β := besselI0_hasDerivAt β
  have hd1 : HasDerivAt (fun x : ℝ => besselI 1 x) (besselI 0 β - besselI 1 β / β) β := besselI1_hasDerivAt β (ne_of_gt hβ)
  have hdiv := hd1.div hd0 hI0
  convert hdiv using 1
  field_simp [hI0]

/-- **The Riccati equation for the activity** `s = 1 − I₁/I₀`: `s′ = s² − (2+1/β)s + 1/β`, from
`r′ = 1 − r/β − r²` with `s = 1 − r`. The comparison input for the concentration `s ≤ C/β`. -/
theorem activity_hasDerivAt (β : ℝ) (hβ : 0 < β) :
    HasDerivAt (fun x : ℝ => 1 - besselI 1 x / besselI 0 x)
      ((1 - besselI 1 β / besselI 0 β)^2 - (2 + 1/β) * (1 - besselI 1 β / besselI 0 β) + 1/β) β := by
  have hr := bessel_ratio_hasDerivAt β hβ
  convert HasDerivAt.const_sub (1 : ℝ) hr using 1
  ring

/-- **The Bessel order `I₁ < I₀` for all β > 0**: `I₀ − I₁ = (1/π)∫(1−cos θ)e^{β cos θ} dθ > 0`
because the integrand is positive on (0, π). Input to the `w = βI₁ − (β−1)I₀` comparison. -/
theorem besselI1_lt_besselI0 {β : ℝ} (hβ : 0 < β) :
    besselI 1 β < besselI 0 β := by
  have hcont_exp : Continuous (fun θ : ℝ => Real.exp (β * Real.cos θ)) := by
    simpa [Function.comp_def] using (Real.continuous_exp.comp ((continuous_const : Continuous (fun _ : ℝ => β)).mul Real.continuous_cos))
  have hdiff : (∫ θ in (0 : ℝ)..π, Real.exp (β * Real.cos θ) * (1 - Real.cos θ)) = π * (besselI 0 β - besselI 1 β) := by
    calc
      (∫ θ in (0 : ℝ)..π, Real.exp (β * Real.cos θ) * (1 - Real.cos θ))
        = (∫ θ in (0 : ℝ)..π, Real.exp (β * Real.cos θ) - Real.exp (β * Real.cos θ) * Real.cos θ) := by
          apply intervalIntegral.integral_congr
          intro θ hθ
          ring
      _ = (∫ θ in (0 : ℝ)..π, Real.exp (β * Real.cos θ)) - (∫ θ in (0 : ℝ)..π, Real.exp (β * Real.cos θ) * Real.cos θ) := by
          simpa [Pi.mul_apply] using (intervalIntegral.integral_sub (hcont_exp.intervalIntegrable (μ := MeasureTheory.volume) (0 : ℝ) π) ((hcont_exp.mul Real.continuous_cos).intervalIntegrable (μ := MeasureTheory.volume) (0 : ℝ) π))
      _ = π * besselI 0 β - π * besselI 1 β := by
          rw [show (∫ θ in (0 : ℝ)..π, Real.exp (β * Real.cos θ)) = π * besselI 0 β by
            simpa [Function.comp_def] using integral_exp_cos_eq_besselI0 β]
          rw [show (∫ θ in (0 : ℝ)..π, Real.exp (β * Real.cos θ) * Real.cos θ) = π * besselI 1 β by
            simpa [Function.comp_def] using integral_exp_cos_mul_cos_eq_besselI1 β]
      _ = π * (besselI 0 β - besselI 1 β) := by ring
  have hpos : 0 < (∫ θ in (0 : ℝ)..π, Real.exp (β * Real.cos θ) * (1 - Real.cos θ)) := by
    apply intervalIntegral.integral_pos Real.pi_pos
    · exact ((hcont_exp.mul (continuous_const.sub Real.continuous_cos))).continuousOn
    · intro θ hθ
      have hcos : Real.cos θ ≤ 1 := Real.cos_le_one θ
      have h1 : 0 ≤ 1 - Real.cos θ := by linarith
      exact mul_nonneg (le_of_lt (Real.exp_pos _)) h1
    · refine ⟨(π / 2 : ℝ), ?_, ?_⟩
      · exact ⟨by positivity, by linarith [Real.pi_pos]⟩
      · rw [Real.cos_pi_div_two]
        norm_num
  rw [hdiff] at hpos
  have h : 0 < besselI 0 β - besselI 1 β := (mul_pos_iff_of_pos_left Real.pi_pos).mp hpos
  exact lt_of_sub_pos h

/-- **The derivative of the barrier** `w = βI₁ − (β−1)I₀`: from `I₀′=I₁`, `I₁′=I₀−I₁/β`, the product
rule gives `w′ = (β−1)(I₀ − I₁)`, positive for β>1 since `I₀ > I₁`. The FTC input for `w > 0`. -/
theorem barrier_hasDerivAt (β : ℝ) (hβ : β ≠ 0) :
    HasDerivAt (fun x : ℝ => x * besselI 1 x - (x - 1) * besselI 0 x)
      ((β - 1) * (besselI 0 β - besselI 1 β)) β := by
  have hd0 : HasDerivAt (fun x : ℝ => besselI 0 x) (besselI 1 β) β := besselI0_hasDerivAt β
  have hd1 : HasDerivAt (fun x : ℝ => besselI 1 x) (besselI 0 β - besselI 1 β / β) β := besselI1_hasDerivAt β hβ
  have hmul1 : HasDerivAt (fun x : ℝ => x * besselI 1 x) (1 * besselI 1 β + β * (besselI 0 β - besselI 1 β / β)) β :=
    (hasDerivAt_id β).mul hd1
  have hmul0 : HasDerivAt (fun x : ℝ => (x - 1) * besselI 0 x) (1 * besselI 0 β + (β - 1) * besselI 1 β) β :=
    ((hasDerivAt_id β).sub_const 1).mul hd0
  have h := hmul1.sub hmul0
  convert h using 1
  field_simp [hβ]
  ring

/-- **Continuity of `I₀`** from `I₀′=I₁` (`HasDerivAt` ⟹ `ContinuousAt` at every point). -/
theorem besselI0_continuous : Continuous (fun x : ℝ => besselI 0 x) := by
  rw [continuous_iff_continuousAt]
  intro x
  exact (besselI0_hasDerivAt x).continuousAt

/-- **Continuity of `I₁` on `[1, ∞)`** from `I₁′=I₀−I₁/x` (x ≠ 0 on [1,∞)). -/
theorem besselI1_continuousOn_Ici_one : ContinuousOn (fun x : ℝ => besselI 1 x) (Set.Ici (1 : ℝ)) := by
  intro x hx
  have hx0 : x ≠ 0 := ne_of_gt (lt_of_lt_of_le zero_lt_one (Set.mem_Ici.mp hx))
  exact (besselI1_hasDerivAt x hx0).continuousAt.continuousWithinAt

/-- **The barrier positivity**: `w = βI₁ − (β−1)I₀ > 0` for β > 1. From `w′=(β−1)(I₀−I₁)>0` on
(1,∞) and `w` continuous, `w` is strictly increasing on [1,∞), so `w(β) > w(1) = I₁(1) > 0`. -/
theorem barrier_pos {β : ℝ} (hβ : 1 < β) :
    0 < β * besselI 1 β - (β - 1) * besselI 0 β := by
  let w : ℝ → ℝ := fun x => x * besselI 1 x - (x - 1) * besselI 0 x
  have hmono : StrictMonoOn w (Set.Ici (1 : ℝ)) := by
    apply strictMonoOn_of_deriv_pos (convex_Ici (1 : ℝ))
    · have hc1 : ContinuousOn (fun x : ℝ => x * besselI 1 x) (Set.Ici (1 : ℝ)) :=
        continuousOn_id.mul besselI1_continuousOn_Ici_one
      have hc0 : ContinuousOn (fun x : ℝ => (x - 1) * besselI 0 x) (Set.Ici (1 : ℝ)) :=
        (continuousOn_id.sub continuousOn_const).mul besselI0_continuous.continuousOn
      exact hc1.sub hc0
    · intro x hx
      rw [interior_Ici] at hx
      have hx1 : 1 < x := Set.mem_Ioi.mp hx
      have hx0 : x ≠ 0 := ne_of_gt (lt_trans zero_lt_one hx1)
      have hderiv := barrier_hasDerivAt x hx0
      have hd : deriv w x = (x - 1) * (besselI 0 x - besselI 1 x) := hderiv.deriv
      rw [hd]
      exact mul_pos (sub_pos.mpr hx1) (sub_pos.mpr (besselI1_lt_besselI0 (lt_trans zero_lt_one hx1)))
  have hw1 : 0 < w 1 := by
    dsimp [w]
    have hI1 : 0 < besselI 1 (1 : ℝ) := besselI_pos (by norm_num : (0 : ℝ) < 1)
    simpa using hI1
  have hw : w 1 < w β := hmono (by norm_num : (1 : ℝ) ∈ Set.Ici (1 : ℝ)) (le_of_lt hβ) hβ
  dsimp [w] at hw
  have hβI1 : 0 < β * besselI 1 β - (β - 1) * besselI 0 β := lt_trans hw1 hw
  exact hβI1

/-- **The concentration bound**: `1 − I₁/I₀ ≤ 1/β` for all β > 0. For β ≤ 1 the activity is ≤ 1 ≤ 1/β;
for β > 1 the barrier `βI₁ − (β−1)I₀ > 0` gives `I₁/I₀ > (β−1)/β = 1 − 1/β`. This is the ym-bakry-ceiling
antipode-suppression bound — the Clay step, now closed. -/
theorem bessel_activity_le_one_div_beta {β : ℝ} (hβ : 0 < β) :
    1 - besselI 1 β / besselI 0 β ≤ 1 / β := by
  by_cases hβle : β ≤ 1
  · have hI0 : 0 < besselI 0 β := besselI_pos hβ
    have hI1 : 0 ≤ besselI 1 β := le_of_lt (besselI_pos hβ)
    have hratio : 0 ≤ besselI 1 β / besselI 0 β := div_nonneg hI1 (le_of_lt hI0)
    have hle1 : 1 - besselI 1 β / besselI 0 β ≤ 1 := by linarith
    have hle2 : (1 : ℝ) ≤ 1 / β := (one_le_div hβ).mpr hβle
    exact le_trans hle1 hle2
  · have hβ1 : 1 < β := lt_of_not_ge hβle
    have hbar := barrier_pos hβ1
    have hI0 : 0 < besselI 0 β := besselI_pos hβ
    have h : 1 - besselI 1 β / besselI 0 β < 1 / β := by
      field_simp [ne_of_gt hI0, ne_of_gt hβ]
      nlinarith [hbar]
    exact le_of_lt h

/-- **The full SU(2) plaquette concentration**: `E[z] = 1 − I₂/I₁ < 2/β` for all β > 0. The mean
`(1/2)Tr U = I₂/I₁` under the SU(2) Haar measure (`sin²(θ/2) dθ`), and `I₁ − I₂ = (I₁−I₀) + (2/β)I₁ <
(2/β)I₁` by the recurrence `I₀−I₂=(2/β)I₁` and the order `I₁<I₀`. This is the actual 4D cluster-expansion
input — the diagonal-torus concentration lifted to the SU(2) character. -/
theorem bessel_ratio_I2_I1_lt_two_div_beta {β : ℝ} (hβ : 0 < β) :
    1 - besselI 2 β / besselI 1 β < 2 / β := by
  have hrec : besselI 0 β - besselI 2 β = (2 / β) * besselI 1 β := bessel_recurrence hβ
  have horder : besselI 1 β < besselI 0 β := besselI1_lt_besselI0 hβ
  have hI1 : 0 < besselI 1 β := besselI_pos hβ
  have hdiff : besselI 1 β - besselI 2 β < 2 * besselI 1 β / β := by
    have h1 : besselI 1 β - besselI 2 β = (besselI 1 β - besselI 0 β) + (besselI 0 β - besselI 2 β) := by ring
    rw [h1, hrec]
    have h2 : besselI 1 β - besselI 0 β < 0 := sub_neg.mpr horder
    have h3 : (besselI 1 β - besselI 0 β) + (2 / β) * besselI 1 β < (2 / β) * besselI 1 β := by linarith
    simpa [div_eq_mul_inv, mul_comm, mul_left_comm, mul_assoc] using h3
  have hdiv : (besselI 1 β - besselI 2 β) / besselI 1 β < 2 / β := by
    rw [div_lt_iff₀ hI1]
    simpa [div_eq_mul_inv, mul_comm, mul_left_comm, mul_assoc] using hdiff
  have hmain : 1 - besselI 2 β / besselI 1 β = (besselI 1 β - besselI 2 β) / besselI 1 β := by
    field_simp [ne_of_gt hI1]
  rw [hmain]
  exact hdiv

end QM

/-- **No-crossing barrier**: a continuous `f` with `f 0 = 0` and `deriv f x < 0` whenever `f x ≥ 0`
stays `≤ 0` on `[0,∞)`. Proof: if `f x₀ > 0`, the closed set `S = {y ∈ [0,x₀] : f y = 0}` is nonempty
and compact, so it has a maximum `c`; on `(c,x₀)` we have `f > 0` (else the IVT gives a larger zero),
so the barrier gives `deriv f < 0` there, and `strictAntiOn_of_deriv_neg` forces `f x₀ < f c = 0`. -/
theorem no_crossing_barrier {f : ℝ → ℝ} (hf_cont : Continuous f)
    (hf_deriv : ∀ x, 0 < x → HasDerivAt f (deriv f x) x)
    (hsign : ∀ x, 0 < x → 0 ≤ f x → deriv f x < 0)
    (hf0 : f 0 = 0) : ∀ x, 0 ≤ x → f x ≤ 0 := by
  intro x₀ hx₀
  by_contra h
  have hpos : 0 < f x₀ := lt_of_not_ge h
  have hxpos : 0 < x₀ := by
    by_contra hz
    have : x₀ = 0 := by linarith
    subst x₀
    rw [hf0] at hpos
    linarith
  let S : Set ℝ := {y : ℝ | y ∈ Set.Icc 0 x₀ ∧ f y = 0}
  have hS_closed : IsClosed S := by
    have hz : IsClosed ({y : ℝ | f y = 0}) := isClosed_singleton.preimage hf_cont
    exact (isClosed_Icc (a := (0 : ℝ)) (b := x₀)).inter hz
  have hS_compact : IsCompact S := isCompact_Icc.of_isClosed_subset hS_closed (by
    intro y hy
    exact hy.1)
  have hS_ne : S.Nonempty := ⟨0, by
    constructor
    · exact ⟨le_rfl, hx₀⟩
    · exact hf0⟩
  rcases hS_compact.exists_isMaxOn hS_ne (f := fun y : ℝ => y) continuous_id.continuousOn with ⟨c, hcS, hcmax⟩
  have hfc : f c = 0 := hcS.2
  have hc0 : 0 ≤ c := (Set.mem_Icc.mp hcS.1).1
  have hcx : c ≤ x₀ := (Set.mem_Icc.mp hcS.1).2
  have hc_lt_x : c < x₀ := by
    by_contra h
    have : x₀ = c := by linarith
    subst x₀
    rw [hfc] at hpos
    linarith
  have hfpos : ∀ y ∈ Set.Ioo c x₀, 0 < f y := by
    intro y hy
    have hyc : c < y := (Set.mem_Ioo.mp hy).1
    have hyx : y < x₀ := (Set.mem_Ioo.mp hy).2
    by_contra hneg
    have hle : f y ≤ 0 := le_of_not_gt hneg
    by_cases hy0 : f y = 0
    · have yS : y ∈ S := by
        refine ⟨?_, hy0⟩
        exact ⟨le_trans hc0 (le_of_lt hyc), le_of_lt hyx⟩
      have hyle : y ≤ c := hcmax yS
      linarith
    · have hneg' : f y < 0 := lt_of_le_of_ne hle hy0
      have hcont : ContinuousOn f (Set.Icc y x₀) := hf_cont.continuousOn.mono (Set.subset_univ _)
      have hivt := intermediate_value_Icc (le_of_lt hyx) hcont
      have h0mem : (0 : ℝ) ∈ Set.Icc (f y) (f x₀) := ⟨le_of_lt hneg', le_of_lt hpos⟩
      rcases hivt h0mem with ⟨z, hzIcc, hz0⟩
      have hz_gt_c : c < z := lt_of_lt_of_le hyc hzIcc.1
      have hzS : z ∈ S := by
        refine ⟨?_, hz0⟩
        exact ⟨le_trans hc0 (le_of_lt hz_gt_c), hzIcc.2⟩
      have hz_le_c : z ≤ c := hcmax hzS
      linarith
  have hanti : StrictAntiOn f (Set.Icc c x₀) := by
    refine strictAntiOn_of_deriv_neg (convex_Icc c x₀) (hf_cont.continuousOn) ?_
    intro y hy
    rw [interior_Icc] at hy
    exact hsign y (lt_of_le_of_lt hc0 hy.1) (le_of_lt (hfpos y hy))
  have hlt : f x₀ < f c := hanti ⟨le_rfl, hcx⟩ ⟨hcx, le_rfl⟩ hc_lt_x
  rw [hfc] at hlt
  linarith

namespace QM

/-- `I₀(0) = 1` — the only surviving term of the series is `k = 0`. -/
theorem besselI_zero_zero : besselI 0 0 = 1 := by
  dsimp [besselI]
  rw [tsum_eq_single 0]
  · norm_num
  · intro b hb
    have hb2 : 2 * b ≠ 0 := by omega
    simp [hb2]

/-- `I₁(0) = 0` — every term of the series has a positive power of `x`, so it vanishes at `0`. -/
theorem besselI_one_zero : besselI 1 0 = 0 := by
  dsimp [besselI]
  rw [tsum_eq_single 0]
  · norm_num
  · intro b hb
    have hb1 : 2 * b + 1 ≠ 0 := by omega
    simp [hb1]

/-- `I₁` is continuous on every `[0,b]` (`b ≥ 0`) — the Bessel series converges locally uniformly,
with the `k`-th term bounded by `(b/2)^(2k+1)/(k!(k+1)!)` (summable by `besselI_summable_of_nonneg`). -/
theorem besselI1_continuousOn_Icc (b : ℝ) (hb : 0 ≤ b) :
    ContinuousOn (fun x => besselI 1 x) (Set.Icc 0 b) := by
  let f : ℕ → ℝ → ℝ := fun k x => (x / 2) ^ (2 * k + 1) / ((k.factorial : ℝ) * (k + 1).factorial)
  have htsum : ContinuousOn (fun x => ∑' k, f k x) (Set.Icc 0 b) :=
    continuousOn_tsum
      (fun k => (by fun_prop : ContinuousOn (f k) (Set.Icc 0 b)))
      (besselI_summable_of_nonneg 1 hb)
      (by
        intro k x hx
        have hx0 : 0 ≤ x := hx.1
        have hxb : x ≤ b := hx.2
        have hx2 : 0 ≤ x / 2 := div_nonneg hx0 (by norm_num)
        have hx2b : x / 2 ≤ b / 2 := div_le_div_of_nonneg_right hxb (by norm_num)
        have hpow : (x / 2) ^ (2 * k + 1) ≤ (b / 2) ^ (2 * k + 1) :=
          pow_le_pow_left₀ hx2 hx2b (2 * k + 1)
        dsimp [f]
        rw [abs_of_nonneg (div_nonneg (pow_nonneg hx2 _) (mul_nonneg (Nat.cast_nonneg _) (Nat.cast_nonneg _)))]
        exact div_le_div_of_nonneg_right hpow (mul_nonneg (Nat.cast_nonneg _) (Nat.cast_nonneg _)))
  simpa [f, besselI] using htsum

/-- **The Amos sign analysis** (algebraic core of the barrier): if `r` satisfies the Riccati
`r′ = 1 − r² − r/x` and the barrier `f = (x+1/2)·r − x ≥ 0` (i.e. `r ≥ x/(x+1/2)`), then the derivative
`f′ = r + (x+1/2)·r′ − 1` is strictly negative. Indeed `f′ = (x−1/2) − r/(2x) − (x+1/2)·r²` is strictly
decreasing in `r`, and at the boundary `r = x/(x+1/2)` it equals `−3/(2(2x+1)) < 0`. -/
theorem amos_sign {x r r' : ℝ} (hx : 0 < x) (hr : 0 < r)
    (hriccati : r' = 1 - r ^ 2 - r / x) (hf : 0 ≤ (x + 1 / 2) * r - x) :
    r + (x + 1 / 2) * r' - 1 < 0 := by
  have hx2 : 0 < x + 1 / 2 := by nlinarith
  have hrle : x / (x + 1 / 2) ≤ r := by
    exact (div_le_iff₀ hx2).mpr (by nlinarith [hf])
  have hderiv : r + (x + 1 / 2) * r' - 1 = (x - 1 / 2) - r / (2 * x) - (x + 1 / 2) * r ^ 2 := by
    rw [hriccati]
    field_simp [ne_of_gt hx]
    ring
  have hdec : (x - 1 / 2) - r / (2 * x) - (x + 1 / 2) * r ^ 2
      ≤ (x - 1 / 2) - (x / (x + 1 / 2)) / (2 * x) - (x + 1 / 2) * (x / (x + 1 / 2)) ^ 2 := by
    have h1 : (x / (x + 1 / 2)) / (2 * x) ≤ r / (2 * x) := by
      exact div_le_div_of_nonneg_right hrle (by positivity : 0 ≤ 2 * x)
    have h2 : (x + 1 / 2) * (x / (x + 1 / 2)) ^ 2 ≤ (x + 1 / 2) * r ^ 2 := by
      have hrnonneg : 0 ≤ r := le_of_lt hr
      have hxr : 0 ≤ x / (x + 1 / 2) := div_nonneg (le_of_lt hx) (le_of_lt hx2)
      have hsq : (x / (x + 1 / 2)) ^ 2 ≤ r ^ 2 := by
        exact sq_le_sq.mpr (by rw [abs_of_nonneg hxr, abs_of_nonneg hrnonneg]; exact hrle)
      exact mul_le_mul_of_nonneg_left hsq (by nlinarith)
    nlinarith
  rw [hderiv]
  have hbound : (x - 1 / 2) - (x / (x + 1 / 2)) / (2 * x) - (x + 1 / 2) * (x / (x + 1 / 2)) ^ 2 < 0 := by
    field_simp [ne_of_gt hx, ne_of_gt hx2]
    nlinarith [hx]
  nlinarith

/-- `I₁` is continuous on every symmetric `[−b,b]` (`b ≥ 0`) — the Bessel series converges locally
uniformly, bounded by `(b/2)^(2k+1)/(k!(k+1)!)` on `[−b,b]`. -/
theorem besselI1_continuousOn_symm (b : ℝ) (hb : 0 ≤ b) :
    ContinuousOn (fun x => besselI 1 x) (Set.Icc (-b) b) := by
  let f : ℕ → ℝ → ℝ := fun k x => (x / 2) ^ (2 * k + 1) / ((k.factorial : ℝ) * (k + 1).factorial)
  have htsum : ContinuousOn (fun x => ∑' k, f k x) (Set.Icc (-b) b) :=
    continuousOn_tsum
      (fun k => (by fun_prop : ContinuousOn (f k) (Set.Icc (-b) b)))
      (besselI_summable_of_nonneg 1 hb)
      (by
        intro k x hx
        have hxle : |x| ≤ b := abs_le.mpr ⟨(Set.mem_Icc.mp hx).1, (Set.mem_Icc.mp hx).2⟩
        have hx2 : |x / 2| ≤ b / 2 := by
          rw [abs_div, abs_of_nonneg (by norm_num : 0 ≤ (2 : ℝ))]
          exact div_le_div_of_nonneg_right hxle (by norm_num)
        have hpow : |(x / 2) ^ (2 * k + 1)| ≤ (b / 2) ^ (2 * k + 1) := by
          rw [abs_pow]
          exact pow_le_pow_left₀ (abs_nonneg _) hx2 (2 * k + 1)
        dsimp [f]
        rw [abs_div]
        rw [abs_of_nonneg (by positivity : 0 ≤ (k.factorial : ℝ) * ((k + 1).factorial : ℝ))]
        exact div_le_div_of_nonneg_right hpow (by positivity : 0 ≤ (k.factorial : ℝ) * ((k + 1).factorial : ℝ)))
  simpa [f, besselI] using htsum

/-- `I₁` is continuous on all of ℝ — `besselI1_hasDerivAt` away from 0, and continuity at 0 from the
symmetric-interval bound. -/
theorem besselI1_continuous : Continuous (fun x => besselI 1 x) := by
  rw [continuous_iff_continuousAt]
  intro x
  by_cases hx0 : x = 0
  · subst x
    exact (besselI1_continuousOn_symm 1 (by norm_num)).continuousAt
      (Icc_mem_nhds (by norm_num : (-1 : ℝ) < 0) (by norm_num : (0 : ℝ) < 1))
  · exact (besselI1_hasDerivAt x hx0).continuousAt

/-- `I₀(x) > 0` for all `x` — positive for `x > 0`, equals 1 at 0, even for `x < 0`. -/
theorem besselI0_pos_all (x : ℝ) : 0 < besselI 0 x := by
  by_cases hx0 : x = 0
  · subst x
    rw [besselI_zero_zero]
    norm_num
  · have hx : 0 < |x| := abs_pos.mpr hx0
    have heven : besselI 0 x = besselI 0 (|x|) := by
      dsimp [besselI]
      congr 1
      funext k
      have h : (x / 2) ^ (2 * k) = (|x| / 2) ^ (2 * k) := by
        rw [pow_mul (x / 2) 2 k, pow_mul (|x| / 2) 2 k]
        congr 1
        rw [div_pow, div_pow, sq_abs]
      simpa [h]
    rw [heven]
    exact besselI_pos hx

/-- `r = I₁/I₀` is continuous on all ℝ. -/
theorem bessel_ratio_continuous : Continuous (fun x => besselI 1 x / besselI 0 x) := by
  exact besselI1_continuous.div besselI0_continuous (fun x => ne_of_gt (besselI0_pos_all x))

/-- `r(0) = I₁(0)/I₀(0) = 0/1 = 0`. -/
theorem bessel_ratio_zero : besselI 1 0 / besselI 0 0 = 0 := by
  rw [besselI_one_zero, besselI_zero_zero]
  norm_num

/-- **The Amos bound**: `I₁(x)/I₀(x) ≤ x/(x+1/2)` for `x ≥ 0`. The Riccati `r′ = 1 − r/x − r²` and the
no-crossing barrier `f(t) = (t+1/2)·r(t) − t` (with `f(0) = 0` and `f ≥ 0 ⟹ f′ < 0` by `amos_sign`). -/
theorem besselI_one_div_besselI_zero_le_x_div_x_add_half (x : ℝ) (hx : 0 ≤ x) :
    besselI 1 x / besselI 0 x ≤ x / (x + 1 / 2) := by
  let f : ℝ → ℝ := fun t => (t + 1 / 2) * (besselI 1 t / besselI 0 t) - t
  have hf0 : f 0 = 0 := by
    dsimp [f]
    rw [bessel_ratio_zero]
    norm_num
  have hf_cont : Continuous f := by
    dsimp [f]
    exact ((continuous_id.add continuous_const).mul bessel_ratio_continuous).sub continuous_id
  have hf_deriv_explicit : ∀ t, 0 < t → HasDerivAt f
      (besselI 1 t / besselI 0 t + (t + 1 / 2) * (1 - (besselI 1 t / besselI 0 t) / t - (besselI 1 t / besselI 0 t) ^ 2) - 1) t := by
    intro t ht
    dsimp [f]
    have hlin : HasDerivAt (fun s : ℝ => s + 1 / 2) 1 t := (hasDerivAt_id t).add_const (1 / 2 : ℝ)
    have hmul := hlin.mul (bessel_ratio_hasDerivAt t ht)
    have hsub := hmul.sub (hasDerivAt_id t)
    change HasDerivAt f (1 * (besselI 1 t / besselI 0 t) + (t + 1 / 2) * (1 - (besselI 1 t / besselI 0 t) / t - (besselI 1 t / besselI 0 t) ^ 2) - 1) t at hsub
    convert hsub using 1
    ring_nf
  have hf_deriv : ∀ t, 0 < t → HasDerivAt f (deriv f t) t := fun t ht => (hf_deriv_explicit t ht).congr_deriv (hf_deriv_explicit t ht).deriv.symm
  have hsign : ∀ t, 0 < t → 0 ≤ f t → deriv f t < 0 := by
    intro t ht hf_nonneg
    have hrpos : 0 < besselI 1 t / besselI 0 t := div_pos (besselI_pos ht) (besselI0_pos_all t)
    have hdf : deriv f t = besselI 1 t / besselI 0 t + (t + 1 / 2) * (1 - (besselI 1 t / besselI 0 t) / t - (besselI 1 t / besselI 0 t) ^ 2) - 1 :=
      (hf_deriv_explicit t ht).deriv
    have hsign' := amos_sign (x := t) (r := besselI 1 t / besselI 0 t)
      (r' := 1 - (besselI 1 t / besselI 0 t) / t - (besselI 1 t / besselI 0 t) ^ 2)
      ht hrpos (by ring) (by simpa [f] using hf_nonneg)
    rwa [hdf]
  have hbar : ∀ t, 0 ≤ t → f t ≤ 0 :=
    no_crossing_barrier hf_cont hf_deriv hsign hf0
  have hfx : f x ≤ 0 := hbar x hx
  dsimp [f] at hfx
  have hx2 : 0 < x + 1 / 2 := by nlinarith [hx]
  have : (x + 1 / 2) * (besselI 1 x / besselI 0 x) ≤ x := by nlinarith [hfx]
  exact (le_div_iff₀ hx2).2 (by simpa [mul_comm] using this)

/-- **The sharp polynomial bound**: `heatKernelMassGap β = 1 − I₁(2β)/I₀(2β) ≥ 1/(4β+1)` — the Amos
bound `I₁/I₀ ≤ x/(x+1/2)` at `x = 2β` gives `I₁(2β)/I₀(2β) ≤ 2β/(2β+1/2)`, hence the gap is at least
`1 − 2β/(2β+1/2) = 1/(4β+1)`. -/
theorem heat_kernel_gap_poly (β : ℝ) (hβ : 0 < β) :
    1 / (4 * β + 1) ≤ heatKernelMassGap β := by
  have hx : 0 ≤ 2 * β := by positivity
  have hamos := besselI_one_div_besselI_zero_le_x_div_x_add_half (2 * β) hx
  have hx2 : 0 < 2 * β + 1 / 2 := by positivity
  have hbound : besselI 1 (2 * β) / besselI 0 (2 * β) ≤ (2 * β) / (2 * β + 1 / 2) := by
    simpa using hamos
  have hsub : 1 - (2 * β) / (2 * β + 1 / 2) = 1 / (4 * β + 1) := by
    field_simp [ne_of_gt hx2]
    ring
  dsimp [heatKernelMassGap]
  rw [← hsub]
  exact sub_le_sub_left hbound 1

/-- **The sharp coefficient `A = 1/2`**: `heatKernelMassGap β ≥ (1/2)·e^(−(12π²/11)β)` — the sharp
polynomial bound `1/(4β+1) ≤ gap` combined with `poly_beats_exp` (`(1/2)e^(−cβ) ≤ 1/(4β+1)`). This
upgrades the mass-gap coefficient from `1/2−1/π` to the sharp `1/2`. -/
theorem heat_kernel_gap_sharp (β : ℝ) (hβ : 0 < β) :
    (1 / 2) * Real.exp (-(12 * Real.pi ^ 2 / 11) * β) ≤ heatKernelMassGap β := by
  exact le_trans (poly_beats_exp β hβ) (heat_kernel_gap_poly β hβ)

/-- **The transfer-matrix decay is summable**: `λ₁ = I₁(2β)/I₀(2β) < 1` (the spectral gap
`heat_kernel_spectral_gap` gives `0 < 1 − λ₁`), so the geometric series `Σₙ λ₁ⁿ` converges — the
foundation for the connected correlation's thermodynamic-limit convergence (the double sum
`Σᵢⱼ χᵢχⱼ (T^|i−j|)ᵢⱼ` is controlled by the geometric tail). -/
theorem transfer_matrix_power_summable (β : ℝ) (hβ : 0 < β) :
    Summable (fun n : ℕ => (besselI 1 (2 * β) / besselI 0 (2 * β)) ^ n) := by
  have hgap : 0 < 1 - besselI 1 (2 * β) / besselI 0 (2 * β) := heat_kernel_spectral_gap β hβ
  have hlam_lt_one : besselI 1 (2 * β) / besselI 0 (2 * β) < 1 := by nlinarith [hgap]
  have hlam_nonneg : 0 ≤ besselI 1 (2 * β) / besselI 0 (2 * β) :=
    div_nonneg (besselI_nonneg (by positivity : 0 ≤ 2 * β)) (le_of_lt (besselI_pos (by positivity : 0 < 2 * β)))
  have hnorm : |besselI 1 (2 * β) / besselI 0 (2 * β)| < 1 := by
    rw [abs_of_nonneg hlam_nonneg]
    exact hlam_lt_one
  exact summable_geometric_of_norm_lt_one hnorm

/-- **The SU(2) log mass gap is positive**: `c = −log(I₁(2β)/I₀(2β)) > 0` — the concrete `c` in the
cluster-expansion convergence `mayer_series_converges`. Equivalent to the spectral gap `0 < 1 − I₁/I₀`
(`heat_kernel_spectral_gap`) via `log λ₁ < 0 ⟺ λ₁ < 1` for `λ₁ ∈ (0,1)`. This is the concrete activity-decay
rate `exp(−c·n)` for the SU(2) cluster weights. -/
theorem su2_log_gap_pos (β : ℝ) (hβ : 0 < β) :
    0 < -Real.log (besselI 1 (2 * β) / besselI 0 (2 * β)) := by
  have hgap : 0 < 1 - besselI 1 (2 * β) / besselI 0 (2 * β) := heat_kernel_spectral_gap β hβ
  have hlam_lt_one : besselI 1 (2 * β) / besselI 0 (2 * β) < 1 := by nlinarith [hgap]
  have hlam_pos : 0 < besselI 1 (2 * β) / besselI 0 (2 * β) :=
    div_pos (besselI_pos (by positivity : 0 < 2 * β)) (besselI_pos (by positivity : 0 < 2 * β))
  exact neg_pos.mpr (Real.log_neg hlam_pos hlam_lt_one)

/-- **The SU(2) cluster/Mayer series converges**: any activity `φ` bounded by the transfer-matrix decay
`|φ n| ≤ λ₁ⁿ` with `λ₁ = I₁(2β)/I₀(2β) < 1` (the proved mass gap) is summable, so the partial sums
`Σ_{n<V} φ n` tend to the infinite sum as `V → ∞`. This is the concrete SU(2) infinite-volume convergence of
the cluster expansion, tying the proved spectral gap to the Mayer/polymer expansion. -/
theorem su2_mayer_series_converges (β : ℝ) (hβ : 0 < β) (activity : ℕ → ℝ)
    (hφ : ∀ n : ℕ, |activity n| ≤ (besselI 1 (2 * β) / besselI 0 (2 * β))^n) :
    ∃ S : ℝ, Filter.Tendsto (fun V : ℕ => (Finset.range V).sum (fun n => activity n)) Filter.atTop (𝓝 S) := by
  have hsum : Summable activity := by
    exact Summable.of_norm_bounded (g := fun n : ℕ => (besselI 1 (2 * β) / besselI 0 (2 * β))^n)
      (summable_geometric_of_norm_lt_one (by
        have hgap : 0 < 1 - besselI 1 (2 * β) / besselI 0 (2 * β) := heat_kernel_spectral_gap β hβ
        have hlam_lt_one : besselI 1 (2 * β) / besselI 0 (2 * β) < 1 := by nlinarith [hgap]
        have hlam_nonneg : 0 ≤ besselI 1 (2 * β) / besselI 0 (2 * β) :=
          div_nonneg (besselI_nonneg (by positivity : 0 ≤ 2 * β)) (le_of_lt (besselI_pos (by positivity : 0 < 2 * β)))
        rw [Real.norm_eq_abs, abs_of_nonneg hlam_nonneg]
        exact hlam_lt_one))
      (fun n => by simpa [Real.norm_eq_abs] using hφ n)
  exact ⟨∑' n, activity n, hsum.hasSum.tendsto_sum_nat⟩

/-- **The bare lattice gap vanishes in the continuum limit**: `1 − I₁(2β)/I₀(2β) → 0` as `β → ∞`.
This is the expected physics — the *bare* lattice gap is not the physical mass; the physical mass is the
RG-invariant scale (the 't Hooft cutoff-independence), a *different* scale from the bare gap. Squeeze:
`0 ≤ heatKernelMassGap β ≤ (1/2)/β` (via `heat_kernel_spectral_gap` and `bessel_activity_le_one_div_beta (2β)`),
and both bounds tend to 0. -/
theorem heat_kernel_gap_tendsto_zero :
    Filter.Tendsto (fun β : ℝ => heatKernelMassGap β) Filter.atTop (nhds 0) := by
  refine tendsto_of_tendsto_of_tendsto_of_le_of_le' tendsto_const_nhds ?_ ?_ ?_
  · simpa using (tendsto_inv_atTop_zero.const_mul (1 / 2 : ℝ))
  · filter_upwards [eventually_atTop.mpr ⟨1, by intro β hβ; linarith⟩] with β hβ
    exact le_of_lt (heat_kernel_spectral_gap β hβ)
  · filter_upwards [eventually_atTop.mpr ⟨1, by intro β hβ; linarith⟩] with β hβ
    calc
      heatKernelMassGap β ≤ 1 / (2 * β) := by
        simpa [heatKernelMassGap] using bessel_activity_le_one_div_beta (2 * β) (by positivity : 0 < 2 * β)
      _ = (1 / 2) / β := by field_simp [hβ.ne']

/-- **The naive scale-matching ratio grows exponentially**: the bare lattice gap divided by the
running-coupling scale `e^(−cβ)` is bounded below by `e^(cβ)/(4β+1)` (via `heat_kernel_gap_poly`
`1/(4β+1) ≤ gap`). So the ratio is **not** the constant the `tHooftRenormalizable` placeholder demands —
the bare gap and the running-coupling scale live on *different* scales, and the physical mass must come
from the correct RG scale-matching, not from `gap / e^(−cβ)`. -/
theorem naive_scale_ratio_lower_bound (β c : ℝ) (hc : 0 < c) (hβ : 0 < β) :
    Real.exp (c * β) / (4 * β + 1) ≤ heatKernelMassGap β / Real.exp (-(c * β)) := by
  have hpoly : 1 / (4 * β + 1) ≤ heatKernelMassGap β := heat_kernel_gap_poly β hβ
  have hle : (1 / (4 * β + 1)) / Real.exp (-(c * β)) ≤ heatKernelMassGap β / Real.exp (-(c * β)) :=
    div_le_div_of_nonneg_left hpoly (Real.exp_pos _).le
  have hid : (1 / (4 * β + 1)) / Real.exp (-(c * β)) = Real.exp (c * β) / (4 * β + 1) := by
    rw [div_eq_mul_inv, div_eq_mul_inv]
    rw [Real.exp_neg]
    field_simp [Real.exp_pos (c * β).ne']
  rwa [← hid]

/-- **The correct scale-matching: the physical mass `β·(1 − I₁/I₀)` is finite and positive.** In the
correct scale `1/β` (the inverse coupling, NOT the running-coupling `e^(−cβ)`), the rescaled mass is
bounded `1/5 ≤ β·heatKernelMassGap β ≤ 1/2` for `β ≥ 1`. This is the honest content of the 't Hooft
cutoff-independence: the physical mass lives on the `1/β` scale (where it is bounded away from 0 and ∞),
not on the bare `1 − I₁/I₀` (which → 0) nor the naive `e^(−cβ)` (which → ∞). -/
theorem physical_mass_scale_bounds (β : ℝ) (hβ : 1 ≤ β) :
    1 / 5 ≤ β * heatKernelMassGap β ∧ β * heatKernelMassGap β ≤ 1 / 2 := by
  constructor
  · have hpoly : 1 / (4 * β + 1) ≤ heatKernelMassGap β := heat_kernel_gap_poly β (by linarith)
    have hmul : β * (1 / (4 * β + 1)) ≤ β * heatKernelMassGap β :=
      mul_le_mul_of_nonneg_left hpoly (by linarith)
    have hlow : 1 / 5 ≤ β * (1 / (4 * β + 1)) := by
      field_simp [by linarith : 4 * β + 1 ≠ 0]
      nlinarith [hβ]
    exact le_trans hlow hmul
  · have hupper : heatKernelMassGap β ≤ 1 / (2 * β) := by
      simpa [heatKernelMassGap] using bessel_activity_le_one_div_beta (2 * β) (by positivity)
    have hmul : β * heatKernelMassGap β ≤ β * (1 / (2 * β)) :=
      mul_le_mul_of_nonneg_left hupper (by linarith)
    have hup : β * (1 / (2 * β)) ≤ 1 / 2 := by
      field_simp [by linarith : β ≠ 0]
      linarith
    exact le_trans hmul hup

/-- **The physical-mass lower bound converges to `1/4`**: `β/(4β+1) → 1/4` as `β → ∞`. Combined with
`physical_mass_scale_bounds` (`β/(4β+1) ≤ β·heatKernelMassGap β`), this shows the physical mass is at least
`1/4` in the limit — the sharp value the 't Hooft cutoff-independence predicts for `β·(1 − I₁/I₀)`. -/
theorem physical_mass_lower_bound_tendsto :
    Filter.Tendsto (fun β : ℝ => β / (4 * β + 1)) Filter.atTop (nhds (1 / 4 : ℝ)) := by
  have hrewrite : (fun β : ℝ => β / (4 * β + 1)) = (fun β => (4 + β⁻¹)⁻¹) := by
    funext β
    field_simp [by nlinarith : (4 * β + 1 : ℝ) ≠ 0]
    ring
  rw [hrewrite]
  have h1 : Filter.Tendsto (fun β : ℝ => 4 + β⁻¹) Filter.atTop (nhds (4 : ℝ)) :=
    tendsto_const_nhds.add tendsto_inv_atTop_zero
  exact (continuousAt_inv₀ (by norm_num : (4 : ℝ) ≠ 0)).tendsto.comp h1

/-- **The lower-barrier sign**: for `g = x − (x+3)·r`, the derivative `g′ = 1 − r − (x+3)r′` is negative
on `g ≥ 0` (`r ≤ x/(x+3)`). The Riccati gives `g′ = −x − 2 − r + (x+3)r² + (x+3)r/x`, increasing in `r`, with
value `−(5x+3)/(x+3) < 0` at the boundary `r = x/(x+3)`. -/
theorem bessel_ratio_lower_sign {x r r' : ℝ} (hx : 0 < x) (hr : 0 < r)
    (hriccati : r' = 1 - r ^ 2 - r / x) (hg : 0 ≤ x - (x + 3) * r) :
    1 - r - (x + 3) * r' < 0 := by
  have hx3 : 0 < x + 3 := by nlinarith
  have hrle : r ≤ x / (x + 3) := by
    exact (div_le_iff₀ hx3).mp (by nlinarith [hg])
  have hbound : (x + 3) * r ≤ x := by nlinarith [hrle]
  rw [hriccati]
  ring_nf
  have hb2 : (x + 3) * r ^ 2 ≤ x * r := by
    calc
      (x + 3) * r ^ 2 = r * ((x + 3) * r) := by ring
      _ ≤ r * x := mul_le_mul_of_nonneg_left hbound (le_of_lt hr)
  have hb3 : (x + 3) * r / x ≤ 1 := (div_le_one hx).mpr hbound
  nlinarith [hb2, hb3, hr, hx]

/-- **The lower bound on the Bessel ratio**: `x/(x+3) ≤ I₁(x)/I₀(x)` for `x ≥ 0` — the Riccati no-crossing
with the barrier `x − (x+3)r`. This gives the pointwise seed `s(1) = 1 − I₁(1)/I₀(1) ≤ 3/4` for the sharp
upper-barrier argument. -/
theorem bessel_ratio_ge_x_div_x_add_three (x : ℝ) (hx : 0 ≤ x) :
    x / (x + 3) ≤ besselI 1 x / besselI 0 x := by
  let f : ℝ → ℝ := fun t => t - (t + 3) * (besselI 1 t / besselI 0 t)
  have hf0 : f 0 = 0 := by
    dsimp [f]
    rw [bessel_ratio_zero]
    norm_num
  have hf_cont : Continuous f := by
    dsimp [f]
    exact continuous_id.sub ((continuous_id.add_const (3 : ℝ)).mul bessel_ratio_continuous)
  have hf_deriv_explicit : ∀ t, 0 < t → HasDerivAt f
      (1 - (besselI 1 t / besselI 0 t) - (t + 3) * (1 - (besselI 1 t / besselI 0 t) / t - (besselI 1 t / besselI 0 t) ^ 2)) t := by
    intro t ht
    dsimp [f]
    have hlin : HasDerivAt (fun s : ℝ => s + 3) 1 t := (hasDerivAt_id t).add_const (3 : ℝ)
    have hmul := hlin.mul (bessel_ratio_hasDerivAt t ht)
    have hsub := (hasDerivAt_id t).sub hmul
    change HasDerivAt f (1 - (besselI 1 t / besselI 0 t) - (t + 3) * (1 - (besselI 1 t / besselI 0 t) / t - (besselI 1 t / besselI 0 t) ^ 2)) t at hsub
    convert hsub using 1
    ring_nf
  have hf_deriv : ∀ t, 0 < t → HasDerivAt f (deriv f t) t := fun t ht => (hf_deriv_explicit t ht).congr_deriv (hf_deriv_explicit t ht).deriv.symm
  have hsign : ∀ t, 0 < t → 0 ≤ f t → deriv f t < 0 := by
    intro t ht hf_nonneg
    have hrpos : 0 < besselI 1 t / besselI 0 t := div_pos (besselI_pos ht) (besselI0_pos_all t)
    have hdf : deriv f t = 1 - (besselI 1 t / besselI 0 t) - (t + 3) * (1 - (besselI 1 t / besselI 0 t) / t - (besselI 1 t / besselI 0 t) ^ 2) :=
      (hf_deriv_explicit t ht).deriv
    have hsign' := bessel_ratio_lower_sign (x := t) (r := besselI 1 t / besselI 0 t)
      (r' := 1 - (besselI 1 t / besselI 0 t) / t - (besselI 1 t / besselI 0 t) ^ 2)
      ht hrpos (by ring) (by simpa [f] using hf_nonneg)
    rwa [hdf]
  have hbar : ∀ t, 0 ≤ t → f t ≤ 0 :=
    no_crossing_barrier hf_cont hf_deriv hsign hf0
  have hfx : f x ≤ 0 := hbar x hx
  dsimp [f] at hfx
  have hx3 : 0 < x + 3 := by nlinarith
  have : x ≤ (x + 3) * (besselI 1 x / besselI 0 x) := by nlinarith [hfx]
  exact (le_div_iff₀ hx3).2 (by simpa [mul_comm] using this)

/-- **The restart no-crossing barrier**: same as `no_crossing_barrier` but starting at `a` with the seed
`f a ≤ 0` (not `f 0 = 0`), for barriers that have a pole at `0`. If `f a ≤ 0`, `f` is differentiable on
`(a, ∞)`, and `f ≥ 0 ⟹ deriv f < 0` there, then `f ≤ 0` on `[a, ∞)`. -/
theorem no_crossing_barrier_from {a : ℝ} {f : ℝ → ℝ} (hf_cont : Continuous f)
    (hf_deriv : ∀ x, a < x → HasDerivAt f (deriv f x) x)
    (hsign : ∀ x, a < x → 0 ≤ f x → deriv f x < 0)
    (hfa : f a ≤ 0) : ∀ x, a ≤ x → f x ≤ 0 := by
  intro x₀ hx₀
  by_contra h
  have hpos : 0 < f x₀ := lt_of_not_ge h
  have hax : a < x₀ := by
    by_contra hz
    have : x₀ = a := by linarith
    subst x₀
    linarith [hfa, hpos]
  let S : Set ℝ := {y : ℝ | y ∈ Set.Icc a x₀ ∧ f y = 0}
  have hS_closed : IsClosed S := by
    have hz : IsClosed ({y : ℝ | f y = 0}) := isClosed_singleton.preimage hf_cont
    exact (isClosed_Icc (a := a) (b := x₀)).inter hz
  have hS_compact : IsCompact S := isCompact_Icc.of_isClosed_subset hS_closed (by
    intro y hy
    exact hy.1)
  have hS_ne : S.Nonempty := by
    have hcont_ax : ContinuousOn f (Set.Icc a x₀) := hf_cont.continuousOn.mono (Set.subset_univ _)
    rcases intermediate_value_Icc (le_of_lt hax) hcont_ax ⟨hfa, le_of_lt hpos⟩ with ⟨c, hcIcc, hc0⟩
    exact ⟨c, ⟨hcIcc, hc0⟩⟩
  rcases hS_compact.exists_isMaxOn hS_ne (f := fun y : ℝ => y) continuous_id.continuousOn with ⟨c, hcS, hcmax⟩
  have hfc : f c = 0 := hcS.2
  have hca : a ≤ c := (Set.mem_Icc.mp hcS.1).1
  have hcx : c ≤ x₀ := (Set.mem_Icc.mp hcS.1).2
  have hc_lt_x : c < x₀ := by
    by_contra h
    have : x₀ = c := by linarith
    subst x₀
    rw [hfc] at hpos
    linarith
  have hfpos : ∀ y ∈ Set.Ioo c x₀, 0 < f y := by
    intro y hy
    have hyc : c < y := (Set.mem_Ioo.mp hy).1
    have hyx : y < x₀ := (Set.mem_Ioo.mp hy).2
    by_contra hneg
    have hle : f y ≤ 0 := le_of_not_gt hneg
    by_cases hy0 : f y = 0
    · have yS : y ∈ S := by
        refine ⟨?_, hy0⟩
        exact ⟨le_trans hca (le_of_lt hyc), le_of_lt hyx⟩
      have hyle : y ≤ c := hcmax yS
      linarith
    · have hneg' : f y < 0 := lt_of_le_of_ne hle hy0
      have hcont : ContinuousOn f (Set.Icc y x₀) := hf_cont.continuousOn.mono (Set.subset_univ _)
      have hivt := intermediate_value_Icc (le_of_lt hyx) hcont
      have h0mem : (0 : ℝ) ∈ Set.Icc (f y) (f x₀) := ⟨le_of_lt hneg', le_of_lt hpos⟩
      rcases hivt h0mem with ⟨z, hzIcc, hz0⟩
      have hz_gt_c : c < z := lt_of_lt_of_le hyc hzIcc.1
      have hzS : z ∈ S := by
        refine ⟨?_, hz0⟩
        exact ⟨le_trans hca (le_of_lt hz_gt_c), hzIcc.2⟩
      have hz_le_c : z ≤ c := hcmax hzS
      linarith
  have hanti : StrictAntiOn f (Set.Icc c x₀) := by
    refine strictAntiOn_of_deriv_neg (convex_Icc c x₀) (hf_cont.continuousOn) ?_
    intro y hy
    rw [interior_Icc] at hy
    exact hsign y (lt_of_le_of_lt hca hy.1) (le_of_lt (hfpos y hy))
  have hlt : f x₀ < f c := hanti ⟨le_rfl, hcx⟩ ⟨hcx, le_rfl⟩ hc_lt_x
  rw [hfc] at hlt
  linarith

/-- **The Riccati equation for the reciprocal ratio `Φ = I₀/I₁`**: `Φ′ = 1 + Φ/x − Φ²` (Segura's
difference-differential system, the inverse of the `I₁/I₀` Riccati). This is the equation whose nullcline
`λ⁺ = (1/2 + √(1/4 + x²))/x` gives the sharp lower bound `Φ > λ⁺` (hence `s = 1 − I₁/I₀ ≥ 1 − x/λ⁺`). -/
theorem bessel_ratio_inv_hasDerivAt (x : ℝ) (hx : 0 < x) :
    HasDerivAt (fun t : ℝ => besselI 0 t / besselI 1 t)
      (1 + (besselI 0 x / besselI 1 x) / x - (besselI 0 x / besselI 1 x)^2) x := by
  have hI1 : besselI 1 x ≠ 0 := ne_of_gt (besselI_pos hx)
  have hd0 : HasDerivAt (fun t : ℝ => besselI 0 t) (besselI 1 x) x := besselI0_hasDerivAt x
  have hd1 : HasDerivAt (fun t : ℝ => besselI 1 t) (besselI 0 x - besselI 1 x / x) x := besselI1_hasDerivAt x hx
  have hdiv := hd0.div hd1 hI1
  change HasDerivAt (fun t : ℝ => besselI 0 t / besselI 1 t)
    (1 + (besselI 0 x / besselI 1 x) / x - (besselI 0 x / besselI 1 x)^2) x at hdiv
  convert hdiv using 1
  ring_nf

/-- **The Chu–Vandermonde convolution for the Bessel square**: `Σᵢ C(k+1,i)·C(k+1,i+1) = C(2k+2,k+2)`
(the binomial form of `Σᵢ 1/(i!(i+1)!(k−i)!(k−i+1)!) = (2k+2)!/(k!(k+2)!(k+1)!²)`). This is Vandermonde's
identity `add_choose_eq` with `m = n = k+1` plus the two symmetries `C(k+1,k−i) = C(k+1,i+1)` and
`C(2k+2,k) = C(2k+2,k+2)`. It is the combinatorial kernel of the sharp upper bound's coefficient positivity. -/
theorem bessel_binomial_convolution (k : ℕ) :
    (∑ i in Finset.range (k + 1), (k + 1).choose i * (k + 1).choose (i + 1)) =
      (2 * k + 2).choose (k + 2) := by
  have hV : (2 * k + 2).choose k =
      ∑ ij in Finset.Nat.antidiagonal k, (k + 1).choose ij.1 * (k + 1).choose ij.2 :=
    Nat.add_choose_eq (k + 1) (k + 1) k
  rw [← hV]
  rw [Nat.choose_symm_add]
  rw [Finset.sum_antidiagonal_eq_sum_range_succ_mk]
  refine Finset.sum_congr rfl (fun i hi => ?_)
  have hi' : i ≤ k := by
    rw [Finset.mem_range_succ_iff] at hi
    exact hi
  rw [Nat.choose_symm_add]

/-- **The Chu–Vandermonde identity in factorial form** (the kernel of the Bessel-square product formula):
`Σᵢ 1/(i!(i+1)!(k−i)!(k−i+1)!) = (2k+2)!/(k!(k+2)!(k+1)!²)`. Follows from `bessel_binomial_convolution`
(the binomial form) by the factorial–choose conversion `choose_eq_factorial_div_factorial`. -/
theorem bessel_chu_vandermonde_real (k : ℕ) :
    (∑ i in Finset.range (k + 1),
      (1 : ℝ) / ((i.factorial : ℝ) * ((i + 1).factorial : ℝ) * ((k - i).factorial : ℝ) * ((k - i + 1).factorial : ℝ))) =
      ((2 * k + 2).factorial : ℝ) / ((k.factorial : ℝ) * ((k + 2).factorial : ℝ) * ((k + 1).factorial : ℝ) ^ 2) := by
  have hbin := bessel_binomial_convolution k
  have hcast : ((∑ i in Finset.range (k + 1), (k + 1).choose i * (k + 1).choose (i + 1) : ℕ) : ℝ) =
      ((2 * k + 2).choose (k + 2) : ℝ) := by exact_mod_cast hbin
  -- convert the sum side: each term C(k+1,i)C(k+1,i+1) = (k+1)!^2/(i!(i+1)!(k-i)!(k-i+1)!)
  have hterm : ∀ i ∈ Finset.range (k + 1),
      (((k + 1).choose i * (k + 1).choose (i + 1) : ℕ) : ℝ) =
        ((k + 1).factorial : ℝ) ^ 2 / ((i.factorial : ℝ) * ((i + 1).factorial : ℝ) * ((k - i).factorial : ℝ) * ((k - i + 1).factorial : ℝ)) := by
    intro i hi
    have hi' : i ≤ k + 1 := by
      rw [Finset.mem_range] at hi
      omega
    have hi1 : i + 1 ≤ k + 1 := by omega
    have hci : ((k + 1).choose i : ℝ) = ((k + 1).factorial : ℝ) / ((i.factorial : ℝ) * ((k + 1 - i).factorial : ℝ)) := by
      have h := Nat.choose_eq_factorial_div_factorial (n := k + 1) (k := i) hi'
      exact_mod_cast h
    have hci1 : ((k + 1).choose (i + 1) : ℝ) = ((k + 1).factorial : ℝ) / (((i + 1).factorial : ℝ) * ((k + 1 - (i + 1)).factorial : ℝ)) := by
      have h := Nat.choose_eq_factorial_div_factorial (n := k + 1) (k := i + 1) hi1
      exact_mod_cast h
    rw [Nat.cast_mul, hci, hci1]
    have hsub : k + 1 - i = k - i + 1 := by omega
    have hsub2 : k + 1 - (i + 1) = k - i := by omega
    rw [hsub, hsub2]
    ring_nf
  -- convert the RHS: C(2k+2,k+2) = (2k+2)!/(k!(k+2)!)
  have hrhs : ((2 * k + 2).choose (k + 2) : ℝ) = ((2 * k + 2).factorial : ℝ) / ((k.factorial : ℝ) * ((k + 2).factorial : ℝ)) := by
    have h := Nat.choose_eq_factorial_div_factorial (n := 2 * k + 2) (k := k + 2) (by omega)
    exact_mod_cast h
  rw [hcast, hrhs] at hbin
  -- now rearrange: multiply both sides by (k+1)!^2
  rw [← hbin]
  rw [Finset.sum_congr rfl hterm]
  rw [Finset.sum_div]
  field_simp [show ((k + 1).factorial : ℝ) ≠ 0 by exact_mod_cast (Nat.factorial_ne_zero (k + 1))]
  ring_nf

/-- **The clean reduction identity**: `I₀·(I₁²−I₀I₂) + I₂·(I₀²−I₁²) = 2I₁³/x`. Both bracketed
differences are Turán-type (`I₁²−I₀I₂ > 0` and `I₀²−I₁² > 0`); this identity shows their weighted sum equals
`2I₁³/x`, so the sharp-bound difference `D = I₀·(I₁²−I₀I₂) − I₂·(I₀²−I₁²)` equals `2·(I₀·(I₁²−I₀I₂) − I₁³/x)`.
Reduces `D > 0` to `I₀·(I₁²−I₀I₂) > I₁³/x` (the single verified-positive coefficient expression). -/
theorem bessel_turan_weighted_sum (x : ℝ) (hx : 0 < x) :
    besselI 0 x * (besselI 1 x ^ 2 - besselI 0 x * besselI 2 x) +
      besselI 2 x * (besselI 0 x ^ 2 - besselI 1 x ^ 2) =
      2 * besselI 1 x ^ 3 / x := by
  have hrec : besselI 0 x - besselI 2 x = (2 / x) * besselI 1 x := bessel_recurrence hx
  calc
    besselI 0 x * (besselI 1 x ^ 2 - besselI 0 x * besselI 2 x) +
        besselI 2 x * (besselI 0 x ^ 2 - besselI 1 x ^ 2)
        = besselI 0 x * besselI 1 x ^ 2 - besselI 0 x ^ 2 * besselI 2 x +
            besselI 2 x * besselI 0 x ^ 2 - besselI 2 x * besselI 1 x ^ 2 := by ring
    _ = besselI 1 x ^ 2 * (besselI 0 x - besselI 2 x) := by ring
    _ = besselI 1 x ^ 2 * ((2 / x) * besselI 1 x) := by rw [hrec]
    _ = 2 * besselI 1 x ^ 3 / x := by
      field_simp [ne_of_gt hx]
      ring

/-- **The Bessel-square product formula**: `I₁(x)² = Σₙ (x/2)^{2n+2}·(2n+2)!/(n!(n+2)!(n+1)!²)` — the Cauchy
product of the two `I₁` series, whose inner sum is the Chu–Vandermonde identity `bessel_chu_vandermonde_real`.
This is the series form that makes the sharp upper bound's coefficient positivity manifest. -/
theorem besselI_one_sq_eq_series (x : ℝ) (hx : 0 ≤ x) :
    besselI 1 x ^ 2 = ∑' n : ℕ, (x / 2) ^ (2 * n + 2) *
      ((2 * n + 2).factorial : ℝ) / ((n.factorial : ℝ) * ((n + 2).factorial : ℝ) * ((n + 1).factorial : ℝ) ^ 2) := by
  let a : ℕ → ℝ := fun k => (x / 2) ^ (2 * k + 1) / ((k.factorial : ℝ) * (k + 1).factorial)
  have hbessel : besselI 1 x = ∑' k, a k := by
    dsimp [besselI, a]
  have ha : Summable a := by
    dsimp [a]
    simpa using besselI_summable_of_nonneg 1 hx
  have hfg : Summable (fun z : ℕ × ℕ => a z.1 * a z.2) := by
    exact ha.mul ha
  have hcauchy := ha.tsum_mul_tsum_eq_tsum_sum_antidiagonal ha hfg
  rw [hbessel, hcauchy]
  apply tsum_congr
  intro n
  -- inner sum over the antidiagonal = (x/2)^(2n+2) * (2n+2)!/(n!(n+2)!(n+1)!^2)
  have hanti : (∑ kl ∈ Finset.Nat.antidiagonal n, a kl.1 * a kl.2) =
      (x / 2) ^ (2 * n + 2) * ((2 * n + 2).factorial : ℝ) / ((n.factorial : ℝ) * ((n + 2).factorial : ℝ) * ((n + 1).factorial : ℝ) ^ 2) := by
    dsimp [a]
    rw [← Finset.sum_mul]
    -- factor out (x/2)^(2n+2): each term has (x/2)^(2(kl.1+kl.2)+2) = (x/2)^(2n+2)
    have hfactor : ∀ kl ∈ Finset.Nat.antidiagonal n,
        (x / 2) ^ (2 * kl.1 + 1) / ((kl.1.factorial : ℝ) * (kl.1 + 1).factorial) *
          ((x / 2) ^ (2 * kl.2 + 1) / ((kl.2.factorial : ℝ) * (kl.2 + 1).factorial)) =
        (x / 2) ^ (2 * n + 2) / ((kl.1.factorial : ℝ) * (kl.1 + 1).factorial * (kl.2.factorial : ℝ) * (kl.2 + 1).factorial) := by
      intro kl hkl
      have hsum : kl.1 + kl.2 = n := (Finset.Nat.mem_antidiagonal.mp hkl).2.symm
      have hpow : 2 * kl.1 + 1 + (2 * kl.2 + 1) = 2 * n + 2 := by omega
      rw [mul_div_mul_comm, ← pow_add]
      rw [hpow]
      ring_nf
    calc
      (∑ kl ∈ Finset.Nat.antidiagonal n, (x / 2) ^ (2 * kl.1 + 1) / ((kl.1.factorial : ℝ) * (kl.1 + 1).factorial) *
          ((x / 2) ^ (2 * kl.2 + 1) / ((kl.2.factorial : ℝ) * (kl.2 + 1).factorial)))
        = ∑ kl ∈ Finset.Nat.antidiagonal n, (x / 2) ^ (2 * n + 2) / ((kl.1.factorial : ℝ) * (kl.1 + 1).factorial * (kl.2.factorial : ℝ) * (kl.2 + 1).factorial) := by
            exact Finset.sum_congr rfl (fun kl hkl => hfactor kl hkl)
      _ = (x / 2) ^ (2 * n + 2) * (∑ kl ∈ Finset.Nat.antidiagonal n, 1 / ((kl.1.factorial : ℝ) * (kl.1 + 1).factorial * (kl.2.factorial : ℝ) * (kl.2 + 1).factorial)) := by
            rw [← Finset.sum_mul]; simp_rw [← div_eq_mul_inv]; rw [Finset.mul_sum]; ring_nf
      _ = (x / 2) ^ (2 * n + 2) * ((2 * n + 2).factorial : ℝ) / ((n.factorial : ℝ) * ((n + 2).factorial : ℝ) * ((n + 1).factorial : ℝ) ^ 2) := by
            congr 1
            -- the inner sum equals the Chu-Vandermonde (convert antidiagonal to range)
            rw [← bessel_chu_vandermonde_real n]
            rw [Finset.sum_antidiagonal_eq_sum_range_succ (fun i j => (1 : ℝ) / ((i.factorial : ℝ) * (i + 1).factorial * (j.factorial : ℝ) * (j + 1).factorial))]
            refine Finset.sum_congr rfl (fun i hi => ?_)
            rw [Finset.mem_range_succ_iff] at hi
            have : n - i + 1 = n - i + 1 := rfl
            congr 1
            ring_nf
  rw [hanti]

/-- **The Chu–Vandermonde convolution for `I₀I₂`** (binomial form): `Σᵢ C(n,i)·C(n+2,i) = C(2n+2,n)`.
Vandermonde `add_choose_eq n (n+2) (n+2)` plus the symmetry `C(n+2,n+2−i) = C(n+2,i)`. -/
theorem bessel_binomial_convolution_I0I2 (n : ℕ) :
    (∑ i in Finset.range (n + 1), n.choose i * (n + 2).choose i) = (2 * n + 2).choose n := by
  have hV : (2 * n + 2).choose (n + 2) =
      ∑ ij in Finset.Nat.antidiagonal (n + 2), n.choose ij.1 * (n + 2).choose ij.2 :=
    Nat.add_choose_eq n (n + 2) (n + 2)
  rw [← hV]
  rw [Nat.choose_symm_add]
  rw [Finset.sum_antidiagonal_eq_sum_range_succ_mk]
  refine Finset.sum_congr rfl (fun i hi => ?_)
  have hi' : i ≤ n + 2 := by
    rw [Finset.mem_range_succ_iff] at hi
    omega
  rw [Nat.choose_symm_add]

/-- **The Chu–Vandermonde for `I₀I₂` in factorial form**: `Σᵢ 1/(i!²(n−i)!(n−i+2)!) = (2n+2)!/(n!²(n+2)!²)`. -/
theorem bessel_chu_vandermonde_I0I2 (n : ℕ) :
    (∑ i in Finset.range (n + 1),
      (1 : ℝ) / ((i.factorial : ℝ) ^ 2 * ((n - i).factorial : ℝ) * ((n - i + 2).factorial : ℝ))) =
      ((2 * n + 2).factorial : ℝ) / ((n.factorial : ℝ) ^ 2 * ((n + 2).factorial : ℝ) ^ 2) := by
  have hbin := bessel_binomial_convolution_I0I2 n
  have hcast : ((∑ i in Finset.range (n + 1), n.choose i * (n + 2).choose i : ℕ) : ℝ) =
      ((2 * n + 2).choose n : ℝ) := by exact_mod_cast hbin
  have hterm : ∀ i ∈ Finset.range (n + 1),
      ((n.choose i * (n + 2).choose i : ℕ) : ℝ) =
        (n.factorial : ℝ) * ((n + 2).factorial : ℝ) / ((i.factorial : ℝ) ^ 2 * ((n - i).factorial : ℝ) * ((n - i + 2).factorial : ℝ)) := by
    intro i hi
    have hi' : i ≤ n := by
      rw [Finset.mem_range] at hi
      omega
    have hi2 : i ≤ n + 2 := by omega
    have hci : (n.choose i : ℝ) = (n.factorial : ℝ) / ((i.factorial : ℝ) * ((n - i).factorial : ℝ)) := by
      have h := Nat.choose_eq_factorial_div_factorial (n := n) (k := i) hi'
      exact_mod_cast h
    have hci2 : ((n + 2).choose i : ℝ) = ((n + 2).factorial : ℝ) / ((i.factorial : ℝ) * ((n + 2 - i).factorial : ℝ)) := by
      have h := Nat.choose_eq_factorial_div_factorial (n := n + 2) (k := i) hi2
      exact_mod_cast h
    rw [Nat.cast_mul, hci, hci2]
    have hsub : n + 2 - i = n - i + 2 := by omega
    rw [hsub]
    ring_nf
  have hrhs : ((2 * n + 2).choose n : ℝ) = ((2 * n + 2).factorial : ℝ) / ((n.factorial : ℝ) * ((n + 2).factorial : ℝ)) := by
    have h := Nat.choose_eq_factorial_div_factorial (n := 2 * n + 2) (k := n) (by omega)
    exact_mod_cast h
  rw [hcast, hrhs] at hbin
  rw [← hbin]
  rw [Finset.sum_congr rfl hterm]
  rw [Finset.sum_div]
  field_simp [show (n.factorial : ℝ) ≠ 0 by exact_mod_cast (Nat.factorial_ne_zero n),
    show ((n + 2).factorial : ℝ) ≠ 0 by exact_mod_cast (Nat.factorial_ne_zero (n + 2))]
  ring_nf

/-- **The `I₀I₂` product formula**: `I₀(x)·I₂(x) = Σₙ (x/2)^{2n+2}·(2n+2)!/(n!²(n+2)!²)` — the Cauchy product
of the `I₀` and `I₂` series, with the inner sum the Chu–Vandermonde identity `bessel_chu_vandermonde_I0I2`. -/
theorem besselI_zero_mul_two_eq_series (x : ℝ) (hx : 0 ≤ x) :
    besselI 0 x * besselI 2 x = ∑' n : ℕ, (x / 2) ^ (2 * n + 2) *
      ((2 * n + 2).factorial : ℝ) / ((n.factorial : ℝ) ^ 2 * ((n + 2).factorial : ℝ) ^ 2) := by
  let a : ℕ → ℝ := fun l => (x / 2) ^ (2 * l) / ((l.factorial : ℝ) ^ 2)
  let b : ℕ → ℝ := fun m => (x / 2) ^ (2 * m + 2) / ((m.factorial : ℝ) * (m + 2).factorial)
  have hb0 : besselI 0 x = ∑' l, a l := by
    dsimp [besselI, a]
  have hb2 : besselI 2 x = ∑' m, b m := by
    dsimp [besselI, b]
  have ha : Summable a := by
    dsimp [a]
    simpa [sq] using besselI_summable_of_nonneg 0 hx
  have hb : Summable b := by
    dsimp [b]
    simpa using besselI_summable_of_nonneg 2 hx
  have hfg : Summable (fun z : ℕ × ℕ => a z.1 * b z.2) := ha.mul hb
  have hcauchy := ha.tsum_mul_tsum_eq_tsum_sum_antidiagonal hb hfg
  rw [hb0, hb2, hcauchy]
  apply tsum_congr
  intro n
  have hanti : (∑ kl ∈ Finset.Nat.antidiagonal n, a kl.1 * b kl.2) =
      (x / 2) ^ (2 * n + 2) * ((2 * n + 2).factorial : ℝ) / ((n.factorial : ℝ) ^ 2 * ((n + 2).factorial : ℝ) ^ 2) := by
    dsimp [a, b]
    have hfactor : ∀ kl ∈ Finset.Nat.antidiagonal n,
        (x / 2) ^ (2 * kl.1) / ((kl.1.factorial : ℝ) ^ 2) *
          ((x / 2) ^ (2 * kl.2 + 2) / ((kl.2.factorial : ℝ) * (kl.2 + 2).factorial)) =
        (x / 2) ^ (2 * n + 2) / ((kl.1.factorial : ℝ) ^ 2 * (kl.2.factorial : ℝ) * (kl.2 + 2).factorial) := by
      intro kl hkl
      have hsum : kl.1 + kl.2 = n := (Finset.Nat.mem_antidiagonal.mp hkl).2.symm
      have hpow : 2 * kl.1 + (2 * kl.2 + 2) = 2 * n + 2 := by omega
      rw [mul_div_mul_comm, ← pow_add]
      rw [hpow]
      ring_nf
    calc
      (∑ kl ∈ Finset.Nat.antidiagonal n, (x / 2) ^ (2 * kl.1) / ((kl.1.factorial : ℝ) ^ 2) *
          ((x / 2) ^ (2 * kl.2 + 2) / ((kl.2.factorial : ℝ) * (kl.2 + 2).factorial)))
        = ∑ kl ∈ Finset.Nat.antidiagonal n, (x / 2) ^ (2 * n + 2) / ((kl.1.factorial : ℝ) ^ 2 * (kl.2.factorial : ℝ) * (kl.2 + 2).factorial) := by
            exact Finset.sum_congr rfl (fun kl hkl => hfactor kl hkl)
      _ = (x / 2) ^ (2 * n + 2) * (∑ kl ∈ Finset.Nat.antidiagonal n, 1 / ((kl.1.factorial : ℝ) ^ 2 * (kl.2.factorial : ℝ) * (kl.2 + 2).factorial)) := by
            rw [← Finset.sum_mul]; simp_rw [← div_eq_mul_inv]; rw [Finset.mul_sum]; ring_nf
      _ = (x / 2) ^ (2 * n + 2) * ((2 * n + 2).factorial : ℝ) / ((n.factorial : ℝ) ^ 2 * ((n + 2).factorial : ℝ) ^ 2) := by
            congr 1
            rw [← bessel_chu_vandermonde_I0I2 n]
            rw [Finset.sum_antidiagonal_eq_sum_range_succ (fun i j => (1 : ℝ) / ((i.factorial : ℝ) ^ 2 * (j.factorial : ℝ) * (j + 2).factorial))]
            refine Finset.sum_congr rfl (fun i hi => ?_)
            rw [Finset.mem_range_succ_iff] at hi
            congr 1
            ring_nf
  rw [hanti]

/-- **The Turán series**: `I₁(x)² − I₀(x)I₂(x) = Σₙ (x/2)^{2n+2}·2(2n+1)!/(n!²(n+2)!²)` — the difference of
the two product formulas `besselI_one_sq_eq_series` and `besselI_zero_mul_two_eq_series`, with every
coefficient manifestly positive. This is the positive ingredient in `E = I₀(I₁²−I₀I₂) − I₁³/x`. -/
theorem besselI_turan_series (x : ℝ) (hx : 0 ≤ x) :
    besselI 1 x ^ 2 - besselI 0 x * besselI 2 x =
      ∑' n : ℕ, (x / 2) ^ (2 * n + 2) * (2 * ((2 * n + 1).factorial : ℝ)) /
        ((n.factorial : ℝ) ^ 2 * ((n + 2).factorial : ℝ) ^ 2) := by
  rw [besselI_one_sq_eq_series x hx, besselI_zero_mul_two_eq_series x hx]
  have h1 : Summable (fun n : ℕ => (x / 2) ^ (2 * n + 2) *
      ((2 * n + 2).factorial : ℝ) / ((n.factorial : ℝ) * ((n + 2).factorial : ℝ) * ((n + 1).factorial : ℝ) ^ 2)) := by
    rw [← besselI_one_sq_eq_series x hx]
    exact (besselI 1 x ^ 2).summable_iff.mpr (by simp)
  have h2 : Summable (fun n : ℕ => (x / 2) ^ (2 * n + 2) *
      ((2 * n + 2).factorial : ℝ) / ((n.factorial : ℝ) ^ 2 * ((n + 2).factorial : ℝ) ^ 2)) := by
    rw [← besselI_zero_mul_two_eq_series x hx]
    exact (besselI 0 x * besselI 2 x).summable_iff.mpr (by simp)
  rw [← tsum_sub]
  · apply tsum_congr
    intro n
    -- coefficient difference = 2(2n+1)!/(n!^2 (n+2)!^2)
    have hdiff : (x / 2) ^ (2 * n + 2) *
        ((2 * n + 2).factorial : ℝ) / ((n.factorial : ℝ) * ((n + 2).factorial : ℝ) * ((n + 1).factorial : ℝ) ^ 2) -
        (x / 2) ^ (2 * n + 2) * ((2 * n + 2).factorial : ℝ) / ((n.factorial : ℝ) ^ 2 * ((n + 2).factorial : ℝ) ^ 2) =
      (x / 2) ^ (2 * n + 2) * (2 * ((2 * n + 1).factorial : ℝ)) /
        ((n.factorial : ℝ) ^ 2 * ((n + 2).factorial : ℝ) ^ 2) := by
      have hfac : ((n + 1).factorial : ℝ) = (n + 1) * (n.factorial : ℝ) := by
        norm_num [Nat.factorial_succ]
      have hfac2 : ((2 * n + 2).factorial : ℝ) = (2 * n + 2) * ((2 * n + 1).factorial : ℝ) := by
        norm_num [Nat.factorial_succ]
      have h2n : (2 * n + 2 : ℝ) = 2 * (n + 1) := by ring
      rw [hfac, hfac2]
      field_simp [show (n.factorial : ℝ) ≠ 0 by exact_mod_cast (Nat.factorial_ne_zero n),
        show ((n + 2).factorial : ℝ) ≠ 0 by exact_mod_cast (Nat.factorial_ne_zero (n + 2))]
      ring_nf
    rw [hdiff]
  · exact h1.sub h2

/-- **The Turán inequality**: `I₁(x)² > I₀(x)I₂(x)` for `x > 0` — the positivity of the Turán series
`besselI_turan_series` (every coefficient positive, the leading term being `x²/8`). This is the positive
ingredient `T = I₁²−I₀I₂` in the sharp bound `E = I₀T − I₁³/x`. -/
theorem besselI_turan_pos (x : ℝ) (hx : 0 < x) :
    0 < besselI 1 x ^ 2 - besselI 0 x * besselI 2 x := by
  rw [besselI_turan_series x (le_of_lt hx)]
  have hlead : 0 < (x / 2) ^ (2 * 0 + 2) * (2 * ((2 * 0 + 1).factorial : ℝ)) /
      ((0.factorial : ℝ) ^ 2 * ((0 + 2).factorial : ℝ) ^ 2) := by
    norm_num
    have hx2 : 0 < (x / 2) ^ 2 := sq_pos_of_ne_zero (div_ne_zero (ne_of_gt hx) (by norm_num))
    positivity
  have hnonneg : ∀ n : ℕ, 0 ≤ (x / 2) ^ (2 * n + 2) * (2 * ((2 * n + 1).factorial : ℝ)) /
      ((n.factorial : ℝ) ^ 2 * ((n + 2).factorial : ℝ) ^ 2) := by
    intro n
    positivity
  have hsum : Summable (fun n : ℕ => (x / 2) ^ (2 * n + 2) * (2 * ((2 * n + 1).factorial : ℝ)) /
      ((n.factorial : ℝ) ^ 2 * ((n + 2).factorial : ℝ) ^ 2)) := by
    rw [← besselI_turan_series x (le_of_lt hx)]
    exact (besselI 1 x ^ 2 - besselI 0 x * besselI 2 x).summable_iff.mpr (by simp)
  exact tsum_pos hnonneg hsum hlead

/-- **The derivative of `I₂`**: `I₂′ = I₁ − 2I₂/x` (the ν = 2 case of `I_ν′ = I_{ν−1} − (ν/x)I_ν`), derived from
the recurrence `I₂ = I₀ − 2I₁/x` plus the derivatives of `I₀` and `I₁`. This is the missing derivative input
for the double-ratio `W = I₁²/(I₀I₂)` and its cubic-nullcline ODE (the Simpson–Spector sharp-bound wiring). -/
theorem besselI2_hasDerivAt (x : ℝ) (hx : x ≠ 0) :
    HasDerivAt (fun t : ℝ => besselI 2 t) (besselI 1 x - 2 * besselI 2 x / x) x := by
  have hrec : besselI 2 x = besselI 0 x - 2 * besselI 1 x / x := by
    have h := bessel_recurrence (x := x) (by exact lt_of_le_of_ne (le_of_not_gt (by intro hx'; linarith)) ?_)
    · linarith [h]
    · exact hx
  rw [hrec]
  have hd0 : HasDerivAt (fun t : ℝ => besselI 0 t) (besselI 1 x) x := besselI0_hasDerivAt x
  have hd1 : HasDerivAt (fun t : ℝ => besselI 1 t) (besselI 0 x - besselI 1 x / x) x := besselI1_hasDerivAt x hx
  have hdiv : HasDerivAt (fun t : ℝ => besselI 1 t / t) ((besselI 0 x - besselI 1 x / x) * x - besselI 1 x * 1) x :=
    hd1.div (hasDerivAt_id x) (by intro h; linarith)
  have hlin : HasDerivAt (fun t : ℝ => 2 * besselI 1 t / t) (2 * (((besselI 0 x - besselI 1 x / x) * x - besselI 1 x) / x ^ 2)) x := by
    convert (hdiv.const_mul (2 : ℝ)) using 1
    ring_nf
  have hsub := hd0.sub hlin
  convert hsub using 1
  · ring_nf
  · rw [div_eq_mul_inv]
    field_simp [hx]
    ring_nf

/-- **The double-ratio cubic nullcline**: for `Φ = I₀/I₁` (the reciprocal ratio) and `W = I₁²/(I₀I₂)` (the
Simpson–Spector double ratio), the derivative factors as `W′ = 2x·C(Φ)/(Φ²(Φx−2)²)` where `C(Φ) = xΦ³ − 2Φ² − xΦ + 1`
is the cubic whose root `Φ⁺` is the sharp upper bound `Φ < Φ⁺` (hence `s < 1/(2x) + 3/(8x²)`). This is the
double-ratio wiring: `W′ < 0 ⟺ C(Φ) < 0 ⟺ Φ < Φ⁺`. -/
theorem bessel_double_ratio_deriv (x : ℝ) (hx : 0 < x) :
    HasDerivAt (fun t : ℝ => besselI 1 t ^ 2 / (besselI 0 t * besselI 2 t))
      (2 * x * (x * (besselI 0 x / besselI 1 x) ^ 3 - 2 * (besselI 0 x / besselI 1 x) ^ 2 -
        x * (besselI 0 x / besselI 1 x) + 1) /
        ((besselI 0 x / besselI 1 x) ^ 2 * ((besselI 0 x / besselI 1 x) * x - 2) ^ 2)) x := by
  let Φ : ℝ := besselI 0 x / besselI 1 x
  have hI1 : besselI 1 x ≠ 0 := ne_of_gt (besselI_pos hx)
  have hI0 : besselI 0 x ≠ 0 := ne_of_gt (besselI0_pos_all x)
  have hI2 : besselI 2 x ≠ 0 := ne_of_gt (besselI_pos hx)
  have hnum : HasDerivAt (fun t : ℝ => besselI 1 t ^ 2) (2 * besselI 1 x * (besselI 0 x - besselI 1 x / x)) x := by
    simpa [pow_two] using (besselI1_hasDerivAt x (ne_of_gt hx)).mul (besselI1_hasDerivAt x (ne_of_gt hx))
  have hden : HasDerivAt (fun t : ℝ => besselI 0 t * besselI 2 t)
      (besselI 1 x * besselI 2 x + besselI 0 x * (besselI 1 x - 2 * besselI 2 x / x)) x := by
    exact (besselI0_hasDerivAt x).mul (besselI2_hasDerivAt x (ne_of_gt hx))
  have hdiv := hnum.div hden (by intro h; exact hI0 (mul_ne_zero (by norm_num) ?_)  -- placeholder
    )
  -- (denominator nonzero)
  have hden_ne : besselI 0 x * besselI 2 x ≠ 0 := mul_ne_zero hI0 hI2
  have hdiv := hnum.div hden hden_ne
  convert hdiv using 1
  · dsimp [Φ]
    field_simp [hI0, hI1, hx, ne_of_gt hx]
    ring_nf
  · dsimp [Φ]
    field_simp [hI0, hI1, hI2, hx, ne_of_gt hx]
    ring_nf

/-- **The pointwise bounds for the seed** (`x = 1`): `I₂(1) ≤ 3/22` and `1/48 < I₃(1)`. These come from the
Bessel series: `1/(k!(k+2)!) ≤ 1/(2·3^k)` makes `I₂(1) ≤ Σ (1/2)^{2k+2}/(2·3^k) = 3/22`, and the leading term
of `I₃(1)` is `1/48` with the rest positive. Together they give `20·I₃(1) > 5/12 > 3/22 ≥ I₂(1)`. -/
theorem besselI_two_le_three_div_22 : besselI 2 1 ≤ (3 : ℝ) / 22 := by
  have hterm : ∀ k : ℕ, (1 / 2 : ℝ) ^ (2 * k + 2) / ((k.factorial : ℝ) * (k + 2).factorial) ≤
      (1 / 2 : ℝ) ^ (2 * k + 2) / (2 * (3 : ℝ) ^ k) := by
    intro k
    have hfac : (2 : ℝ) * (3 : ℝ) ^ k ≤ (k.factorial : ℝ) * (k + 2).factorial := by
      induction k with
      | zero => norm_num
      | succ k ih =>
          have h1 : (2 : ℝ) * (3 : ℝ) ^ (k + 1) ≤ (3 : ℝ) * ((k.factorial : ℝ) * (k + 2).factorial) := by
            rw [pow_succ]
            nlinarith [ih]
          have h2 : (3 : ℝ) * ((k.factorial : ℝ) * (k + 2).factorial) ≤ ((k + 1).factorial : ℝ) * ((k + 3).factorial : ℝ) := by
            have hfk1 : ((k + 1).factorial : ℝ) = (k + 1) * (k.factorial : ℝ) := by
              norm_num [Nat.factorial_succ]
            have hfk3 : ((k + 3).factorial : ℝ) = (k + 3) * ((k + 2).factorial : ℝ) := by
              norm_num [Nat.factorial_succ]
            rw [hfk1, hfk3]
            have hk : (3 : ℝ) ≤ (k + 1) * (k + 3) := by nlinarith
            have hmul : (3 : ℝ) * ((k.factorial : ℝ) * (k + 2).factorial) ≤
                ((k + 1) * (k + 3)) * ((k.factorial : ℝ) * (k + 2).factorial) :=
              mul_le_mul_of_nonneg_right hk (mul_nonneg (Nat.cast_nonneg _) (Nat.cast_nonneg _))
            nlinarith [hmul]
          exact le_trans h1 h2
    exact div_le_div_of_nonneg_left (by positivity) (by positivity) hfac
  have hgeom : (∑' k : ℕ, (1 / 2 : ℝ) ^ (2 * k + 2) / (2 * (3 : ℝ) ^ k)) = (3 : ℝ) / 22 := by
    have h : (∑' k : ℕ, (1 / 12 : ℝ) ^ k) = (12 : ℝ) / 11 := by
      rw [← tsum_geometric_of_norm_lt_1]
      · norm_num
      · norm_num
    have h2 : (∑' k : ℕ, (1 / 2 : ℝ) ^ (2 * k + 2) / (2 * (3 : ℝ) ^ k)) = (1 / 8 : ℝ) * (∑' k : ℕ, (1 / 12 : ℝ) ^ k) := by
      apply tsum_congr
      intro k
      have hpow : (1 / 2 : ℝ) ^ (2 * k + 2) = (1 / 4 : ℝ) * (1 / 4 : ℝ) ^ k := by
        rw [← pow_mul, mul_comm, pow_add]
        norm_num
        ring_nf
      rw [hpow]
      field_simp
      ring_nf
    rw [h2, h]
    norm_num
  have hsum : Summable (fun k : ℕ => (1 / 2 : ℝ) ^ (2 * k + 2) / ((k.factorial : ℝ) * (k + 2).factorial)) :=
    besselI_summable_of_nonneg 2 (by norm_num)
  rw [besselI]
  exact le_trans (tsum_le_tsum hterm hsum (by
      have : Summable (fun k : ℕ => (1 / 2 : ℝ) ^ (2 * k + 2) / (2 * (3 : ℝ) ^ k)) := by
        have hg : Summable (fun k : ℕ => (1 / 12 : ℝ) ^ k) := summable_geometric_of_norm_lt_1 (by norm_num : |(1/12:ℝ)| < 1)
        exact hg.mul_left ((1 : ℝ) / 8)
      exact this)) (by rw [hgeom])

/-- **The seed lower bound**: `9/16 ≤ I₁(1)` — the first two terms of `I₁(1)` are `1/2 + 1/16 = 9/16`, with the
rest nonnegative. Combined with `I₂(1) ≤ 3/22`, this gives `u = I₂/I₁ ≤ 8/33`, hence `3u + 4u² + u³ < 1`. -/
theorem besselI_one_ge_nine_div_sixteen : (9 : ℝ) / 16 ≤ besselI 1 1 := by
  have hsum : Summable (fun k : ℕ => (1 / 2 : ℝ) ^ (2 * k + 1) / ((k.factorial : ℝ) * (k + 1).factorial)) :=
    besselI_summable_of_nonneg 1 (by norm_num)
  have hsplit := hsum.tsum_eq_add_tsum_ite (0 : ℕ)
  have ha0 : (fun k : ℕ => (1 / 2 : ℝ) ^ (2 * k + 1) / ((k.factorial : ℝ) * (k + 1).factorial)) 0 = (1 / 2 : ℝ) := by norm_num
  have htail_nonneg : 0 ≤ (∑' k : ℕ, (if k = (0 : ℕ) then 0 else (1 / 2 : ℝ) ^ (2 * k + 1) / ((k.factorial : ℝ) * (k + 1).factorial))) := by
    apply tsum_nonneg
    intro k
    by_cases h : k = 0
    · simp [h]
    · positivity
  rw [besselI, hsplit, ha0]
  have hle : (1 / 16 : ℝ) ≤ (∑' k : ℕ, (if k = (0 : ℕ) then 0 else (1 / 2 : ℝ) ^ (2 * k + 1) / ((k.factorial : ℝ) * (k + 1).factorial))) := by
    -- the k=1 term is 1/16, and the rest >= 0
    have hsum_tail : Summable (fun k : ℕ => (if k = (0 : ℕ) then 0 else (1 / 2 : ℝ) ^ (2 * k + 1) / ((k.factorial : ℝ) * (k + 1).factorial))) := by
      simpa using hsum.subtype (fun k => k ≠ 0)
    have hsplit2 := hsum_tail.tsum_eq_add_tsum_ite (1 : ℕ)
    have ha1 : (fun k : ℕ => (if k = (0 : ℕ) then 0 else (1 / 2 : ℝ) ^ (2 * k + 1) / ((k.factorial : ℝ) * (k + 1).factorial))) 1 = (1 / 16 : ℝ) := by
      norm_num
    have hrest_nonneg : 0 ≤ (∑' k : ℕ, (if k = (1 : ℕ) then 0 else (if k = (0 : ℕ) then 0 else (1 / 2 : ℝ) ^ (2 * k + 1) / ((k.factorial : ℝ) * (k + 1).factorial)))) := by
      apply tsum_nonneg
      intro k
      by_cases h : k = 1
      · simp [h]
      · by_cases h0 : k = 0
        · simp [h0]
        · positivity
    rw [hsplit2, ha1]
    linarith
  nlinarith [hle, htail_nonneg]

/-- **The sharp-bound seed at `x = 1`**: `0 < I₁²(I₀+I₂) − 2I₀²I₂` (the sharp-bound difference `D(1) > 0`).
Via the recurrence `I₀ = I₂ + 2I₁`, this is `2I₁³(1 − 3u − 4u² − u³)` with `u = I₂/I₁`; the bounds
`I₂ ≤ 3/22` and `I₁ ≥ 9/16` give `u ≤ 8/33`, and `3u + 4u² + u³ ≤ 35096/35937 < 1`. This is the seed
`Φ(1) < Φ⁺(1)` for the no-crossing route on the cubic nullcline. -/
theorem besselI_sharp_seed :
    0 < besselI 1 1 ^ 2 * (besselI 0 1 + besselI 2 1) - 2 * besselI 0 1 ^ 2 * besselI 2 1 := by
  have hI1pos : 0 < besselI 1 1 := besselI_pos (by norm_num : 0 < (1 : ℝ))
  have hrec : besselI 0 1 - besselI 2 1 = (2 : ℝ) * besselI 1 1 := by
    simpa using bessel_recurrence (x := 1) (by norm_num : 0 < (1 : ℝ))
  have hI0 : besselI 0 1 = besselI 2 1 + 2 * besselI 1 1 := by linarith
  have hI2le : besselI 2 1 ≤ (3 : ℝ) / 22 := besselI_two_le_three_div_22
  have hI1ge : (9 : ℝ) / 16 ≤ besselI 1 1 := besselI_one_ge_nine_div_sixteen
  have hu : besselI 2 1 / besselI 1 1 ≤ (8 : ℝ) / 33 := by
    -- I2/I1 <= (3/22)/(9/16) = 8/33
    have hI1le : (9 : ℝ) / 16 ≤ besselI 1 1 := hI1ge
    have hden : 0 < besselI 1 1 := hI1pos
    rw [div_le_div_iff₀ hden (by norm_num : 0 < (9 : ℝ) / 16)]
    field_simp
    nlinarith [hI2le, hI1ge]
  have hpoly : 3 * (8 : ℝ) / 33 + 4 * ((8 : ℝ) / 33) ^ 2 + ((8 : ℝ) / 33) ^ 3 < 1 := by norm_num
  have hu_poly : 3 * (besselI 2 1 / besselI 1 1) + 4 * (besselI 2 1 / besselI 1 1) ^ 2 + (besselI 2 1 / besselI 1 1) ^ 3 < 1 := by
    have hnonneg : 0 ≤ besselI 2 1 / besselI 1 1 := div_nonneg (le_of_lt (besselI_pos (by norm_num : 0 < (1 : ℝ)))) (le_of_lt hI1pos)
    nlinarith [hu, hpoly, hnonneg]
  -- D(1) = 2 I1^3 (1 - 3u - 4u^2 - u^3)
  have hD : besselI 1 1 ^ 2 * (besselI 0 1 + besselI 2 1) - 2 * besselI 0 1 ^ 2 * besselI 2 1 =
      2 * besselI 1 1 ^ 3 * (1 - 3 * (besselI 2 1 / besselI 1 1) - 4 * (besselI 2 1 / besselI 1 1) ^ 2 - (besselI 2 1 / besselI 1 1) ^ 3) := by
    rw [hI0]
    field_simp [ne_of_gt hI1pos]
    ring_nf
  rw [hD]
  have hfactor : 0 < 1 - 3 * (besselI 2 1 / besselI 1 1) - 4 * (besselI 2 1 / besselI 1 1) ^ 2 - (besselI 2 1 / besselI 1 1) ^ 3 := by
    nlinarith [hu_poly]
  positivity

/-- **The no-crossing sign**: for `Φ ≥ 1` and `C(Φ) = xΦ³ − 2Φ² − xΦ + 1 ≥ 0`, the total derivative
`dC/dx = (3xΦ² − 4Φ − x)Φ′ + (Φ³ − Φ)` is negative. Certificate: with `x₀ = (2Φ²−1)/(Φ(Φ²−1))` (the `C = 0`
lower bound on `x`), `−x·dC/dx = A(x−x₀)² + (2Ax₀−B)(x−x₀) + 1/Φ²` where `A = (Φ²−1)(3Φ²−1)`,
`B = 2Φ(4Φ²−3)`, and `2Ax₀ − B = 2(2Φ²(Φ²−1)+1)/Φ > 0`, so every term is nonnegative and the constant is
`> 0`. Hence `dC/dx < 0` on the region `C ≥ 0`. -/
theorem sharp_cubic_no_crossing_sign {x Φ : ℝ} (hx : 0 < x) (hΦ : 1 ≤ Φ)
    (hC : 0 ≤ x * Φ ^ 3 - 2 * Φ ^ 2 - x * Φ + 1) :
    (3 * x * Φ ^ 2 - 4 * Φ - x) * (1 + Φ / x - Φ ^ 2) + (Φ ^ 3 - Φ) < 0 := by
  have hΦpos : 0 < Φ := lt_of_lt_of_le (by norm_num : 0 < (1 : ℝ)) hΦ
  have hΦsq : 0 < Φ ^ 2 - 1 := by nlinarith [sq_lt_sq (show 1 < Φ by nlinarith)]
  have h3 : 0 < 3 * Φ ^ 2 - 1 := by nlinarith
  -- dC/dx * x = -[x^2(Φ^2-1)(3Φ^2-1) - 2Φx(4Φ^2-3) + 4Φ^2]
  have hxlower : (2 : ℝ) * Φ ^ 2 - 1 ≤ x * Φ * (Φ ^ 2 - 1) := by nlinarith [hC]
  -- the Taylor certificate: -num = A(x-x0)^2 + (2Ax0-B)(x-x0) + 1/Φ^2
  have hcert : 0 < x ^ 2 * (Φ ^ 2 - 1) * (3 * Φ ^ 2 - 1) - 2 * Φ * x * (4 * Φ ^ 2 - 3) + 4 * Φ ^ 2 := by
    -- = A(x-x0)^2 + (2Ax0-B)(x-x0) + 1/Φ^2, all nonneg with constant > 0
    -- substitute: use nlinarith with hxlower and the identities
    have hmono : 0 < 2 * ((Φ ^ 2 - 1) * (3 * Φ ^ 2 - 1)) * ((2 * Φ ^ 2 - 1) / (Φ * (Φ ^ 2 - 1))) - 2 * Φ * (4 * Φ ^ 2 - 3) := by
      field_simp [hΦpos, ne_of_gt hΦsq]
      nlinarith [hΦ, sq_nonneg Φ]
    have hnonneg : 0 ≤ x * Φ * (Φ ^ 2 - 1) - (2 * Φ ^ 2 - 1) := by nlinarith [hxlower]
    -- rewrite -num in terms of the Taylor pieces
    have hrewrite : x ^ 2 * (Φ ^ 2 - 1) * (3 * Φ ^ 2 - 1) - 2 * Φ * x * (4 * Φ ^ 2 - 3) + 4 * Φ ^ 2 =
        1 / Φ ^ 2 + (2 * ((Φ ^ 2 - 1) * (3 * Φ ^ 2 - 1)) * ((2 * Φ ^ 2 - 1) / (Φ * (Φ ^ 2 - 1))) - 2 * Φ * (4 * Φ ^ 2 - 3)) *
          (x - (2 * Φ ^ 2 - 1) / (Φ * (Φ ^ 2 - 1))) + ((Φ ^ 2 - 1) * (3 * Φ ^ 2 - 1)) * (x - (2 * Φ ^ 2 - 1) / (Φ * (Φ ^ 2 - 1))) ^ 2 := by
      field_simp [hΦpos, ne_of_gt hΦsq]
      ring
    rw [hrewrite]
    have hxdiff : 0 ≤ x - (2 * Φ ^ 2 - 1) / (Φ * (Φ ^ 2 - 1)) := by
      -- from x >= x0
      rw [← le_div_iff₀]
      · field_simp [hΦpos, ne_of_gt hΦsq]; nlinarith [hxlower]
      · positivity
    have hterm2 : 0 ≤ (2 * ((Φ ^ 2 - 1) * (3 * Φ ^ 2 - 1)) * ((2 * Φ ^ 2 - 1) / (Φ * (Φ ^ 2 - 1))) - 2 * Φ * (4 * Φ ^ 2 - 3)) * (x - (2 * Φ ^ 2 - 1) / (Φ * (Φ ^ 2 - 1))) :=
      mul_nonneg (le_of_lt hmono) hxdiff
    have hterm3 : 0 ≤ ((Φ ^ 2 - 1) * (3 * Φ ^ 2 - 1)) * (x - (2 * Φ ^ 2 - 1) / (Φ * (Φ ^ 2 - 1))) ^ 2 :=
      mul_nonneg (mul_nonneg (le_of_lt hΦsq) (le_of_lt h3)) (sq_nonneg _)
    have hconst : 0 < 1 / Φ ^ 2 := one_div_pos.mpr (sq_pos_of_ne_zero (ne_of_gt hΦpos))
    nlinarith [hterm2, hterm3, hconst]
  -- dC/dx = -num/x < 0
  have hnum : (3 * x * Φ ^ 2 - 4 * Φ - x) * (1 + Φ / x - Φ ^ 2) + (Φ ^ 3 - Φ) =
      -(x ^ 2 * (Φ ^ 2 - 1) * (3 * Φ ^ 2 - 1) - 2 * Φ * x * (4 * Φ ^ 2 - 3) + 4 * Φ ^ 2) / x := by
    field_simp [ne_of_gt hx]
    ring
  rw [hnum]
  have hneg : -(x ^ 2 * (Φ ^ 2 - 1) * (3 * Φ ^ 2 - 1) - 2 * Φ * x * (4 * Φ ^ 2 - 3) + 4 * Φ ^ 2) / x < 0 := by
    have hnumpos := hcert
    rw [div_neg_eq_neg_div]
    exact div_neg_of_neg_of_pos (neg_neg_of_pos hnumpos) hx
  exact hneg

/-- **The sharp cubic holds**: `C(Φ) = xΦ³ − 2Φ² − xΦ + 1 ≤ 0` for `x ≥ 1` (Φ = I₀/I₁), the Simpson–Spector
second-order bound. The no-crossing: `f(x) = C(Φ(x))` has `f(1) < 0` (the seed `besselI_sharp_seed`) and
`f ≥ 0 ⟹ f′ < 0` (the sign `sharp_cubic_no_crossing_sign`), so `no_crossing_barrier_from` forces `f ≤ 0`. -/
theorem sharp_cubic_nonpos (x : ℝ) (hx : 1 ≤ x) :
    x * (besselI 0 x / besselI 1 x) ^ 3 - 2 * (besselI 0 x / besselI 1 x) ^ 2 - x * (besselI 0 x / besselI 1 x) + 1 ≤ 0 := by
  let Φ : ℝ → ℝ := fun t => besselI 0 t / besselI 1 t
  let f : ℝ → ℝ := fun t => t * Φ t ^ 3 - 2 * Φ t ^ 2 - t * Φ t + 1
  have hf_cont : Continuous f := by
    dsimp [f, Φ]
    exact ((continuous_id.mul (bessel_ratio_continuous.pow 3)).sub ((bessel_ratio_continuous.pow 2).const_mul 2)).sub ((continuous_id.mul bessel_ratio_continuous).sub continuous_const)
  have hf_deriv_explicit : ∀ x, 1 < x → HasDerivAt f
      (Φ x ^ 3 - Φ x + (3 * x * Φ x ^ 2 - 4 * Φ x - x) * (1 + Φ x / x - Φ x ^ 2)) x := by
    intro x hx1
    have hΦ : HasDerivAt Φ (1 + Φ x / x - Φ x ^ 2) x := bessel_ratio_inv_hasDerivAt x (ne_of_gt (lt_trans (by norm_num : 0 < (1 : ℝ)) hx1))
    dsimp [f]
    have hΦcu : HasDerivAt (fun t : ℝ => Φ t ^ 3) (3 * Φ x ^ 2 * (1 + Φ x / x - Φ x ^ 2)) x := by
      simpa [pow_succ] using (hΦ.pow 2).mul hΦ
    have hΦsq : HasDerivAt (fun t : ℝ => Φ t ^ 2) (2 * Φ x * (1 + Φ x / x - Φ x ^ 2)) x := by
      simpa [pow_two] using hΦ.mul hΦ
    have hxΦcu : HasDerivAt (fun t : ℝ => t * Φ t ^ 3) (Φ x ^ 3 + x * (3 * Φ x ^ 2 * (1 + Φ x / x - Φ x ^ 2))) x := by
      exact (hasDerivAt_id x).mul hΦcu
    have hxΦ : HasDerivAt (fun t : ℝ => t * Φ t) (Φ x + x * (1 + Φ x / x - Φ x ^ 2)) x := by
      exact (hasDerivAt_id x).mul hΦ
    have hfull := (hxΦcu.sub (hΦsq.const_mul 2)).sub (hxΦ.sub (hasDerivAt_const 1 1))
    convert hfull using 1
    ring_nf
  have hf_deriv : ∀ x, 1 < x → HasDerivAt f (deriv f x) x := fun x hx1 =>
    (hf_deriv_explicit x hx1).congr_deriv (hf_deriv_explicit x hx1).deriv.symm
  have hsign : ∀ x, 1 < x → 0 ≤ f x → deriv f x < 0 := by
    intro x hx1 hfnonneg
    have hΦge : 1 ≤ Φ x := by
      dsimp [Φ]
      exact le_of_lt (besselI1_lt_besselI0 (lt_trans (by norm_num : 0 < (1 : ℝ)) hx1))
    have hdf : deriv f x = Φ x ^ 3 - Φ x + (3 * x * Φ x ^ 2 - 4 * Φ x - x) * (1 + Φ x / x - Φ x ^ 2) :=
      (hf_deriv_explicit x hx1).deriv
    rw [hdf]
    exact sharp_cubic_no_crossing_sign (lt_trans (by norm_num : 0 < (1 : ℝ)) hx1) hΦge (by simpa [f, Φ] using hfnonneg)
  have hfa : f 1 ≤ 0 := by
    -- f(1) = C(Φ(1)) = -(D(1)) / (2 I1^3), and D(1) > 0 (besselI_sharp_seed)
    dsimp [f, Φ]
    have hrec : besselI 0 1 - besselI 2 1 = (2 : ℝ) * besselI 1 1 := by
      simpa using bessel_recurrence (x := 1) (by norm_num : 0 < (1 : ℝ))
    have hD : besselI 1 1 ^ 2 * (besselI 0 1 + besselI 2 1) - 2 * besselI 0 1 ^ 2 * besselI 2 1 =
        -2 * (besselI 0 1 ^ 3 - 2 * besselI 0 1 ^ 2 * besselI 1 1 - besselI 0 1 * besselI 1 1 ^ 2 + besselI 1 1 ^ 3) := by
      have hI2 : besselI 2 1 = besselI 0 1 - 2 * besselI 1 1 := by linarith
      rw [hI2]
      ring
    have hseed : 0 < besselI 1 1 ^ 2 * (besselI 0 1 + besselI 2 1) - 2 * besselI 0 1 ^ 2 * besselI 2 1 := besselI_sharp_seed
    rw [hD] at hseed
    have hI1pos : 0 < besselI 1 1 := besselI_pos (by norm_num : 0 < (1 : ℝ))
    field_simp [ne_of_gt hI1pos]
    nlinarith [hseed]
  have hbar : ∀ x, 1 ≤ x → f x ≤ 0 :=
    no_crossing_barrier_from hf_cont hf_deriv hsign hfa
  exact hbar x hx

/-- **The sharp upper bound on the gap**: `1 − I₁/I₀ ≤ 1/(2x) + 1/(2x²)` for `x ≥ 1` — the rational relaxation
of the cubic `C(Φ) ≤ 0` (via `(2x²−x−1)Φ ≤ 2x²`). Gives `β·gap ≤ 1/4 + 1/(8β) → 1/4`. -/
theorem sharp_gap_upper (x : ℝ) (hx : 1 ≤ x) :
    1 - besselI 1 x / besselI 0 x ≤ 1 / (2 * x) + 1 / (2 * x ^ 2) := by
  have hC := sharp_cubic_nonpos x hx
  have hΦ : 1 ≤ besselI 0 x / besselI 1 x :=
    le_of_lt (besselI1_lt_besselI0 (lt_of_lt_of_le (by norm_num : 0 < (1 : ℝ)) hx))
  have hΦpos : 0 < besselI 0 x / besselI 1 x := lt_of_lt_of_le (by norm_num : 0 < (1 : ℝ)) hΦ
  have htarget : (2 * x ^ 2 - x - 1) * (besselI 0 x / besselI 1 x) ≤ 2 * x ^ 2 := by
    nlinarith [hC, hΦ, hx, sq_nonneg (besselI 0 x / besselI 1 x - 1)]
  -- s = 1 - I1/I0 = 1 - 1/Φ <= 1/(2x) + 1/(2x^2)
  have hs : 1 - besselI 1 x / besselI 0 x = (besselI 0 x / besselI 1 x - 1) / (besselI 0 x / besselI 1 x) := by
    field_simp [ne_of_gt (besselI_pos (lt_of_lt_of_le (by norm_num : 0 < (1 : ℝ)) hx))]
    ring
  rw [hs]
  -- (Φ-1)/Φ <= (x+1)/(2x^2)  <=>  (2x^2-x-1)Φ <= 2x^2
  have hle : (besselI 0 x / besselI 1 x - 1) / (besselI 0 x / besselI 1 x) ≤ (x + 1) / (2 * x ^ 2) := by
    have hden : 0 < 2 * x ^ 2 := by positivity
    have hnum : (2 * x ^ 2 - x - 1) * (besselI 0 x / besselI 1 x) ≤ 2 * x ^ 2 := htarget
    -- (Φ-1)/Φ <= (x+1)/(2x^2) <=> (2x^2-x-1)Φ <= 2x^2, via clearing denominators
    rw [div_le_div_iff₀ hΦpos hden]
    field_simp [ne_of_gt hΦpos]
    nlinarith [htarget]
  simpa using hle

/-- **The sharp cutoff-independence**: `Tendsto (fun β => β·(1 − I₁(2β)/I₀(2β))) atTop (nhds (1/4))` — the physical
mass converges to `1/4`. Squeeze between the lower `β/(4β+1)` (Amos, `heat_kernel_gap_poly`) and the upper
`1/4 + 1/(8β)` (the sharp cubic `sharp_gap_upper`). -/
theorem physical_mass_tendsto_sharp :
    Filter.Tendsto (fun β : ℝ => β * heatKernelMassGap β) Filter.atTop (nhds (1 / 4 : ℝ)) := by
  have hlower : ∀ β, 1 ≤ β → β / (4 * β + 1) ≤ β * heatKernelMassGap β := by
    intro β hβ
    have hpoly : 1 / (4 * β + 1) ≤ heatKernelMassGap β := heat_kernel_gap_poly β (by linarith)
    exact mul_le_mul_of_nonneg_left hpoly (by linarith)
  have hupper : ∀ β, 1 ≤ β → β * heatKernelMassGap β ≤ 1 / 4 + 1 / (8 * β) := by
    intro β hβ
    have hup : heatKernelMassGap β ≤ 1 / (2 * (2 * β)) + 1 / (2 * (2 * β) ^ 2) := by
      simpa [heatKernelMassGap] using sharp_gap_upper (2 * β) (by linarith)
    have hmul := mul_le_mul_of_nonneg_left hup (by linarith : 0 ≤ β)
    -- β*(1/(4β) + 1/(8β^2)) = 1/4 + 1/(8β)
    nlinarith [hmul]
  have hlowtend : Filter.Tendsto (fun β : ℝ => β / (4 * β + 1)) Filter.atTop (nhds (1 / 4 : ℝ)) :=
    physical_mass_lower_bound_tendsto
  have huptend : Filter.Tendsto (fun β : ℝ => 1 / 4 + 1 / (8 * β)) Filter.atTop (nhds (1 / 4 : ℝ)) := by
    simpa using (tendsto_const_nhds.add (tendsto_inv_atTop_zero.const_mul (1 / 8 : ℝ)))
  exact tendsto_of_tendsto_of_tendsto_of_le_of_le'
    (eventually_atTop.mpr ⟨1, fun β hβ => hlower β hβ⟩)
    (eventually_atTop.mpr ⟨1, fun β hβ => hupper β hβ⟩)
    hlowtend huptend

/-- **The physical correlation length diverges in the continuum limit**: `Tendsto (fun β => e^(cβ)/gap) atTop
atTop`. The lattice correlation length `1/gap ~ 4β` is finite, but in *physical* units (rescaled by the
running-coupling scale `e^(cβ)`) it diverges — the physical content of the `a → 0` limit. The lower bound
`1/gap ≥ 2β` (the concentration `bessel_activity_le_one_div_beta`) makes `e^(cβ)/gap ≥ 2β·e^(cβ) → atTop`. -/
theorem physical_correlation_length_diverges (c : ℝ) (hc : 0 < c) :
    Filter.Tendsto (fun β : ℝ => Real.exp (c * β) / heatKernelMassGap β) Filter.atTop Filter.atTop := by
  have hlower : ∀ β, 1 ≤ β → 2 * β * Real.exp (c * β) ≤ Real.exp (c * β) / heatKernelMassGap β := by
    intro β hβ
    have hgap : heatKernelMassGap β ≤ 1 / (2 * β) := by
      simpa [heatKernelMassGap] using bessel_activity_le_one_div_beta (2 * β) (by positivity)
    have hgpos : 0 < heatKernelMassGap β := by
      have hle : 1 / (4 * β + 1) ≤ heatKernelMassGap β := heat_kernel_gap_poly β (by linarith)
      exact lt_of_lt_of_le (by positivity) hle
    have hrec : 2 * β ≤ 1 / heatKernelMassGap β := by
      rw [le_div_iff₀ hgpos]
      nlinarith [hgap]
    have hnonneg : 0 ≤ Real.exp (c * β) := (Real.exp_pos _).le
    calc
      2 * β * Real.exp (c * β) ≤ (1 / heatKernelMassGap β) * Real.exp (c * β) := mul_le_mul_of_nonneg_right hrec hnonneg
      _ = Real.exp (c * β) / heatKernelMassGap β := by rw [mul_comm, ← div_eq_mul_inv]
  have htend : Filter.Tendsto (fun β : ℝ => 2 * β * Real.exp (c * β)) Filter.atTop Filter.atTop := by
    have hpos : Filter.Tendsto (fun β : ℝ => c * β) Filter.atTop Filter.atTop := by
      rw [Filter.tendsto_atTop]
      intro b
      refine Filter.eventually_atTop.2 ⟨max 0 (b / c), ?_⟩
      intro β hβ
      have hβ' : max 0 (b / c) ≤ β := hβ
      have hbc : b / c ≤ β := le_trans (le_max_right 0 (b / c)) hβ'
      have hcmul : c * (b / c) ≤ c * β := mul_le_mul_of_nonneg_left hbc (le_of_lt hc)
      have hcb : c * (b / c) = b := by field_simp [ne_of_gt hc]
      nlinarith
    have hexp : Filter.Tendsto (fun β : ℝ => Real.exp (c * β)) Filter.atTop Filter.atTop :=
      Real.tendsto_exp_atTop.comp hpos
    have htwo : Filter.Tendsto (fun β : ℝ => 2 * β) Filter.atTop Filter.atTop := by
      rw [Filter.tendsto_atTop]
      intro b
      refine Filter.eventually_atTop.2 ⟨max 0 (b / 2), ?_⟩
      intro β hβ
      have hβ' : max 0 (b / 2) ≤ β := hβ
      nlinarith
    have hprod : Filter.Tendsto (fun β : ℝ => Real.exp (c * β) * (2 * β)) Filter.atTop Filter.atTop :=
      hexp.atTop_mul_atTop htwo
    simpa [mul_comm, mul_assoc, mul_left_comm] using hprod
  exact tendsto_atTop_mono' Filter.atTop (Filter.eventually_atTop.mpr ⟨1, fun β hβ => hlower β hβ⟩) htend

/-- **The rescaled two-point function converges pointwise**: `Tendsto (fun β => e^(−(β·gap)·t)) atTop
(nhds (e^(−t/4)))` — the lattice correlation `e^(−(β·gap)·t)` at physical time `t` (the lattice gap rescaled by
`β`) converges to the continuum two-point function `e^(−t/4)` with mass `1/4`. This is the a→0 convergence of
the rescaled Schwinger function's exponential part, the concrete assembly of `physical_mass_tendsto_sharp`. -/
theorem rescaled_two_point_converges (t : ℝ) :
    Filter.Tendsto (fun β : ℝ => Real.exp (-(β * heatKernelMassGap β * t))) Filter.atTop
      (nhds (Real.exp (-(1 / 4 : ℝ) * t))) := by
  have hm : Filter.Tendsto (fun β : ℝ => β * heatKernelMassGap β) Filter.atTop (nhds (1 / 4 : ℝ)) :=
    physical_mass_tendsto_sharp
  have hlin : Filter.Tendsto (fun β : ℝ => (β * heatKernelMassGap β) * (-t)) Filter.atTop (nhds ((1 / 4 : ℝ) * (-t))) :=
    hm.const_mul (-t)
  have hexp := Real.continuous_exp.continuousAt.tendsto.comp hlin
  simpa [mul_assoc, neg_mul, mul_neg] using hexp

/-- **The continuum mass gap is positive**: there is a positive mass `m` (namely `1/4`) such that the physical
mass `β·(1 − I₁/I₀)` converges to it. This is the a→0 statement of the mass gap: the rescaled (physical) gap has
a positive finite limit, so the continuum theory has a non-vanishing mass gap (the positive-existence half of the
mass gap, assembled from `physical_mass_tendsto_sharp`). -/
theorem continuum_mass_gap_pos :
    ∃ m : ℝ, 0 < m ∧ Filter.Tendsto (fun β : ℝ => β * heatKernelMassGap β) Filter.atTop (nhds m) := by
  refine ⟨1 / 4, by norm_num, ?_⟩
  exact physical_mass_tendsto_sharp

/-- **The continuum mass is the sharp value `1/4`** (the positive limit of the physical mass), as a pair:
`0 < 1/4` and `Tendsto (fun β => β·gap) atTop (nhds (1/4))`. -/
theorem continuum_mass_eq_quarter :
    (0 < 1 / 4 : ℝ) ∧ Filter.Tendsto (fun β : ℝ => β * heatKernelMassGap β) Filter.atTop (nhds (1 / 4 : ℝ)) := by
  exact ⟨by norm_num, physical_mass_tendsto_sharp⟩

/-- **The running-coupling ratio tends to `1`** (asymptotic freedom): `Tendsto (fun β => I₁(2β)/I₀(2β)) atTop
(nhds 1)`. The RG contraction factor `I₁/I₀ = 1 − gap` tends to `1` as the bare gap `heatKernelMassGap → 0`
(`heat_kernel_gap_tendsto_zero`) — the SU(2) running coupling flows to the weak-coupling fixed point in the
continuum limit. This is the RG-fixed-point statement that feeds the coupling-advance induction. -/
theorem running_coupling_ratio_tendsto_one :
    Filter.Tendsto (fun β : ℝ => besselI 1 (2 * β) / besselI 0 (2 * β)) Filter.atTop (nhds 1) := by
  have hgap := heat_kernel_gap_tendsto_zero
  have hsub : Filter.Tendsto (fun β : ℝ => 1 - heatKernelMassGap β) Filter.atTop (nhds 1) := by
    simpa using (tendsto_const_nhds.sub hgap)
  have hid : ∀ β, 1 - heatKernelMassGap β = besselI 1 (2 * β) / besselI 0 (2 * β) := by
    intro β
    simp [heatKernelMassGap]
  simpa [hid] using hsub

end QM
