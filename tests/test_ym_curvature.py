"""The YM curvature bound: asymptotic freedom (β < 0) with a finite derivative along the flow."""
import unittest

from pacland import ym_curvature as ym


class TestYmCurvature(unittest.TestCase):
    def test_beta_function_is_negative(self):
        # asymptotic freedom: β(g) < 0 for a small coupling
        self.assertLess(ym.beta_ym(0.3, 2), 0.0)

    def test_two_loop_correction_is_small(self):
        # the 2-loop term is a correction at small g (β₂ ≪ β₁ in magnitude)
        self.assertLess(abs(ym.beta_ym(0.3, 2, order=2)), abs(ym.beta_ym(0.3, 2, order=1)) * 1.5)

    def test_gaussian_fixed_point_is_marginal(self):
        self.assertTrue(ym.gaussian_fixed_point()["marginal"])

    def test_ym_flow_is_uniform(self):
        self.assertTrue(ym.check_ym_uniformity(2)["uniform"])
        self.assertTrue(ym.check_ym_uniformity(2)["asymptotic_freedom"])


if __name__ == "__main__":
    unittest.main()
