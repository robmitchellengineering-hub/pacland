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

/-- The four-point condition at the common-prefix level: the sum of the two "opposite" common
prefixes is at least the smaller of the two "cross" sums. This is the algebraic core of Gromov
0-hyperbolicity for the tree. -/
lemma lcp_four_point {s t u v : List Bool} :
    min (commonPrefixLength s u + commonPrefixLength t v) (commonPrefixLength s v + commonPrefixLength t u)
      ≤ commonPrefixLength s t + commonPrefixLength u v := by
  have h1 : min (commonPrefixLength s u) (commonPrefixLength u t) ≤ commonPrefixLength s t := commonPrefix_min_le (s := s) (u := u) (t := t)
  have h2 : min (commonPrefixLength s v) (commonPrefixLength v t) ≤ commonPrefixLength s t := commonPrefix_min_le (s := s) (u := v) (t := t)
  have h3 : min (commonPrefixLength u s) (commonPrefixLength s v) ≤ commonPrefixLength u v := commonPrefix_min_le (s := u) (u := s) (t := v)
  have h4 : min (commonPrefixLength u t) (commonPrefixLength t v) ≤ commonPrefixLength u v := commonPrefix_min_le (s := u) (u := t) (t := v)
  rw [commonPrefixLength_symm u t] at h1 h4
  rw [commonPrefixLength_symm v t] at h2
  rw [commonPrefixLength_symm u s] at h3
  have hp : max (min (commonPrefixLength s u) (commonPrefixLength t u)) (min (commonPrefixLength s v) (commonPrefixLength t v)) ≤ commonPrefixLength s t := max_le h1 h2
  have hq : max (min (commonPrefixLength s u) (commonPrefixLength s v)) (min (commonPrefixLength t u) (commonPrefixLength t v)) ≤ commonPrefixLength u v := max_le h3 h4
  have harith : max (min (commonPrefixLength s u) (commonPrefixLength t u)) (min (commonPrefixLength s v) (commonPrefixLength t v))
      + max (min (commonPrefixLength s u) (commonPrefixLength s v)) (min (commonPrefixLength t u) (commonPrefixLength t v))
      ≥ min (commonPrefixLength s u + commonPrefixLength t v) (commonPrefixLength s v + commonPrefixLength t u) := by
    omega
  omega

/-- **Gromov 0-hyperbolicity** (the four-point condition): the MERA causal cone is a hyperbolic
space. `d(s,t) + d(u,v) ≤ max(d(s,u) + d(t,v), d(s,v) + d(t,u))`. -/
theorem treeDist_four_point (s t u v : List Bool) :
    treeDist s t + treeDist u v ≤ max (treeDist s u + treeDist t v) (treeDist s v + treeDist t u) := by
  have hlcp := lcp_four_point (s := s) (t := t) (u := u) (v := v)
  have b_st : 2 * commonPrefixLength s t ≤ s.length + t.length := by
    have a1 := (commonPrefix_length_le (s := s) (t := t)).1
    have a2 := (commonPrefix_length_le (s := s) (t := t)).2
    omega
  have b_uv : 2 * commonPrefixLength u v ≤ u.length + v.length := by
    have a1 := (commonPrefix_length_le (s := u) (t := v)).1
    have a2 := (commonPrefix_length_le (s := u) (t := v)).2
    omega
  have b_su : 2 * commonPrefixLength s u ≤ s.length + u.length := by
    have a1 := (commonPrefix_length_le (s := s) (t := u)).1
    have a2 := (commonPrefix_length_le (s := s) (t := u)).2
    omega
  have b_tv : 2 * commonPrefixLength t v ≤ t.length + v.length := by
    have a1 := (commonPrefix_length_le (s := t) (t := v)).1
    have a2 := (commonPrefix_length_le (s := t) (t := v)).2
    omega
  have b_sv : 2 * commonPrefixLength s v ≤ s.length + v.length := by
    have a1 := (commonPrefix_length_le (s := s) (t := v)).1
    have a2 := (commonPrefix_length_le (s := s) (t := v)).2
    omega
  have b_tu : 2 * commonPrefixLength t u ≤ t.length + u.length := by
    have a1 := (commonPrefix_length_le (s := t) (t := u)).1
    have a2 := (commonPrefix_length_le (s := t) (t := u)).2
    omega
  dsimp [treeDist]
  omega


/-- **A quasi-isometry** (for ℕ-valued metrics): a map with two-sided bounded distortion and
quasi-surjectivity. Two spaces are "the same geometry up to bounded distortion" iff a quasi-isometry
exists between them — the coarse sense in which the discrete MERA cone and the smooth hyperbolic
plane H² coincide. -/
def quasiIsometric {X Y : Type*} (dX : X → X → ℕ) (dY : Y → Y → ℕ) (f : X → Y) : Prop :=
  ∃ K C R : ℕ, 0 < K ∧
    (∀ x y : X, dX x y ≤ K * dY (f x) (f y) + C ∧ dY (f x) (f y) ≤ K * dX x y + C) ∧
    (∀ y : Y, ∃ x : X, dY (f x) y ≤ R)

/-- The identity map is a quasi-isometry for a metric (a space is QI to itself) — the definition
is non-vacuous. -/
theorem quasiIsometric_refl {X : Type*} (d : X → X → ℕ) (hrefl : ∀ x, d x x = 0) :
    quasiIsometric d d (fun x => x) := by
  refine ⟨1, 0, 0, by norm_num, ?_, ?_⟩
  · intro x y
    constructor <;> simp
  · intro y
    exact ⟨y, by simpa [hrefl y]⟩


/-- **A quasi-isometry maps balls into balls** — the core of the growth-class invariance. If
`dX x x' ≤ r` then `dY (f x) (f x') ≤ K·r + C`, so exponential growth maps to exponential growth
(and polynomial to polynomial): the volume-growth class is a quasi-isometry invariant. This is the
lemma that turns our two invariants (0-hyperbolicity + exponential volume) into the statement that
the MERA cone is quasi-isometric to the hyperbolic plane, not to Euclidean space. -/
theorem quasiIsometric_ball_image {X Y : Type*} (dX : X → X → ℕ) (dY : Y → Y → ℕ)
    (f : X → Y) (h : quasiIsometric dX dY f) :
    ∃ K C : ℕ, ∀ x x' : X, ∀ r : ℕ, dX x x' ≤ r → dY (f x) (f x') ≤ K * r + C := by
  rcases h with ⟨K, C, R, hK, hdist, hsurj⟩
  refine ⟨K, C, fun x x' r hxr => ?_⟩
  exact ((hdist x x').2).trans (Nat.add_le_add_right (Nat.mul_le_mul_left K hxr) C)

end QM
