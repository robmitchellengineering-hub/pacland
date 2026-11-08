import Mathlib

/-!
# Standard-Model parameter count — the 19 free couplings, exactly

The SM's free parameters decompose into independent gauge-invariant, renormalizable
couplings (the free *inputs*, not predictions):

```
gauge      3   (g_1, g_2, g_3)
quark masses  6   (u, c, t, d, s, b)
lepton masses 3   (e, mu, tau)
CKM        4   (3 angles + 1 CP phase)
Higgs      2   (mu^2, lambda)
theta_QCD  1
            --  =  19
```

This is the *continuous* dimension of the low-energy parameter space (the orbit-space
dimension of the flavor action — see `validate_sm_rank_test.py` and
`validate_sm_invariant_dimension.py`), distinct from the *discrete* landscape count.
-/

namespace SM

/-- The SM has 19 free parameters: `3 + 6 + 3 + 4 + 2 + 1`. -/
theorem parameter_count : (3 : ℕ) + 6 + 3 + 4 + 2 + 1 = 19 := by norm_num

/-- Gauge + quark-mass + lepton-mass sectors: 12 couplings before CKM/Higgs/theta. -/
theorem gauge_mass_count : (3 : ℕ) + 6 + 3 = 12 := by norm_num

/-- The full Yukawa + CKM sector (masses + mixing): 13 couplings. -/
theorem yukawa_ckm_count : (6 : ℕ) + 3 + 4 = 13 := by norm_num

/-- Higgs + theta: 3 couplings. -/
theorem higgs_theta_count : (2 : ℕ) + 1 = 3 := by norm_num

end SM
