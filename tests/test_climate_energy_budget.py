"""The first real-data guard run — Earth's energy budget closure."""
import unittest

from pacland.climate.energy_budget import closure


class TestEnergyBudget(unittest.TestCase):
    def test_single_reservoir_undercloses(self):
        r = closure()
        self.assertFalse(r["guard_0_2000m_only"]["pass"])
        self.assertGreater(r["residual_0_2000m_only_wm2"], 0.05)

    def test_full_budget_closes(self):
        r = closure()
        self.assertTrue(r["guard_full"]["pass"])
        self.assertLess(abs(r["residual_full_wm2"]), 0.05)

    def test_verdict_is_the_reservoir_lesson(self):
        self.assertEqual(closure()["verdict"], "budget closes only with all reservoirs")


if __name__ == "__main__":
    unittest.main()
