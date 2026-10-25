"""The constraint set — plural by design, and its independence measured."""
import unittest

from pacland.economics import constraint_set as C


class TestInventory(unittest.TestCase):
    def test_eleven_constraints(self):
        self.assertEqual(len(C.CONSTRAINTS), 11)

    def test_every_constraint_is_sourced_and_typed(self):
        self.assertTrue(C.guard_every_constraint_sourced()[0])
        self.assertTrue(C.guard_kinds_are_known()[0])

    def test_kinds_are_counted(self):
        kinds = C.guard_kinds_are_known()[1]
        self.assertIn("identity", kinds)
        self.assertIn("model", kinds)
        self.assertIn("domain", kinds)

    def test_an_unsourced_constraint_is_refused(self):
        bad = C.Constraint(key="probe", kind="model", statement="", source="", residual=lambda s: 0.0)
        saved = C.CONSTRAINTS
        try:
            C.CONSTRAINTS = saved + (bad,)
            ok, msg = C.guard_every_constraint_sourced()
        finally:
            C.CONSTRAINTS = saved
        self.assertFalse(ok)
        self.assertIn("UNSOURCED", msg)


class TestReferenceState(unittest.TestCase):
    def test_the_reference_state_satisfies_everything(self):
        ok, msg = C.guard_default_state_is_admissible()
        self.assertTrue(ok, msg)

    def test_all_eleven_rows_pass(self):
        rows = C.evaluate()
        self.assertEqual(len(rows), 11)
        self.assertEqual([r["key"] for r in rows if not r["ok"]], [])


class TestViolationsAreCaught(unittest.TestCase):
    def test_circular_flow(self):
        s = C._default_state()
        s["income"] += 1.0
        self.assertIn("circular_flow", C.violated(s))

    def test_sectoral_balances(self):
        s = C._default_state()
        s["foreign_balance"] = -4.0
        self.assertIn("sectoral_balances", C.violated(s))

    def test_stock_flow(self):
        s = C._default_state()
        s["flow"] = 2.0
        self.assertIn("stock_flow", C.violated(s))

    def test_passive_rule(self):
        s = C._default_state()
        s["phi_pi"] = 0.5
        self.assertIn("taylor_principle", C.violated(s))

    def test_non_zero_target_leaves_the_domain(self):
        s = C._default_state()
        s["pi_star"] = 0.02
        self.assertIn("zero_inflation_domain", C.violated(s))

    def test_resource_shares(self):
        s = C._default_state()
        s["c_over_y"] = 0.80
        self.assertIn("resource_shares", C.violated(s))

    def test_budget_inequality(self):
        s = C._default_state()
        s["spend"] = 500.0
        self.assertIn("budget", C.violated(s))


class TestIndependence(unittest.TestCase):
    def test_rank_of_the_equalities(self):
        ind = C.independence()
        self.assertEqual(ind["n_equality"], 8)
        self.assertEqual(ind["rank"], 8)
        self.assertEqual(ind["dependent"], 0)

    def test_the_detector_notices_a_duplicate(self):
        # a constraint that is another constraint times two is ONE constraint
        dup = C.Constraint(
            "fisher_doubled", "model", "2*(i - r* - pi) = 0",
            "tests/test_economics_constraint_set.py",
            residual=lambda s: 2.0 * (s["i"] - (s["r_star"] + s["pi"])),
        )
        saved = C.CONSTRAINTS
        try:
            C.CONSTRAINTS = saved + (dup,)
            ind = C.independence()
        finally:
            C.CONSTRAINTS = saved
        self.assertEqual(ind["n_equality"], 9)
        self.assertEqual(ind["rank"], 8)
        self.assertEqual(ind["dependent"], 1)

    def test_slack_is_ordered_by_bindingness(self):
        order = [k for k, _ in C.slack()]
        self.assertEqual(len(order), 11)
        # the inequalities with real slack must sort last; the equalities that hold at
        # the reference state all have slack 0
        self.assertEqual(order[-1], "nonneg_price")
        self.assertIn(order[0], {"circular_flow", "sectoral_balances", "stock_flow",
                                 "fisher", "lrpc", "resource_shares", "capital_output",
                                 "zero_inflation_domain"})


if __name__ == "__main__":
    unittest.main()
