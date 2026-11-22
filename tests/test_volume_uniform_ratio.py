"""The discovery engine, pointed at m/Λ > 0 uniform in V at weak coupling (the three mechanisms)."""
import tempfile
import unittest
from pathlib import Path

from pacland import registry, volume_uniform_ratio as vur


class TestVolumeUniformRatio(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self._old = registry.REGISTRY_DIR
        registry.REGISTRY_DIR = Path(self._tmp.name)

    def tearDown(self):
        registry.REGISTRY_DIR = self._old

    def test_the_three_mechanisms_are_positive_at_weak_coupling(self):
        self.assertGreater(vur.flow_rate_lower_bound(1.0, 4.0, 10.77), 0.0)
        self.assertLess(vur.antipode_suppression(4.0), 1.0)       # measure-suppressed
        self.assertGreater(vur.integrated_curvature(4.0, 1.0), 0.0)  # positive at weak coupling

    def test_candidate_ratio_is_positive_and_v_independent(self):
        r = vur.run_target(betas=(2.0, 3.0, 4.0, 6.0))
        self.assertTrue(r["uniform"])
        self.assertTrue(r["volume_independent"])

    def test_target_states_the_equivalent_bound(self):
        self.assertIn("ξ(β,V,a) ≤ C·e^(12π²/11·β)", vur.TARGET["equivalent_bound"])

    def test_run_target_records_the_claim(self):
        vur.run_target()
        self.assertTrue(any("volume-uniform-ratio" in c["id"] for c in registry.claims()))


if __name__ == "__main__":
    unittest.main()
