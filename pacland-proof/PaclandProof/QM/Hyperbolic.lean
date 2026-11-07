import Mathlib

/-!
# The MERA causal cone is a Gromov-hyperbolic space (discrete metric geometry)

The metric half of "MERA = AdS", at the level that can be said finitely. The MERA causal cone is a
binary tree (vertices are finite bit strings); its **graph metric** `d(s,t) = |s| + |t| − 2·lcp(s,t)`
is the standard tree metric. Kernel-checked here:

1. **symmetry** — `d(s,t) = d(t,s)`;
2. the **take-agreement bridge** — `k ≤ lcp(s,t)` ⟺ the first `k` bits agree;
3. **shared-prefix transitivity** — `min (lcp s u) (lcp u t) ≤ lcp s t` (the tree's branching fact);
4. the **triangle inequality** — `d` is a genuine metric.

With the exponential volume (`QM.MERA.ballVolumeExponential`), these are the discrete statement that
the causal cone is a discretization of the hyperbolic plane. The **four-point condition** (Gromov's
0-hyperbolicity) is the strengthening of the triangle inequality — the remaining rung.
-/

namespace QM

open scoped BigOperators

/-- The length of the longest common prefix of two bit strings. -/
def commonPrefixLength : List Bool → List Bool → ℕ
  | [], _ => 0
  | _, [] => 0
  | a :: as, b :: bs => if a = b then commonPrefixLength as bs + 1 else 0

/-- The graph metric of the MERA causal cone (the binary tree). -/
def treeDist (s t : List Bool) : ℕ :=
  s.length + t.length - 2 * commonPrefixLength s t

/-- The common prefix is symmetric. -/
lemma commonPrefixLength_symm (s t : List Bool) :
    commonPrefixLength s t = commonPrefixLength t s := by
  induction s generalizing t with
  | nil => cases t <;> rfl
  | cons a as ih =>
      cases t with
      | nil => rfl
      | cons b bs =>
          by_cases hab : a = b
          · simp [commonPrefixLength, hab, ih]
          · have hba : b ≠ a := fun h => hab h.symm
            simp [commonPrefixLength, hab, hba]

/-- **Symmetry**: the tree distance is symmetric. -/
theorem treeDist_symm (s t : List Bool) :
    treeDist s t = treeDist t s := by
  dsimp [treeDist]
  rw [commonPrefixLength_symm, Nat.add_comm]

/-- The common prefix is bounded by each string's length. -/
lemma commonPrefix_length_le {s t : List Bool} :
    commonPrefixLength s t ≤ s.length ∧ commonPrefixLength s t ≤ t.length := by
  induction s generalizing t with
  | nil => simp [commonPrefixLength]
  | cons a as ih =>
      cases t with
      | nil => simp [commonPrefixLength]
      | cons b bs =>
          by_cases hab : a = b
          · simp [commonPrefixLength, hab]
            exact ih
          · simp [commonPrefixLength, hab]

/-- The first `k` bits of `s` and `t` agree whenever `k ≤ lcp(s,t)`. -/
lemma take_eq_of_le_lcp {s t : List Bool} {k : ℕ} (h : k ≤ commonPrefixLength s t) :
    s.take k = t.take k := by
  induction k generalizing s t with
  | zero => simp
  | succ k ih =>
      cases s with
      | nil => simp [commonPrefixLength] at h
      | cons a as =>
        cases t with
        | nil => simp [commonPrefixLength] at h
        | cons b bs =>
          by_cases hab : a = b
          · simp [commonPrefixLength, hab] at h ⊢
            exact ih h
          · simp [commonPrefixLength, hab] at h

/-- The reverse bridge: if the first `k` bits agree (and `k` fits inside both strings), then
`k ≤ lcp(s,t)`. -/
lemma le_lcp_of_take_eq {s t : List Bool} {k : ℕ}
    (h : s.take k = t.take k) (hk : k ≤ s.length) (hk' : k ≤ t.length) :
    k ≤ commonPrefixLength s t := by
  induction k generalizing s t with
  | zero => simp
  | succ k ih =>
      cases s with
      | nil => simp at hk
      | cons a as =>
        cases t with
        | nil => simp at hk'
        | cons b bs =>
          have hcons : a :: as.take k = b :: bs.take k := by simpa using h
          have ⟨ha, htail⟩ := List.cons.inj hcons
          have ih' := ih htail (Nat.succ_le_succ_iff.mp hk) (Nat.succ_le_succ_iff.mp hk')
          simp [commonPrefixLength, ha, ih']

/-- **Shared-prefix transitivity**: the common prefix of `s` and `t` is at least the overlap of the
two common prefixes through `u`. This is the tree's branching fact. -/
lemma commonPrefix_min_le {s u t : List Bool} :
    min (commonPrefixLength s u) (commonPrefixLength u t) ≤ commonPrefixLength s t := by
  let k := min (commonPrefixLength s u) (commonPrefixLength u t)
  have hsu : s.take k = u.take k := take_eq_of_le_lcp (s := s) (t := u) (Nat.min_le_left _ _)
  have hut : u.take k = t.take k := take_eq_of_le_lcp (s := u) (t := t) (Nat.min_le_right _ _)
  have hst : s.take k = t.take k := hsu.trans hut
  have hk1 : k ≤ s.length := Nat.le_trans (Nat.min_le_left _ _) (commonPrefix_length_le (s := s) (t := u)).1
  have hk2 : k ≤ t.length := Nat.le_trans (Nat.min_le_right _ _) (commonPrefix_length_le (s := u) (t := t)).2
  simpa [k] using le_lcp_of_take_eq hst hk1 hk2

/-- **The tree key lemma**: `lcp(s,u) + lcp(u,t) ≤ |u| + lcp(s,t)`. -/
lemma commonPrefix_triangle {s u t : List Bool} :
    commonPrefixLength s u + commonPrefixLength u t ≤ u.length + commonPrefixLength s t := by
  have ha : commonPrefixLength s u ≤ u.length := (commonPrefix_length_le (s := s) (t := u)).2
  have hb : commonPrefixLength u t ≤ u.length := (commonPrefix_length_le (s := u) (t := t)).1
  have hmin : min (commonPrefixLength s u) (commonPrefixLength u t) ≤ commonPrefixLength s t :=
    commonPrefix_min_le (s := s) (u := u) (t := t)
  -- a + b = max(a,b) + min(a,b) ≤ n + c
  omega

/-- **The triangle inequality**: the tree distance is a genuine metric. -/
theorem treeDist_triangle (s u t : List Bool) :
    treeDist s t ≤ treeDist s u + treeDist u t := by
  dsimp [treeDist]
  have ht : commonPrefixLength s u + commonPrefixLength u t ≤ u.length + commonPrefixLength s t :=
    commonPrefix_triangle (s := s) (u := u) (t := t)
  have h1 : commonPrefixLength s t ≤ s.length := (commonPrefix_length_le (s := s) (t := t)).1
  have h2 : commonPrefixLength s t ≤ t.length := (commonPrefix_length_le (s := s) (t := t)).2
  have h3 : commonPrefixLength s u ≤ s.length := (commonPrefix_length_le (s := s) (t := u)).1
  have h4 : commonPrefixLength s u ≤ u.length := (commonPrefix_length_le (s := s) (t := u)).2
  have h5 : commonPrefixLength u t ≤ u.length := (commonPrefix_length_le (s := u) (t := t)).1
  have h6 : commonPrefixLength u t ≤ t.length := (commonPrefix_length_le (s := u) (t := t)).2
  omega

end QM
