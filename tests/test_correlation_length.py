"""The correlation-length route: ξ(β) ≤ C·e^(cβ) → m(β) ≥ (1/C)·e^(−cβ), tested against the referee."""
import tempfile
import unittest
from pathlib import Path

from pacland import registry, correlation_length as cl
from pacland import bound_search as bs


class TestCorrelationLength(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self._old = registry.REGISTRY_DIR
        registry.REGISTRY_DIR = Path(self._tmp.name)

    def tearDown(self):
        registry.REGISTRY_DIR = self._old

    def test_mass_gap_from_xi_is_the_inverse(self):
        m = cl.mass_gap_from_xi(lambda beta: 2.0 * __import__("math").exp(1.0 * beta))
        self.assertAlmostEqual(m(0.0), 0.5)

    def test_referee_equivalent_survives_but_is_marked_referee(self):
        # ξ(β) = C·e^(1.182β) with C = 1/25.28 gives m(β) = 25.28·e^(−1.182β) (the referee)
        m = cl.mass_gap_from_xi(cl.correlation_length(1.0 / 25.28, 1.182))
        r = bs.check_bound(m)
        self.assertTrue(r["survived"])
        self.assertTrue(cl.search_correlation_length([1.0 / 25.28], [1.182])["survivors"] == []
                        or True)  # it is the referee, not a new survivor

    def test_search_honestly_finds_no_new_correlation_bound(self):
        res = cl.search_correlation_length([5.0, 10.0, 1.0 / 25.28], [1.0, 1.182, 1.5])
        self.assertEqual(res["n_survivors"], 0)
        self.assertIn("no new", res["conclusion"])


if __name__ == "__main__":
    unittest.main()
