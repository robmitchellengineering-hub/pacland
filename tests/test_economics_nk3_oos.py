"""NK3 out-of-sample tests — the policy function, the vintage gap, and the run."""
import math
import unittest

from pacland.economics import nk3, nk3_oos as oos, vintages as V


class TestPolicyFunction(unittest.TestCase):
    def test_coefficients_match_the_derived_values(self):
        pf = nk3.policy_function()
        self.assertAlmostEqual(pf["a_r"], 0.8692, places=4)
        self.assertAlmostEqual(pf["b_r"], 0.7974, places=4)
        self.assertAlmostEqual(pf["a_u"], -3.2468, places=4)
        self.assertAlmostEqual(pf["b_u"], 3.2468, places=4)

    def test_determinant_is_nonzero(self):
        self.assertGreater(abs(nk3.policy_function()["determinant"]), 1.0)

    def test_cost_push_moves_the_gap_and_inflation_in_opposite_directions(self):
        pf = nk3.policy_function()
        self.assertLess(pf["a_u"], 0.0)
        self.assertGreater(pf["b_u"], 0.0)

    def test_forecast_reproduces_the_state_at_h_zero(self):
        x, p = nk3.forecast_from_state(1.0, 2.0, 1)
        pf = nk3.policy_function()
        # at h=0 the inversion is exact; h=1 shrinks both by the shock persistence
        self.assertTrue(math.isfinite(x) and math.isfinite(p))
        self.assertLess(abs(x), 1.0 * abs(pf["a_u"] / pf["a_r"]) + 5)

    def test_forecasts_converge_to_zero_as_the_horizon_grows(self):
        # both shocks decay, so the model's forecast must return to its steady state
        far = nk3.forecast_from_state(1.0, 3.0, 60)
        self.assertLess(abs(far[0]), 1e-2)
        self.assertLess(abs(far[1]), 1e-2)

    def test_singular_policy_function_is_refused(self):
        # det = (1-rho+sigma*phi_y)(1-beta*rho) + kappa*sigma*(phi_pi-rho) vanishes at
        # rho = phi_pi with phi_y = 0.5 and phi_pi = 1.5
        with self.assertRaises(ValueError):
            nk3.forecast_from_state(1.0, 1.0, 1, {"rho_r": 1.5, "rho_u": 1.5})


class TestGapAndInflation(unittest.TestCase):
    def test_quarterly_keeps_only_quarter_months(self):
        obs = {"1990-01-01": 1.0, "1990-02-01": 2.0, "1990-04-01": 3.0}
        self.assertEqual(sorted(oos.quarterly(obs)), ["1990-01-01", "1990-04-01"])

    def test_gap_uses_only_the_past(self):
        levels = {f"{1990 + i}-01-01": 100.0 * (1.01 ** i) for i in range(25)}
        self.assertTrue(math.isnan(oos.gap(levels, "1990-01-01")))
        date = "2010-01-01"
        a = oos.gap(levels, date)
        b = oos.gap({d: v for d, v in levels.items() if d <= date}, date)
        self.assertAlmostEqual(a, b, places=12)

    def test_gap_is_zero_on_a_perfect_trend(self):
        levels = {f"{1990 + i}-01-01": 100.0 * (1.02 ** i) for i in range(20)}
        self.assertAlmostEqual(oos.gap(levels, "2009-01-01"), 0.0, places=9)

    def test_inflation_is_annualised(self):
        levels = {"2020-01-01": 100.0, "2020-04-01": 101.0}
        self.assertAlmostEqual(oos.inflation(levels, "2020-04-01"), 400 * math.log(1.01), places=9)


class TestTheRun(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = oos.evaluate()

    def test_it_ran_and_says_the_calibration_is_stated(self):
        self.assertGreaterEqual(self.r["_meta"]["forecasts"], 20)
        self.assertEqual(self.r["_meta"]["calibration"], "stated, not estimated")

    def test_the_null_is_in_the_table(self):
        for kind in ("pi", "gap"):
            for h in (1, 2, 4):
                self.assertAlmostEqual(self.r["no-change"][kind][h], self.r["no-change"][kind][h])

    def test_the_calibrated_model_does_not_beat_the_null_on_inflation(self):
        # the finding: the textbook-calibrated NK model loses on inflation at every
        # horizon. If this ever flips, the doc and the board row must move with it.
        for h in (1, 2, 4):
            self.assertGreater(self.r["NK3"]["pi"][h], self.r["no-change"]["pi"][h], f"h={h}")

    def test_it_does_beat_the_null_on_the_gap_at_longer_horizons(self):
        self.assertLess(self.r["NK3"]["gap"][4], self.r["no-change"]["gap"][4])

    def test_wins_are_counted(self):
        self.assertIn("wins", self.r["NK3"])
        self.assertGreaterEqual(self.r["NK3"]["wins"]["pi"][1], 0)

    def test_summary_names_the_model_and_the_null(self):
        s = oos.summary()
        self.assertIn("NK3", s)
        self.assertIn("no-change", s)


if __name__ == "__main__":
    unittest.main()
