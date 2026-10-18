import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import unittest

from pacland.constraints import elimination_certificate, elimination_fraction


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


if __name__ == "__main__":
    unittest.main()
