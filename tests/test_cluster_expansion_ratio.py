"""The cluster-expansion V-independent bound + the three mechanisms → the V-uniform ratio."""
import tempfile
import unittest
from pathlib import Path

from pacland import registry, cluster_expansion_ratio as cer


class TestClusterExpansionRatio(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self._old = registry.REGISTRY_DIR
        registry.REGISTRY_DIR = Path(self._tmp.name)

    def tearDown(self):
        registry.REGISTRY_DIR = self._old

    def test_cluster_correction_is_v_independent(self):
        # the correction depends on K and β, NOT on V
        self.assertAlmostEqual(cer.cluster_correction(1.0, 3.0), 1.0 * __import__("math").exp(-6.0))

    def test_combined_ratio_is_positive_and_v_independent(self):
        r = cer.run_target(betas=(2.0, 3.0, 4.0, 6.0))
        self.assertTrue(r["uniform"])
        self.assertTrue(r["volume_independent"])

    def test_ratio_is_the_same_for_every_volume(self):
        # V-independence by construction: the correction has no V, so every volume agrees
        r = cer.check_v_uniform(1.0, 10.77, 1.0, (4.0,), volumes=(8, 64, 10 ** 6))
        self.assertEqual(len(r["ratio_values"]), 1)

    def test_run_target_records_the_claim(self):
        cer.run_target()
        self.assertTrue(any("cluster-expansion-v-uniform-ratio" in c["id"] for c in registry.claims()))


if __name__ == "__main__":
    unittest.main()
