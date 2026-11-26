# interchange integral_exp_cos_eq_pi_mul_besselI_zero — ~99% working proof

The FULL proof that compiles up to the 2 pinned errors. Route: interval-integral `tsum_intervalIntegral_eq_of_summable_norm` (no MeasureTheory/ENNReal).

```lean
theorem integral_exp_cos_eq_pi_mul_besselI_zero (x : ℝ) (hx : 0 ≤ x) :
    ∫ θ in (0 : ℝ)..Real.pi, Real.exp (x * Real.cos θ) = Real.pi * besselI 0 x := by
  simp_rw [jacobi_anger_real]          -- KEY: avoids the EqOn beta-reduction
  rw [intervalIntegral.integral_add]
  · have hI0 : (∫ θ in (0 : ℝ)..Real.pi, (besselI 0 x)) = Real.pi * besselI 0 x := by
      simp   -- ERROR 1: (π-0) • besselI 0 x = π·besselI 0 x  (the SMul • → · won't reduce)
    have htail : (∫ θ in (0 : ℝ)..Real.pi, (2 * ∑' n : ℕ, besselI (n + 1) x * Real.cos ((n + 1 : ℝ) * θ))) = 0 := by
      let f : ℕ → C(ℝ, ℝ) := fun n => ⟨fun θ => besselI (n + 1) x * Real.cos ((n + 1 : ℝ) * θ), by
        exact continuous_const.mul (Real.continuous_cos.comp (continuous_const.mul continuous_id))⟩
      have hf_sum : Summable (fun n => ‖(f n).restrict (⟨Set.uIcc (0 : ℝ) Real.pi, isCompact_uIcc⟩ : TopologicalSpace.Compacts ℝ)‖) := by
        refine Summable.of_nonneg_of_le (fun n => ?_) (fun n => ?_) (by simpa [Nat.succ_eq_add_one] using (besselI_summable hx).comp_injective Nat.succ_injective)
        · apply norm_nonneg
        · exact (ContinuousMap.norm_le (f := (f n).restrict (⟨Set.uIcc (0 : ℝ) Real.pi, isCompact_uIcc⟩ : TopologicalSpace.Compacts ℝ)) (C := besselI (n + 1) x) (besselI_nonneg hx)).mpr (fun θ => by
            dsimp [f]
            refine (norm_mul_le (besselI (n + 1) x) (Real.cos ((n + 1 : ℝ) * θ))).trans ?_
            have hcos : ‖Real.cos ((n + 1 : ℝ) * θ)‖ ≤ 1 := by simpa using Real.abs_cos_le_one ((n + 1 : ℝ) * θ)
            simpa [Real.norm_of_nonneg (besselI_nonneg (n := n + 1) hx)] using (mul_le_mul_of_nonneg_left hcos (besselI_nonneg (n := n + 1) hx)))
      change (∫ θ in (0 : ℝ)..Real.pi, (2 * ∑' n : ℕ, (f n) θ)) = 0
      rw [intervalIntegral.integral_const_mul]
      rw [← intervalIntegral.tsum_intervalIntegral_eq_of_summable_norm (f := f) hf_sum]
      simp [integral_cos_n_zero]
    rw [hI0, htail, add_zero]
    ring
  · exact intervalIntegrable_const   -- ERROR 2: IntervalIntegrable (fun _ => c) μ a b  (μ/c not inferred)
  · exact intervalIntegrable_const
```

## The 2 pinned errors
1. **hI0 `SMul •`**: `(π-0) • besselI 0 x = π·besselI 0 x`. `integral_const : ∫ _ in a..b, c = (b-a) • c` (ℝ SMul). Tried `simp`/`norm_num`/`ring`/`ring_nf`/`change…;ring`/`simp [sub_zero, smul_eq_mul]` — the `•`→`·` reduction won't fire. Likely need `simpa only [intervalIntegral.integral_const, sub_zero]` then `norm_num`/`ring`, or `change (Real.pi - 0) * besselI 0 x = …; ring` (the `•` is `SMul ℝ ℝ`, definitionally `·`).
2. **intervalIntegrable_const**: `integral_add` needs `IntervalIntegrable (fun _ => c) MeasureTheory.volume (0:ℝ) Real.pi`. The `{c}` implicit isn't inferred — use `(intervalIntegrable_const (c := besselI 0 x) : IntervalIntegrable (fun _ : ℝ => besselI 0 x) MeasureTheory.volume (0 : ℝ) Real.pi)` (and analogously for the `2Σ` term, or via `continuous …).intervalIntegrable`).

Everything else in the file compiles; the tower is green at 9047 jobs with this lemma absent.
