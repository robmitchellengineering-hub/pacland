"""Vintage sensitivity: is the null-beating finding about forecasting or about revisions?"""
import unittest

from pacland.economics import vintage_sensitivity as vs


class TestStability(unittest.TestCase):
    def test_the_conclusion_holds_in_both_revision_regimes(self):
        s = vs.stability()
        self.assertTrue(s["both_regimes"], s["verdict"])
        self.assertLess(s["worst_ratio_shift"], 0.25)

    def test_the_var_beats_the_null_at_every_horizon_in_both_regimes(self):
        s = vs.stability()
        for h, v in s["verdict"]["VAR(1)"].items():
            self.assertLess(v["latest"], 1.0, h)
            self.assertLess(v["next"], 1.0, h)

    def test_both_regimes_are_actually_different(self):
        # if the two regimes produced identical numbers the check would be measuring nothing
        s = vs.stability()
        self.assertGreater(s["worst_ratio_shift"], 1e-3)

    def test_the_forecast_counts_are_disclosed(self):
        s = vs.stability()
        self.assertEqual(set(s["forecasts"]), {"latest", "next"})
        self.assertGreater(s["forecasts"]["latest"], 0)


class TestSeededFault(unittest.TestCase):
    def test_a_look_ahead_regime_is_detected(self):
        ok, msg = vs.guard_no_lookahead()
        self.assertTrue(ok, msg)

    def test_the_audit_is_green(self):
        r = vs.audit()
        self.assertTrue(r["all_pass"], r["checks"])


if __name__ == "__main__":
    unittest.main()
