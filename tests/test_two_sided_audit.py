"""The two-sided audit: exact claims owe no prediction, and a fit is judged by its intervals."""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("tsa", ROOT / "scripts" / "two_sided_audit.py")


def _module():
    mod = importlib.util.module_from_spec(SPEC)
    SPEC.loader.exec_module(mod)
    return mod


class TestTwoSidedAudit(unittest.TestCase):

    def test_the_degrees_of_freedom_are_counted_not_guessed(self):
        r = _module().fit_report("x", ((2, 20), (4, 1480), (6, 107100)))
        self.assertEqual(r["n_points"], 3)
        self.assertEqual(r["n_params"], 2)
        self.assertEqual(r["dof"], 1)

    def test_a_perfect_exponential_has_agreeing_intervals(self):
        r = _module().fit_report("x", ((1, 10.0), (2, 100.0), (3, 1000.0)))
        self.assertTrue(r["intervals_agree"])
        self.assertAlmostEqual(r["interval_spread"], 1.0, places=6)

    def test_the_accessibility_intervals_disagree(self):
        r = _module().fit_report("accessibility", _module().B.ACCESSIBILITY)
        self.assertFalse(r["intervals_agree"])
        self.assertGreater(r["interval_spread"], 1.5)

    def test_the_content_intervals_agree_and_it_is_not_called_an_exact_law(self):
        r = _module().fit_report("content", _module().B.CONTENT)
        self.assertTrue(r["intervals_agree"])
        self.assertGreater(r["interval_spread"], 1.0)     # agreement is real, but it is not exact

    def test_r_squared_can_hide_disagreeing_intervals(self):
        # the point of reporting intervals: a high R^2 is compatible with a bad form
        r = _module().fit_report("accessibility", _module().B.ACCESSIBILITY)
        self.assertGreater(r["r2"], 0.95)
        self.assertFalse(r["intervals_agree"])


if __name__ == "__main__":
    unittest.main()
