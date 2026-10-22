"""Economics set-identification tests — the theoretical axis (axis 2)."""
import unittest
from fractions import Fraction as F

from pacland.economics.identification import (
    aggregate_from_distribution,
    cobb_douglas_aggregate_excess_demand,
    constraint_set_model,
    guard_point_identified,
    sectoral_balance_set,
)


class TestEconomicsIdentification(unittest.TestCase):
    def test_two_distributions_give_same_aggregate(self):
        d1 = [(F(1), F(0)), (F(0), F(1))]
        d2 = [(F(1, 2), F(1, 2)), (F(1, 2), F(1, 2))]
        self.assertEqual(aggregate_from_distribution(d1, F(2)),
                         aggregate_from_distribution(d2, F(2)))

    def test_total_is_identified(self):
        z1 = cobb_douglas_aggregate_excess_demand((F(1), F(1)), F(2))
        z2 = cobb_douglas_aggregate_excess_demand((F(2), F(1)), F(2))
        self.assertNotEqual(z1, z2)

    def test_guard_fails_point_claim_when_set_identified(self):
        ok, msg = guard_point_identified({"dist": "D1"}, [{"dist": "D2"}])
        self.assertFalse(ok)
        self.assertIn("set-identified", msg)

    def test_guard_passes_point_claim_when_identified(self):
        ok, _ = guard_point_identified({"total": (F(1), F(1))}, [])
        self.assertTrue(ok)

    def test_sectoral_balance_identified_split_not(self):
        private, msg = sectoral_balance_set(F("-1774.684"), F("-246.023"))
        self.assertEqual(private, F("2020.707"))
        self.assertIn("set-identified", msg)

    def test_constraint_set_model_refuses_point_forecasts(self):
        model = constraint_set_model(F("-1774.684"), F("-246.023"))
        self.assertEqual(model["identified"]["private_balance"], F("2020.707"))
        self.assertIn("no point forecast", model["refused"])


if __name__ == "__main__":
    unittest.main()
