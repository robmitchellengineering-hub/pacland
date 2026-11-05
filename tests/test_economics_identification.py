"""Economics set-identification tests — the theoretical axis (axis 2)."""
import unittest
from fractions import Fraction as F

from pacland.economics.identification import (
    aggregate_from_distribution,
    cobb_douglas_aggregate_excess_demand,
    constraint_set_model,
    guard_point_identified,
    prior_weighted_set,
    sectoral_balance_prior_weighted,
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


class TestPriorWeightedSet(unittest.TestCase):
    """Build 7 — the prior-weighted posterior over the identified set (Mode P)."""

    def test_posterior_sums_to_one(self):
        r = prior_weighted_set(["a", "b", "c"], [1, 1, 2])
        self.assertAlmostEqual(sum(r["posterior"]), 1.0)

    def test_posterior_is_the_normalised_prior(self):
        r = prior_weighted_set(["a", "b", "c"], [1, 1, 2])
        self.assertEqual(r["posterior"], [0.25, 0.25, 0.5])

    def test_flag_names_the_prior_and_the_mode(self):
        r = prior_weighted_set(["a", "b"], [3, 1])
        self.assertEqual(r["mode"], "pluralism")
        self.assertIn("PRIOR", r["flag"])
        self.assertIn("no point emitted", r["refused"])

    def test_empty_set_refuses(self):
        with self.assertRaises(ValueError):
            prior_weighted_set([], [])

    def test_length_mismatch_refuses(self):
        with self.assertRaises(ValueError):
            prior_weighted_set(["a", "b"], [1])

    def test_zero_total_refuses(self):
        with self.assertRaises(ValueError):
            prior_weighted_set(["a", "b"], [0, 0])

    def test_sectoral_balance_prior_weighted_keeps_the_identified_line(self):
        r = sectoral_balance_prior_weighted(
            F("-1774.684"), F("-246.023"),
            saving_candidates=[F("1000"), F("2000")],
            saving_prior=[1, 3],
        )
        # S − I must equal the identified private balance for every candidate
        private = F("2020.707")
        for (s, i) in r["set"]:
            self.assertEqual(s - i, private)
        self.assertEqual(r["posterior"], [0.25, 0.75])


if __name__ == "__main__":
    unittest.main()
