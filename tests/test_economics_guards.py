"""Mutation tests for the economics guard-suite (playbook item #3).

Each test proves a guard passes on a valid case AND goes red on the seeded fault
it exists to catch (KNOWN-HAZARDS H17: a check that never runs reads as a pass).
"""
import unittest

from pacland.economics.guards import (
    guard_budget_constraint,
    guard_circular_flow,
    guard_nonnegative_price,
    guard_sectoral_balances,
    guard_stock_flow,
)


class TestEconomicsGuards(unittest.TestCase):
    def test_circular_flow_passes_when_three_measures_agree(self):
        ok, _ = guard_circular_flow(income=1000.0, expenditure=1000.0, output=1000.0)
        self.assertTrue(ok)

    def test_circular_flow_fires_on_flow_leak(self):
        ok, msg = guard_circular_flow(income=1000.0, expenditure=1000.0, output=980.0)
        self.assertFalse(ok)
        self.assertIn("circular-flow", msg)

    def test_sectoral_balances_pass_when_zero(self):
        ok, _ = guard_sectoral_balances(2.0, -3.0, 1.0)
        self.assertTrue(ok)

    def test_sectoral_balances_fire_on_imbalance(self):
        ok, msg = guard_sectoral_balances(2.0, -3.0, 2.0)
        self.assertFalse(ok)
        self.assertIn("sectoral-balance", msg)

    def test_stock_flow_passes_when_consistent(self):
        ok, _ = guard_stock_flow(d_stock=50.0, flow=50.0)
        self.assertTrue(ok)

    def test_stock_flow_fires_on_missing_flow(self):
        ok, msg = guard_stock_flow(d_stock=50.0, flow=30.0)
        self.assertFalse(ok)
        self.assertIn("stock-flow", msg)

    def test_budget_passes_within_income_plus_borrowing(self):
        ok, _ = guard_budget_constraint(expenditure=1200.0, income=1000.0, net_borrowing=200.0)
        self.assertTrue(ok)

    def test_budget_fires_on_overspend(self):
        ok, msg = guard_budget_constraint(expenditure=1500.0, income=1000.0, net_borrowing=200.0)
        self.assertFalse(ok)
        self.assertIn("budget excess", msg)

    def test_nonnegative_price_passes_clean(self):
        ok, _ = guard_nonnegative_price([1.0, 2.5, 0.0])
        self.assertTrue(ok)

    def test_nonnegative_price_fires_on_negative(self):
        ok, msg = guard_nonnegative_price([1.0, -0.5, 2.5])
        self.assertFalse(ok)
        self.assertIn("negative price/quantity", msg)


if __name__ == "__main__":
    unittest.main()
