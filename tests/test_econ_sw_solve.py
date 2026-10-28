"""Smets–Wouters solved from the authors' file: extraction, solution, stability, economics."""
import unittest

from pacland.economics import sw_solve as S

SOLVED = None


def solved():
    global SOLVED
    if SOLVED is None:
        SOLVED = S.solve_model()
    return SOLVED


class TestExtraction(unittest.TestCase):
    def test_the_system_is_square(self):
        m = S.matrices()
        self.assertTrue(m["square"], (m["n_equations"], m["n_endogenous"]))
        self.assertEqual(m["n_equations"], 34)

    def test_every_equation_vanishes_at_the_steady_state(self):
        self.assertLess(S.matrices()["worst_steady_state_residual"], 1e-9)

    def test_the_innovations_are_the_seven_declared_ones(self):
        m = S.matrices()
        self.assertEqual(sorted(m["innovations"]), sorted(S.INNOVATIONS))


class TestSolution(unittest.TestCase):
    def test_the_policy_solves_the_system(self):
        s = solved()
        self.assertLess(s["residual_P"], 1e-9)
        self.assertLess(s["residual_Q"], 1e-9)

    def test_the_policy_is_stable(self):
        self.assertTrue(solved()["stable"])

    def test_more_than_one_shock_has_a_nonzero_response(self):
        s = solved()
        nonzero = sum(1 for j in range(len(s["innovations"]))
                      if any(abs(s["Q"][i][j]) > 1e-12 for i in range(len(s["endo"]))))
        self.assertGreaterEqual(nonzero, 5)


class TestEconomics(unittest.TestCase):
    def test_a_contractionary_monetary_shock_lowers_output_and_inflation(self):
        ok, msg = S.guard_monetary_shock_sign(solved())
        self.assertTrue(ok, msg)

    def test_a_cost_push_shock_raises_inflation(self):
        path = S.irf(solved(), "epinf", horizon=8)
        self.assertGreater(path["pinf"][0], 0.0)


class TestAudit(unittest.TestCase):
    def test_all_four_checks_are_green(self):
        self.assertTrue(S.audit()["all_pass"])


if __name__ == "__main__":
    unittest.main()
