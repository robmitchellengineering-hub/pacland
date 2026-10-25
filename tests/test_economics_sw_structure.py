"""SW equilibrium-condition inventory tests — the derivation and its stated scope."""
import unittest

from pacland.economics import sw2007, sw_structure as S


class TestInventory(unittest.TestCase):
    def test_twenty_conditions_are_listed(self):
        self.assertEqual(len(S.CONDITIONS), 20)

    def test_every_condition_has_a_verdict_and_a_reference(self):
        ok, msg = S.guard_conditions_inventory()
        self.assertTrue(ok, msg)

    def test_a_condition_with_no_verdict_is_refused(self):
        bad = S.Condition(key="probe", paper_ref="", verdict="probably", note="")
        saved = S.CONDITIONS
        try:
            S.CONDITIONS = saved + (bad,)
            ok, msg = S.guard_conditions_inventory()
        finally:
            S.CONDITIONS = saved
        self.assertFalse(ok)
        self.assertIn("UNSETTLED", msg)

    def test_coverage_is_counted_and_not_complete(self):
        cov = S.coverage()
        self.assertEqual(cov["n_total"], 20)
        self.assertEqual(cov["n_proved"], 13)
        self.assertEqual(cov["n_dynamic_only"], 3)
        self.assertEqual(cov["n_cited"], 4)
        # ...which is why the roster must NOT claim exact_structure yet
        self.assertFalse(cov["complete"])

    def test_dynamic_and_cited_are_named(self):
        cov = S.coverage()
        self.assertIn("calvo_price_foc", cov["dynamic_only"])
        self.assertIn("shock_processes", cov["cited"])


class TestSteadyState(unittest.TestCase):
    def test_nominal_rate_from_the_euler_equation(self):
        self.assertAlmostEqual(S.nominal_rate_quarterly() * 100, 1.5407, places=4)

    def test_fisher_exact_and_additive_differ_only_by_the_cross_term(self):
        exact = S.fisher_exact_annual_pct()
        additive = sw2007.nominal_rate_annual_pct()
        self.assertLess(abs(exact - additive), 0.05)
        self.assertGreater(exact, additive)

    def test_rental_rate(self):
        self.assertAlmostEqual(S.rental_rate(), S.real_rate_quarterly() + S.DELTA, places=15)

    def test_capital_output_ratio_rises_with_markups(self):
        low = S.capital_output_ratio(1 / 1.3)
        high = S.capital_output_ratio(1 / 1.1)
        self.assertGreater(high, low)

    def test_shares_exhaust_output(self):
        sh = S.shares(1 / 1.2)
        self.assertAlmostEqual(sh["c_over_y"] + sh["i_over_y"] + sh["g_over_y"], 1.0, places=12)
        self.assertGreater(sh["c_over_y"], 0.0)

    def test_investment_share_is_depreciation_times_capital(self):
        sh = S.shares(1 / 1.2)
        self.assertAlmostEqual(sh["i_over_y"], S.DELTA * sh["k_over_y"], places=12)


class TestGuards(unittest.TestCase):
    def test_shares_guard_green(self):
        ok, msg = S.guard_steady_state_shares()
        self.assertTrue(ok, msg)

    def test_shares_guard_red_when_government_swallows_everything(self):
        ok, msg = S.guard_steady_state_shares(g_over_y=0.95)
        self.assertFalse(ok)
        self.assertIn("DOES NOT SUM", msg)

    def test_cost_identity_green_on_a_crs_technology(self):
        ok, msg = S.guard_cost_identity()
        self.assertTrue(ok, msg)
        self.assertIn("consistent (CRS)", msg)

    def test_cost_identity_red_when_the_technology_is_not_crs(self):
        # the seeded fault: labour exponent below 1-alpha
        ok, msg = S.guard_cost_identity(labour_exponent=0.6)
        self.assertFalse(ok)
        self.assertIn("INCONSISTENT", msg)

    def test_policy_rule_contrast_is_stated(self):
        self.assertIn("ANY inflation target", S.summary())


if __name__ == "__main__":
    unittest.main()
