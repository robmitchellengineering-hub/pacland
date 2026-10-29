"""The zero computation must reproduce known values, and the statistics need the right control."""
import unittest

from pacland.spectral import zeros as Z


class TestZeta(unittest.TestCase):
    def test_the_first_five_zeros_are_reproduced(self):
        v = Z.validate()
        self.assertTrue(v["pass"], v["max_error"])
        self.assertLess(v["max_error"], 1e-9)

    def test_the_zero_count_matches_the_counting_formula(self):
        zs = Z.find_zeros(t_to=200.0)
        self.assertLessEqual(abs(len(zs) - round(Z.smooth_count(200.0))), 1)

    def test_the_engines_agree_at_low_height(self):
        rs = Z.find_zeros(t_to=60.0)
        em = Z.zeros_euler_maclaurin(60.0)
        self.assertLess(max(abs(a - b) for a, b in zip(rs, em)), 1e-2)


class TestStatistics(unittest.TestCase):
    def test_spacings_unfold_to_mean_one(self):
        zs = Z.find_zeros(t_to=400.0)
        sp = Z.unfolded_spacings(zs)
        self.assertAlmostEqual(sum(sp) / len(sp), 1.0, delta=0.05)

    def test_the_estimator_on_synthetic_gue_landing_near_its_own_mean(self):
        g = Z.gue_control(200)
        self.assertAlmostEqual(g["mean"], 0.61, delta=0.05)

    def test_the_asymptotic_value_is_not_the_finite_sample_one(self):
        g = Z.gue_control(200)
        self.assertGreater(abs(g["mean"] - Z.RATIO_GUE), 0.05)


class TestAudit(unittest.TestCase):
    def test_all_checks_are_green(self):
        a = Z.audit()
        self.assertTrue(a["all_pass"], [c for c in a["checks"] if not c["pass"]])

    def test_the_run_is_now_deep_enough_to_tighten_the_statistic(self):
        a = Z.audit()
        self.assertGreaterEqual(a["n_zeros"], 1500)
        # the control spread must be small enough that "not Poisson" is not a matter of taste
        self.assertLess(a["gue"]["sd"], 0.02)

    def test_the_zeros_beat_poisson_decisively(self):
        a = Z.audit()
        self.assertGreater(abs(a["ratio"] - a["poisson"]) / a["gue"]["sd"], 5.0)


if __name__ == "__main__":
    unittest.main()


class TestTheReferenceIsTheRightEnsemble(unittest.TestCase):
    """#197: the constant this module called RATIO_GUE is the GOE value, and a VERIFIED certificate
    repeated it as fact. These tests are the guard that could have caught it."""

    def test_the_gue_reference_is_measured_not_quoted(self):
        import random
        rng = random.Random(11)
        measured = Z.ratio_statistic(Z.wigner_sample(20000, rng))
        self.assertLess(abs(measured - Z.RATIO_GUE_SURMISE), 0.01,
                        f"GUE-surmise sampler gives {measured:.4f}, constant says {Z.RATIO_GUE_SURMISE}")

    def test_the_goe_value_is_not_the_gue_value(self):
        # the whole defect: 0.5307 is a real-symmetric asymptotic value, and it is FAR from GUE's
        self.assertGreater(abs(Z.RATIO_GOE - Z.RATIO_GUE_SURMISE), 0.05)

    def test_the_zeros_sit_near_gue_and_far_from_goe(self):
        a = Z.audit()
        self.assertLess(abs(a["ratio"] - Z.RATIO_GUE_SURMISE), 0.05)
        self.assertGreater(abs(a["ratio"] - Z.RATIO_GOE), 0.05)

    def test_the_deprecated_alias_still_points_at_the_goe_number(self):
        # a constant that silently changes value is worse than one with a wrong name
        self.assertEqual(Z.RATIO_GUE, Z.RATIO_GOE)
