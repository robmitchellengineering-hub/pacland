import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import random
import unittest

from pacland.measure import Measure, Observable


def _two_observables():
    return (
        Observable("alpha_s_MZ", target_log=-2.14, computable=True),
        Observable("cosmo_constant", target_log=None, computable=False),
    )


class TestMeasure(unittest.TestCase):
    def test_weight_validation(self):
        obs = _two_observables()
        with self.assertRaises(ValueError):
            Measure(obs, (0.5, 0.6))  # sums to 1.1
        with self.assertRaises(ValueError):
            Measure(obs, (0.5, -0.5, 1.0))  # wrong length
        with self.assertRaises(ValueError):
            Measure(obs, (-0.5, 1.5))  # negative

    def test_uniform_weights(self):
        obs = _two_observables()
        m = Measure.uniform(obs)
        self.assertEqual(m.weights, (0.5, 0.5))

    def test_sampling_respects_weights(self):
        obs = (Observable("a", 0.0, True), Observable("b", 0.0, True))
        m = Measure(obs, (0.7, 0.3))
        idx = m.sample_indices(10000, rng=random.Random(1))
        frac_a = sum(1 for i in idx if i == 0) / len(idx)
        self.assertAlmostEqual(frac_a, 0.7, delta=0.05)

    def test_exact_disagreement(self):
        obs = (Observable("a", 0.0, True), Observable("b", 0.0, True))
        m = Measure.uniform(obs)
        h = {"a": 0.0, "b": 0.0}
        o = {"a": 0.0, "b": 0.1}
        self.assertAlmostEqual(m.exact_disagreement(h, o, threshold=0.05), 0.5)

    def test_exact_disagreement_missing_raises(self):
        obs = (Observable("a", 0.0, True),)
        m = Measure.uniform(obs)
        with self.assertRaises(KeyError):
            m.exact_disagreement({"a": 0.0}, {}, threshold=0.05)


if __name__ == "__main__":
    unittest.main()
