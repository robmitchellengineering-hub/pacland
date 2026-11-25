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

/-- **Every finite tree has a closed walk visiting every vertex with length at most `2·(n−1)`** —
the Euler-tour bound. Strong induction on the vertex count: peel a leaf `ℓ` (degree 1), get the tour
on the remaining vertices by induction, splice in the excursion `p → ℓ → p` at `ℓ`'s unique neighbor
`p`, adding exactly 2 to the length. -/
theorem tree_euler_tour_length {V : Type u} [Fintype V] [DecidableEq V] [Nonempty V]
    (G : SimpleGraph V) [DecidableRel G.Adj] [Fintype G.edgeSet] (hG : G.IsTree) :
    ∃ v : V, ∃ w : G.Walk v v, (∀ x : V, x ∈ w.support) ∧ w.length ≤ 2 * (Fintype.card V - 1) := by
  classical
  have hmain : ∀ (m : ℕ) (V' : Type u) [Fintype V'] [DecidableEq V'] [Nonempty V']
      (G' : SimpleGraph V') [DecidableRel G'.Adj] [Fintype G'.edgeSet],
      Fintype.card V' = m → G'.IsTree →
      ∃ v : V', ∃ w : G'.Walk v v, (∀ x : V', x ∈ w.support) ∧ w.length ≤ 2 * (m - 1) := by
    intro m
    induction m using Nat.strong_induction_on with
    | h n ih =>
      intro V' _ _ _ G' _ _ hcard hTree
      by_cases hn1 : n = 1
      · have hcard1 : Fintype.card V' = 1 := by simpa [hn1] using hcard
        obtain ⟨x, hx⟩ := Fintype.card_eq_one_iff.mp hcard1
        refine ⟨x, SimpleGraph.Walk.nil, ?_, ?_⟩
        · intro y
          simpa [SimpleGraph.Walk.support_nil] using hx y
        · simp [hn1]
      · have hcard_pos : 0 < Fintype.card V' := Fintype.card_pos
        have h1lt : 1 < n := by omega
        haveI : Nontrivial V' :=
          Fintype.one_lt_card_iff_nontrivial.mp (by simpa [hcard] using h1lt)
        obtain ⟨ℓ, hdeg⟩ := hTree.exists_vert_degree_one_of_nontrivial
        obtain ⟨p, hadj, _⟩ := SimpleGraph.degree_eq_one_iff_existsUnique_adj.mp hdeg
        have hpne : p ≠ ℓ := G'.ne_of_adj hadj.symm
        haveI : Nonempty ({ℓ}ᶜ : Set V') := ⟨⟨p, by simpa using hpne⟩⟩
        have hTree' : (G'.induce ({ℓ}ᶜ : Set V')).IsTree :=
          ⟨hTree.connected.induce_compl_singleton_of_degree_eq_one hdeg,
            hTree.isAcyclic.induce ({ℓ}ᶜ : Set V')⟩
        have hsing : Fintype.card ({ℓ} : Set V') = 1 := by
          rw [Fintype.card_eq_one_iff]
          refine ⟨⟨ℓ, by simp⟩, ?_⟩
          intro y
          apply Subtype.ext
          exact Set.mem_singleton_iff.mp y.2
        have hcard' : Fintype.card ({ℓ}ᶜ : Set V') = n - 1 := by
          rw [Fintype.card_compl_set ({ℓ} : Set V')]
          rw [hsing]
          rw [hcard]
        obtain ⟨v', w', hvisit', hlen'⟩ :=
          ih (n - 1) (by omega) ({ℓ}ᶜ : Set V') (G'.induce ({ℓ}ᶜ : Set V')) hcard' hTree'
        let f : (G'.induce ({ℓ}ᶜ : Set V')) →g G' :=
          { toFun := fun v => (v : V'),
            map_rel' := by intro a b h; simpa using h }
        let wlift : G'.Walk (v' : V') (v' : V') := w'.map f
        have hp_mem : (p : V') ∈ wlift.support := by
          dsimp [wlift]
          rw [SimpleGraph.Walk.support_map]
          exact List.mem_map_of_mem (f := ⇑f) (hvisit' ⟨p, by simpa using hpne⟩)
        obtain ⟨a, b, hab⟩ := SimpleGraph.Walk.mem_support_iff_exists_append.mp hp_mem
        let exc : G'.Walk p p := hadj.symm.toWalk.append hadj.toWalk
        let wfinal : G'.Walk (v' : V') (v' : V') := (a.append exc).append b
        refine ⟨(v' : V'), wfinal, ?_, ?_⟩
        · intro x
          by_cases hxℓ : x = ℓ
          · subst x
            have hℓexc : ℓ ∈ exc.support := by
              simp [exc, SimpleGraph.Walk.support_append, SimpleGraph.Adj.support_toWalk]
            have hℓmid : ℓ ∈ (a.append exc).support :=
              SimpleGraph.Walk.support_subset_support_append_right a exc hℓexc
            exact SimpleGraph.Walk.support_subset_support_append_left (a.append exc) b hℓmid
          · have hx_sub : (⟨x, by simpa using hxℓ⟩ : ({ℓ}ᶜ : Set V')) ∈ w'.support :=
              hvisit' ⟨x, by simpa using hxℓ⟩
            have hx_lift : x ∈ wlift.support := by
              dsimp [wlift]
              rw [SimpleGraph.Walk.support_map]
              exact List.mem_map_of_mem (f := ⇑f) hx_sub
            have hx_ab : x ∈ a.support ∨ x ∈ b.support.tail := by
              have h : x ∈ (a.append b).support := by simpa [hab] using hx_lift
              simpa [SimpleGraph.Walk.support_append] using h
            rcases hx_ab with hxa | hxb
            · have hxmid : x ∈ (a.append exc).support :=
                SimpleGraph.Walk.support_subset_support_append_left a exc hxa
              exact SimpleGraph.Walk.support_subset_support_append_left (a.append exc) b hxmid
            · have hxb_full : x ∈ b.support := List.tail_subset b.support hxb
              exact SimpleGraph.Walk.support_subset_support_append_right (a.append exc) b hxb_full
        · have hab_len : a.length + b.length = w'.length := by
            have h1 : (a.append b).length = wlift.length := by rw [← hab]
            rw [SimpleGraph.Walk.length_append] at h1
            have h2 : wlift.length = w'.length := by
              dsimp [wlift]
              simp
            omega
          have hlen_eq : wfinal.length = w'.length + 2 := by
            simp [wfinal, exc, SimpleGraph.Walk.length_append, SimpleGraph.Adj.length_toWalk]
            omega
          rw [hlen_eq]
          omega
  exact hmain (Fintype.card V) V G rfl hG

/-- **A connected induced subset of a tree has a tour** — every vertex of `S` is visited by a closed
walk of length `≤ 2·(|S|−1)`. Direct consequence of `tree_euler_tour_length` on the induced subtree,
lifted back to `G` by the subtype embedding. -/
theorem connected_subset_tour {V : Type u} [Fintype V] [DecidableEq V]
    (G : SimpleGraph V) [DecidableRel G.Adj] [Fintype G.edgeSet] (hG : G.IsTree)
    (S : Finset V) (hconn : (G.induce (S : Set V)).Connected) (hS : S.Nonempty) :
    ∃ r : V, ∃ w : G.Walk r r, (∀ x ∈ S, x ∈ w.support) ∧ w.length ≤ 2 * (S.card - 1) := by
  classical
  have htree : (G.induce (S : Set V)).IsTree :=
    ⟨hconn, hG.isAcyclic.induce (S : Set V)⟩
  haveI : Nonempty (S : Set V) := ⟨⟨hS.choose, hS.choose_spec⟩⟩
  obtain ⟨v, w, hw, hl⟩ := tree_euler_tour_length (G.induce (S : Set V)) htree
  let f : (G.induce (S : Set V)) →g G :=
    { toFun := fun v => (v : V), map_rel' := by intro a b h; simpa using h }
  let wlift : G.Walk (v : V) (v : V) := w.map f
  refine ⟨(v : V), wlift, ?_, ?_⟩
  · intro x hx
    dsimp [wlift]
    rw [SimpleGraph.Walk.support_map]
    exact List.mem_map_of_mem (f := ⇑f) (hw ⟨x, hx⟩)
  · dsimp [wlift]
    rw [SimpleGraph.Walk.length_map]
    have hcard : Fintype.card (S : Set V) = S.card := by
      simp [Fintype.card_coe]
    rw [hcard] at hl
    exact hl

/-- **A tree has a rooted tour** — a closed walk starting and ending at any prescribed root `r`,
visiting every vertex, of length `≤ 2·(n−1)`. Obtained by rotating `tree_euler_tour_length`'s tour
to start at `r`. -/
theorem rooted_tree_tour {V : Type u} [Fintype V] [DecidableEq V] [Nonempty V]
    (G : SimpleGraph V) [DecidableRel G.Adj] [Fintype G.edgeSet] (hG : G.IsTree) (r : V) :
    ∃ w : G.Walk r r, (∀ x : V, x ∈ w.support) ∧ w.length ≤ 2 * (Fintype.card V - 1) := by
  classical
  obtain ⟨v, w, hw, hl⟩ := tree_euler_tour_length G hG
  have hr_mem : r ∈ w.support := hw r
  obtain ⟨q, r', hwq⟩ := SimpleGraph.Walk.mem_support_iff_exists_append.mp hr_mem
  let wrot : G.Walk r r := r'.append q
  refine ⟨wrot, ?_, ?_⟩
  · intro x
    have hx : x ∈ w.support := hw x
    dsimp [wrot]
    rw [SimpleGraph.Walk.support_append, List.mem_append]
    have this : x ∈ q.support ∨ x ∈ r'.support.tail := by
      have h : x ∈ (q.append r').support := by simpa [hwq] using hx
      simpa [SimpleGraph.Walk.support_append, List.mem_append] using h
    rcases this with hxq | hxr
    · by_cases hxv : x = v
      · subst x; left; exact SimpleGraph.Walk.end_mem_support r'
      · right
        exact (List.mem_cons.mp (by simpa using hxq)).resolve_left hxv
    · left; exact List.tail_subset r'.support hxr
  · dsimp [wrot]
    rw [SimpleGraph.Walk.length_append]
    have hlen : q.length + r'.length = w.length := by
      have : (q.append r').length = w.length := congrArg (fun p : G.Walk v v => p.length) hwq.symm
      simpa [SimpleGraph.Walk.length_append] using this
    omega

/-- **A rooted connected subset has a rooted tour** — for `r ∈ S` connected, there is a closed walk from
`r` visiting every `x ∈ S` with length `≤ 2·(|S|−1)`. `rooted_tree_tour` on the induced subtree, lifted. -/
theorem rooted_subset_tour {V : Type u} [Fintype V] [DecidableEq V]
    (G : SimpleGraph V) [DecidableRel G.Adj] [Fintype G.edgeSet] (hG : G.IsTree)
    (S : Finset V) (hconn : (G.induce (S : Set V)).Connected) (r : V) (hr : r ∈ S) :
    ∃ w : G.Walk r r, (∀ x, x ∈ w.support ↔ x ∈ S) ∧ w.length ≤ 2 * (S.card - 1) := by
  classical
  have htree : (G.induce (S : Set V)).IsTree := ⟨hconn, hG.isAcyclic.induce (S : Set V)⟩
  haveI : Nonempty (S : Set V) := ⟨⟨r, hr⟩⟩
  obtain ⟨w, hw, hl⟩ := rooted_tree_tour (G.induce (S : Set V)) htree ⟨r, hr⟩
  let f : (G.induce (S : Set V)) →g G :=
    { toFun := fun v => (v : V), map_rel' := by intro a b h; simpa using h }
  let wlift : G.Walk r r := w.map f
  refine ⟨wlift, ?_, ?_⟩
  · intro x
    constructor
    · intro hx
      dsimp [wlift] at hx
      rw [SimpleGraph.Walk.support_map] at hx
      obtain ⟨s, hs, hfs⟩ := List.mem_map.mp hx
      have hx' : s.1 = x := by simpa [f] using hfs
      simpa [hx'] using s.2
    · intro hx
      dsimp [wlift]
      rw [SimpleGraph.Walk.support_map]
      exact List.mem_map_of_mem (f := ⇑f) (hw ⟨x, hx⟩)
  · dsimp [wlift]
    rw [SimpleGraph.Walk.length_map]
    have hcard : Fintype.card (S : Set V) = S.card := by simp [Fintype.card_coe]
    rw [hcard] at hl
    exact hl

/-- **The rooted-animals count** — rooted connected induced subsets of size `n` inject into rooted closed
walks of length `≤ 2(n−1)`, which `walk_count_bound` bounds. The `2·n` factor is the geometric-sum
constant and `Δ+1` absorbs the zero-degree edge; the exponent `2(n−1)` is the Euler-tour length. -/
theorem rooted_animals_count_bound {V : Type u} [Fintype V] [DecidableEq V]
    (G : SimpleGraph V) [DecidableRel G.Adj] [Fintype G.edgeSet] (hG : G.IsTree)
    (r : V) (Δ : ℕ) (hΔ : G.maxDegree ≤ Δ) (n : ℕ) :
    ((Finset.univ.filter (fun S : Finset V => r ∈ S ∧ (G.induce (S : Set V)).Connected ∧ S.card = n)).card : ℕ)
      ≤ (2*n) * (Δ+1)^(2*(n-1)) := by
  classical
  let T : Finset (Finset V) :=
    Finset.univ.filter (fun S : Finset V => r ∈ S ∧ (G.induce (S : Set V)).Connected ∧ S.card = n)
  let tour (S : Finset V) (hconn : (G.induce (S : Set V)).Connected) (hr : r ∈ S) : G.Walk r r :=
    Classical.choose (rooted_subset_tour G hG S hconn r hr)
  let W : Finset (G.Walk r r) :=
    (Finset.range (2*(n-1)+1)).biUnion (fun L => G.finsetWalkLength L r r)
  by_cases hn0 : n = 0
  · subst n
    have hT : T.card = 0 := by
      by_contra h
      have hnon : T.Nonempty := Finset.card_pos.mp (Nat.pos_of_ne_zero h)
      obtain ⟨S, hS⟩ := hnon
      have hcard0 : S.card = 0 := (Finset.mem_filter.mp hS).2.2.2
      have hS0 : S = ∅ := Finset.card_eq_zero.mp hcard0
      have hr : r ∈ S := (Finset.mem_filter.mp hS).2.1
      simpa [hS0] using hr
    rw [hT]
    simp
  · have mem_spec : ∀ S : {S : Finset V // S ∈ T},
        r ∈ S.1 ∧ (G.induce (S.1 : Set V)).Connected ∧ S.1.card = n := by
      intro S
      exact (Finset.mem_filter.mp S.property).2
    have hinj : Function.Injective (fun S : {S : Finset V // S ∈ T} => tour S.1 (mem_spec S).2.1 (mem_spec S).1) := by
      intro S₁ S₂ hw
      apply Subtype.ext
      apply Finset.ext
      intro x
      have h₁ : x ∈ (tour S₁.1 (mem_spec S₁).2.1 (mem_spec S₁).1).support ↔ x ∈ S₁.1 :=
        (Classical.choose_spec (rooted_subset_tour G hG S₁.1 (mem_spec S₁).2.1 r (mem_spec S₁).1)).1 x
      have h₂ : x ∈ (tour S₂.1 (mem_spec S₂).2.1 (mem_spec S₂).1).support ↔ x ∈ S₂.1 :=
        (Classical.choose_spec (rooted_subset_tour G hG S₂.1 (mem_spec S₂).2.1 r (mem_spec S₂).1)).1 x
      have hsupp : (tour S₁.1 (mem_spec S₁).2.1 (mem_spec S₁).1).support =
                   (tour S₂.1 (mem_spec S₂).2.1 (mem_spec S₂).1).support := by simpa [hw]
      rw [hsupp] at h₁
      exact h₁.symm.trans h₂
    let f : Finset V → G.Walk r r := fun S =>
      if hS : S ∈ T then tour S (mem_spec ⟨S, hS⟩).2.1 (mem_spec ⟨S, hS⟩).1 else SimpleGraph.Walk.nil
    have hcard : T.card ≤ W.card := Finset.card_le_card_of_injOn f
      (by
        intro a ha
        simp only [f]
        split_ifs with hS
        · have hlen : (tour a (mem_spec ⟨a, hS⟩).2.1 (mem_spec ⟨a, hS⟩).1).length ≤ 2*(n-1) := by
            have := (Classical.choose_spec (rooted_subset_tour G hG a (mem_spec ⟨a, hS⟩).2.1 r (mem_spec ⟨a, hS⟩).1)).2
            simpa [tour, (mem_spec ⟨a, hS⟩).2.2] using this
          have hlt : (tour a (mem_spec ⟨a, hS⟩).2.1 (mem_spec ⟨a, hS⟩).1).length < 2*(n-1)+1 := by omega
          exact Finset.mem_biUnion.mpr ⟨(tour a (mem_spec ⟨a, hS⟩).2.1 (mem_spec ⟨a, hS⟩).1).length,
            by simpa using hlt, by simpa [G.mem_finsetWalkLength_iff]⟩
        · exfalso; exact hS ha)
      (by
        intro a ha b hb h
        have hfa : f a = tour a (mem_spec ⟨a, ha⟩).2.1 (mem_spec ⟨a, ha⟩).1 := by
          dsimp [f]
          exact dif_pos ha
        have hfb : f b = tour b (mem_spec ⟨b, hb⟩).2.1 (mem_spec ⟨b, hb⟩).1 := by
          dsimp [f]
          exact dif_pos hb
        have hf : tour a (mem_spec ⟨a, ha⟩).2.1 (mem_spec ⟨a, ha⟩).1 =
                  tour b (mem_spec ⟨b, hb⟩).2.1 (mem_spec ⟨b, hb⟩).1 := by
          rw [hfa, hfb] at h
          exact h
        have ha' : a ∈ T := by simpa using ha
        have hb' : b ∈ T := by simpa using hb
        exact (congrArg Subtype.val (@hinj (Subtype.mk a ha') (Subtype.mk b hb') hf)))
    have hW : W.card ≤ ∑ L ∈ Finset.range (2*(n-1)+1), (G.finsetWalkLength L r r).card := by
      dsimp [W]
      exact Finset.card_biUnion_le
    have hsum : (∑ L ∈ Finset.range (2*(n-1)+1), (G.finsetWalkLength L r r).card)
                ≤ (2*n) * (Δ+1)^(2*(n-1)) := by
      have hΔ1 : 1 ≤ Δ+1 := Nat.succ_le_succ (Nat.zero_le Δ)
      have hle : ∀ L ∈ Finset.range (2*(n-1)+1), (G.finsetWalkLength L r r).card ≤ (Δ+1)^(2*(n-1)) := by
        intro L hL
        have hLb : L ≤ 2*(n-1) := by simpa using hL
        have hw : (G.finsetWalkLength L r r).card ≤ G.maxDegree ^ L := walk_count_bound G r r L
        have hΔL : G.maxDegree ^ L ≤ Δ ^ L := Nat.pow_le_pow_left hΔ L
        have hΔL' : Δ ^ L ≤ (Δ+1) ^ L := Nat.pow_le_pow_left (Nat.le_succ Δ) L
        have hLΔ : (Δ+1) ^ L ≤ (Δ+1) ^ (2*(n-1)) := pow_le_pow_right' hΔ1 hLb
        exact (hw.trans hΔL).trans (hΔL'.trans hLΔ)
      exact (Finset.sum_le_sum hle).trans (by
        have hle2 : (Finset.range (2*(n-1)+1)).card ≤ 2*n := by
          simp only [Finset.card_range]
          omega
        calc
          (∑ _L ∈ Finset.range (2*(n-1)+1), (Δ+1)^(2*(n-1))) = (Finset.range (2*(n-1)+1)).card * (Δ+1)^(2*(n-1)) := by simp
          _ ≤ (2*n) * (Δ+1)^(2*(n-1)) := Nat.mul_le_mul_right _ hle2)
    exact hcard.trans (hW.trans hsum)

/-- **A connected induced subset of an ARBITRARY finite graph has a tour** — the spanning-tree
reduction: `Connected.exists_isTree_le` gives a spanning tree `T ≤ G.induce S`, whose Euler tour lifts to
`G.induce S` (the subgraph inclusion) and then to `G` (the subtype embedding), length `≤ 2·(|S|−1)`. -/
theorem connected_subset_tour_gen {V : Type u} [Fintype V] [DecidableEq V]
    (G : SimpleGraph V) [DecidableRel G.Adj] [Fintype G.edgeSet]
    (S : Finset V) (hconn : (G.induce (S : Set V)).Connected) (hS : S.Nonempty) :
    ∃ r : V, ∃ w : G.Walk r r, (∀ x, x ∈ w.support ↔ x ∈ S) ∧ w.length ≤ 2 * (S.card - 1) := by
  classical
  obtain ⟨T, hTle, hTtree⟩ := hconn.exists_isTree_le
  haveI : Nonempty (S : Set V) := ⟨⟨hS.choose, hS.choose_spec⟩⟩
  obtain ⟨v, w, hw, hl⟩ := tree_euler_tour_length T hTtree
  let fT : T →g (G.induce (S : Set V)) :=
    { toFun := fun v => v, map_rel' := by intro a b hab; exact hTle hab }
  let wlift : (G.induce (S : Set V)).Walk v v := w.map fT
  let f : (G.induce (S : Set V)) →g G :=
    { toFun := fun v => (v : V), map_rel' := by intro a b h; simpa using h }
  let wG : G.Walk (v : V) (v : V) := wlift.map f
  refine ⟨(v : V), wG, ?_, ?_⟩
  · intro x
    constructor
    · intro hx
      dsimp [wG, wlift] at hx
      rw [SimpleGraph.Walk.support_map, SimpleGraph.Walk.support_map] at hx
      obtain ⟨s, _hs, hfs⟩ := List.mem_map.mp hx
      have hs1 : s.1 = x := by simpa [f] using hfs
      simpa [hs1] using s.2
    · intro hx
      dsimp [wG, wlift]
      rw [SimpleGraph.Walk.support_map, SimpleGraph.Walk.support_map]
      exact List.mem_map_of_mem (f := ⇑f) (List.mem_map_of_mem (f := ⇑fT) (hw ⟨x, hx⟩))
  · dsimp [wG, wlift]
    rw [SimpleGraph.Walk.length_map, SimpleGraph.Walk.length_map]
    have hcard : Fintype.card (S : Set V) = S.card := by simp [Fintype.card_coe]
    rw [hcard] at hl
    exact hl

end QM
