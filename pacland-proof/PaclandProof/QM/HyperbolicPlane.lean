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
  ⟨(Real.cosh (s.length : ℝ), Real.sinh (s.length : ℝ) * Real.cos (pathAngle s),
     Real.sinh (s.length : ℝ) * Real.sin (pathAngle s)), by
     constructor
     · calc
         -(Real.cosh (s.length : ℝ)) ^ 2 + (Real.sinh (s.length : ℝ) * Real.cos (pathAngle s)) ^ 2
           + (Real.sinh (s.length : ℝ) * Real.sin (pathAngle s)) ^ 2
           = -(Real.cosh (s.length : ℝ)) ^ 2 + (Real.sinh (s.length : ℝ)) ^ 2
               * ((Real.cos (pathAngle s)) ^ 2 + (Real.sin (pathAngle s)) ^ 2) := by ring
         _ = -(Real.cosh (s.length : ℝ)) ^ 2 + (Real.sinh (s.length : ℝ)) ^ 2 := by
               rw [Real.cos_sq_add_sin_sq]
               ring
         _ = -1 := by
               have h := Real.cosh_sq_sub_sinh_sq (s.length : ℝ)
               nlinarith
     · exact Real.cosh_pos (s.length : ℝ)⟩


/-- **The map is radially isometric** (the first QI inequality's core). The hyperbolic distance from
the root to a vertex is exactly its depth `|s|` — the map encodes the tree's radial coordinate as the
hyperbolic distance from the base point. -/
theorem treeToH2_depth (s : List Bool) :
    hyperbolicDist (treeToH2 []) (treeToH2 s) = (s.length : ℝ) := by
  dsimp [hyperbolicDist, treeToH2, minkowski]
  simp [pathAngle, Real.sinh_zero, Real.cosh_zero]
  exact Real.arcosh_cosh (by exact_mod_cast (Nat.zero_le s.length))


/-- **The map is injective in depth.** Vertices at different depths map to different hyperboloid
points — the radial coordinate (proven isometric by `treeToH2_depth`) separates them. This is the
"coarse injectivity in the radial direction" the quasi-isometry needs. -/
theorem treeToH2_depth_inj (s t : List Bool) (h : s.length ≠ t.length) :
    treeToH2 s ≠ treeToH2 t := by
  intro heq
  have hd : hyperbolicDist (treeToH2 []) (treeToH2 s) = hyperbolicDist (treeToH2 []) (treeToH2 t) := by
    rw [heq]
  rw [treeToH2_depth, treeToH2_depth] at hd
  exact h (by exact_mod_cast hd)

end QM
