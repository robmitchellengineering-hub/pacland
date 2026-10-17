import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import random
import unittest
from math import log, sqrt

from pacland.learnability import (
    finite_class_radius,
    sample_complexity,
    sample_flux_vacua,
    shatters,
    vc_lower_bound,
)


def _threshold_hypotheses(theta_grid):
    return [lambda p, t=theta: 1 if p >= t else 0 for theta in theta_grid]


def _interval_hypotheses(grid):
    hs = []
    for a in grid:
        for b in grid:
            if a < b:
                hs.append(lambda p, a=a, b=b: 1 if a <= p <= b else 0)
    return hs


class TestVC(unittest.TestCase):
    def test_threshold_class_vc_is_one(self):
        # Thresholds on the line have VC dimension 1.
        hs = _threshold_hypotheses([0.5, 1.5, 2.5, 3.5])
        self.assertEqual(vc_lower_bound(hs, [1, 2, 3]), 1)

    def test_interval_class_vc_is_two(self):
        # Intervals on the line have VC dimension 2.
        hs = _interval_hypotheses([0.5, 1.5, 2.5, 3.5, 4.5])
        self.assertEqual(vc_lower_bound(hs, [1, 2, 3]), 2)

    def test_shatters_single_point(self):
        hs = _threshold_hypotheses([0.5, 1.5])
        self.assertTrue(shatters(hs, [1]))

    def test_sample_complexity_scaling(self):
        small = sample_complexity(10, 0.1, 0.05)
        big = sample_complexity(100, 0.1, 0.05)
        self.assertGreater(big, small)
        finer = sample_complexity(10, 0.01, 0.05)
        self.assertGreater(finer, small)

    def test_finite_class_radius_matches_definition(self):
        r = finite_class_radius(class_size=100, n=1000, delta=0.05)
        self.assertAlmostEqual(r, sqrt(log(100 / 0.05) / 2000.0), places=12)


class TestSampler(unittest.TestCase):
    def test_sample_distinct_within_bound(self):
        vacua = sample_flux_vacua(50, dim=3, tadpole_bound=10, rng=random.Random(0))
        self.assertEqual(len(vacua), 50)
        self.assertEqual(len({v.flux for v in vacua}), 50)  # distinct
        for v in vacua:
            self.assertLessEqual(v.tadpole(), 10)

    def test_impossible_budget_raises(self):
        with self.assertRaises(RuntimeError):
            sample_flux_vacua(5, dim=1, tadpole_bound=0, rng=random.Random(0))


if __name__ == "__main__":
    unittest.main()
