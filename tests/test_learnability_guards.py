"""Learnability guard tests — positive case plus the required-to-fail mutation.

``guard_no_linear_structure`` must PASS on a random target (no structure) and
FAIL on a target that is a known linear function of the features — proving the
guard can actually detect linear structure rather than always passing.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import random
import unittest

from pacland.learnability_guards import guard_no_linear_structure


def make_features(n, dim, seed=0):
    rng = random.Random(seed)
    return [[rng.randint(-5, 5) for _ in range(dim)] for _ in range(n)]


class TestNoLinearStructureGuard(unittest.TestCase):
    def test_passes_on_random_target(self):
        rng = random.Random(1)
        feats = make_features(100, 6)
        targets = [rng.gauss(0, 1) for _ in feats]  # pure noise
        self.assertTrue(guard_no_linear_structure(feats, targets)[0])

    def test_fails_on_linear_target(self):
        # mutation: a target that IS a linear function of the features
        rng = random.Random(2)
        feats = make_features(100, 6)
        weights = [rng.uniform(-1, 1) for _ in range(6)]
        targets = [sum(w * f[i] for i, w in enumerate(weights)) for f in feats]
        passed, msg = guard_no_linear_structure(feats, targets)
        self.assertFalse(passed)  # the guard must catch linear structure
        self.assertIn("R2", msg)


if __name__ == "__main__":
    unittest.main()
