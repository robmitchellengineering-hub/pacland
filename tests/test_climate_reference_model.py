"""Verified reference model — guards the GISS-E2-1-G result against drift.

Known answers: of the 19 models with full drift data, exactly one family (GISS)
passes all three gates; the canonical member GISS-E2-1-G has ECS 2.71 K,
ERF2x 3.95 W/m2, 0 ledgers leaked.
"""
import unittest

from pacland.climate.reference_model import projections, reference_model, summary


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


class TestProjections(unittest.TestCase):
    def test_ssp585_warming_is_4_6_to_5_2(self):
        w = projections()["warming_2100_C"]["SSP5-8.5"]
        self.assertAlmostEqual(w["lo"], 4.6, places=1)
        self.assertAlmostEqual(w["hi"], 5.2, places=1)

    def test_ssp126_warming_below_2(self):
        w = projections()["warming_2100_C"]["SSP1-2.6"]
        self.assertEqual(w["hi"], 2.0)

    def test_source_is_nazarenko_2022(self):
        p = projections()
        self.assertEqual(p["doi"], "10.1029/2021MS002871")
        self.assertIn("Nazarenko", p["source"])

    def test_ecs_method_dependence_recorded(self):
        # the model's own reported ECS (2.9-3.0) vs our Zelinka gate (2.71 K)
        p = projections()
        self.assertEqual(p["ecs_model_own_C"], (2.9, 3.0))
        self.assertAlmostEqual(p["ecs_zelinka_C"], 2.71, places=2)

    def test_sea_level_thermosteric_recorded(self):
        # thermosteric only, SSP2-4.5 — with the caveat stated, not hidden
        p = projections()
        sl = p["sea_level_2100_thermosteric_m"]["SSP2-4.5"]
        self.assertAlmostEqual(sl["lo"], 0.21, places=2)
        self.assertAlmostEqual(sl["hi"], 0.24, places=2)
        self.assertIn("thermosteric", p["sea_level_2100_thermosteric_m"]["note"])


if __name__ == "__main__":
    unittest.main()
