import Mathlib

/-!
# The Stern-Brocot tree — the fix for the QI map's boundary collapse

The binary-expansion angle `pathAngle s = Σ sᵢ · 2⁻ⁱ⁻¹` used by `treeToH2` in
`PaclandProof/QM/HyperbolicPlane.lean` is **not** a quasi-isometry: its boundary is the Cantor set,
and it has the dyadic collapse `0.0111…₂ = 0.1000…₂` — two far-apart branches converge to the same
angle. This file is the fix: the **Stern-Brocot** encoding of the same binary tree, in which a path
maps to a *rational* `p/q` by the mediant rule, and the boundary is `ℚ ∪ {∞}` — the circle — with no
collapse.

The map is exactly the **Calkin–Wilf tree**: root `1/1`; a node `p/q` has left child `p/(p+q)` and
right child `(p+q)/q`. Every positive rational appears *exactly once*, in lowest terms. The three
facts proven here are the ones that make it the fix:

* **reduced** — `rational_coprime` / `rational_reduced`: every Stern-Brocot rational is in lowest
  terms;
* **injective** — `rational_injective`: the binary-expansion collapse is eliminated — distinct paths
  give distinct rationals, in fact even across different depths (so *a fortiori* at equal depth);
* **boundary = circle** — `rational_existsUnique`: every positive reduced rational is hit by exactly
  one path, a bijection between the tree and the positive rationals (the circle).

Follow-up (not attempted here): define the corrected map to H². A path `s` carries a word
`word(s) = s₁ ⋯ sₙ` in the generators `L(z) = z/(z+1)` and `R(z) = z+1` (PSL(2,ℤ)); the rational
`rational s` is exactly `word(s) · ∞`, and the vertex `s` maps into H² via the Möbius orbit
`word(s) · i`. Proving that this map is a quasi-isometry (the Švarc–Milnor step) is the follow-up;
this file supplies the boundary bijection that the binary expansion lacked.
-/

namespace SternBrocot

/-- One Stern-Brocot mediant step: `true` is the right child `(p+q)/q`, `false` is the left child
`p/(p+q)`. -/
def step : Bool → ℕ × ℕ → ℕ × ℕ
  | false, pq => (pq.1, pq.1 + pq.2)
  | true, pq => (pq.1 + pq.2, pq.2)

/-- The Stern-Brocot rational of a tree path. The empty path is the root `1/1`; for `b :: t` the
head bit `b` is applied *on top of* the tail, i.e. `rational = List.foldr step (1,1)` (a path is
read right-to-left as a descent from the root). This is definitionally the mediant fold
`let (p, q) := rational t in if b then (p + q, q) else (p, p + q)`. -/
def rational : List Bool → ℕ × ℕ
  | [] => (1, 1)
  | b :: t => step b (rational t)

/-! ### The defining examples -/

example : rational [false] = (1, 2) := by decide
example : rational [true] = (2, 1) := by decide
example : rational [false, true] = (2, 3) := by decide
example : rational [true, false] = (3, 2) := by decide

/-! ### Positivity and the reduced (coprime) fact -/

/-- Every Stern-Brocot rational is strictly positive in both coordinates. -/
theorem rational_pos (s : List Bool) : 0 < (rational s).1 ∧ 0 < (rational s).2 := by
  induction s with
  | nil => simp [rational]
  | cons b t ih =>
      cases b <;> simp [rational, step] <;> omega

/-- The `true` child always has numerator greater than denominator. -/
theorem rational_true_gt (t : List Bool) : (rational (true :: t)).1 > (rational (true :: t)).2 := by
  have h := rational_pos t
  simp [rational, step]
  omega

/-- The `false` child always has numerator less than denominator. -/
theorem rational_false_lt (t : List Bool) :
    (rational (false :: t)).1 < (rational (false :: t)).2 := by
  have h := rational_pos t
  simp [rational, step]
  omega

/-- **Reduced.** Every Stern-Brocot rational is in lowest terms: `gcd p q = 1` for `rational s =
(p, q)`. The mediant step preserves coprimality (`gcd p q = gcd p (p+q) = gcd (p+q) q`). -/
theorem rational_coprime (s : List Bool) : Nat.Coprime (rational s).1 (rational s).2 := by
  induction s with
  | nil => simp [rational]
  | cons b t ih => cases b <;> simpa [rational, step] using ih

/-- **Reduced** (explicit form): if a path hits `(p, q)` then `p` and `q` are coprime. -/
theorem rational_reduced {s : List Bool} {p q : ℕ} (h : rational s = (p, q)) : Nat.Coprime p q := by
  have hp : (rational s).1 = p := congrArg Prod.fst h
  have hq : (rational s).2 = q := congrArg Prod.snd h
  rw [← hp, ← hq]
  exact rational_coprime s

/-! ### Injectivity (no collapse) -/

/-- A nonempty path never maps to the root `(1, 1)`. -/
theorem rational_cons_ne_root (b : Bool) (t : List Bool) : rational (b :: t) ≠ (1, 1) := by
  intro h
  cases b <;> simp only [rational, step] at h
  · have hpos := rational_pos t
    have hfst : (rational t).1 = 1 := congrArg Prod.fst h
    have hsnd : (rational t).1 + (rational t).2 = 1 := congrArg Prod.snd h
    omega
  · have hpos := rational_pos t
    have hfst : (rational t).1 + (rational t).2 = 1 := congrArg Prod.fst h
    have hsnd : (rational t).2 = 1 := congrArg Prod.snd h
    omega

/-- Peeling one step: if `rational (b :: s) = rational (c :: t)` then `b = c` (the child direction
is determined by whether the value is greater or less than `1`) and the parents agree. This is the
Euclidean-algorithm inverse of the mediant rule. -/
theorem rational_cons_inj (b c : Bool) {s t : List Bool}
    (h : rational (b :: s) = rational (c :: t)) : b = c ∧ rational s = rational t := by
  cases b with
  | false =>
      cases c with
      | false =>
          simp only [rational, step] at h
          injection h with hp hsum
          constructor
          · rfl
          · have hq : (rational s).2 = (rational t).2 := by omega
            exact Prod.ext hp hq
      | true =>
          simp only [rational, step] at h
          injection h with hf hsn
          have hp := rational_pos s
          have hq := rational_pos t
          omega
  | true =>
      cases c with
      | false =>
          simp only [rational, step] at h
          injection h with hf hsn
          have hp := rational_pos s
          have hq := rational_pos t
          omega
      | true =>
          simp only [rational, step] at h
          injection h with hsum hq
          constructor
          · rfl
          · have hp : (rational s).1 = (rational t).1 := by omega
            exact Prod.ext hp hq

/-- **Injective.** Distinct paths give distinct rationals — the collapse `0.0111…₂ = 0.1000…₂` of
the binary expansion is eliminated. (Stronger than the same-length statement: it holds across all
depths, since the Stern-Brocot / Calkin–Wilf tree hits each positive rational at most once.) -/
theorem rational_injective {s t : List Bool} (h : rational s = rational t) : s = t := by
  induction s generalizing t with
  | nil =>
      cases t with
      | nil => rfl
      | cons c t' =>
          have hne : rational (c :: t') ≠ (1, 1) := rational_cons_ne_root c t'
          exact (hne (by simpa [rational] using h.symm)).elim
  | cons b s' ih =>
      cases t with
      | nil =>
          have hne : rational (b :: s') ≠ (1, 1) := rational_cons_ne_root b s'
          exact (hne (by simpa [rational] using h)).elim
      | cons c t' =>
          obtain ⟨hbc, hst⟩ := rational_cons_inj b c h
          subst c
          rw [ih hst]

/-- **Injective at equal depth** (the property that directly rules out the dyadic collapse). -/
theorem rational_injective_of_same_length {s t : List Bool} (h : rational s = rational t)
    (_hl : s.length = t.length) : s = t :=
  rational_injective h

/-! ### Boundary = circle (every reduced rational, exactly once) -/

/-- **Surjective.** Every positive reduced rational `p/q` is the Stern-Brocot rational of some path,
via the Euclidean algorithm / continued-fraction descent. -/
theorem rational_surjective (p q : ℕ) (hp : 0 < p) (hq : 0 < q) (hcop : Nat.Coprime p q) :
    ∃ s : List Bool, rational s = (p, q) := by
  induction h : p + q using Nat.strong_induction_on generalizing p q with
  | h n ih =>
      subst h
      by_cases hpq : p = q
      · -- p = q = 1 (coprime forces it)
        have hp1 : p = 1 := by
          simpa [hpq, Nat.gcd_self] using hcop
        subst p
        subst q
        exact ⟨[], rfl⟩
      · -- p ≠ q
        rcases (by omega : q < p ∨ p < q) with hgt | hlt
        · -- q < p: the parent is (p - q, q), reached by a `true` step
          have hp_sub : 0 < p - q := by omega
          have hcop' : Nat.Coprime (p - q) q := by
            have h' : (p - q) + q = p := by omega
            have hbase : Nat.Coprime ((p - q) + q) q := by simpa [h'] using hcop
            exact (Nat.coprime_add_self_left (m := p - q) (n := q)).mp hbase
          have hlt_sum : (p - q) + q < p + q := by omega
          obtain ⟨s', hs'⟩ := ih ((p - q) + q) hlt_sum (p - q) q hp_sub hq hcop' rfl
          refine ⟨true :: s', ?_⟩
          simp [rational, step, hs']
          omega
        · -- p < q: the parent is (p, q - p), reached by a `false` step
          have hq_sub : 0 < q - p := by omega
          have hcop' : Nat.Coprime p (q - p) := by
            have h' : (q - p) + p = q := by omega
            have hbase : Nat.Coprime p ((q - p) + p) := by simpa [h'] using hcop
            exact (Nat.coprime_add_self_right (m := p) (n := q - p)).mp hbase
          have hlt_sum : p + (q - p) < p + q := by omega
          obtain ⟨s', hs'⟩ := ih (p + (q - p)) hlt_sum p (q - p) hp hq_sub hcop' rfl
          refine ⟨false :: s', ?_⟩
          simp [rational, step, hs']
          omega

/-- **Boundary = circle, exactly once.** Every positive reduced rational `p/q` is the Stern-Brocot
rational of *exactly one* path. The boundary of the tree is therefore the positive rationals (the
circle / projective line over ℚ), not the Cantor set — this is the fix for the QI map's collapse. -/
theorem rational_existsUnique (p q : ℕ) (hp : 0 < p) (hq : 0 < q) (hcop : Nat.Coprime p q) :
    ∃! s : List Bool, rational s = (p, q) := by
  obtain ⟨s, hs⟩ := rational_surjective p q hp hq hcop
  refine ⟨s, hs, ?_⟩
  intro t ht
  exact rational_injective (by rw [hs, ht])

end SternBrocot
