import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import unittest

from pacland.structure import (
    classify_observable,
    mi_significance,
    mutual_information,
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


if __name__ == "__main__":
    unittest.main()
