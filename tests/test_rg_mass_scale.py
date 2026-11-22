"""The RG track's mathematics: asymptotic freedom derives the mass-gap scale + the uniformity check."""
import unittest

from pacland import rg_mass_scale as rg


class TestRgMassScale(unittest.TestCase):
    def test_beta_function_is_negative(self):
        # asymptotic freedom: the beta function is negative for a positive coupling
        self.assertLess(rg.beta_function(0.5, 2), 0.0)

    def test_running_coupling_vanishes_at_high_energy(self):
        # g(μ)² → 0 as μ → ∞ (asymptotic freedom)
        low = rg.running_coupling(2.0, 1.0, 2)
        high = rg.running_coupling(100.0, 1.0, 2)
        self.assertGreater(low, high)
        self.assertGreater(high, 0.0)

    def test_uniformity_holds(self):
        # the coupling stays finite for all μ > Λ — no Landau pole
        self.assertTrue(rg.check_uniformity(2, 1.0)["uniform"])

    def test_derived_form_is_the_asymptotic_freedom_scale(self):
        d = rg.derive_mass_gap_form(2)
        self.assertIn("exp(−1/(2β₀·g²))", d["mass_gap_form"])
        self.assertGreater(d["beta0"], 0.0)


if __name__ == "__main__":
    unittest.main()
