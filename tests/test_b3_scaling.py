"""The two b3 scales — one is a clean exponential, the other is not, and the product survives both."""
import unittest

from pacland.exactness import b3_scaling as S


class TestTheContentScale(unittest.TestCase):
    def test_the_content_factor_is_about_8_55_per_unit_b3(self):
        self.assertAlmostEqual(S.per_unit_factor(S.CONTENT)["factor"], 8.554, places=2)

    def test_the_content_intervals_agree(self):
        # 8.602 then 8.507 -- a clean exponential, which is what makes A quotable
        r = S.per_unit_factor(S.CONTENT)
        self.assertTrue(r["consistent_exponential"])
        fs = [f for _, _, f in r["intervals"]]
        self.assertLess((max(fs) - min(fs)) / (sum(fs) / len(fs)), 0.02)


class TestTheAccessibilityScale(unittest.TestCase):
    def test_it_falls_but_not_exponentially(self):
        # per-interval 0.575 then 0.308: the rate steepens, so a single B would hide that
        r = S.per_unit_factor(S.ACCESSIBILITY)
        self.assertLess(r["factor"], 1.0)
        self.assertFalse(r["consistent_exponential"])

    def test_the_steepening_is_visible(self):
        fs = [f for _, _, f in S.per_unit_factor(S.ACCESSIBILITY)["intervals"]]
        self.assertLess(fs[1], fs[0])


class TestTheProduct(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s = S.scales()

    def test_the_product_exceeds_one_on_every_interval(self):
        self.assertGreater(self.s["product_range"][0], 1.0)

    def test_the_verdict_says_grows(self):
        self.assertIn("GROWS", self.s["verdict"])

    def test_the_caveat_names_the_window_problem(self):
        self.assertIn("windows scale together", self.s["caveat"])
        self.assertIn("heuristic", self.s["caveat"])

    def test_the_falsifier_is_stated(self):
        self.assertIn("fourth b3", self.s["falsifier"])


if __name__ == "__main__":
    unittest.main()


class TestThePreRegisteredPrediction(unittest.TestCase):
    """The b3=14 extrapolation test, on record before the measurement."""

    def test_the_two_branches_differ_by_about_2x(self):
        p = S.PREDICTION_B3_14
        self.assertAlmostEqual(p["steepening_points"], 1.04, places=1)
        self.assertAlmostEqual(p["global_fit_points"], 2.54, places=1)

    def test_a_measurement_of_one_point_lands_on_the_steepening_branch(self):
        r = S.check_prediction(1)
        self.assertIn("steepening", r["verdict"])

    def test_a_measurement_of_three_points_lands_on_the_global_fit(self):
        r = S.check_prediction(3)
        self.assertIn("global", r["verdict"])

    def test_zero_points_is_recorded_as_a_rate_not_a_failure(self):
        r = S.check_prediction(0)
        self.assertEqual(r["measured_rate"], 0.0)


class TestTheConePrediction(unittest.TestCase):
    """Pre-registered before h12=6's shape was read: the rate must track cone structure monotonically."""

    def test_the_three_measured_rungs(self):
        self.assertEqual(S.CONES[6]["rays"], 2)
        self.assertEqual(S.CONES[10]["rays"], 4)
        self.assertEqual(S.CONES[12]["rays"], 5)

    def test_the_prediction_follows_from_the_measured_rate(self):
        # b3=14's rate is 10x the b3=12 rate, so under monotonicity it must have FEWER rays
        self.assertGreater(S.CONES[14]["rate"], 10 * S.CONES[12]["rate"])
        self.assertLess(S.PREDICTION_CONE_MONOTONE["rays_max"], S.CONES[12]["rays"])

    def test_a_small_cone_confirms(self):
        self.assertIn("tracks cone structure", S.cone_verdict(3, 9)["verdict"])

    def test_a_large_cone_refutes(self):
        self.assertIn("REFUTED", S.cone_verdict(7, 14)["verdict"])


class TestTheConeVerdictIsIn(unittest.TestCase):
    """The pre-registered prediction was REFUTED by the measurement: rays = 8, not <= 4."""

    def test_the_measured_shape_is_recorded(self):
        self.assertEqual(S.CONES[14]["rays"], 8)
        self.assertEqual(S.CONES[14]["hp"], 7)

    def test_the_rays_rise_monotonically_with_b3(self):
        # 2, 4, 5, 8 -- the cone gets bigger at every rung
        rays = [S.CONES[b]["rays"] for b in (6, 10, 12, 14)]
        self.assertEqual(rays, sorted(rays))
        self.assertEqual(rays, [2, 4, 5, 8])

    def test_the_rate_does_NOT_follow_the_rays(self):
        # the rate dips at b3=12 (0.00137) and recovers at b3=14 (0.0151) while rays only grow
        rates = [S.CONES[b]["rate"] for b in (6, 10, 12, 14)]
        self.assertLess(rates[2], rates[1])
        self.assertGreater(rates[3], rates[2])

    def test_the_verdict_is_refuted(self):
        v = S.cone_verdict(S.CONES[14]["rays"], S.CONES[14]["hp"])
        self.assertIn("REFUTED", v["verdict"])


class TestTheBudgetVerdict(unittest.TestCase):
    """The budget test decides the accessibility question, and the answer is: it was our budget, not the landscape."""

    @classmethod
    def setUpClass(cls):
        cls.v = S.budget_verdict()

    def test_more_tries_recover_the_yield(self):
        # base 2+0 points, wide 8+8 points, control (b3=14) 6+8
        self.assertEqual(self.v["base_points"], 2)
        self.assertEqual(self.v["wide_points"], 16)
        self.assertEqual(self.v["control_points"], 14)
        self.assertTrue(self.v["yield_recovered_by_more_tries"])

    def test_a_deeper_solve_does_not(self):
        # newton_max_iters=1000 at the same try count: 0 + 0
        self.assertEqual(self.v["deep_points"], 0)
        self.assertFalse(self.v["yield_recovered_by_deeper_solve"])

    def test_the_cost_is_tenfold(self):
        self.assertGreater(self.v["cost_ratio"], 8.0)

    def test_the_verdict_demotes_the_minimum(self):
        self.assertIn("BUDGET ARTEFACT", self.v["verdict"])
        self.assertIn("points-per-budget", self.v["consequence"])
