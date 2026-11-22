"""The SU(2) Bochner identity: the Bakry-Emery curvature 1/4 + 2β·cos θ + the good/bad sets."""
import unittest

from pacland import bochner_identity as bi


class TestBochnerIdentity(unittest.TestCase):
    def test_ricci_is_quarter(self):
        self.assertAlmostEqual(bi.su2_ricci(), 0.25)

    def test_curvature_negative_at_antipode_for_large_beta(self):
        import math
        self.assertLess(bi.bakry_emery_curvature(1.0, math.pi), 0.0)

    def test_curvature_positive_at_vacuum(self):
        self.assertGreater(bi.bakry_emery_curvature(1.0, 0.0), 0.0)

    def test_antipode_measure_suppressed_at_weak_coupling(self):
        self.assertLess(bi.antipode_measure(2.0), bi.antipode_measure(0.5))

    def test_good_set_threshold_positive_for_large_beta(self):
        self.assertGreater(bi.good_set_threshold(2.0), 0.0)


if __name__ == "__main__":
    unittest.main()
