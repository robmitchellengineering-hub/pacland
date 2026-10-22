"""CMIP6 conservation-drift guard — known-answer tests (Irving et al. 2021 data)."""
import unittest

from pacland.climate.cmip6_drift import (
    drift_wm2,
    load,
    mass_drift_mm_per_yr,
    summary,
    trust_ranking,
    verdict_table,
)


class TestCmip6Drift(unittest.TestCase):
    def test_19_models(self):
        self.assertEqual(len(load()["models"]), 19)

    def test_unit_conversion(self):
        # ACCESS-CM2: 5.92e21 J/yr -> ~0.368 W/m2
        self.assertAlmostEqual(drift_wm2(5.92e21), 0.368, places=2)

    def test_twelve_models_fail_conservation_at_0p1(self):
        self.assertEqual(summary(tol_wm2=0.1)["n_failing_conservation"], 12)

    def test_two_models_leak_faster_than_eei(self):
        self.assertEqual(summary(tol_wm2=0.1)["n_exceeding_eei"], 2)

    def test_worst_leaker_is_cnrm_esm2(self):
        s = summary(tol_wm2=0.1)
        self.assertEqual(s["worst_model"], "CNRM-ESM2-1")
        self.assertAlmostEqual(s["worst_drift_wm2"], 1.485, places=2)
        self.assertAlmostEqual(s["worst_ratio_to_eei"], 1.93, places=2)

    def test_leak_lives_in_the_atmosphere(self):
        # median total TOA drift >> median ocean drift (0.241 vs 0.051 W/m2)
        s = summary(tol_wm2=0.1)
        self.assertAlmostEqual(s["median_abs_nettoa_wm2"], 0.241, places=2)
        self.assertAlmostEqual(s["median_abs_ocean_wm2"], 0.051, places=2)
        self.assertGreater(s["median_abs_nettoa_wm2"], 3 * s["median_abs_ocean_wm2"])

    def test_cnrm_ocean_is_clean_but_atmosphere_leaks(self):
        # CNRM-ESM2-1: total leak 1.485, ocean drift 0.086 -> non-ocean ~1.4
        row = next(r for r in verdict_table() if r["model"] == "CNRM-ESM2-1")
        self.assertLess(abs(row["ocean_drift_wm2"]), 0.1)
        self.assertAlmostEqual(row["non_ocean_leak_wm2"], 1.399, places=2)

    def test_trust_ranking_tiers(self):
        t = trust_ranking(tol_wm2=0.1)
        self.assertEqual(t["broken"], ["CNRM-ESM2-1", "CNRM-CM6-1"])
        self.assertEqual(len(t["clean"]), 7)
        self.assertEqual(len(t["leaking"]), 10)

    def test_mass_unit_conversion(self):
        # 3.6e14 kg/yr = 1 mm/yr sea-level equivalent
        self.assertAlmostEqual(mass_drift_mm_per_yr(3.6e14), 1.0, places=6)

    def test_six_models_leak_mass(self):
        self.assertEqual(summary(tol_mm_per_yr=0.3)["n_failing_mass"], 6)

    def test_worst_mass_leaker_is_access_esm1_5(self):
        s = summary(tol_mm_per_yr=0.3)
        self.assertEqual(s["worst_mass_model"], "ACCESS-ESM1-5")
        self.assertAlmostEqual(s["worst_mass_mm_per_yr"], -1.032, places=2)
        self.assertAlmostEqual(s["worst_mass_ratio_to_slr"], 0.30, places=2)


if __name__ == "__main__":
    unittest.main()
