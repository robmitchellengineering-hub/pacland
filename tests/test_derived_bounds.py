"""M3 — the derived-bound mechanism: known mechanisms tested against the referee + recorded as claims."""
import tempfile
import unittest
from pathlib import Path

from pacland import registry, derived_bounds as db


class TestDerivedBounds(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self._old = registry.REGISTRY_DIR
        registry.REGISTRY_DIR = Path(self._tmp.name)

    def tearDown(self):
        registry.REGISTRY_DIR = self._old

    def test_cluster_expansion_does_not_reach_the_scale(self):
        r = db.evaluate_derived()
        self.assertFalse(r["cluster-expansion"]["survived"])

    def test_dobrushin_dies(self):
        r = db.evaluate_derived()
        self.assertFalse(r["dobrushin"]["survived"])

    def test_asymptotic_freedom_is_the_referee_not_new(self):
        r = db.evaluate_derived()
        self.assertTrue(r["asymptotic-freedom"]["survived"])
        self.assertTrue(r["asymptotic-freedom"]["is_referee"])

    def test_all_known_mechanisms_recorded_as_failed_claims(self):
        db.evaluate_derived()
        statements = [f["payload"]["statement"] for f in registry.failed_directions()]
        self.assertTrue(any("cluster-expansion" in s for s in statements))
        self.assertTrue(any("dobrushin" in s for s in statements))
        self.assertTrue(any("asymptotic-freedom" in s for s in statements))


if __name__ == "__main__":
    unittest.main()
