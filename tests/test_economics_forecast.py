"""Economics forecast-failure tests — the empirical axis (axis 1)."""
import unittest

from pacland.economics.forecast import forecast_failure, guard_forecast_is_extrapolation, rmse

ACTUALS = [10.0, 10.2, 9.8, 10.5, 10.3, 10.8]
NO_SKILL = [10.5, 10.7, 10.3, 11.0, 10.8]   # no-change + constant bias (worse)
ORACLE = ACTUALS[1:]                          # perfect one-step-ahead


class TestEconomicsForecast(unittest.TestCase):
    def test_rmse_of_zero_is_zero(self):
        self.assertEqual(rmse([0.0, 0.0, 0.0]), 0.0)

    def test_no_skill_does_not_beat_naive(self):
        r = forecast_failure(NO_SKILL, ACTUALS)
        self.assertFalse(r["beat"])
        self.assertGreaterEqual(r["model_rmse"], r["naive_rmse"])

    def test_oracle_beats_naive(self):
        r = forecast_failure(ORACLE, ACTUALS)
        self.assertTrue(r["beat"])
        self.assertEqual(r["model_rmse"], 0.0)

    def test_guard_green_on_no_skill(self):
        ok, _ = guard_forecast_is_extrapolation(NO_SKILL, ACTUALS)
        self.assertTrue(ok)

    def test_guard_red_on_oracle(self):
        ok, msg = guard_forecast_is_extrapolation(ORACLE, ACTUALS)
        self.assertFalse(ok)
        self.assertIn("beats", msg)


if __name__ == "__main__":
    unittest.main()
