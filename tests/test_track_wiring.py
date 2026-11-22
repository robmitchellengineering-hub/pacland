"""The four tracks are wired into the engine as hypotheses + falsifiers (action 4)."""
import tempfile
import unittest
from pathlib import Path

from pacland import registry, track_wiring as tw
from pacland import runner


class TestTrackWiring(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self._old = registry.REGISTRY_DIR
        registry.REGISTRY_DIR = Path(self._tmp.name)

    def tearDown(self):
        registry.REGISTRY_DIR = self._old

    def test_four_tracks_register_as_hypotheses(self):
        n = tw.register_tracks()
        self.assertEqual(n, 4)
        from pacland import hypotheses
        self.assertIn("coulomb", hypotheses.HYPOTHESES)
        self.assertIn("rg", hypotheses.HYPOTHESES)
        self.assertIn("gribov", hypotheses.HYPOTHESES)
        self.assertIn("curvature", hypotheses.HYPOTHESES)

    def test_falsifiers_are_wired_into_the_runner(self):
        tw.wire_falsifiers()
        for key in ("string-tension-positive", "flow-curvature-bounded",
                    "gribov-no-residual-copy", "curvature-measure-negligible"):
            self.assertIn(key, runner.FALSIFIERS)

    def test_flow_curvature_falsifier_runs(self):
        tw.wire_falsifiers()
        survived, evidence = runner.FALSIFIERS["flow-curvature-bounded"]()
        self.assertTrue(survived)
        self.assertIn("FRG", evidence)

    def test_unresolved_tracks_are_honest_not_a_verdict(self):
        tw.wire_falsifiers()
        survived, evidence = runner.FALSIFIERS["gribov-no-residual-copy"]()
        self.assertFalse(survived)
        self.assertIn("unresolved", evidence)

    def test_run_track_records_a_claim(self):
        tw.wire_falsifiers()
        out = tw.run_track("rg")
        self.assertTrue(out["survived"])
        claims = registry.claims()
        self.assertTrue(any("track-rg" in c["id"] for c in claims))


if __name__ == "__main__":
    unittest.main()
