import Mathlib

/-!
# The hyperbolic metric on the hyperboloid model of H² — the triangle inequality

This file carries a **self-contained** copy of the hyperboloid model (`Hyperboloid`,
`minkowski`, `hyperbolicDist`) and proves the **triangle inequality**

```
hyperbolicDist p r ≤ hyperbolicDist p q + hyperbolicDist q r
```

for the hyperbolic distance `d(p,q) = arcosh(−⟨p,q⟩_M)`.

The definitions mirror `PaclandProof.QM.HyperbolicPlane` exactly (same names, same bodies) but live
in the `HyperbolicMetric` namespace so this file builds independently of that file. When the
parallel edge-upper-bound work in `HyperbolicPlane.lean` lands, the two copies are definitionally
equal and can be reconciled (or this file can be re-pointed at the shared definitions).

## The proof (reversed Cauchy–Schwarz + Gram determinant)

1. **Reversed Cauchy–Schwarz** (`neg_minkowski_ge_one`): for two points on the upper hyperboloid,
   `-⟨p,q⟩_M ≥ 1`, so every `arcosh` input is `≥ 1`.
2. **Gram determinant** (`gram_det_le_zero`): for three points the Gram determinant of the
   Minkowski inner product satisfies `A² + B² + C² + 2ABC ≤ 1` where `A = ⟨p,q⟩`, `B = ⟨q,r⟩`,
   `C = ⟨p,r⟩` — because it equals `-det[p q r]² ≤ 0`.
3. **Cosh-form reverse triangle** (`cosh_triangle_from_gram`): with `a = -A`, `b = -B`, `c = -C`
   this is `a² + b² + c² - 2abc ≤ 1`, which by completing the square is
   `(c - ab)² ≤ (a²-1)(b²-1)`, giving `c ≤ ab + √(a²-1)√(b²-1)`.
4. **`arcosh` monotonicity** (`arcosh_triangle`): `√(a²-1) = sinh(arcosh a)`, so the bound is
   `cosh(arcosh c) ≤ cosh(arcosh a + arcosh b)`, and `cosh` is strictly monotone on `[0, ∞)`.

No `sorry`/`axiom`/`admit`; everything is kernel-checked.
-/

open scoped Real

namespace HyperbolicMetric

/-- The hyperboloid model of H²: points `(t, x, y)` on the upper sheet of `-t² + x² + y² = -1`. -/
def Hyperboloid : Type := { p : ℝ × ℝ × ℝ // -p.1 ^ 2 + p.2.1 ^ 2 + p.2.2 ^ 2 = -1 ∧ 0 < p.1 }

/-- The Minkowski inner product `⟨p, q⟩_M = -t_p t_q + x_p x_q + y_p y_q`. -/
def minkowski (p q : ℝ × ℝ × ℝ) : ℝ :=
  -p.1 * q.1 + p.2.1 * q.2.1 + p.2.2 * q.2.2

/-- The hyperbolic distance on the hyperboloid model: `d(p, q) = arcosh(−⟨p, q⟩_M)`. -/
noncomputable def hyperbolicDist (p q : Hyperboloid) : ℝ :=
  Real.arcosh (-minkowski p.1 q.1)

/-- The Minkowski self-product of a hyperboloid point is `-1`. -/
lemma minkowski_self (p : Hyperboloid) : minkowski p.1 p.1 = -1 := by
  rcases p with ⟨⟨t, x, y⟩, h⟩
  simpa [minkowski, sq] using h.1

/-- The `t`-coordinate of a hyperboloid point is `≥ 1`. -/
lemma hyperboloid_t_ge_one (p : Hyperboloid) : 1 ≤ p.1.1 := by
  rcases p with ⟨⟨t, x, y⟩, h⟩
  have hrel : x ^ 2 + y ^ 2 = t ^ 2 - 1 := by nlinarith [h.1]
  have ht2 : 1 ≤ t ^ 2 := by nlinarith [sq_nonneg x, sq_nonneg y, hrel]
  exact (one_le_sq_iff₀ (le_of_lt h.2)).mp ht2

/-- **Reversed Cauchy-Schwarz** for the Minkowski product: for two points on the upper
hyperboloid, `-⟨p,q⟩_M ≥ 1`. -/
lemma neg_minkowski_ge_one (p q : Hyperboloid) : 1 ≤ -minkowski p.1 q.1 := by
  rcases p with ⟨⟨tp, xp, yp⟩, hp⟩
  rcases q with ⟨⟨tq, xq, yq⟩, hq⟩
  dsimp [minkowski] at ⊢
  have htp : 0 ≤ tp := le_of_lt hp.2
  have htq : 0 ≤ tq := le_of_lt hq.2
  have htp1 : 1 ≤ tp := by
    have hrel : xp ^ 2 + yp ^ 2 = tp ^ 2 - 1 := by nlinarith [hp.1]
    have ht2 : 1 ≤ tp ^ 2 := by nlinarith [sq_nonneg xp, sq_nonneg yp, hrel]
    exact (one_le_sq_iff₀ htp).mp ht2
  have htq1 : 1 ≤ tq := by
    have hrel : xq ^ 2 + yq ^ 2 = tq ^ 2 - 1 := by nlinarith [hq.1]
    have ht2 : 1 ≤ tq ^ 2 := by nlinarith [sq_nonneg xq, sq_nonneg yq, hrel]
    exact (one_le_sq_iff₀ htq).mp ht2
  have hcs : (xp * xq + yp * yq) ^ 2 ≤ (xp ^ 2 + yp ^ 2) * (xq ^ 2 + yq ^ 2) := by
    nlinarith [sq_nonneg (xp * yq - xq * yp)]
  have hrel_p : xp ^ 2 + yp ^ 2 = tp ^ 2 - 1 := by nlinarith [hp.1]
  have hrel_q : xq ^ 2 + yq ^ 2 = tq ^ 2 - 1 := by nlinarith [hq.1]
  have hcs2 : (xp * xq + yp * yq) ^ 2 ≤ (tp ^ 2 - 1) * (tq ^ 2 - 1) := by
    nlinarith [hcs, hrel_p, hrel_q]
  have hsq : (tp ^ 2 - 1) * (tq ^ 2 - 1) ≤ (tp * tq - 1) ^ 2 := by
    nlinarith [sq_nonneg (tp - tq)]
  have hcs3 : (xp * xq + yp * yq) ^ 2 ≤ (tp * tq - 1) ^ 2 := by nlinarith [hcs2, hsq]
  have hpq : 0 ≤ tp * tq - 1 := by nlinarith [htp1, htq1]
  have hdot : xp * xq + yp * yq ≤ tp * tq - 1 := by
    by_cases hpos : 0 ≤ xp * xq + yp * yq
    · have habs : |xp * xq + yp * yq| ≤ |tp * tq - 1| := (sq_le_sq.mp hcs3)
      nlinarith [habs, abs_of_nonneg hpos, abs_of_nonneg hpq]
    · nlinarith [hpos, hpq]
  nlinarith [hdot]

/-- The signed volume `det[u v w]` of three vectors in `ℝ³`. -/
def tripleDet (u v w : ℝ × ℝ × ℝ) : ℝ :=
  u.1 * (v.2.1 * w.2.2 - v.2.2 * w.2.1)
    - u.2.1 * (v.1 * w.2.2 - v.2.2 * w.1)
    + u.2.2 * (v.1 * w.2.1 - v.2.1 * w.1)

/-- **Gram determinant identity**: the Gram determinant of three vectors in Minkowski space
equals `-det[u v w]²`. This is the algebraic core of the hyperbolic triangle inequality. -/
lemma gram_det_eq_neg_det_sq (u v w : ℝ × ℝ × ℝ) :
    minkowski u u * minkowski v v * minkowski w w
      + 2 * minkowski u v * minkowski v w * minkowski u w
      - minkowski u u * minkowski v w ^ 2
      - minkowski v v * minkowski u w ^ 2
      - minkowski w w * minkowski u v ^ 2
      = -(tripleDet u v w) ^ 2 := by
  rcases u with ⟨tu, xu, yu⟩
  rcases v with ⟨tv, xv, yv⟩
  rcases w with ⟨tw, xw, yw⟩
  dsimp [minkowski, tripleDet]
  ring

/-- For three points on the hyperboloid, `A² + B² + C² + 2ABC ≤ 1` where
`A = ⟨p,q⟩`, `B = ⟨q,r⟩`, `C = ⟨p,r⟩`. -/
lemma gram_det_le_zero (p q r : Hyperboloid) :
    minkowski p.1 q.1 ^ 2 + minkowski q.1 r.1 ^ 2 + minkowski p.1 r.1 ^ 2
      + 2 * minkowski p.1 q.1 * minkowski q.1 r.1 * minkowski p.1 r.1 ≤ 1 := by
  have hid := gram_det_eq_neg_det_sq p.1 q.1 r.1
  rw [minkowski_self p, minkowski_self q, minkowski_self r] at hid
  have hsq : 0 ≤ (tripleDet p.1 q.1 r.1) ^ 2 := sq_nonneg _
  nlinarith [hid, hsq]

/-- From the Gram determinant bound and `a ≥ 1`, the reversed triangle inequality in
cosh form: `c ≤ ab + √(a²−1)√(b²−1)`. -/
lemma cosh_triangle_from_gram {a b c : ℝ} (ha : 1 ≤ a)
    (hgram : a ^ 2 + b ^ 2 + c ^ 2 - 2 * a * b * c ≤ 1) :
    c ≤ a * b + Real.sqrt (a ^ 2 - 1) * Real.sqrt (b ^ 2 - 1) := by
  have hsq : (c - a * b) ^ 2 ≤ (a ^ 2 - 1) * (b ^ 2 - 1) := by nlinarith [hgram]
  have hsq_nonneg : 0 ≤ a ^ 2 - 1 := by nlinarith [ha]
  have hsqrt : |c - a * b| ≤ Real.sqrt ((a ^ 2 - 1) * (b ^ 2 - 1)) := by
    have h0 := Real.sqrt_le_sqrt hsq
    simpa [Real.sqrt_sq_eq_abs] using h0
  have hsqrt_mul : Real.sqrt ((a ^ 2 - 1) * (b ^ 2 - 1)) =
      Real.sqrt (a ^ 2 - 1) * Real.sqrt (b ^ 2 - 1) := by
    rw [Real.sqrt_mul hsq_nonneg]
  have hR_nonneg : 0 ≤ Real.sqrt (a ^ 2 - 1) * Real.sqrt (b ^ 2 - 1) := by positivity
  by_cases hle : c ≤ a * b
  · nlinarith [hle, hR_nonneg]
  · have hpos : 0 ≤ c - a * b := by nlinarith [hle]
    have h'' : c - a * b ≤ Real.sqrt ((a ^ 2 - 1) * (b ^ 2 - 1)) := by
      simpa [abs_of_nonneg hpos] using hsqrt
    have h''' : c - a * b ≤ Real.sqrt (a ^ 2 - 1) * Real.sqrt (b ^ 2 - 1) := by
      rwa [hsqrt_mul] at h''
    nlinarith [h''']

/-- From the cosh-form bound, the triangle inequality for `arcosh`. -/
lemma arcosh_triangle {a b c : ℝ} (ha : 1 ≤ a) (hb : 1 ≤ b) (hc : 1 ≤ c)
    (h : c ≤ a * b + Real.sqrt (a ^ 2 - 1) * Real.sqrt (b ^ 2 - 1)) :
    Real.arcosh c ≤ Real.arcosh a + Real.arcosh b := by
  have hca : Real.cosh (Real.arcosh c) = c := Real.cosh_arcosh hc
  have hcb : Real.cosh (Real.arcosh b) = b := Real.cosh_arcosh hb
  have haa : Real.cosh (Real.arcosh a) = a := Real.cosh_arcosh ha
  have hsa : Real.sinh (Real.arcosh a) = Real.sqrt (a ^ 2 - 1) := Real.sinh_arcosh ha
  have hsb : Real.sinh (Real.arcosh b) = Real.sqrt (b ^ 2 - 1) := Real.sinh_arcosh hb
  have hcosh : Real.cosh (Real.arcosh c) ≤ Real.cosh (Real.arcosh a + Real.arcosh b) := by
    rw [Real.cosh_add]
    calc
      Real.cosh (Real.arcosh c) = c := hca
      _ ≤ a * b + Real.sqrt (a ^ 2 - 1) * Real.sqrt (b ^ 2 - 1) := h
      _ = Real.cosh (Real.arcosh a) * Real.cosh (Real.arcosh b)
            + Real.sinh (Real.arcosh a) * Real.sinh (Real.arcosh b) := by
        rw [haa, hcb, hsa, hsb]
  have hc_nonneg : 0 ≤ Real.arcosh c := Real.arcosh_nonneg hc
  have hab_nonneg : 0 ≤ Real.arcosh a + Real.arcosh b := by
    have h1 : 0 ≤ Real.arcosh a := Real.arcosh_nonneg ha
    have h2 : 0 ≤ Real.arcosh b := Real.arcosh_nonneg hb
    nlinarith
  have hle := (Real.cosh_le_cosh).mp hcosh
  rwa [abs_of_nonneg hc_nonneg, abs_of_nonneg hab_nonneg] at hle

/-- The full derivation: Gram bound + reversed Cauchy-Schwarz give the triangle inequality
in `arcosh` form. -/
lemma hyperbolic_triangle_of_gram {a b c : ℝ} (ha : 1 ≤ a) (hb : 1 ≤ b) (hc : 1 ≤ c)
    (hgram : a ^ 2 + b ^ 2 + c ^ 2 - 2 * a * b * c ≤ 1) :
    Real.arcosh c ≤ Real.arcosh a + Real.arcosh b :=
  arcosh_triangle ha hb hc (cosh_triangle_from_gram ha hgram)

/-- **The triangle inequality for the hyperboloid distance.**
`d(p, r) ≤ d(p, q) + d(q, r)` for all points of H². -/
theorem hyperbolicDist_triangle (p q r : Hyperboloid) :
    hyperbolicDist p r ≤ hyperbolicDist p q + hyperbolicDist q r := by
  have ha : 1 ≤ -minkowski p.1 q.1 := neg_minkowski_ge_one p q
  have hb : 1 ≤ -minkowski q.1 r.1 := neg_minkowski_ge_one q r
  have hc : 1 ≤ -minkowski p.1 r.1 := neg_minkowski_ge_one p r
  have hgram :
      (-minkowski p.1 q.1) ^ 2 + (-minkowski q.1 r.1) ^ 2 + (-minkowski p.1 r.1) ^ 2
        - 2 * (-minkowski p.1 q.1) * (-minkowski q.1 r.1) * (-minkowski p.1 r.1) ≤ 1 := by
    have hdet := gram_det_le_zero p q r
    nlinarith [hdet]
  have htri := hyperbolic_triangle_of_gram ha hb hc hgram
  simpa [hyperbolicDist] using htri

end HyperbolicMetric
