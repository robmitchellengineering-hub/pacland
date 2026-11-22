"""M3 — the bound-discovery loop: search a family, test against the referee, record the honest result."""
import tempfile
import unittest
from pathlib import Path

from pacland import registry
from pacland import bound_search as bs


class TestBoundSearch(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self._old = registry.REGISTRY_DIR
        registry.REGISTRY_DIR = Path(self._tmp.name)

    def tearDown(self):
        registry.REGISTRY_DIR = self._old

    def test_referee_survives_but_is_not_new(self):
        r = bs.check_bound(bs.exponential(25.28, 1.182))
        self.assertTrue(r["survived"])
        self.assertTrue(r["reaches_scale"])
        self.assertTrue(bs._is_referee(25.28, 1.182))

    def test_weaker_exponential_does_not_reach_scale(self):
        # c(β)=10·e^(−1.5β) is valid but decays faster than m → not AT the mass-gap scale
        r = bs.check_bound(bs.exponential(10.0, 1.5))
        self.assertTrue(r["valid"])
        self.assertFalse(r["reaches_scale"])
        self.assertFalse(r["survived"])

    def test_slower_exponential_is_invalid(self):
        # c(β)=25.28·e^(−1.0β) decays slower than the truth → c > m → false bound
        r = bs.check_bound(bs.exponential(25.28, 1.0))
        self.assertFalse(r["valid"])
        self.assertFalse(r["survived"])

    def test_search_honestly_reports_no_new_bound(self):
        res = bs.search_exponential([5.0, 10.0, 25.28], [1.0, 1.182, 1.5, 2.0])
        self.assertEqual(res["n_survivors"], 0)
        self.assertIn("no new", res["conclusion"])

    def test_failed_direction_is_recorded_as_a_claim(self):
        bs.search_exponential([5.0, 10.0, 25.28], [1.0, 1.182, 1.5])
        failed = registry.failed_directions()
        self.assertTrue(any("mass-gap bound search" in f["payload"]["statement"] for f in failed))

    def test_log_corrected_family_also_has_no_new_bound(self):
        res = bs.search_log_corrected([10.0, 25.28], [1.0, 1.182], [0.0, 0.5, 1.0])
        self.assertEqual(res["n_survivors"], 0)
        self.assertIn("log-corrected", res["family"])
        self.assertIn("no new", res["conclusion"])

    def test_two_families_record_two_failed_directions(self):
        bs.search_exponential([5.0, 25.28], [1.0, 1.182])
        bs.search_log_corrected([10.0, 25.28], [1.0, 1.182], [0.5])
        failed = [f["payload"]["statement"] for f in registry.failed_directions()]
        self.assertTrue(any("exponential" in s for s in failed))
        self.assertTrue(any("log-corrected" in s for s in failed))


if __name__ == "__main__":
    unittest.main()
