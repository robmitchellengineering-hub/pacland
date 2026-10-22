"""Economics accounting closure on real FRED data — the measured three-ledger result."""
import unittest

from pacland.economics.guards import (
    guard_circular_flow,
    guard_sectoral_balances,
    guard_stock_flow,
)


class TestEconomicsAccountingClosure(unittest.TestCase):
    # FRED values, billions of dollars (2026-10-22).
    GDP = 32563.030
    GDI = 32752.528
    DEFICIT = -1774.684
    DEBT_2024 = 28859.125
    DEBT_2025 = 30870.713
    CURRENT_ACCOUNT = -246.023

    def test_circular_flow_leaks_by_statistical_discrepancy(self):
        ok, _ = guard_circular_flow(self.GDI, self.GDP, self.GDP, tol=0.0)
        self.assertFalse(ok)  # 0.58% gap — measured, not zero
        resid = self.GDI - self.GDP
        self.assertAlmostEqual(resid / self.GDP, 0.0058, places=3)

    def test_sectoral_balances_closes_by_construction(self):
        private = -(self.DEFICIT) - self.CURRENT_ACCOUNT
        ok, _ = guard_sectoral_balances(private, self.DEFICIT, self.CURRENT_ACCOUNT, tol=1e-6)
        self.assertTrue(ok)  # double-entry identity — exact

    def test_stock_flow_leaks_by_stock_flow_adjustment(self):
        d_debt = self.DEBT_2025 - self.DEBT_2024
        flow = -self.DEFICIT
        ok, _ = guard_stock_flow(d_debt, flow, tol=0.0)
        self.assertFalse(ok)  # $236.9B residual — measured, not zero
        self.assertAlmostEqual((d_debt - flow) / flow, 0.133, places=2)


if __name__ == "__main__":
    unittest.main()
