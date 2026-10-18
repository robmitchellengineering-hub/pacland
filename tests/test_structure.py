import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import unittest

from pacland.structure import (
    classify_observable,
    cv_predictability,
    mi_significance,
    mutual_information,
    ridge_cv_predictability,
)


class TestMutualInformation(unittest.TestCase):
    def test_identical_is_maximal(self):
        xs = [random.random() for _ in range(200)]
        # I(X;X) = H(X); with 8 bins it is <= log2(8) = 3 bits, and far above
        # the MI of X with an independent shuffle.
        self.assertGreater(
            mutual_information(xs, xs), mutual_information(xs, list(reversed(xs))) + 0.5
        )

    def test_equal_length_required(self):
        with self.assertRaises(ValueError):
            mutual_information([1, 2, 3], [1, 2])


class TestClassifyObservable(unittest.TestCase):
    def test_linear_structure_is_detected(self):
        rng = random.Random(1)
        n = 300
        xs = [rng.uniform(-3, 3) for _ in range(n)]
        noise = [rng.gauss(0, 0.1) for _ in range(n)]
        y = [2.0 * x + n_ for x, n_ in zip(xs, noise)]  # strongly x-dependent
        r = classify_observable([xs], y, permutations=150)
        self.assertEqual(r["verdict"], "structured")

    def test_independent_noise_is_random(self):
        rng = random.Random(2)
        n = 300
        xs = [rng.uniform(-3, 3) for _ in range(n)]
        y = [rng.gauss(0, 1) for _ in range(n)]  # independent of x
        r = classify_observable([xs], y, permutations=150)
        self.assertEqual(r["verdict"], "random")


class TestMISignificance(unittest.TestCase):
    def test_z_score_present(self):
        rng = random.Random(3)
        xs = [rng.uniform(-1, 1) for _ in range(100)]
        y = [rng.uniform(-1, 1) for _ in range(100)]
        r = mi_significance(xs, y, permutations=100)
        self.assertIn("mi", r)
        self.assertIn("z", r)


class TestCVPredictability(unittest.TestCase):
    def test_linear_map_is_predictable(self):
        rng = random.Random(4)
        n = 300
        fluxes = [[rng.uniform(-3, 3), rng.uniform(-3, 3)] for _ in range(n)]
        y = [2.0 * f[0] - f[1] + rng.gauss(0, 0.2) for f in fluxes]  # learnable
        self.assertGreater(cv_predictability(fluxes, y), 0.5)

    def test_independent_noise_is_not_predictable(self):
        rng = random.Random(5)
        n = 300
        fluxes = [[rng.uniform(-3, 3), rng.uniform(-3, 3)] for _ in range(n)]
        y = [rng.gauss(0, 1) for _ in range(n)]  # random
        self.assertLess(cv_predictability(fluxes, y), 0.2)


class TestRidgeCV(unittest.TestCase):
    def test_deterministic_quadratic_is_captured(self):
        rng = random.Random(6)
        n = 150
        fluxes = [[rng.uniform(-2, 2) for _ in range(5)] for _ in range(n)]
        y = [f[0] * f[1] + 2 * f[2] ** 2 - f[3] * f[4] for f in fluxes]
        self.assertGreater(ridge_cv_predictability(fluxes, y), 0.9)

    def test_independent_noise_is_low(self):
        rng = random.Random(7)
        n = 150
        fluxes = [[rng.uniform(-2, 2) for _ in range(5)] for _ in range(n)]
        y = [rng.gauss(0, 1) for _ in range(n)]
        self.assertLess(ridge_cv_predictability(fluxes, y), 0.3)


if __name__ == "__main__":
    unittest.main()
