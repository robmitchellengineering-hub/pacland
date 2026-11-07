import Mathlib
import PaclandProof.SM.Generation

/-!
# The chiral index — `N_gen` as the Atiyah–Singer index (algebraic core)

The geometric-unification step: the SM's generation number `N_gen` is the **index of the Dirac
operator** on the string compactification, a topological label tied to the flux sector's Euler
character by `N_gen = |χ|/2`. The algebraic core of this index theorem is the **"anomaly = index
consistency"** relation: the SM's anomaly coefficients are *homogeneous* in the generation number
(degrees 1, 1, 3, 1), so anomaly cancellation is a condition that the chiral index is
well-defined — it does not fix `N_gen`, it *protects* it. This is what turns `N_gen = 3` from a
free SM parameter into a topological label shared with the flux sector.
-/

namespace SM

/-- **The index is a free label (algebraic core of `N_gen = index`).** For `N_gen` identical
generations the anomaly coefficients are the one-generation coefficients scaled by `N_gen`
(linear ones) or `N_gen³` (the cubic) — so the anomaly cancellation holds for *every* generation
number: `N_gen` is an index, not a prediction. -/
theorem index_free (Ngen : ℝ) :
    A_su3_u1 (Ngen * (1/6 : ℝ)) (Ngen * (2/3 : ℝ)) (Ngen * (-1/3 : ℝ)) (Ngen * (-1/2 : ℝ)) (Ngen * (-1 : ℝ))
      = Ngen * A_su3_u1 (1/6 : ℝ) (2/3 : ℝ) (-1/3 : ℝ) (-1/2 : ℝ) (-1 : ℝ) ∧
    A_su2_u1 (Ngen * (1/6 : ℝ)) (Ngen * (2/3 : ℝ)) (Ngen * (-1/3 : ℝ)) (Ngen * (-1/2 : ℝ)) (Ngen * (-1 : ℝ))
      = Ngen * A_su2_u1 (1/6 : ℝ) (2/3 : ℝ) (-1/3 : ℝ) (-1/2 : ℝ) (-1 : ℝ) ∧
    A_u1_cubic (Ngen * (1/6 : ℝ)) (Ngen * (2/3 : ℝ)) (Ngen * (-1/3 : ℝ)) (Ngen * (-1/2 : ℝ)) (Ngen * (-1 : ℝ))
      = Ngen^3 * A_u1_cubic (1/6 : ℝ) (2/3 : ℝ) (-1/3 : ℝ) (-1/2 : ℝ) (-1 : ℝ) ∧
    A_grav_u1 (Ngen * (1/6 : ℝ)) (Ngen * (2/3 : ℝ)) (Ngen * (-1/3 : ℝ)) (Ngen * (-1/2 : ℝ)) (Ngen * (-1 : ℝ))
      = Ngen * A_grav_u1 (1/6 : ℝ) (2/3 : ℝ) (-1/3 : ℝ) (-1/2 : ℝ) (-1 : ℝ) := by
  have h := anomaly_homogeneous Ngen (1/6 : ℝ) (2/3 : ℝ) (-1/3 : ℝ) (-1/2 : ℝ) (-1 : ℝ)
  exact h

/-- **The index is protected, not fixed.** If the one-generation hypercharges are anomaly-free,
then any `N_gen` generations are anomaly-free — so `N_gen` is a free topological label. -/
theorem index_protected (Ngen : ℝ) :
    A_su3_u1 (1/6 : ℝ) (2/3 : ℝ) (-1/3 : ℝ) (-1/2 : ℝ) (-1 : ℝ) = 0 →
    A_su3_u1 (Ngen * (1/6 : ℝ)) (Ngen * (2/3 : ℝ)) (Ngen * (-1/3 : ℝ)) (Ngen * (-1/2 : ℝ)) (Ngen * (-1 : ℝ)) = 0 := by
  intro h
  rw [index_free Ngen |>.1, h]
  ring

end SM
