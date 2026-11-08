import Mathlib

/-!
# Standard-Model generation structure — `N_gen` is a free label, not a prediction

The "yes" side's precision for the SM: the anomaly-cancellation conditions are **homogeneous**
in the hypercharges, so they fix the hypercharges only up to an overall scale and do *not* fix
the generation number `N_gen`. `N_gen` copies of a generation scale every coefficient by a
common factor, leaving the cancellation intact — so `N_gen = 3` is an observed *label* (like
the topological labels `h¹¹, h²¹`), not a value forced by consistency. This is the
"relations, never values" principle: the SM's *forced* content is the hypercharge uniqueness +
the cancellation; the generation number and the normalization are the free column.
-/

namespace SM

/-- `[SU(3)]²U(1)` anomaly coefficient. -/
def A_su3_u1 (YQ Yu Yd YL Ye : ℝ) : ℝ := 2 * YQ - Yu - Yd

/-- `[SU(2)]²U(1)` anomaly coefficient. -/
def A_su2_u1 (YQ Yu Yd YL Ye : ℝ) : ℝ := 3 * YQ + YL

/-- `[U(1)]³` anomaly coefficient. -/
def A_u1_cubic (YQ Yu Yd YL Ye : ℝ) : ℝ := 6 * YQ^3 - 3 * Yu^3 - 3 * Yd^3 + 2 * YL^3 - Ye^3

/-- `[grav]²U(1)` anomaly coefficient. -/
def A_grav_u1 (YQ Yu Yd YL Ye : ℝ) : ℝ := 6 * YQ - 3 * Yu - 3 * Yd + 2 * YL - Ye

/-- **Homogeneity.** The anomaly coefficients are homogeneous: degrees 1, 1, 3, 1 in the
hypercharges. So a global rescale `Y ↦ t·Y` (equivalently, `N_gen` identical generations) scales
each coefficient by `t`, `t`, `t³`, `t`. -/
theorem anomaly_homogeneous (t : ℝ) (YQ Yu Yd YL Ye : ℝ) :
    A_su3_u1 (t * YQ) (t * Yu) (t * Yd) (t * YL) (t * Ye) = t * A_su3_u1 YQ Yu Yd YL Ye ∧
    A_su2_u1 (t * YQ) (t * Yu) (t * Yd) (t * YL) (t * Ye) = t * A_su2_u1 YQ Yu Yd YL Ye ∧
    A_u1_cubic (t * YQ) (t * Yu) (t * Yd) (t * YL) (t * Ye) = t^3 * A_u1_cubic YQ Yu Yd YL Ye ∧
    A_grav_u1 (t * YQ) (t * Yu) (t * Yd) (t * YL) (t * Ye) = t * A_grav_u1 YQ Yu Yd YL Ye := by
  constructor
  · dsimp [A_su3_u1]; ring
  constructor
  · dsimp [A_su2_u1]; ring
  constructor
  · dsimp [A_u1_cubic]; ring_nf
  · dsimp [A_grav_u1]; ring

/-- **`N_gen` is a free label.** If a hypercharge assignment cancels the anomalies, so does
any scalar multiple of it — in particular `N_gen` identical generations. Hence the generation
number is not forced by consistency. -/
theorem anomaly_scale_invariant (t : ℝ) (YQ Yu Yd YL Ye : ℝ)
    (h : A_su3_u1 YQ Yu Yd YL Ye = 0 ∧ A_su2_u1 YQ Yu Yd YL Ye = 0 ∧
         A_u1_cubic YQ Yu Yd YL Ye = 0 ∧ A_grav_u1 YQ Yu Yd YL Ye = 0) :
    A_su3_u1 (t * YQ) (t * Yu) (t * Yd) (t * YL) (t * Ye) = 0 ∧
    A_su2_u1 (t * YQ) (t * Yu) (t * Yd) (t * YL) (t * Ye) = 0 ∧
    A_u1_cubic (t * YQ) (t * Yu) (t * Yd) (t * YL) (t * Ye) = 0 ∧
    A_grav_u1 (t * YQ) (t * Yu) (t * Yd) (t * YL) (t * Ye) = 0 := by
  have hhom := anomaly_homogeneous t YQ Yu Yd YL Ye
  rcases h with ⟨h1, h2, h3, h4⟩
  rcases hhom with ⟨g1, g2, g3, g4⟩
  constructor
  · rw [g1, h1]; ring
  constructor
  · rw [g2, h2]; ring
  constructor
  · rw [g3, h3]; ring
  · rw [g4, h4]; ring

end SM
