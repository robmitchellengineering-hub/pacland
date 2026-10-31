"""The thermal bound must survive its own simulation — and it did not, at first."""
import sys
import unittest

sys.path.insert(0, "scripts")
import thermal_ceiling_check as T  # noqa: E402
from pacland.spectral import em_modes as E  # noqa: E402


class TestTheConstant(unittest.TestCase):
    def test_the_bound_uses_four_not_two(self):
        # eta=0.1, BER 1e-3 -> 4 * 3.0902^2 / 0.01 = 3820
        self.assertAlmostEqual(T.samples_per_bit(0.1, 1e-3), 3820, delta=5)

    def test_the_module_agrees_with_the_check(self):
        m = E.thermal_capacity(contrast=0.1, bandwidth=1e6, target_ber=1e-3)["samples_per_bit"]
        self.assertAlmostEqual(m, T.samples_per_bit(0.1, 1e-3), delta=5)

    def test_scaling_is_inverse_square_in_contrast(self):
        self.assertAlmostEqual(T.samples_per_bit(0.1, 1e-3) / T.samples_per_bit(0.2, 1e-3), 4.0, places=6)


class TestTheSimulationAgrees(unittest.TestCase):
    def test_simulation_lands_near_the_target(self):
        import random
        rng = random.Random(4)
        m = int(T.samples_per_bit(0.1, 1e-2))
        ber = T.simulate(0.1, m, 120000, rng)
        self.assertLess(ber, 2.0e-2, ber)     # within 2x of the 1e-2 target
        self.assertGreater(ber, 5.0e-3, ber)


if __name__ == "__main__":
    unittest.main()
