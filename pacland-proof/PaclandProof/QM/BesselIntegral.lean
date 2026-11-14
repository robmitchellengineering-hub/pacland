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

end QM
