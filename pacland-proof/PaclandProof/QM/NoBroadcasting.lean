import Mathlib
open scoped TensorProduct

/-!
# The no-broadcasting theorem — `M ↦ M⊗M` is not linear (mixed-state no-cloning)

The falsification rung that excludes broadcasting an unknown quantum *state* (density matrix).
No-cloning rules out copying a pure state `v ↦ v⊗v`; no-broadcasting is the same linearity
argument at the level of *operators*: a broadcasting machine would be a linear map
`T : End(V) → End(V)⊗End(V)` with `T M = M⊗M` for every operator `M`. But `M⊗M` is quadratic
in `M`, so no linear map realizes it — proven here concretely for `2×2` matrices, with the two
independent basis matrices `E₀₀ = [[1,0],[0,0]]` and `E₁₁ = [[0,0],[0,1]]` and the coordinate
functional `(ev₀₀ ⊗ ev₁₁)` separating the cross terms `E₀₀⊗E₁₁` from `E₁₁⊗E₀₀`.
-/

namespace QM

noncomputable section

/-- The basis matrix `E₀₀ = [[1,0],[0,0]]`. -/
def E00 (K : Type*) [Zero K] [One K] : Matrix (Fin 2) (Fin 2) K := !![1, 0; 0, 0]

/-- The basis matrix `E₁₁ = [[0,0],[0,1]]`. -/
def E11 (K : Type*) [Zero K] [One K] : Matrix (Fin 2) (Fin 2) K := !![0, 0; 0, 1]

/-- The coordinate functional `M ↦ M 0 0`. -/
def ev00 (K : Type*) [CommRing K] : Matrix (Fin 2) (Fin 2) K →ₗ[K] K where
  toFun M := M 0 0
  map_add' := by intro M N; rfl
  map_smul' := by intro r M; rfl

/-- The coordinate functional `M ↦ M 1 1`. -/
def ev11 (K : Type*) [CommRing K] : Matrix (Fin 2) (Fin 2) K →ₗ[K] K where
  toFun M := M 1 1
  map_add' := by intro M N; rfl
  map_smul' := by intro r M; rfl

/-- The separating functional `(ev00 ⊗ ev11)` followed by multiplication. -/
def broadcastFunctional (K : Type*) [CommRing K] :
    (Matrix (Fin 2) (Fin 2) K) ⊗[K] (Matrix (Fin 2) (Fin 2) K) →ₗ[K] K :=
  (TensorProduct.lift (LinearMap.mul K K)).comp (TensorProduct.map (ev00 K) (ev11 K))

/-- `broadcastFunctional` on a simple tensor evaluates to `M 0 0 * N 1 1`. -/
lemma broadcastFunctional_tmul (K : Type*) [CommRing K] (M N : Matrix (Fin 2) (Fin 2) K) :
    broadcastFunctional K (M ⊗ₜ[K] N) = M 0 0 * N 1 1 := by
  change ((TensorProduct.lift (LinearMap.mul K K)).comp (TensorProduct.map (ev00 K) (ev11 K))) (M ⊗ₜ[K] N) = M 0 0 * N 1 1
  rw [LinearMap.comp_apply]
  rw [TensorProduct.map_tmul]
  rw [TensorProduct.lift.tmul]
  rfl

/-- **No-broadcasting.** No linear map `T : End(V) → End(V)⊗End(V)` broadcasts every operator:
`T M = M ⊗ M` for all `M` is impossible. -/
theorem no_broadcasting (K : Type*) [Field K] :
    ¬ ∃ T : Matrix (Fin 2) (Fin 2) K →ₗ[K]
        (Matrix (Fin 2) (Fin 2) K) ⊗[K] (Matrix (Fin 2) (Fin 2) K),
      ∀ M, T M = M ⊗ₜ[K] M := by
  rintro ⟨T, hT⟩
  -- the functional (ev00 ⊗ ev11) followed by multiplication, on the tensor product
  let f := broadcastFunctional K
  -- T(E00 + E11) = E00⊗E00 + E11⊗E11 (linearity), but = (E00+E11)⊗(E00+E11) (broadcasting)
  have hkey : (E00 K + E11 K) ⊗ₜ[K] (E00 K + E11 K) = E00 K ⊗ₜ[K] E00 K + E11 K ⊗ₜ[K] E11 K := by
    calc
      (E00 K + E11 K) ⊗ₜ[K] (E00 K + E11 K) = T (E00 K + E11 K) := by rw [hT]
      _ = T (E00 K) + T (E11 K) := map_add T (E00 K) (E11 K)
      _ = E00 K ⊗ₜ[K] E00 K + E11 K ⊗ₜ[K] E11 K := by rw [hT, hT]
  have hf := congrArg f hkey
  -- expand (E00+E11)⊗(E00+E11) = E00⊗E00 + E00⊗E11 + E11⊗E00 + E11⊗E11
  rw [TensorProduct.add_tmul (E00 K) (E11 K) (E00 K + E11 K)] at hf
  rw [TensorProduct.tmul_add (E00 K) (E00 K) (E11 K)] at hf
  rw [TensorProduct.tmul_add (E11 K) (E00 K) (E11 K)] at hf
  -- apply map_add to unfold f on the sum
  have hf' : f (E00 K ⊗ₜ[K] E00 K) + f (E00 K ⊗ₜ[K] E11 K) + f (E11 K ⊗ₜ[K] E00 K) + f (E11 K ⊗ₜ[K] E11 K)
      = f (E00 K ⊗ₜ[K] E00 K) + f (E11 K ⊗ₜ[K] E11 K) := by
    simpa [f, map_add, add_assoc, add_left_comm] using hf
  rw [show f (E00 K ⊗ₜ[K] E00 K) = (0 : K) by simp [f, broadcastFunctional_tmul, E00, E11],
      show f (E00 K ⊗ₜ[K] E11 K) = (1 : K) by simp [f, broadcastFunctional_tmul, E00, E11],
      show f (E11 K ⊗ₜ[K] E00 K) = (0 : K) by simp [f, broadcastFunctional_tmul, E00, E11],
      show f (E11 K ⊗ₜ[K] E11 K) = (0 : K) by simp [f, broadcastFunctional_tmul, E00, E11]] at hf'
  have h1eq0 : (1 : K) = 0 := by simpa using hf'
  exact one_ne_zero h1eq0

end

end QM
