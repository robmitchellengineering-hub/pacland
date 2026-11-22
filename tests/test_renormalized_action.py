"""Rung A's reconciliation: the mass gap follows 12π²/11 (β-function), not 8π²/g² (instanton)."""
import unittest

from pacland import renormalized_action as ra


class TestRenormalizedAction(unittest.TestCase):
    def test_su2_exponent_is_12pi2_over_11(self):
        c = ra.mass_gap_exponent(2.0)
        self.assertAlmostEqual(c, 12 * __import__("math").pi ** 2 / 11, places=10)

    def test_instanton_is_a_different_scale(self):
        # the instanton action 8π² is NOT the mass-gap exponent 12π²/11
        self.assertNotAlmostEqual(ra.instanton_action(), ra.mass_gap_exponent(2.0), places=3)

    def test_ratio_is_22_over_3(self):
        r = ra.reconcile(2.0)
        self.assertAlmostEqual(r["ratio_instanton_over_gap"], 22.0 / 3.0, places=6)

    def test_conclusion_states_the_reconciliation(self):
        r = ra.reconcile(2.0)
        self.assertIn("12π²/11", r["conclusion"])
        self.assertIn("NOT the instanton", r["conclusion"])


if __name__ == "__main__":
    unittest.main()
