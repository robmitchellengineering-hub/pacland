"""The full-lattice extension reveals the V → ∞ obstacle (the cluster expansion removes it)."""
import unittest

from pacland import full_lattice_ratio as flr


class TestFullLatticeRatio(unittest.TestCase):
    def test_naive_correction_grows_with_volume(self):
        self.assertGreater(flr.full_lattice_correction(64, 2.0), flr.full_lattice_correction(8, 2.0))

    def test_ratio_positive_for_small_volume_weak_coupling(self):
        self.assertTrue(flr.volume_uniformity_condition(1.0, 10.77, 8, 4.0))

    def test_ratio_breaks_for_large_volume(self):
        # at fixed β, growing V eventually overtakes t·c·β·e^(2β)
        self.assertFalse(flr.volume_uniformity_condition(1.0, 10.77, 10 ** 6, 2.0))

    def test_check_reports_the_obstacle(self):
        r = flr.check_full_lattice_uniform(1.0, 10.77, (2.0, 4.0), (8, 64, 10 ** 6))
        self.assertFalse(r["uniform_under_union_bound"])
        self.assertIn("cluster expansion", r["obstacle"])


if __name__ == "__main__":
    unittest.main()
