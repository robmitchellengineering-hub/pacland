"""The RE solver: verified against closed forms and against nk3's analytic policy."""
import unittest

from pacland.economics import resolve as R


class TestClosedForm(unittest.TestCase):
    def test_a_hand_solved_forward_model(self):
        r = R.univariate_forward_check()
        self.assertTrue(r["pass"], r)
        self.assertLess(r["residuals"][0], 1e-9)

    def test_the_policy_satisfies_the_structural_equations(self):
        A, B, C, D = R.nk3_matrices()
        sol = R.solve(A, B, C, D, 0.8)
        self.assertLess(sol["residual_P"], 1e-9)
        self.assertLess(sol["residual_Q"], 1e-9)


class TestNk3CrossCheck(unittest.TestCase):
    def test_two_routes_agree_on_the_policy(self):
        r = R.nk3_cross_check()
        self.assertTrue(r["pass"], r)
        self.assertLess(r["error"], 1e-9)

    def test_they_agree_for_a_different_calibration_too(self):
        r = R.nk3_cross_check(phi_pi=2.0, phi_y=0.2)
        self.assertTrue(r["pass"], r)


class TestDeterminacy(unittest.TestCase):
    def test_a_passive_rule_is_refused(self):
        r = R.determinacy_refusal()
        self.assertTrue(r["refused"], r)

    def test_the_wrapper_refuses_before_the_numerics(self):
        with self.assertRaises(ValueError):
            R.solve_nk3(phi_pi=0.8)


class TestAudit(unittest.TestCase):
    def test_all_three_verifications_are_green(self):
        self.assertTrue(R.audit()["all_pass"])


if __name__ == "__main__":
    unittest.main()
