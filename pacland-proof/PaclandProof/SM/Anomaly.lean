import Mathlib

/-!
# Standard-Model anomaly cancellation — the five conditions vanish

The SM's exact *constraint* structure (the gauge-sector analog of the flux tadpole). One
generation of SM fermions has the chirality-signed hypercharge content

```
Q (doublet, 3 colors):  +6 · Y_Q      u (singlet, 3 colors):  −3 · Y_u
d (singlet, 3 colors):  −3 · Y_d      L (doublet):             +2 · Y_L
e (singlet):            −1 · Y_e
```

with the physical assignment `(Y_Q, Y_u, Y_d, Y_L, Y_e) = (1/6, 2/3, −1/3, −1/2, −1)`.
The five gauge/gravitational anomaly coefficients all vanish:

```
[SU(3)]³      = 2 − 1 − 1
[SU(3)]²U(1)  = 2 Y_Q − Y_u − Y_d
[SU(2)]²U(1)  = 3 Y_Q + Y_L
[U(1)]³       = 6 Y_Q³ − 3 Y_u³ − 3 Y_d³ + 2 Y_L³ − Y_e³
[grav]²U(1)   = 6 Y_Q − 3 Y_u − 3 Y_d + 2 Y_L − Y_e
```

This file machine-checks that all five vanish (a finite rational computation — the
hypercharges are *required for consistency*, not predicted; they are the SM's first exact
constraint).
-/

namespace SM

/-- The five SM anomaly coefficients vanish for the physical hypercharge assignment. -/
theorem anomaly_cancellation :
    (2 - 1 - 1 = 0) ∧
    (2 * (1/6 : ℝ) - (2/3 : ℝ) - (-1/3 : ℝ) = 0) ∧
    (3 * (1/6 : ℝ) + (-1/2 : ℝ) = 0) ∧
    (6 * (1/6 : ℝ)^3 - 3 * (2/3 : ℝ)^3 - 3 * (-1/3 : ℝ)^3 + 2 * (-1/2 : ℝ)^3 - (-1 : ℝ)^3 = 0) ∧
    (6 * (1/6 : ℝ) - 3 * (2/3 : ℝ) - 3 * (-1/3 : ℝ) + 2 * (-1/2 : ℝ) - (-1 : ℝ) = 0) := by
  norm_num

/-- `[SU(3)]³` vanishes: each generation has as many triplets as anti-triplets. -/
theorem su3_cubic : (2 - 1 - 1 = 0) := by norm_num

/-- `[SU(3)]²U(1)` vanishes. -/
theorem su3_sq_u1 : 2 * (1/6 : ℝ) - (2/3 : ℝ) - (-1/3 : ℝ) = 0 := by norm_num

/-- `[SU(2)]²U(1)` vanishes. -/
theorem su2_sq_u1 : 3 * (1/6 : ℝ) + (-1/2 : ℝ) = 0 := by norm_num

/-- `[U(1)]³` vanishes. -/
theorem u1_cubic : 6 * (1/6 : ℝ)^3 - 3 * (2/3 : ℝ)^3 - 3 * (-1/3 : ℝ)^3 + 2 * (-1/2 : ℝ)^3 - (-1 : ℝ)^3 = 0 := by
  norm_num

/-- `[grav]²U(1)` vanishes. -/
theorem grav_sq_u1 : 6 * (1/6 : ℝ) - 3 * (2/3 : ℝ) - 3 * (-1/3 : ℝ) + 2 * (-1/2 : ℝ) - (-1 : ℝ) = 0 := by
  norm_num

end SM
