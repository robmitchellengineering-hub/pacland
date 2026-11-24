"""C > 0: the dimensionless ratio is positive — the equivalence to the mass gap + the honest status."""
import tempfile
import unittest
from pathlib import Path

from pacland import registry, ratio_positivity as rp


class TestRatioPositivity(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self._old = registry.REGISTRY_DIR
        registry.REGISTRY_DIR = Path(self._tmp.name)

    def tearDown(self):
        registry.REGISTRY_DIR = self._old

    def test_ratio_is_gap_over_scale(self):
        self.assertAlmostEqual(rp.ratio(2.0, 4.0), 0.5)

    def test_ratio_positive_iff_gap_positive(self):
        c_pos, eq = rp.ratio_positive_iff_gap_positive(1.0, 2.0)
        self.assertTrue(c_pos)
        self.assertTrue(eq)  # C > 0 ⟺ m > 0 holds for Λ > 0

    def test_target_states_the_equivalence(self):
        self.assertIn("C > 0 ⟺ m > 0", rp.TARGET["equivalent"])

    def test_run_target_records_as_open(self):
        r = rp.run_target()
        self.assertEqual(r["status"], "open — C > 0 is the Clay statement (mass-gap positivity)")
        self.assertTrue(any("ratio-positivity-C" in c["id"] for c in registry.claims()))


if __name__ == "__main__":
    unittest.main()
