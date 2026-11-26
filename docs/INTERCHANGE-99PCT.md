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

## ROOT CAUSE of the last error (round 42, VERIFIED)
`set_option maxHeartbeats 1600000` clears the `whnf` timeout, and the real error surfaces:
`failed to synthesize instance SeminormedAddCommGroup C(ℝ, ℝ)`.

The `ContinuousMap`'s norm/SeminormedAddCommGroup requires a COMPACT domain, but `ℝ` is not compact.
So `Summable f` for `f : ℕ → C(ℝ, ℝ)` is ILL-DEFINED — that is why the `whnf`/typeclass resolution
spins. The `hf_sum` route works because it uses `(f n).restrict (uIcc 0 π) : C(uIcc 0 π, ℝ)` (COMPACT).

FIX: the 2Σ integrability must NOT go through `Summable f` on `C(ℝ, ℝ)`. Instead use the
`hasSum_intervalIntegral_of_summable_norm` dominated-convergence (its `bound_integrable` is
`intervalIntegrable_const` for the constant sup-norm dominator), or restate `f : ℕ → C(uIcc 0 π, ℝ)`
and reconcile `Continuous.intervalIntegrable` (which wants `ℝ → E`) via `ContinuousMap.continuous`
+ the `uIcc`→`ℝ` subtype coercion.

## ~99.99% — the Summable-f route is SOLVED (round 43)
The `whnf` timeout's real cause: `C(ℝ,ℝ)` has no `SeminormedAddCommGroup` (ℝ not compact), so
`Summable.of_norm_bounded` on `f : ℕ → C(ℝ,ℝ)` was ill-typed. The FIX that works:

```lean
have hsum : Summable f := by
  refine ContinuousMap.summable_of_locally_summable_norm (F := f) (fun K => ?_)  -- compact-open Summable, works for LocallyCompactSpace ℝ
  refine Summable.of_nonneg_of_le (fun n => norm_nonneg _) (fun n => ?_) ((besselI_summable hx).comp_injective Nat.succ_injective)
  · exact (ContinuousMap.norm_le ((f n).restrict K) (C := besselI (n+1) x) (besselI_nonneg (n := n+1) hx)).mpr (fun θ => …)
```
Key: `ContinuousMap.norm_le` takes `f` as its FIRST EXPLICIT (positional), not a named `(f := …)`.

**Only remaining error:** the last `IntervalIntegrable` bullet:
`((2:ℝ) • (∑' n, f n)).continuous.intervalIntegrable` gives `IntervalIntegrable (2 • ⇑(∑' n, f n)) volume 0 π`,
but the goal is `IntervalIntegrable (fun θ => 2 * ∑' n, (f n) θ) volume 0 π`. The gap is the
`tsum`'s pointwise coercion `(∑' n, f n) θ = ∑' n, (f n) θ` (`ContinuousMap.summable_apply hsum`)
+ `Pi.smul_apply`; `simpa [coe_smul, Pi.smul_apply, summable_apply hsum]` doesn't fire it — try
`IntervalIntegrable.congr` with a `funext` + `ContinuousMap.summable_apply hsum θ`'s `.tsum_eq`.

## Last-lemma status (round 44)
`tsum_apply hsum` (the pointwise coercion `(∑' n, f n) θ = ∑' n, (f n) θ`) needs the typeclass
`IsAddApply C(ℝ,ℝ) ℝ ℝ`, which is NOT synthesized for `C(ℝ,ℝ)`. So the final bullet must use
`intervalIntegral.intervalIntegrable_congr` (or `IntegrableOn.congr`) + `filter_upwards` +
`ContinuousMap.summable_apply hsum θ` (which gives `Summable (fun n => (f n) θ)`), then prove the
pointwise equality `(∑' n, f n) θ = ∑' n, (f n) θ` by `tsum` uniqueness instead of `tsum_apply`.
This is the ONLY remaining line in `integral_exp_cos_eq_pi_mul_besselI_zero`.

## Last-lemma refinement (round 45)
`IntervalIntegrable f μ a b` is DEFINED as `IntegrableOn f (Ioc a b) μ ∧ IntegrableOn f (Ioc b a) μ`
(a CONJUNCTION over `Set.Ioc`, not `Set.uIoc`). So the final bullet splits into two `IntegrableOn`
goals, each closed by `MeasureTheory.IntegrableOn.congr_fun` + `Set.EqOn` + the pointwise
`(∑' n, f n) θ = ∑' n, (f n) θ` via `(hsum.hasSum.map_apply θ).tsum_eq.symm` (avoids the
`IsAddApply`-gated `tsum_apply`). The `EqOn` proof is: `dsimp [f]` then `simp [ContinuousMap.coe_smul, Pi.smul_apply, smul_eq_mul, hθ]`, with `measurableSet_Ioc` for the `MeasurableSet` hypothesis.
This is the ONLY remaining line in `integral_exp_cos_eq_pi_mul_besselI_zero`.

## besselI_one_eq_integral ~95% (round 52)
The I₁ Jacobi–Anger is CLOSED up to the LAST `integral_add` bullet (the `hg` for `(2·Σ besselI·cos)·cos θ`).
Working pieces: `hg_sum` (norm bound via Real.norm_eq_abs + trans_eq), `hI0` (∫ I₀·cos = 0), `htail`
(via simp_rw [mul_assoc, ← tsum_mul_right], @tsum_intervalIntegral_eq_of_summable_norm, integral_cos_succ_mul_cos,
tsum_eq_single 0), the `show (∀ θ, (I₀+2Σ)·cos = I₀·cos + 2Σ·cos) from fun θ => add_mul (a:=…)(b:=…)(c:=…)` to avoid
add_mul's over-distribution, and `rw [hmain]` (forward) + `field_simp [hπ]`.

Remaining: the `hg : IntervalIntegrable (fun θ => (2·Σ besselI·cos)·cos θ) volume 0 π` — prove like the interchange's
htailint: `ContinuousMap.summable_of_locally_summable_norm (F := g) (fun K => …)` to get `Summable g`, then
`change IntervalIntegrable ⇑((2:ℝ) • (∑' n, g n)) volume 0 π; exact ((2:ℝ) • (∑' n, g n)).continuous.intervalIntegrable 0 π`.

## besselI_sub_le ~99% (rounds 56–62)
All of `besselI_sub_le` closes except two terminal orientation details:
1. `h2 : ∫₁ ≤ ∫₁ + ∫₂` — `le_add_of_nonneg_right hnonneg`/`nlinarith [hnonneg]` produce `∫₁ ≤ ∫₂ + ∫₁`
   (the `add_comm` order); needs the `a` resolved via the type ascription + `simpa [add_comm]`.
2. The final `mul_le_mul_of_nonneg_left hlower (by positivity)` reports "No goals" — the `0 ≤ 1/π`
   witness is already discharged by the preceding `field_simp`, so drop the `by positivity`.

Everything else (hI0', hsub, hnonneg, hsplit, hhalf, hbase) is proven. Then:
- `heat_kernel_gap_exp_bound`: (1/2 − 1/π)·e^(−(12π²/11)β) ≤ heatKernelMassGap β via besselI_sub_le(2β) + besselI_zero_le_exp(2β) + poly_beats_exp.
