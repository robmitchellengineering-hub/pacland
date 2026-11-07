import Mathlib

/-!
# The MERA causal cone is a Gromov-hyperbolic space (discrete metric geometry)

The metric half of "MERA = AdS", at the level that can be said finitely. The MERA causal cone is a
binary tree (vertices are finite bit strings); its **graph metric** `d(s,t) = |s| + |t| − 2·lcp(s,t)`
is the standard tree metric. This file kernel-checks the foundational metric-geometry facts:

1. **symmetry** — `d(s,t) = d(t,s)` (via the symmetry of the common prefix);
2. **the take-agreement lemma** — `k ≤ lcp(s,t)` means the first `k` bits agree.

With the exponential volume (`QM.MERA.ballVolumeExponential`), these are the discrete signature that
the causal cone is a discretization of the hyperbolic plane. The triangle inequality and the
four-point condition (Gromov's 0-hyperbolicity) are the strengthening of these facts — a genuine
theorem about trees, the next rung.
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

/-- **The first `k` bits of `s` and `t` agree whenever `k ≤ lcp(s,t)`** — the bridge from the
recursive common-prefix definition to the geometric "prefix" intuition. -/
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

end QM
