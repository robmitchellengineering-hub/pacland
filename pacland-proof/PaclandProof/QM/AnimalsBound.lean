import Mathlib
import PaclandProof.QM.FullLattice

namespace QM
open scoped BigOperators

/-- **A connected graph has a walk visiting every vertex** — the existence half of the Euler tour.
The walk is built by `Finset` induction: append, for each new vertex `a`, the connecting path
`v₀ → a → v₀` (via `Connected.exists_isPath`). -/
theorem connected_exists_visiting_walk {V : Type*} [Fintype V] [DecidableEq V] [Nonempty V]
    (G : SimpleGraph V) [DecidableRel G.Adj] (hG : G.Connected) :
    ∃ v : V, ∃ w : G.Walk v v, ∀ x : V, x ∈ w.support := by
  classical
  let v₀ : V := Classical.choice inferInstance
  refine ⟨v₀, ?_⟩
  have hwalk : ∀ s : Finset V, ∃ w : G.Walk v₀ v₀, ∀ x ∈ s, x ∈ w.support := by
    intro s
    induction s using Finset.induction_on with
    | empty =>
      exact ⟨SimpleGraph.Walk.nil, by intro x hx; exact (Finset.not_mem_empty x hx).elim⟩
    | insert a s ha ih =>
      obtain ⟨w, hw⟩ := ih
      obtain ⟨p₁, _⟩ := hG.exists_isPath v₀ a
      let w' : G.Walk v₀ v₀ := w.append (p₁.append p₁.reverse)
      refine ⟨w', fun x hx => ?_⟩
      rw [SimpleGraph.Walk.support_append, List.mem_append]
      by_cases hxa : x = a
      · subst x
        right
        rw [SimpleGraph.Walk.support_append]
        exact List.mem_append.mpr (Or.inl (SimpleGraph.Walk.end_mem_support p₁))
      · left
        exact hw x (by simpa [hxa] using hx)
  obtain ⟨w, hw⟩ := hwalk Finset.univ
  exact ⟨w, fun x => hw x (Finset.mem_univ x)⟩

end QM
