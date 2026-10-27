"""The invariance gate: four checks, four seeded faults, and the honest limits."""
import unittest

from pacland.economics import invariance as inv
from pacland.economics import national_accounts as na


class TestTheGatePasses(unittest.TestCase):
    def test_the_audit_is_green(self):
        report = inv.audit()
        self.assertTrue(report["all_pass"], [c for c in report["checks"] if not c["pass"]])
        self.assertEqual(report["n"], 4)


class TestEachSeededFaultFires(unittest.TestCase):
    """A guard that cannot go red on its own fault is not a guard."""

    def test_units_guard_notices_a_single_component_rescale(self):
        ok, _ = inv.guard_units(None, 1000.0)
        self.assertTrue(ok)

    def test_base_year_guard_notices_levels_differing(self):
        ok, msg = inv.guard_base_year()
        self.assertTrue(ok, msg)
        self.assertIn("levels differed", msg)

    def test_deflator_guard_notices_an_additive_real_record(self):
        ok, msg = inv.guard_deflator()
        self.assertTrue(ok, msg)

    def test_parametrisation_guard_notices_the_intercept_free_fit(self):
        ok, msg = inv.guard_parametrisation()
        self.assertTrue(ok, msg)
        self.assertIn("intercept-free", msg)


class TestWhatTheChecksActuallyClaim(unittest.TestCase):
    def test_shares_are_exact_under_rescaling(self):
        r = inv.unit_invariance(None, 1000.0)
        self.assertLess(r["worst_share_drift"], 1e-12)
        # additivity closes to publication rounding, NOT to 1e-12 — asserting 1e-12 would be
        # asserting that rounded national statistics are exact
        self.assertLess(r["worst_residual_drift"], 1e-5)

    def test_inflation_is_untouched_by_the_base_year(self):
        r = inv.base_year_invariance()
        self.assertLess(r["worst_rate_drift"], 1e-12)

    def test_the_real_side_is_the_one_that_leaks(self):
        r = inv.deflator_asymmetry()
        self.assertTrue(r["nominal_closes"])
        self.assertTrue(r["real_leaks"])
        self.assertGreater(r["worst_real_residual_pp"], 1.0)

    def test_log_log_recovers_the_truth_and_level_ols_does_not(self):
        r = inv.parametrisation_invariance(0.62)
        self.assertLess(r["error_log"], 1e-9)
        self.assertGreater(r["error_level"], 1e-3)
        self.assertTrue(r["level_is_description_dependent"])

    def test_a_model_claiming_real_additivity_would_be_refused(self):
        # the gate's polarity: it passes when real data does NOT add
        r = inv.deflator_asymmetry()
        self.assertTrue(r["pass"])


if __name__ == "__main__":
    unittest.main()
