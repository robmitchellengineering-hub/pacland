"""Economics constraint-first — the exact, provable half (deep analog of the SM frontier)."""
import unittest
from fractions import Fraction as F

from pacland.economics.constraint_first import (
    cobb_douglas_exchange,
    conservation_laws,
    net_balances,
    realize,
    total_balance,
    walras_law,
)


class TestEconomicsConstraintFirst(unittest.TestCase):
    def test_double_entry_conserves(self):
        flows = [[0, 1, 2], [3, 0, 4], [5, 6, 0]]
        self.assertEqual(total_balance(net_balances(flows)), F(0))

    def test_any_balance_summing_to_zero_is_realizable(self):
        balances = [F(2), F(-5), F(3)]
        flows = realize(balances)
        self.assertEqual(net_balances(flows), balances)
        self.assertEqual(total_balance(net_balances(flows)), F(0))

    def test_conservation_law_is_unique(self):
        rank, basis = conservation_laws(4)
        self.assertEqual(rank, 3)
        self.assertEqual(basis, [[F(1), F(1), F(1), F(1)]])

    def test_walras_law_holds_identically(self):
        for r in (F(1, 2), F(2, 1), F(7, 3)):
            z, _ = cobb_douglas_exchange(r)
            # p·z with p = (1, r) is z1 + r·z2 = walras residual
            self.assertEqual(walras_law(z, [F(1), r]), F(0))

    def test_equilibrium_fixes_ratio_not_level(self):
        z_eq, _ = cobb_douglas_exchange(1)
        self.assertEqual(z_eq, [F(0), F(0)])
        z_off, _ = cobb_douglas_exchange(2)
        self.assertNotEqual(z_off[0], F(0))


if __name__ == "__main__":
    unittest.main()
