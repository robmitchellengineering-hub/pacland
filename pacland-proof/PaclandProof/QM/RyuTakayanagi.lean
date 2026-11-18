import Mathlib
import PaclandProof.QM.PerfectTensor

/-!
# Ryu–Takayanagi — "minimal cut = entanglement", the single-tile (HaPPY hexagon) case

The discrete Ryu–Takayanagi formula says the entanglement of a boundary region equals the area of
the *minimal* cut separating it from its complement. In the stabilizer language the entanglement
content is: **a boundary region's reduced state is maximally mixed iff its stabilizer group carries
no non-identity element supported on that region** (the standard `ρ_A = 2^{-|A|} Σ_{g ∈ S, supp g ⊆ A} g|_A`
fact — cited, not re-proven here, matching the algebraic style of `QM.MERA`).

This file kernel-checks the single-tile case — the HaPPY hexagon (`QM.PerfectTensor`), whose legs
are the whole boundary. There are no internal bonds, so the minimal cut separating a region `a` from
its complement is just the smaller side: `min |a| (6 - |a|)`. The theorem: **no stabilizer of the
hexagon is supported on any region of ≤ 3 legs**, so every region on the smaller side of its minimal
cut is maximally entangled — the minimal cut *is* the entanglement, saturated.

The multi-tile generalisation — where the cut may pass through internal bonds of a hyperbolic tiling,
and the "max-flow = min-cut" argument of HaPPY picks the minimal one — is the next rung; this file
provides the region/cut/support vocabulary it builds on.
-/

namespace QM

/-- A boundary region of the HaPPY hexagon: a subset of the 6 legs, as a bitmask (leg `i` is in the
region iff bit `i` is set). `regionSize` is the number of legs in it. -/
def regionSize (a : Nat) : Nat :=
  pWeight (a, 0)

/-- A Pauli string is *supported on* region `a` when every non-identity leg lies in `a` — the
stabilizer form of "the operator acts only inside the boundary region" (a decidable `Bool`). -/
def supportedOn (p : Pauli6) (a : Nat) : Bool :=
  Nat.land (Nat.lor p.1 p.2) a == Nat.lor p.1 p.2

/-- The **minimal cut** separating region `a` from its complement. For the single hexagon tile there
are no internal bonds to cut, so the cut is the smaller side. -/
def minCut (a : Nat) : Nat :=
  min (regionSize a) (6 - regionSize a)

/-- **Ryu–Takayanagi, single tile (stabilizer form).** No non-identity element of the HaPPY
hexagon's stabilizer group is supported on any region of ≤ 3 legs. Equivalently: for every boundary
region `a` on the smaller side of its minimal cut (`regionSize a ≤ 3`), the reduced state carries no
stabilizer and is therefore maximally mixed — the entanglement across the minimal cut is saturated
(rank `2 ^ regionSize a`, the "area" of the cut). -/
theorem happy_rt_single_tile :
    (List.range 64).all (fun a =>
      decide (3 < regionSize a) ||
      (List.range 64).all (fun k =>
        k == 0 || ! supportedOn (prodOf happyGens k) a)) = true := by
  decide

end QM
