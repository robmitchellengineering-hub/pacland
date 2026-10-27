"""Water: the fifth conservation invariant, closed with free data."""
import unittest

from pacland.climate import structure as S
from pacland.climate import water


class TestClosure(unittest.TestCase):
    def test_precipitation_and_evaporation_balance(self):
        r = water.balance()
        self.assertTrue(r["closes"], r["verdict"])
        self.assertLess(r["worst_imbalance"], water.TOLERANCE)

    def test_the_means_are_physically_plausible(self):
        r = water.balance()
        self.assertGreater(r["mean_precip_mm_day"], 2.0)
        self.assertLess(r["mean_precip_mm_day"], 4.0)
        self.assertGreater(r["mean_evap_mm_day"], 2.0)
        self.assertLess(r["mean_evap_mm_day"], 4.0)

    def test_every_sample_closes(self):
        r = water.balance()
        for month, ratio in r["ratios"].items():
            self.assertLess(abs(ratio - 1.0), water.TOLERANCE, month)


class TestSeededFaults(unittest.TestCase):
    def test_weighting_fault(self):
        ok, msg = water.guard_weighting()
        self.assertTrue(ok, msg)

    def test_units_fault(self):
        ok, msg = water.guard_units()
        self.assertTrue(ok, msg)

    def test_the_audit_is_green(self):
        self.assertTrue(water.audit()["all_pass"])


class TestStructureIsNowComplete(unittest.TestCase):
    def test_all_five_conservation_laws_are_measured(self):
        cov = S.coverage()
        self.assertEqual(cov["n_measured"], 5)
        self.assertEqual(cov["unmeasured"], [])
        self.assertTrue(cov["complete"])


if __name__ == "__main__":
    unittest.main()
