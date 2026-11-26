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

## KEY BREAKTHROUGH (round 36) — the htail is CLOSED
The `Σ ∫ cos((i+1)θ) = 0` step that blocked ~15 rounds was the `Nat.cast` normalization. Fix:

```lean
have hzero : ∀ i : ℕ, (∫ θ in (0:ℝ)..Real.pi, (f i) θ) = 0 := by
  intro i
  dsimp [f]
  rw [intervalIntegral.integral_const_mul]
  set_option maxHeartbeats 800000 in
  have h : ∫ x in (0:ℝ)..Real.pi, Real.cos (((i + 1 : ℕ) : ℝ) * x) = 0 := integral_cos_n_zero (i + 1) (by omega)
  simp [Nat.cast_add, Nat.cast_one]
  right
  simpa using h
```

So `integral_exp_cos_eq_pi_mul_besselI_zero` compiles up to TWO remaining errors:
1. `tsum_intervalIntegral_eq_of_summable_norm`'s `f` arg (use `@... ℕ ℝ _ _ (0:ℝ) Real.pi _ f hf_sum` — but the `f` is `ℕ → C(ℝ,ℝ)` and it's being matched to `hf_sum`; try the `@` form or `have ht := ...`).
2. `integral_add`'s `hg : IntervalIntegrable (fun θ => 2·Σ besselI·cos) volume 0 π` — prove via `ContinuousMap.summable_of_locally_summable_norm (F := f) (fun K => …)` to get `Summable f`, then `(∑' n, f n).continuous.intervalIntegrable`, with a `change` to rewrite `2·Σ besselI·cos = 2 • (∑' n, f n)`.
