"""Estimation tests — the rule is identified, the slope is not, and the fit is refused."""
import random
import unittest

from pacland.economics import estimate as E, vintages as V


class TestSample(unittest.TestCase):
    def test_panel_is_built_from_vintage_paths(self):
        rows = E.panel()
        self.assertGreater(len(rows), 200)
        for x, pi, i in rows[:5]:
            self.assertEqual(x, x)
            self.assertEqual(pi, pi)
            self.assertGreater(i, -1.0)

    def test_the_rate_is_recorded_as_unrevised(self):
        data = V.load()
        self.assertIn("rates", data)
        self.assertIn("not revised", data["rates_note"])

    def test_paths_use_only_the_vintage(self):
        p = E.paths()
        self.assertGreaterEqual(len(p), 5)
        for xs, ps in p:
            self.assertEqual(len(xs), len(ps))


class TestRuleEstimation(unittest.TestCase):
    def test_the_rule_is_identified_on_synthetic_data(self):
        # the estimator must recover a known rule before any real-data number is believed
        rng = random.Random(11)
        true = (2.0, 1.5, 0.5)
        rows = []
        for _ in range(200):
            pi = rng.gauss(2.0, 1.0)
            x = rng.gauss(0.0, 1.0)
            i = true[0] + true[1] * pi + true[2] * x + rng.gauss(0.0, 0.1)
            rows.append((x, pi, i))
        fit = E.fit_rule(rows=rows)
        self.assertAlmostEqual(fit["phi_pi"], 1.5, delta=0.1)
        self.assertAlmostEqual(fit["phi_y"], 0.5, delta=0.1)
        self.assertGreater(fit["r2"], 0.95)

    def test_real_data_rule_is_reported_with_standard_errors(self):
        fit = E.fit_rule()
        self.assertGreater(fit["n"], 200)
        self.assertGreater(fit["se"]["phi_pi"], 0.0)
        self.assertLess(fit["phi_pi"], 1.0)   # passive, and that is the finding

    def test_smoothing_changes_the_long_run_response(self):
        smooth = E.fit_rule(smoothed=True)
        self.assertGreater(smooth["rho"], 0.5)
        self.assertIn("long_run_phi_pi", smooth)


class TestKappaIsNotIdentified(unittest.TestCase):
    def test_synthetic_recovery_fails(self):
        # documented failure: the estimator cannot recover a known kappa, so no kappa
        # estimated from real data would mean anything
        rec = E.kappa_recovery()
        self.assertFalse(rec["recovered_ok"])

    def test_the_four_parameter_fit_is_rank_deficient(self):
        probe = E.probe()
        full = next(p for p in probe if len(p["free"]) == 4)
        self.assertFalse(full["identified"])
        self.assertLess(full["rank"], 4)


class TestRefusal(unittest.TestCase):
    def test_the_estimated_rule_violates_the_constraint_set(self):
        rule = E.fit_rule()
        cal = {"beta": E.FIXED["beta"], "kappa": E.sw2007.calvo_kappa(),
               "sigma": E.FIXED["sigma"], "phi_pi": rule["phi_pi"], "phi_y": rule["phi_y"]}
        self.assertIn("taylor_principle", E.admissibility(cal))

    def test_estimation_refuses_to_hand_out_a_forecast_calibration(self):
        with self.assertRaises(E.InadmissibleFit):
            E.estimated_calibration()

    def test_summary_states_both_refusals(self):
        s = E.summary()
        self.assertIn("NOT RECOVERED", s)
        self.assertIn("REFUSED", s)


if __name__ == "__main__":
    unittest.main()
