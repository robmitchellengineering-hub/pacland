"""Synthetic recovery: every published estimator against a truth we invented."""
import unittest

from pacland.economics import recovery as rec


class TestGate(unittest.TestCase):
    def test_the_audit_is_green(self):
        r = rec.audit()
        self.assertTrue(r["all_pass"], [c for c in r["checks"] if not c["pass"]])
        self.assertEqual(r["n"], 5)


class TestSeededFaultsFire(unittest.TestCase):
    def test_var_fault(self):
        ok, msg = rec.guard_var1()
        self.assertTrue(ok, msg)

    def test_rule_fault(self):
        ok, msg = rec.guard_rule()
        self.assertTrue(ok, msg)

    def test_attenuation_fault(self):
        ok, msg = rec.guard_attenuation()
        self.assertTrue(ok, msg)

    def test_scorer_fault(self):
        ok, msg = rec.guard_scorer()
        self.assertTrue(ok, msg)

    def test_sampling_fault(self):
        ok, msg = rec.guard_sampling()
        self.assertTrue(ok, msg)


class TestWhatEachEstimatorIsWorth(unittest.TestCase):
    def test_the_var_is_recoverable_exactly(self):
        r = rec.var1_recovery()
        self.assertLess(r["error"], 1e-9)

    def test_the_policy_rule_is_recoverable_exactly_from_exogenous_data(self):
        r = rec.rule_recovery()
        self.assertLess(r["error"], 1e-6)

    def test_measurement_error_does_not_wash_out_with_more_data(self):
        r = rec.attenuation_demo()
        self.assertTrue(r["pass"])
        self.assertLess(r["mean_estimate"], r["truth"] - 0.2)

    def test_the_scorer_is_honest_at_the_edges(self):
        r = rec.scorer_checks()
        self.assertEqual(r["mae_perfect"], 0.0)
        self.assertEqual(r["mae_offset"], 1.0)
        self.assertEqual(r["ratio_perfect"], 0.0)

    def test_the_sampling_exponent_is_measured_not_assumed(self):
        law = rec.sampling_law()
        self.assertLess(law["exponent"], 0.0)
        self.assertGreater(law["n_for_1pct"], 1000)


if __name__ == "__main__":
    unittest.main()
