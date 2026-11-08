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

end QM
