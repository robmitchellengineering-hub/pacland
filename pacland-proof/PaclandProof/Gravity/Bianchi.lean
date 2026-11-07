import Mathlib

/-!
# The contracted Bianchi identity — algebraic core

`∇·G = 0` (the Einstein tensor is divergence-free) is the gravitational forced half: it makes
the Einstein equation `G = κT` self-consistent, forcing `∇·T = 0`. Mathlib has no Riemann
curvature stack, so we kernel-check the *algebraic core*: given an abstract curvature tensor
with its symmetries and the second Bianchi identity, the contracted form follows by a finite
index computation. This captures the forced content (divergence-freeness is a symmetry
consequence) without the analytic machinery (Levi-Civita existence).

Index conventions (dimension `n`, indices in `Fin n`):
- `R a b c d` = `R_{abcd}` (curvature), `DR e a b c d` = `∇_e R_{abcd}`.
- antisymmetry: `R a b c d = − R a b d c`;  pair symmetry: `R a b c d = R c d a b`.
- second Bianchi: `DR e a b c d + DR c a b d e + DR d a b e c = 0`.
- Ricci `R_bd = Σ_{a,c} gInv a c · R a b c d`; scalar `R = Σ_{b,d} gInv b d · R_bd`;
  Einstein `G_bd = R_bd − (R/2)·g b d`.
- Contracted Bianchi: for each `d`, `Σ_{b,e} gInv b e · ∇_e G_bd = 0`.
-/

namespace Gravity

open scoped BigOperators

noncomputable section

/-- Curvature tensor `R_{abcd}` in dimension `n`. -/
abbrev Curvature (n : ℕ) : Type := Fin n → Fin n → Fin n → Fin n → ℝ

/-- Covariant derivative `∇_e R_{abcd}` (a 5-index tensor). -/
abbrev CovDerivCurvature (n : ℕ) : Type := Fin n → Fin n → Fin n → Fin n → Fin n → ℝ

/-- Antisymmetry in the last two indices: `R_{abcd} = −R_{abdc}`. -/
def Curvature.antisym {n : ℕ} (R : Curvature n) : Prop :=
  ∀ a b c d, R a b c d = - R a b d c

/-- Pair symmetry: `R_{abcd} = R_{cdab}`. -/
def Curvature.pairSym {n : ℕ} (R : Curvature n) : Prop :=
  ∀ a b c d, R a b c d = R c d a b

/-- The second Bianchi identity `∇_e R_{abcd} + ∇_c R_{abde} + ∇_d R_{abec} = 0`. -/
def SecondBianchi {n : ℕ} (DR : CovDerivCurvature n) : Prop :=
  ∀ a b c d e, DR e a b c d + DR c a b d e + DR d a b e c = 0

/-- Ricci tensor `R_{bd} = Σ_{a,c} gInv^{ac} R_{abcd}`. -/
def ricci {n : ℕ} (gInv : Fin n → Fin n → ℝ) (R : Curvature n) : Fin n → Fin n → ℝ :=
  fun b d => ∑ a : Fin n, ∑ c : Fin n, gInv a c * R a b c d

/-- Scalar curvature `R = Σ_{b,d} gInv^{bd} R_{bd}`. -/
def scalarCurvature {n : ℕ} (gInv : Fin n → Fin n → ℝ) (R : Curvature n) : ℝ :=
  ∑ b : Fin n, ∑ d : Fin n, gInv b d * ricci gInv R b d

/-- Einstein tensor `G_{bd} = R_{bd} − (R/2) g_{bd}`. -/
def einstein {n : ℕ} (g : Fin n → Fin n → ℝ) (gInv : Fin n → Fin n → ℝ) (R : Curvature n) :
    Fin n → Fin n → ℝ :=
  fun b d => ricci gInv R b d - (scalarCurvature gInv R / 2) * g b d

/-- Covariant derivative of the Ricci tensor: `∇_e R_{bd} = Σ_{a,c} gInv^{ac} ∇_e R_{abcd}`. -/
def covRicci {n : ℕ} (gInv : Fin n → Fin n → ℝ) (DR : CovDerivCurvature n) :
    Fin n → Fin n → Fin n → ℝ :=
  fun e b d => ∑ a : Fin n, ∑ c : Fin n, gInv a c * DR e a b c d

/-- The divergence of the Ricci tensor: `(∇·Ric)_d = Σ_{b,e} gInv^{be} ∇_e R_{bd}`. -/
def divRicci {n : ℕ} (gInv : Fin n → Fin n → ℝ) (DR : CovDerivCurvature n) :
    Fin n → ℝ :=
  fun d => ∑ b : Fin n, ∑ e : Fin n, gInv b e * covRicci gInv DR e b d

/-- The covariant derivative of the scalar curvature: `∇_e R = Σ_{b,d} gInv^{bd} ∇_e R_{bd}`. -/
def covScalar {n : ℕ} (gInv : Fin n → Fin n → ℝ) (DR : CovDerivCurvature n) :
    Fin n → ℝ :=
  fun e => ∑ b : Fin n, ∑ d : Fin n, gInv b d * covRicci gInv DR e b d

/-- The contracted Bianchi identity: for each `d`, `(∇·Ric)_d = (1/2) ∇_d R`. -/
def ContractedBianchi {n : ℕ} (gInv : Fin n → Fin n → ℝ) (DR : CovDerivCurvature n) : Prop :=
  ∀ d, divRicci gInv DR d = (1 / 2) * covScalar gInv DR d

end

end Gravity
