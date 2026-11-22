"""The mass gap as a Gaussian comparison: the non-linearity of the trace and the survival condition."""
import tempfile
import unittest
from pathlib import Path

from pacland import registry, gaussian_comparison as gc


class TestGaussianComparison(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self._old = registry.REGISTRY_DIR
        registry.REGISTRY_DIR = Path(self._tmp.name)

    def tearDown(self):
        registry.REGISTRY_DIR = self._old

    def test_character_is_the_trace(self):
        self.assertAlmostEqual(gc.su2_character(0.0), 2.0)   # Tr 1 = 2 for SU(2)

    def test_curvature_is_negative_at_the_antipode(self):
        # at θ = π, κ = 1/4 − 2β < 0 for β > 1/8
        self.assertLess(gc.bakry_emery_curvature(1.0, math := __import__("math").pi), 0.0)

    def test_naive_comparison_bound_is_negative_for_large_beta(self):
        self.assertLess(gc.naive_comparison_bound(1.0), 0.0)

    def test_target_states_the_typed_inequality(self):
        self.assertIn("Gaussian comparison", gc.TARGET["typed_inequality"])

    def test_run_target_records_as_open(self):
        r = gc.run_target(1.0)
        self.assertEqual(r["status"], "open — the comparison must survive the non-linearity (Wang's criterion)")
        self.assertTrue(any("gaussian-comparison" in c["id"] for c in registry.claims()))


if __name__ == "__main__":
    unittest.main()
