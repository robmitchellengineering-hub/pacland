import Mathlib
import PaclandProof.QM.FullLattice

namespace QM
open scoped BigOperators

/-- **A connected graph has a walk visiting every vertex** — the existence half of the Euler tour.
Built by `Finset` induction: append, for each new vertex `a`, the path `v₀ → a → v₀`. -/
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
      exact ⟨SimpleGraph.Walk.nil, by intro x hx; simp at hx⟩
    | insert a s ha ih =>
      obtain ⟨w, hw⟩ := ih
      by_cases hav : a = v₀
      · subst a
        exact ⟨w, fun x hx => by
          by_cases hxv : x = v₀
          · subst x; exact SimpleGraph.Walk.start_mem_support w
          · exact hw x (by simpa [hxv] using hx)⟩
      · obtain ⟨p₁, _⟩ := hG.exists_isPath v₀ a
        let w' : G.Walk v₀ v₀ := w.append (p₁.append p₁.reverse)
        refine ⟨w', fun x hx => ?_⟩
        rw [SimpleGraph.Walk.support_append, List.mem_append]
        by_cases hxa : x = a
        · subst x
          right
          simpa [SimpleGraph.Walk.support_append] using (show a ∈ p₁.support.tail ∨ a ∈ p₁.support.dropLast by
            exact Or.inl (by
              have hmem := SimpleGraph.Walk.end_mem_support p₁
              have hcons : p₁.support = v₀ :: p₁.support.tail := by
                cases p₁ with
                | nil => simp [SimpleGraph.Walk.support] at hav
                | cons h p => rfl
              rw [hcons, List.mem_cons] at hmem
              exact hmem.resolve_left hav))
        · left
          exact hw x (by simpa [hxa] using hx)
  obtain ⟨w, hw⟩ := hwalk Finset.univ
  exact ⟨w, fun x => hw x (Finset.mem_univ x)⟩

end QM
