import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import unittest

from pacland.constraints import (
    elimination_certificate,
    elimination_curve,
    elimination_fraction,
    joint_elimination,
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


class TestJointElimination(unittest.TestCase):
    def test_disjoint_constraints_compose(self):
        # c1 keeps first half, c2 keeps second half -> every point fails one
        sample = list(range(100))
        named = [
            ("c1", lambda v: v < 50),
            ("c2", lambda v: v >= 50),
        ]
        j = joint_elimination(sample, named)
        self.assertAlmostEqual(j["joint"], 1.0)
        self.assertAlmostEqual(j["per"][0]["eliminated"], 0.5)
        self.assertAlmostEqual(j["per"][1]["eliminated"], 0.5)

    def test_identical_constraints_are_redundant(self):
        # both constraints are the same -> joint == single, interaction < 0
        sample = list(range(100))
        named = [
            ("c1", lambda v: v < 50),
            ("c2", lambda v: v < 50),
        ]
        j = joint_elimination(sample, named)
        self.assertAlmostEqual(j["joint"], 0.5)
        self.assertLess(j["interaction"], 0.0)
        self.assertEqual(j["interaction_verdict"], "redundant")

    def test_independent_constraints_are_flagged(self):
        # failure sets independent by construction -> verdict "independent"
        import random
        rng = random.Random(0)
        n = 400
        sample = list(range(n))
        named = [
            ("c1", lambda v: rng.random() < 0.5),
            ("c2", lambda v: rng.random() < 0.5),
        ]
        j = joint_elimination(sample, named, permutations=200)
        self.assertEqual(j["interaction_verdict"], "independent")
        self.assertLess(abs(j["interaction_z"]), 2.0)

    def test_independent_benchmark(self):
        # half fail c1, half fail c2, failure sets disjoint -> joint = 1.0,
        # independent benchmark = 1 - (1-.5)(1-.5) = 0.75
        sample = list(range(100))
        named = [
            ("c1", lambda v: v < 50),
            ("c2", lambda v: v % 2 == 0),
        ]
        j = joint_elimination(sample, named)
        self.assertAlmostEqual(j["independent"], 0.75, places=6)

    def test_empty_raises(self):
        with self.assertRaises(ValueError):
            joint_elimination([], [("c", lambda v: True)])


if __name__ == "__main__":
    unittest.main()
