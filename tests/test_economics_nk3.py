"""New Keynesian 3-equation tests — exact content, guards, and the deficit ceiling.

Every guard here has its seeded fault in this file: each guard is asserted green on a
consistent model and red on the specific violation it exists to catch.
"""
import math
import unittest

from pacland.economics import nk3


class TestSteadyState(unittest.TestCase):
    def test_zero_inflation_steady_state(self):
        ss = nk3.steady_state()
        self.assertEqual(ss["pi"], 0.0)
        self.assertEqual(ss["x"], 0.0)
        self.assertAlmostEqual(ss["i"], nk3.R_STAR, places=15)

    def test_real_rate_is_the_natural_rate(self):
        ss = nk3.steady_state()
        self.assertAlmostEqual(ss["r"], nk3.R_STAR, places=15)

    def test_long_run_phillips_slope_is_exact(self):
        self.assertAlmostEqual(nk3.lrpc_slope(0.99, 0.1), 0.1, places=15)
        self.assertAlmostEqual(nk3.lrpc_slope(0.9, 0.2), 0.5, places=15)

    def test_long_run_phillips_is_vertical_only_at_beta_one(self):
        self.assertEqual(nk3.lrpc_slope(1.0, 0.1), 0.0)
        self.assertNotEqual(nk3.lrpc_slope(0.99, 0.1), 0.0)


class TestDeterminacy(unittest.TestCase):
    def test_boundary_at_zero_phi_y_is_the_taylor_principle(self):
        self.assertAlmostEqual(nk3.taylor_boundary(0.0), 1.0, places=15)

    def test_boundary_falls_with_output_response(self):
        self.assertLess(nk3.taylor_boundary(0.5), nk3.taylor_boundary(0.0))

    def test_boundary_is_sigma_free(self):
        a = nk3.determinacy_margin(0.95, 0.5, sigma=1.0)
        b = nk3.determinacy_margin(0.95, 0.5, sigma=5.0)
        self.assertAlmostEqual(a, b, places=12)

    def test_active_rule_is_determinate_passive_is_not(self):
        self.assertTrue(nk3.is_determinate(1.5, 0.5))
        self.assertFalse(nk3.is_determinate(0.5, 0.5))

    def test_boundary_agrees_with_the_exact_formula(self):
        # the numeric search and the closed form must agree: the analytic arm is
        # validated by the numeric one, not asserted.
        for phi_y in (0.0, 0.25, 0.5, 1.0):
            lo, hi = 0.0, 6.0
            for _ in range(120):
                mid = 0.5 * (lo + hi)
                if nk3.determinacy_margin(mid, phi_y) > 0:
                    hi = mid
                else:
                    lo = mid
            self.assertAlmostEqual(hi, nk3.taylor_boundary(phi_y), places=9)

    def test_spectrum_has_both_roots_outside_when_determinate(self):
        l1, l2 = nk3.spectrum(1.5, 0.5)
        self.assertGreater(min(abs(l1), abs(l2)), 1.0)


class TestGuards(unittest.TestCase):
    def test_steady_state_admissible_at_zero(self):
        ok, msg = nk3.guard_steady_state_admissible(0.0, 0.0)
        self.assertTrue(ok, msg)

    def test_steady_state_refused_at_a_non_zero_target(self):
        # the seeded fault: a 2% target used with the zero-inflation linearisation
        ok, msg = nk3.guard_steady_state_admissible(math.pi * 0 + 0.02, 0.0)
        self.assertFalse(ok)
        self.assertIn("OUT OF DOMAIN", msg)

    def test_steady_state_admissible_at_two_percent_when_beta_is_one(self):
        ok, msg = nk3.guard_steady_state_admissible(0.02, 0.0, beta=1.0)
        self.assertTrue(ok, msg)

    def test_fisher_green_and_red(self):
        ss = nk3.steady_state()
        self.assertTrue(nk3.guard_fisher(ss["i"], ss["pi"])[0])
        ok, msg = nk3.guard_fisher(ss["i"] + 0.0001, ss["pi"])
        self.assertFalse(ok)
        self.assertIn("fisher residual", msg)

    def test_superneutrality_green_and_red(self):
        self.assertTrue(nk3.guard_superneutrality(0.02, 0.0, 0.025, 0.005)[0])
        # money illusion: a nominal shift that moves the real rate
        ok, msg = nk3.guard_superneutrality(0.02, 0.0, 0.030, 0.005)
        self.assertFalse(ok)
        self.assertIn("superneutrality", msg)

    def test_taylor_principle_green_on_active_rule(self):
        ok, msg = nk3.guard_taylor_principle(1.5, 0.5)
        self.assertTrue(ok, msg)

    def test_taylor_principle_red_on_passive_rule(self):
        ok, msg = nk3.guard_taylor_principle(0.9, 0.5)
        self.assertFalse(ok)
        self.assertIn("INDETERMINATE", msg)

    def test_taylor_principle_uses_the_output_gap_offset(self):
        # 0.97 is passive at phi_y=0 but active at phi_y=0.5 (boundary 0.95)
        self.assertFalse(nk3.guard_taylor_principle(0.97, 0.0)[0])
        self.assertTrue(nk3.guard_taylor_principle(0.97, 0.5)[0])

    def test_long_run_phillips_refuses_a_vertical_claim_below_beta_one(self):
        ok, msg = nk3.guard_long_run_phillips(0.99, 0.1, claimed_vertical=True)
        self.assertFalse(ok)
        self.assertIn("claimed vertical", msg)

    def test_long_run_phillips_accepts_a_vertical_claim_at_beta_one(self):
        self.assertTrue(nk3.guard_long_run_phillips(1.0, 0.1, claimed_vertical=True)[0])


class TestDeficit(unittest.TestCase):
    def test_ceiling_is_three_observables(self):
        ceiling, _ = nk3.deficit()
        self.assertEqual(ceiling.n_observables, 3)
        self.assertEqual(ceiling.n_validation, 3)

    def test_ceiling_radius_is_about_78_percent(self):
        ceiling, _ = nk3.deficit(0.025)
        self.assertAlmostEqual(ceiling.radius, 0.784, places=3)

    def test_the_ceiling_cannot_reach_one_percent(self):
        ceiling, _ = nk3.deficit(0.01)
        self.assertGreater(ceiling.radius, 0.5)

    def test_nothing_is_validated_today(self):
        _, today = nk3.deficit()
        self.assertEqual(today.n_validation, 0)
        self.assertTrue(today.vacuous)

    def test_summary_states_the_domain_limit(self):
        self.assertIn("no steady state at a non-zero target", nk3.summary())


if __name__ == "__main__":
    unittest.main()
