"""The cluster-expansion convergence constant K — the target, the structure, and the honest status."""
import tempfile
import unittest
from pathlib import Path

from pacland import registry, cluster_expansion_constant as cec


class TestClusterExpansionConstant(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self._old = registry.REGISTRY_DIR
        registry.REGISTRY_DIR = Path(self._tmp.name)

    def tearDown(self):
        registry.REGISTRY_DIR = self._old

    def test_activity_is_exp_neg_beta(self):
        self.assertAlmostEqual(cec.activity(2.0), __import__("math").exp(-2.0))

    def test_mayer_condition_is_the_sum_bound(self):
        self.assertTrue(cec.mayer_condition(0.5))
        self.assertFalse(cec.mayer_condition(2.0))

    def test_target_names_K_as_the_open_quantity(self):
        self.assertIn("K", cec.TARGET["open_quantity"])

    def test_run_target_records_K_as_open(self):
        r = cec.run_target()
        self.assertEqual(r["status"], "open — K requires the Mayer-expansion combinatorics")
        # the claim is recorded as OPEN, not survived (K is not derived)
        self.assertTrue(any("cluster-expansion-constant-K" in c["id"] for c in registry.claims()))


if __name__ == "__main__":
    unittest.main()
