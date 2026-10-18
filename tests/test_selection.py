import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import unittest

from pacland.selection import ks_uniformity, quantile, typicality_test


class TestQuantile(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(quantile([1, 2, 3, 4], 2.5), 0.5)
        self.assertEqual(quantile([1, 2, 3, 4], 0.0), 0.0)
        self.assertEqual(quantile([1, 2, 3, 4], 4.0), 1.0)

    def test_empty_raises(self):
        with self.assertRaises(ValueError):
            quantile([], 1.0)


class TestTypicality(unittest.TestCase):
    def test_median_is_typical(self):
        sample = list(range(100))  # uniform-ish
        v = typicality_test(sample, observed=50.0)
        self.assertTrue(v.typical)
        self.assertAlmostEqual(v.quantile, 0.51)  # 51/100 <= 50

    def test_extreme_tail_is_atypical(self):
        sample = list(range(100))
        v = typicality_test(sample, observed=99.0)
        self.assertFalse(v.typical)

    def test_central_fraction_bounds(self):
        # an observation just inside the central 50% band is typical; just outside is not
        sample = list(range(100))
        inside = typicality_test(sample, observed=30.0, central_fraction=0.5)
        outside = typicality_test(sample, observed=20.0, central_fraction=0.5)
        self.assertTrue(inside.typical)   # quantile 0.31 in [0.25, 0.75]
        self.assertFalse(outside.typical)  # quantile 0.21 < 0.25

    def test_too_small_sample_raises(self):
        with self.assertRaises(ValueError):
            typicality_test([1.0], observed=1.0)


class TestKSUniformity(unittest.TestCase):
    def test_uniform_data_is_close(self):
        import random

        rng = random.Random(0)
        sample = [rng.uniform(0.0, 1.0) for _ in range(2000)]
        d = ks_uniformity(sample, 0.0, 1.0)
        self.assertLess(d, 0.05)  # genuinely uniform data -> small KS distance

    def test_skewed_data_is_far(self):
        # all mass near 0 -> far from uniform on [0,1]
        d = ks_uniformity([0.01] * 100, 0.0, 1.0)
        self.assertGreater(d, 0.9)


if __name__ == "__main__":
    unittest.main()
