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

/-- The once-contracted divergence `∇^a R_{abcd} = Σ_{a,e} gInv^{ae} ∇_e R_{abcd}`. -/
def covFirst {n : ℕ} (gInv : Fin n → Fin n → ℝ) (DR : CovDerivCurvature n) :
    Fin n → Fin n → Fin n → ℝ :=
  fun b c d => ∑ a : Fin n, ∑ e : Fin n, gInv a e * DR e a b c d

/-- **Twice-contracted second Bianchi.** `∇^a R_{abcd} = ∇_c R_{bd} − ∇_d R_{bc}`:
the once-contracted divergence of the curvature equals the difference of the two covariant
derivatives of the Ricci tensor. Follows from the second Bianchi + antisymmetry. -/
lemma twice_contracted_second_bianchi {n : ℕ} (gInv : Fin n → Fin n → ℝ) (DR : CovDerivCurvature n)
    (h_antisym : ∀ e a b c d, DR e a b c d = - DR e a b d c)
    (h_second : SecondBianchi DR) :
    ∀ b c d, covFirst gInv DR b c d = covRicci gInv DR c b d - covRicci gInv DR d b c := by
  intro b c d
  dsimp [covFirst]
  calc
    (∑ a : Fin n, ∑ e : Fin n, gInv a e * DR e a b c d)
        = (∑ a : Fin n, ∑ e : Fin n, gInv a e * (DR c a b e d - DR d a b e c)) := by
          apply Finset.sum_congr rfl; intro a ha
          apply Finset.sum_congr rfl; intro e he
          have h := h_second a b c d e
          -- h : DR e a b c d + DR c a b d e + DR d a b e c = 0
          have h' : DR e a b c d = DR c a b e d - DR d a b e c := by
            rw [h_antisym c a b d e] at h
            linarith
          rw [h']
    _ = covRicci gInv DR c b d - covRicci gInv DR d b c := by
          simp [covRicci, mul_sub, Finset.sum_sub_distrib]

/-- Flatten a 4-fold sum `Σ_b Σ_d Σ_a Σ_e F b d a e` to a sum over the pair-of-pairs. -/
lemma four_sum_to_pair_sum {n : ℕ} (F : Fin n → Fin n → Fin n → Fin n → ℝ) :
    (∑ b : Fin n, ∑ d : Fin n, ∑ a : Fin n, ∑ e : Fin n, F b d a e)
      = (∑ x : (Fin n × Fin n) × (Fin n × Fin n), F x.1.1 x.1.2 x.2.1 x.2.2) := by
  calc
    (∑ b : Fin n, ∑ d : Fin n, ∑ a : Fin n, ∑ e : Fin n, F b d a e)
        = (∑ bd : Fin n × Fin n, ∑ a : Fin n, ∑ e : Fin n, F bd.1 bd.2 a e) := by
          rw [← Finset.sum_product (Finset.univ : Finset (Fin n)) (Finset.univ : Finset (Fin n))
            (fun bd : Fin n × Fin n => ∑ a : Fin n, ∑ e : Fin n, F bd.1 bd.2 a e)]
          rw [Finset.univ_product_univ]
    _ = (∑ bd : Fin n × Fin n, ∑ ae : Fin n × Fin n, F bd.1 bd.2 ae.1 ae.2) := by
          apply Finset.sum_congr rfl; intro bd hbd
          rw [← Finset.sum_product (Finset.univ : Finset (Fin n)) (Finset.univ : Finset (Fin n))
            (fun ae : Fin n × Fin n => F bd.1 bd.2 ae.1 ae.2)]
          rw [Finset.univ_product_univ]
    _ = (∑ x : (Fin n × Fin n) × (Fin n × Fin n), F x.1.1 x.1.2 x.2.1 x.2.2) := by
          rw [← Finset.sum_product (Finset.univ : Finset (Fin n × Fin n)) (Finset.univ : Finset (Fin n × Fin n))
            (fun x : (Fin n × Fin n) × (Fin n × Fin n) => F x.1.1 x.1.2 x.2.1 x.2.2)]
          rw [Finset.univ_product_univ]

/-- Contracting the once-contracted divergence `∇^a R_{abcd}` with `gInv^{bd}` gives the
divergence of the Ricci tensor. Needs antisymmetry in both the first two and last two indices. -/
lemma covFirst_contract_eq_divRicci {n : ℕ} (gInv : Fin n → Fin n → ℝ) (DR : CovDerivCurvature n)
    (h_asym34 : ∀ e a b c d, DR e a b c d = - DR e a b d c)
    (h_asym12 : ∀ e a b c d, DR e a b c d = - DR e b a c d) :
    ∀ c, (∑ b : Fin n, ∑ d : Fin n, gInv b d * covFirst gInv DR b c d) = divRicci gInv DR c := by
  intro c
  dsimp [covFirst, divRicci, covRicci]
  have h_antisym : ∀ e a b c d, DR e a b c d = DR e b a d c := by
    intro e a b c d; rw [h_asym34, h_asym12, neg_neg]
  calc
    (∑ b : Fin n, ∑ d : Fin n, gInv b d * (∑ a : Fin n, ∑ e : Fin n, gInv a e * DR e a b c d))
        = (∑ b : Fin n, ∑ d : Fin n, gInv b d * (∑ a : Fin n, ∑ e : Fin n, gInv a e * DR e b a d c)) := by
          simp [h_antisym]
    _ = (∑ b : Fin n, ∑ e : Fin n, gInv b e * (∑ a : Fin n, ∑ c' : Fin n, gInv a c' * DR e a b c' c)) := by
          -- pull the inner sums out of the product, then flatten and reindex by the pair swap.
          simp only [Finset.mul_sum]
          rw [four_sum_to_pair_sum]
          rw [four_sum_to_pair_sum]
          refine Fintype.sum_equiv (Equiv.prodComm (Fin n × Fin n) (Fin n × Fin n)) _ _ ?_
          intro x
          dsimp [Equiv.prodComm]
          ring

/-- **Contracted Bianchi (algebraic core).** `∇·G = 0`: the divergence of the Einstein tensor
vanishes, i.e. `divRicci = (1/2) covScalar`. This follows from the twice-contracted second
Bianchi and the curvature symmetries. -/
theorem contracted_bianchi {n : ℕ} (gInv : Fin n → Fin n → ℝ) (DR : CovDerivCurvature n)
    (h_symm : ∀ a b, gInv a b = gInv b a)
    (h_asym34 : ∀ e a b c d, DR e a b c d = - DR e a b d c)
    (h_asym12 : ∀ e a b c d, DR e a b c d = - DR e b a c d)
    (h_second : SecondBianchi DR) :
    ContractedBianchi gInv DR := by
  intro c
  -- Σ_{b,d} gInv^{bd} ∇^a R_{abcd} = divRicci c  (the reindexing)
  have hLHS : (∑ b : Fin n, ∑ d : Fin n, gInv b d * covFirst gInv DR b c d) = divRicci gInv DR c :=
    covFirst_contract_eq_divRicci gInv DR h_asym34 h_asym12 c
  -- the twice-contracted second Bianchi, contracted with gInv^{bd}
  have htwice := twice_contracted_second_bianchi gInv DR h_asym34 h_second
  have hsum : (∑ b : Fin n, ∑ d : Fin n, gInv b d * covFirst gInv DR b c d)
      = (∑ b : Fin n, ∑ d : Fin n, gInv b d * (covRicci gInv DR c b d - covRicci gInv DR d b c)) := by
    apply Finset.sum_congr rfl; intro b hb
    apply Finset.sum_congr rfl; intro d hd
    rw [htwice b c d]
  -- distribute: RHS = covScalar c - divRicci c
  have hdist : (∑ b : Fin n, ∑ d : Fin n, gInv b d * (covRicci gInv DR c b d - covRicci gInv DR d b c))
      = covScalar gInv DR c - divRicci gInv DR c := by
    simp [covScalar, divRicci, covRicci, mul_sub, Finset.sum_sub_distrib]
  -- combine: divRicci c = covScalar c - divRicci c, hence divRicci c = (1/2) covScalar c
  rw [hLHS, hdist] at hsum
  nlinarith [hsum]

end

end Gravity
