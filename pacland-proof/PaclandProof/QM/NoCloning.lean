import Mathlib
open scoped TensorProduct

/-!
# The no-cloning theorem — `v ↦ v⊗v` is not linear

A cloning machine would be a *linear* map `T : V → V⊗V` with `T v = v ⊗ v` for every `v`. But
`v ⊗ v` is *quadratic* in `v`, so no linear map realizes it: for the standard basis `e0, e1`,
linearity gives `T(e0+e1) = T e0 + T e1 = e0⊗e0 + e1⊗e1`, while cloning gives
`T(e0+e1) = (e0+e1)⊗(e0+e1) = e0⊗e0 + e0⊗e1 + e1⊗e0 + e1⊗e1`. Applying the functional
`x ↦ x 0 ⊗ x ↦ x 1` (then multiplication) sends the left side to 1 and the right to 0 —
a contradiction. Proven in the concrete case `V = Fin 2 → K`.
-/

namespace QM

/-- The standard basis vector `e0 = (1, 0)`. -/
def e0 (K : Type*) [Zero K] [One K] : Fin 2 → K := fun i => if i = 0 then 1 else 0

/-- The standard basis vector `e1 = (0, 1)`. -/
def e1 (K : Type*) [Zero K] [One K] : Fin 2 → K := fun i => if i = 1 then 1 else 0

/-- The tensor `(e0+e1) ⊗ (e0+e1)` expands to the four basis tensors. -/
lemma expand_sum_tmul (K : Type*) [CommSemiring K] :
    (e0 K + e1 K) ⊗ₜ[K] (e0 K + e1 K)
      = e0 K ⊗ₜ[K] e0 K + e0 K ⊗ₜ[K] e1 K + e1 K ⊗ₜ[K] e0 K + e1 K ⊗ₜ[K] e1 K := by
  rw [TensorProduct.add_tmul (e0 K) (e1 K) (e0 K + e1 K)]
  rw [TensorProduct.tmul_add (e0 K) (e0 K) (e1 K)]
  rw [TensorProduct.tmul_add (e1 K) (e0 K) (e1 K)]
  abel

/-- **No-cloning.** No linear map `T : V → V⊗V` clones every vector. -/
theorem no_cloning (K : Type*) [Field K] :
    ¬ ∃ T : (Fin 2 → K) →ₗ[K] (Fin 2 → K) ⊗[K] (Fin 2 → K),
      ∀ v, T v = v ⊗ₜ[K] v := by
  rintro ⟨T, hT⟩
  let p0 : (Fin 2 → K) →ₗ[K] K := LinearMap.proj (0 : Fin 2)
  let p1 : (Fin 2 → K) →ₗ[K] K := LinearMap.proj (1 : Fin 2)
  let f : (Fin 2 → K) ⊗[K] (Fin 2 → K) →ₗ[K] K :=
    (TensorProduct.lift (LinearMap.mul K K)).comp (TensorProduct.map p0 p1)
  -- T(e0+e1) = (e0+e1)⊗(e0+e1) = e0⊗e0 + e1⊗e1  (via linearity + cloning)
  have hkey : (e0 K + e1 K) ⊗ₜ[K] (e0 K + e1 K) = e0 K ⊗ₜ[K] e0 K + e1 K ⊗ₜ[K] e1 K := by
    calc
      (e0 K + e1 K) ⊗ₜ[K] (e0 K + e1 K) = T (e0 K + e1 K) := by rw [hT]
      _ = T (e0 K) + T (e1 K) := map_add T (e0 K) (e1 K)
      _ = e0 K ⊗ₜ[K] e0 K + e1 K ⊗ₜ[K] e1 K := by rw [hT, hT]
  have hf := congrArg f hkey
  -- left: f((e0+e1)⊗(e0+e1)) = f(e0⊗e0 + e0⊗e1 + e1⊗e0 + e1⊗e1) = 0 + 1 + 0 + 0 = 1
  -- right: f(e0⊗e0 + e1⊗e1) = 0 + 0 = 0
  rw [expand_sum_tmul K] at hf
  have hf' : f (e0 K ⊗ₜ[K] e0 K) + f (e0 K ⊗ₜ[K] e1 K) + f (e1 K ⊗ₜ[K] e0 K) + f (e1 K ⊗ₜ[K] e1 K)
      = f (e0 K ⊗ₜ[K] e0 K) + f (e1 K ⊗ₜ[K] e1 K) := by
    simpa [map_add] using hf
  have h00 : f (e0 K ⊗ₜ[K] e0 K) = (0 : K) := by dsimp [f, p0, p1, e0, e1]; simp
  have h01 : f (e0 K ⊗ₜ[K] e1 K) = (1 : K) := by dsimp [f, p0, p1, e0, e1]; simp
  have h10 : f (e1 K ⊗ₜ[K] e0 K) = (0 : K) := by dsimp [f, p0, p1, e0, e1]; simp
  have h11 : f (e1 K ⊗ₜ[K] e1 K) = (0 : K) := by dsimp [f, p0, p1, e0, e1]; simp
  rw [h00, h01, h10, h11] at hf'
  have h1eq0 : (1 : K) = 0 := by simpa using hf'
  exact one_ne_zero h1eq0

end QM
