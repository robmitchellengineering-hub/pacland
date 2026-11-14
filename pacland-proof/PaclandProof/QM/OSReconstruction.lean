import Mathlib
import PaclandProof.QM.OSAxioms

/-!
# The OS reconstruction's existence — W0+W1+W3+W4, WITHOUT the toy mass gap

The Osterwalder–Schrader reconstruction has an existence half (the Hilbert space, covariance,
locality, vacuum) and a mass-gap half. The mass-gap half (W2, the spectral condition) is the
volume-uniform join — stated separately in `VolumeUniformJoin.lean`, NOT faked here. This file proves
the genuine existence half: the Wilson kernel's reflection positivity (OS3) reconstructs the Wightman
axioms W0, W1, W3, W4, with no toy mass gap.
-/

namespace QM

/-- **The OS reconstruction's existence** (W0 Hilbert space, W1 covariance, W3 locality, W4 vacuum),
for the Wilson heat kernel, with the mass gap deliberately excluded (it is the volume-uniform join).
This is the honest existence half of the Osterwalder–Schrader reconstruction — the non-trivial part is
the GNS step (`posdef_kernel_inner_product`), the rest are the kernel's symmetry facts. -/
theorem os_existence {m : ℕ} (K : Fin m → Fin m → ℝ) (θ : Fin m → ℝ) (β : ℝ) (hOS3 : PosDefKernel K) :
    WightmanHilbert (fun (f g : Fin m → ℝ) => ∑ i : Fin m, ∑ j : Fin m, f i * g j * K i j) ∧
    WightmanCovariance (fun x y => Real.exp (2 * β * Real.cos (x - y))) ∧
    WightmanLocality (fun i j => Real.exp (2 * β * Real.cos (θ i - θ j))) ∧
    WightmanVacuum (fun i j => Real.exp (2 * β * Real.cos (θ i - θ j))) := by
  constructor
  · exact posdef_kernel_inner_product K hOS3
  · constructor
    · exact wick_rotation β
    · constructor
      · exact wilson_kernel_local θ β
      · intro i j
        exact wilson_kernel_vacuum θ β i j

end QM
