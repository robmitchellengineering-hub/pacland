"""Climate Constraint-First — guards the theorem against drift.

Known answers: 14/19 models leak (conservation is the exact constraint), the
53-model ECS range is 1.83-5.64 K (not exact), and the 2100 projection has
m = 0 (extrapolation).
"""
import unittest

from pacland.climate.deficit import climate_deficit_report
from pacland.climate.drift_correction import repair_report
from pacland.climate.ecs_model import ecs_estimates


class TestConservationIsExact(unittest.TestCase):
    def test_14_leak(self):
        self.assertEqual(repair_report()["n_leaking"], 14)

    def test_ledgers_are_three(self):
        self.assertEqual(len(repair_report()["models"]), 19)


class TestPredictionsAreNotExact(unittest.TestCase):
    def test_ecs_is_a_range(self):
        w = ecs_estimates()["widened_naive"]
        self.assertGreater(w["max_K"] - w["min_K"], 3.0)   # 1.83..5.64 -> spread > 3 K
        self.assertEqual(w["n"], 53)

    def test_projection_is_m_zero(self):
        _, proj = climate_deficit_report()
        self.assertEqual(proj.n_validation, 0)


if __name__ == "__main__":
    unittest.main()
