"""Verified reference model — guards the GISS-E2-1-G result against drift.

Known answers: of the 19 models with full drift data, exactly one family (GISS)
passes all three gates; the canonical member GISS-E2-1-G has ECS 2.71 K,
ERF2x 3.95 W/m2, 0 ledgers leaked.
"""
import unittest

from pacland.climate.reference_model import reference_model, summary


class TestReferenceModel(unittest.TestCase):
    def test_model_is_giss_e2_1_g(self):
        self.assertEqual(reference_model()["model"], "GISS-E2-1-G")

    def test_ecs_is_2_71(self):
        self.assertAlmostEqual(reference_model()["ecs_K"], 2.71, places=2)

    def test_passes_all_three_axes(self):
        r = reference_model()
        self.assertEqual(r["axes_passed"], 3)
        self.assertEqual(r["ledgers_failed"], 0)
        self.assertEqual(r["sensitivity"], "reasonable")
        self.assertEqual(r["forcing"], "reasonable")

    def test_ecs_inside_ipcc_range(self):
        from pacland.climate.sensitivity_crosscheck import load
        lo, hi = load()["likely_range_K"]
        self.assertTrue(lo <= reference_model()["ecs_K"] <= hi)

    def test_summary_names_the_number(self):
        self.assertIn("GISS-E2-1-G", summary())
        self.assertIn("2.71 K", summary())


if __name__ == "__main__":
    unittest.main()
