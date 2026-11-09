import Mathlib

/-!
# The hyperbolic plane H² — the hyperboloid model

The target space for the "entanglement = geometry" bridge: the smooth hyperbolic plane, the
hyperboloid `-t² + x² + y² = -1` (upper sheet), with the Minkowski inner product and the hyperbolic
distance `d(p,q) = arcosh(−⟨p,q⟩_M)`. The MERA causal cone is quasi-isometric to this — the discrete
side (0-hyperbolicity `treeDist_four_point` + exponential volume `ballVolume_growth_class`) and the
growth-class invariance (`quasiIsometric_ball_image` + `quasiIsometric_coarse_injective`) are the
proof that the cone and H² are the same geometry up to bounded distortion.
-/

namespace QM

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

/-- **The quasi-isometry map** (Rung 1). A tree vertex `s` maps to a hyperboloid point at hyperbolic
distance `|s|` from the base `(1,0,0)` and angle `pathAngle s` — the exponential/horocyclic embedding
of the tree into H². This is the map the QI inequalities (Rung 1's "done when") are about. -/
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


/-- **The map is radially isometric** (the first QI inequality's core). The hyperbolic distance from
the root to a vertex is exactly its depth `|s|` — the map encodes the tree's radial coordinate as the
hyperbolic distance from the base point. -/
theorem treeToH2_depth (s : List Bool) :
    hyperbolicDist (treeToH2 []) (treeToH2 s) = (Real.log 2) * (s.length : ℝ) := by
  dsimp [hyperbolicDist, treeToH2, minkowski]
  simp [pathAngle, Real.sinh_zero, Real.cosh_zero]
  exact Real.arcosh_cosh (by positivity)


/-- **The map is injective in depth.** Vertices at different depths map to different hyperboloid
points — the radial coordinate (proven isometric by `treeToH2_depth`) separates them. This is the
"coarse injectivity in the radial direction" the quasi-isometry needs. -/
theorem treeToH2_depth_inj (s t : List Bool) (h : s.length ≠ t.length) :
    treeToH2 s ≠ treeToH2 t := by
  intro heq
  have hd : hyperbolicDist (treeToH2 []) (treeToH2 s) = hyperbolicDist (treeToH2 []) (treeToH2 t) := by
    rw [heq]
  rw [treeToH2_depth, treeToH2_depth] at hd
  have hlog : (Real.log 2 : ℝ) ≠ 0 := ne_of_gt (Real.log_pos (by norm_num : (1 : ℝ) < 2))
  exact h (by exact_mod_cast (mul_left_cancel₀ hlog hd))



/-- The angle of any tree path is nonnegative. -/
theorem pathAngle_nonneg (s : List Bool) : 0 ≤ pathAngle s := by
  induction s with
  | nil => simp [pathAngle]
  | cons b t ih =>
    simp [pathAngle]
    have hb : 0 ≤ (if b then (1 : ℝ) else 0) := by cases b <;> norm_num
    nlinarith [ih, hb]

/-- The angle of any tree path is strictly less than 1 — the binary expansion never wraps. -/
theorem pathAngle_lt_one (s : List Bool) : pathAngle s < 1 := by
  induction s with
  | nil => simp [pathAngle]
  | cons b t ih =>
    simp [pathAngle]
    have hb : (if b then (1 : ℝ) else 0) ≤ 1 := by cases b <;> norm_num
    nlinarith [ih, hb]

/-- **Coarse injectivity, angular.** Two tree paths of the same depth have the same angle only if
they are the same path — distinct branches map to distinct angles. -/
theorem pathAngle_inj {s t : List Bool} (h : pathAngle s = pathAngle t) (hl : s.length = t.length) :
    s = t := by
  induction s generalizing t with
  | nil =>
    cases t with
    | nil => rfl
    | cons c t' => simp at hl
  | cons b s' ih =>
    cases t with
    | nil => simp at hl
    | cons c t' =>
      simp only [List.length_cons] at hl
      have h3 : (if b then (1 : ℝ) else 0) + pathAngle s' = (if c then (1 : ℝ) else 0) + pathAngle t' := by
        simp [pathAngle] at h
        nlinarith [h]
      have hbc : b = c := by
        by_cases hb : b <;> by_cases hc : c <;> simp [hb, hc] at h3 ⊢
        · exfalso
          have hlt := pathAngle_lt_one t'
          have hn : 1 ≤ 1 + pathAngle s' := by nlinarith [pathAngle_nonneg s']
          nlinarith [h3, hlt, hn]
        · exfalso
          have hlt := pathAngle_lt_one s'
          have hn : 1 ≤ 1 + pathAngle t' := by nlinarith [pathAngle_nonneg t']
          nlinarith [h3, hlt, hn]
      have ht' : pathAngle s' = pathAngle t' := by
        rw [hbc] at h3
        nlinarith [h3]
      have hs' : s' = t' := ih ht' (by omega)
      rw [hbc, hs']


/-- The Minkowski product of two tree images: `-cosh r₁ cosh r₂ + sinh r₁ sinh r₂ cos(θs - θt)`. -/
theorem minkowski_treeToH2 (s t : List Bool) :
    minkowski (treeToH2 s).1 (treeToH2 t).1 =
      -(Real.cosh ((Real.log 2) * (s.length : ℝ))) * Real.cosh ((Real.log 2) * (t.length : ℝ))
        + (Real.sinh ((Real.log 2) * (s.length : ℝ))) * Real.sinh ((Real.log 2) * (t.length : ℝ))
          * Real.cos (2 * Real.pi * (pathAngle s - pathAngle t)) := by
  dsimp [treeToH2, minkowski]
  rw [← show 2 * Real.pi * pathAngle s - 2 * Real.pi * pathAngle t =
      2 * Real.pi * (pathAngle s - pathAngle t) by ring]
  rw [Real.cos_sub]
  ring

/-- **The diameter bound** (the upper half of the QI distortion): the hyperbolic distance between
two tree images is at most the sum of their depths — the coarse `hyperbolicDist ≤ |s| + |t|` bound. -/
theorem hyperbolicDist_le_add (s t : List Bool) :
    hyperbolicDist (treeToH2 s) (treeToH2 t) ≤
      (Real.log 2) * ((s.length : ℝ) + (t.length : ℝ)) := by
  dsimp [hyperbolicDist]
  rw [minkowski_treeToH2]
  rw [← Real.arcosh_cosh (show 0 ≤ (Real.log 2) * ((s.length : ℝ) + (t.length : ℝ)) by positivity)]
  rw [Real.arcosh_le_arcosh]
  rotate_left
  · -- 0 < cosh r₁ cosh r₂ - sinh r₁ sinh r₂ cos(2π·Δθ)
    have hc : Real.cos (2 * Real.pi * (pathAngle s - pathAngle t)) ≤ 1 := Real.cos_le_one _
    have hsinh : 0 ≤ Real.sinh ((Real.log 2) * (s.length : ℝ)) * Real.sinh ((Real.log 2) * (t.length : ℝ)) := by positivity
    have hcs : Real.cosh ((Real.log 2) * (s.length : ℝ) - (Real.log 2) * (t.length : ℝ)) =
        Real.cosh ((Real.log 2) * (s.length : ℝ)) * Real.cosh ((Real.log 2) * (t.length : ℝ))
          - Real.sinh ((Real.log 2) * (s.length : ℝ)) * Real.sinh ((Real.log 2) * (t.length : ℝ)) := Real.cosh_sub _ _
    have hone : 1 ≤ Real.cosh ((Real.log 2) * (s.length : ℝ) - (Real.log 2) * (t.length : ℝ)) := Real.one_le_cosh _
    nlinarith [hc, hsinh, hcs, hone]
  · positivity
  · rw [show (Real.log 2) * ((s.length : ℝ) + (t.length : ℝ)) =
        (Real.log 2) * (s.length : ℝ) + (Real.log 2) * (t.length : ℝ) by ring]
    rw [Real.cosh_add]
    have hc : -1 ≤ Real.cos (2 * Real.pi * (pathAngle s - pathAngle t)) :=
      neg_le_of_abs_le (Real.abs_cos_le_one (2 * Real.pi * (pathAngle s - pathAngle t)))
    have hs : 0 ≤ Real.sinh ((Real.log 2) * (s.length : ℝ)) * Real.sinh ((Real.log 2) * (t.length : ℝ)) := by positivity
    nlinarith [hc, hs]


/-- Appending a `false` bit does not change the angle — the trailing zero has weight 0. -/
theorem pathAngle_append_false (p : List Bool) :
    pathAngle (p ++ [false]) = pathAngle p := by
  induction p with
  | nil => simp [pathAngle]
  | cons b t ih =>
    simp [pathAngle, ih]

/-- **The false-child edge is purely radial** — a parent and its `false`-child (same angle) are at
exactly `ln 2` hyperbolic distance. This is the *edge lower bound* of the quasi-isometry: each tree
edge maps to a segment of length at least `ln 2`, so the map cannot collapse the tree. -/
theorem hyperbolicDist_falseChild (p : List Bool) :
    hyperbolicDist (treeToH2 (p ++ [false])) (treeToH2 p) = Real.log 2 := by
  dsimp [hyperbolicDist]
  rw [minkowski_treeToH2]
  rw [pathAngle_append_false]
  simp
  rw [show -(Real.sinh (Real.log 2 * (↑p.length + 1)) * Real.sinh (Real.log 2 * ↑p.length))
      + Real.cosh (Real.log 2 * (↑p.length + 1)) * Real.cosh (Real.log 2 * ↑p.length)
      = Real.cosh (Real.log 2 * (↑p.length + 1)) * Real.cosh (Real.log 2 * ↑p.length)
        - Real.sinh (Real.log 2 * (↑p.length + 1)) * Real.sinh (Real.log 2 * ↑p.length) by ring]
  rw [← Real.cosh_sub]
  rw [show Real.log 2 * (↑p.length + 1) - Real.log 2 * ↑p.length = Real.log 2 by ring]
  exact Real.arcosh_cosh (by positivity)



/-- **The radial lower bound.** The hyperbolic distance between two tree images is at least the
radial difference `ln2 · (|s| − |t|)` (when `|s| ≥ |t|`) — the angular part can only *add* distance.
For a parent–child edge this gives `≥ ln 2`, the coarse-injectivity core of the quasi-isometry. -/
theorem hyperbolicDist_ge_radial (s t : List Bool) (h : t.length ≤ s.length) :
    (Real.log 2) * ((s.length : ℝ) - (t.length : ℝ)) ≤ hyperbolicDist (treeToH2 s) (treeToH2 t) := by
  dsimp [hyperbolicDist]
  rw [minkowski_treeToH2]
  rw [← Real.arcosh_cosh (show 0 ≤ (Real.log 2) * ((s.length : ℝ) - (t.length : ℝ)) by
    have hreal : (t.length : ℝ) ≤ (s.length : ℝ) := by exact_mod_cast h
    nlinarith [Real.log_pos (by norm_num : (1 : ℝ) < 2), hreal])]
  rw [Real.arcosh_le_arcosh]
  rotate_left
  · positivity
  · have hc : Real.cos (2 * Real.pi * (pathAngle s - pathAngle t)) ≤ 1 := Real.cos_le_one _
    have hsinh : 0 ≤ Real.sinh (Real.log 2 * (s.length : ℝ)) * Real.sinh (Real.log 2 * (t.length : ℝ)) := by positivity
    have hcs : Real.cosh (Real.log 2 * (s.length : ℝ) - Real.log 2 * (t.length : ℝ)) =
        Real.cosh (Real.log 2 * (s.length : ℝ)) * Real.cosh (Real.log 2 * (t.length : ℝ))
          - Real.sinh (Real.log 2 * (s.length : ℝ)) * Real.sinh (Real.log 2 * (t.length : ℝ)) := Real.cosh_sub _ _
    have hone : 1 ≤ Real.cosh (Real.log 2 * (s.length : ℝ) - Real.log 2 * (t.length : ℝ)) := Real.one_le_cosh _
    nlinarith [hc, hsinh, hcs, hone]
  · rw [show (Real.log 2) * ((s.length : ℝ) - (t.length : ℝ)) =
        (Real.log 2) * (s.length : ℝ) - (Real.log 2) * (t.length : ℝ) by ring]
    rw [Real.cosh_sub]
    have hc : Real.cos (2 * Real.pi * (pathAngle s - pathAngle t)) ≤ 1 := Real.cos_le_one _
    have hs : 0 ≤ Real.sinh (Real.log 2 * (s.length : ℝ)) * Real.sinh (Real.log 2 * (t.length : ℝ)) := by positivity
    nlinarith [hc, hs]


end QM
