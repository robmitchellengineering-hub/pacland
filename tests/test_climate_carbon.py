"""The carbon invariant: measured, closed, and refused when the sinks are dropped."""
import unittest

from pacland.climate import carbon
from pacland.climate import structure as S


class TestBudget(unittest.TestCase):
    def test_the_airborne_fraction_is_a_fraction_near_the_observed_one(self):
        r = carbon.budget()
        self.assertTrue(r["in_range"])
        self.assertGreater(r["airborne_fraction"], 0.35)
        self.assertLess(r["airborne_fraction"], 0.60)

    def test_the_sinks_are_positive_and_large(self):
        r = carbon.budget()
        self.assertGreater(r["sinks_gtco2"], 500.0)
        self.assertLess(r["airborne_gtco2"], r["emitted_gtco2"])

    def test_every_single_year_is_physically_possible(self):
        r = carbon.budget()
        self.assertTrue(r["every_year_physical"])
        # and the per-year spread is disclosed rather than hidden
        self.assertGreater(r["fraction_max"] - r["fraction_min"], 0.2)


class TestSeededFault(unittest.TestCase):
    def test_a_budget_with_no_sinks_is_refused(self):
        ok, msg = carbon.guard_budget()
        self.assertTrue(ok, msg)
        self.assertIn("impossible", msg)


class TestStructureFollows(unittest.TestCase):
    def test_carbon_is_now_counted_as_measured(self):
        cov = S.coverage()
        self.assertEqual(cov["n_measured"], 4)
        self.assertIn("carbon", cov["measured"])
        self.assertEqual(cov["unmeasured"], ["water"])


if __name__ == "__main__":
    unittest.main()
