"""The Gaussian comparison survives at weak coupling; the cluster expansion covers strong coupling."""
import tempfile
import unittest
from pathlib import Path

from pacland import registry, gaussian_comparison_survival as gcs


class TestGaussianComparisonSurvival(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self._old = registry.REGISTRY_DIR
        registry.REGISTRY_DIR = Path(self._tmp.name)

    def tearDown(self):
        registry.REGISTRY_DIR = self._old

    def test_integrated_curvature_negative_at_strong_coupling(self):
        self.assertLess(gcs.integrated_curvature(0.2, 1.0), 0.0)

    def test_integrated_curvature_positive_at_weak_coupling(self):
        self.assertGreater(gcs.integrated_curvature(2.0, 1.0), 0.0)

    def test_survival_holds_at_weak_coupling(self):
        r = gcs.run_target()
        self.assertTrue(r["survives_at_weak_coupling"])
        self.assertEqual(r["weak_coupling_threshold"], 0.5)

    def test_recorded_as_survived(self):
        gcs.run_target()
        claims = registry.claims("survived")
        self.assertTrue(any("gaussian-comparison-survival" in c["id"] for c in claims))


if __name__ == "__main__":
    unittest.main()
