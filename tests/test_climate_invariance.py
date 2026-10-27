"""The climate invariance gate, and the claim it corrected."""
import unittest

from pacland.climate import invariance as inv


class TestGate(unittest.TestCase):
    def test_the_audit_is_green(self):
        r = inv.audit()
        self.assertTrue(r["all_pass"], [c for c in r["checks"] if not c["pass"]])
        self.assertEqual(r["n"], 3)


class TestSeededFaultsFire(unittest.TestCase):
    def test_baseline_fault(self):
        ok, msg = inv.guard_baseline()
        self.assertTrue(ok, msg)
        self.assertIn("shifted window", msg)

    def test_units_fault(self):
        ok, msg = inv.guard_units()
        self.assertTrue(ok, msg)
        self.assertIn("273.15", msg)

    def test_window_fault(self):
        ok, msg = inv.guard_window()
        self.assertTrue(ok, msg)
        self.assertIn("worse than persistence", msg)


class TestWhatTheClaimsNowSay(unittest.TestCase):
    """The gate's real output: a claim narrowed to what survives."""

    def test_baseline_changes_the_offset_not_the_trend(self):
        r = inv.baseline_invariance()
        self.assertTrue(r["offset_moved"])
        self.assertLess(r["rate_drift"], 1e-10)

    def test_skill_scores_are_unit_free(self):
        r = inv.units_invariance()
        self.assertTrue(r["levels_moved"])
        self.assertLess(r["worst_skill_drift"], 1e-9)

    def test_the_robust_claim_holds(self):
        r = inv.window_invariance()
        self.assertTrue(r["trend_beats_persistence_everywhere"])

    def test_the_ranking_claim_is_not_made_because_it_flips(self):
        r = inv.window_invariance()
        # documented, not asserted: only one window of four has the trend as winner
        self.assertFalse(r["ranking_stable"])
        self.assertGreaterEqual(r["emulator_wins"], 1)


if __name__ == "__main__":
    unittest.main()
