"""The RG side: asymptotic freedom gives the exponential weak-coupling scale (V-independent)."""
import tempfile
import unittest
from pathlib import Path

from pacland import registry, rg_side as rs


class TestRgSide(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self._old = registry.REGISTRY_DIR
        registry.REGISTRY_DIR = Path(self._tmp.name)

    def tearDown(self):
        registry.REGISTRY_DIR = self._old

    def test_scale_decays_exponentially(self):
        # Λ(β) is smaller at larger β (weak coupling)
        self.assertLess(rs.rg_scale(4.0), rs.rg_scale(2.0))

    def test_scale_is_positive_and_v_independent(self):
        r = rs.run_target()
        self.assertTrue(r["scale_exponential"])
        self.assertTrue(r["volume_independent"])

    def test_target_names_the_open_part(self):
        self.assertIn("C > 0", rs.TARGET["open_part"])

    def test_run_target_records_scale_as_open(self):
        rs.run_target()
        self.assertTrue(any("rg-side-scale" in c["id"] for c in registry.claims()))


if __name__ == "__main__":
    unittest.main()
