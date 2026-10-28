"""The known-truth battery: controls recover, naive estimators fail where they must."""
import unittest

from pacland.causal import battery as B


class TestControls(unittest.TestCase):
    def test_clean_did_recovers(self):
        res = B.run(reps=20)
        cell = next(c for c in res["cells"] if c.dgp == "clean DiD")
        self.assertTrue(cell.recovered, cell)

    def test_iv_recovers_under_measurement_error(self):
        res = B.run(reps=20)
        cell = next(c for c in res["cells"]
                    if c.dgp == "measurement error" and c.estimator == "iv_2sls")
        self.assertTrue(cell.recovered, cell)


class TestFailures(unittest.TestCase):
    def test_did_fails_when_trends_are_broken(self):
        res = B.run(reps=20)
        cell = next(c for c in res["cells"] if c.dgp == "broken trends")
        self.assertFalse(cell.recovered, cell)
        self.assertGreater(cell.bias, 0.5)

    def test_ols_is_attenuated_under_measurement_error(self):
        res = B.run(reps=20)
        cell = next(c for c in res["cells"]
                    if c.dgp == "measurement error" and c.estimator == "ols_slope")
        # the textbook factor is var(x*)/(var(x*)+var(e)) = 0.5 with these variances
        self.assertAlmostEqual(cell.estimate, 0.5, delta=0.1)

    def test_2sls_is_unreliable_with_a_weak_instrument(self):
        res = B.run(reps=20)
        cell = next(c for c in res["cells"]
                    if c.dgp == "weak instrument" and c.estimator == "iv_2sls")
        self.assertFalse(cell.recovered, cell)
        self.assertLess(cell.recovery_rate, 0.3)


class TestMechanism(unittest.TestCase):
    def test_twfe_bias_tracks_effect_growth_and_nyt_does_not(self):
        sens = B.staggered_sensitivity(reps=8)
        self.assertTrue(sens["pass"], sens["detail"])
        self.assertGreater(sens["twfe_shift"], sens["nyt_shift"])


class TestReproducibility(unittest.TestCase):
    def test_the_same_seed_gives_the_same_battery(self):
        a = B.run(reps=4, seed=5)
        b = B.run(reps=4, seed=5)
        self.assertEqual([c.estimate for c in a["cells"]], [c.estimate for c in b["cells"]])


class TestAudit(unittest.TestCase):
    def test_the_battery_has_teeth(self):
        self.assertTrue(B.audit()["all_pass"])


if __name__ == "__main__":
    unittest.main()
