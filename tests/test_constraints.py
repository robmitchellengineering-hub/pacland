import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import unittest

from pacland.constraints import (
    elimination_certificate,
    elimination_curve,
    elimination_fraction,
    linearity_r2,
)


class TestEliminationFraction(unittest.TestCase):
    def test_basic(self):
        sample = [1, 2, 3, 4]
        self.assertEqual(elimination_fraction(sample, lambda v: v > 2), 0.5)

    def test_empty_raises(self):
        with self.assertRaises(ValueError):
            elimination_fraction([], lambda v: True)


class TestEliminationCertificate(unittest.TestCase):
    def test_interval_bounds(self):
        sample = list(range(100))
        c = elimination_certificate(sample, lambda v: v < 50)  # eliminates 50%
        self.assertAlmostEqual(c["eliminated"], 0.5)
        self.assertLessEqual(c["lower"], 0.5)
        self.assertGreaterEqual(c["upper"], 0.5)

    def test_all_eliminated(self):
        c = elimination_certificate([1, 2, 3], lambda v: False)
        self.assertEqual(c["eliminated"], 1.0)


class TestEliminationCurve(unittest.TestCase):
    def test_uniform_cdf_is_linear(self):
        # a uniform sample has an (approximately) linear empirical CDF
        import random
        rng = random.Random(0)
        vals = [rng.uniform(0, 1) for _ in range(500)]
        ts = [i / 20 for i in range(21)]
        cdf = elimination_curve(vals, ts)
        self.assertGreater(linearity_r2(ts, cdf), 0.95)

    def test_zigzag_is_not_linear(self):
        # no linear trend -> low R^2 against a line
        xs = [0.0, 1.0, 2.0, 3.0, 4.0]
        ys = [0.0, 1.0, 0.0, 1.0, 0.0]
        self.assertLess(linearity_r2(xs, ys), 0.5)


if __name__ == "__main__":
    unittest.main()
