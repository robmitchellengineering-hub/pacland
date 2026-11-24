import Mathlib
import PaclandProof.QM.FullLattice

namespace QM
open scoped BigOperators

/-- **A connected graph has a walk visiting every vertex** — the existence half of the Euler tour
(the depth-first traversal). The proof is the `Finset` induction over the vertices, appending the
unique connecting path at each step (via `Connected.exists_isPath`). -/
theorem connected_exists_visiting_walk {V : Type*} [Fintype V] [DecidableEq V] [Nonempty V]
    (G : SimpleGraph V) [DecidableRel G.Adj] (hG : G.Connected) :
    ∃ v : V, ∃ w : G.Walk v v, ∀ x : V, x ∈ w.support := by
  classical
  let v₀ : V := Classical.choice inferInstance
  refine ⟨v₀, ?_⟩
  -- the induction over the finite set of vertices: build a walk through any finite set containing v₀
  have hwalk : ∀ s : Finset V, v₀ ∈ s → ∃ w : G.Walk v₀ v₀, ∀ x ∈ s, x ∈ w.support := by
    intro s hv₀
    induction s using Finset.induction_on with
    | empty => exact False.elim (Finset.not_mem_empty v₀ hv₀)
    | insert a s ha ih =>
      by_cases hav : a = v₀
      · subst a
        -- the inserted element is v₀ itself; extend the walk over s (v₀ ∈ s by the induction's hv₀)
        obtain ⟨w, hw⟩ := ih (by simpa using hv₀)
        exact ⟨w, fun x hx => by
          by_cases hxv : x = v₀
          · subst x; exact w.start_mem_support
          · exact hw x (by simpa [hxv] using hx)⟩
      · -- append the path v₀ → a → v₀
        obtain ⟨w, hw⟩ := ih (by simpa using hv₀)
        obtain ⟨p₁, _⟩ := hG.exists_isPath v₀ a
        let w' : G.Walk v₀ v₀ := w.append (p₁.append p₁.reverse)
        refine ⟨w', fun x hx => ?_⟩
        rw [support_append, List.mem_append]
        by_cases hxa : x = a
        · subst x
          right
          rw [support_append]
          simp [SimpleGraph.Walk.end_mem_support p₁]
        · left
          exact hw x (by simpa [hxa] using hx)
  obtain ⟨w, hw⟩ := hwalk Finset.univ (by simp)
  exact ⟨w, fun x => hw x (Finset.mem_univ x)⟩

end QM
