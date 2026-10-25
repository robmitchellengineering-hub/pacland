"""Three-way tests — the derived calibration, the run, and the honesty of the label."""
import unittest

from pacland.economics import nk3, sw2007, three_way as T


class TestCalibration(unittest.TestCase):
    def test_kappa_comes_from_the_published_calvo_estimate(self):
        self.assertAlmostEqual(T.sw_calibration()["kappa"], sw2007.calvo_kappa(), places=15)

    def test_policy_rule_is_the_published_one(self):
        cal = T.sw_calibration()
        self.assertEqual(cal["phi_pi"], sw2007.PUBLISHED_STRUCTURAL["r_pi"])
        self.assertEqual(cal["phi_y"], sw2007.PUBLISHED_STRUCTURAL["r_y"])

    def test_discount_factor_is_the_detrended_one(self):
        self.assertAlmostEqual(T.sw_calibration()["beta"], sw2007.beta_tilde(), places=15)

    def test_borrowed_persistence_is_labelled(self):
        self.assertEqual(set(T.BORROWED_PERSISTENCE), {"rho_r", "rho_u"})

    def test_it_is_not_the_textbook_calibration(self):
        self.assertNotAlmostEqual(T.sw_calibration()["kappa"], nk3.CALIBRATION["kappa"])


class TestRun(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = T.run()

    def test_all_four_arms_are_present(self):
        self.assertEqual(set(self.r), {"sw_subsystem", "nk3", "var1", "params"})

    def test_every_arm_contains_the_null(self):
        for arm in ("sw_subsystem", "nk3"):
            self.assertIn("no-change", self.r[arm])

    def test_the_sw_subsystem_run_reports_its_parameters(self):
        self.assertEqual(self.r["sw_subsystem"]["_meta"]["params"],
                         T.sw_calibration())


class TestFinding(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.f = T.finding()

    def test_the_sw_subsystem_loses_to_the_null_on_inflation(self):
        # the measured result; if it flips, the doc and this test must move together
        self.assertTrue(self.f["sw_loses_pi"])
        for h in (1, 2, 4):
            self.assertGreater(self.f["ratios_pi"][h], 1.0, f"h={h}")

    def test_it_beats_the_null_on_the_gap_at_four_quarters(self):
        self.assertTrue(self.f["sw_beats_gap_h4"])
        self.assertLess(self.f["ratios_gap"][4], 1.0)

    def test_sw_parameters_do_not_rescue_the_inflation_forecast(self):
        # the finding worth having: the loss is not a parameter accident
        self.assertGreater(self.f["ratios_pi"][1], 1.0)
        self.assertLess(abs(self.f["ratios_pi"][1] - 1.0), 0.1)

    def test_the_summary_says_it_is_not_the_sw_model(self):
        s = T.summary()
        self.assertIn("It is NOT the 20-condition SW model", s)


if __name__ == "__main__":
    unittest.main()
