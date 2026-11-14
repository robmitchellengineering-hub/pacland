import Mathlib
import PaclandProof.QM.Bessel

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

end QM
