"""CMIP6 conservation drift — three-ledger known-answer tests (Irving et al. 2021 data)."""
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

    def test_mass_unit_conversion(self):
        # 3.6e14 kg/yr = 1 mm/yr sea-level equivalent
        self.assertAlmostEqual(mass_drift_mm_per_yr(3.6e14), 1.0, places=6)

    # --- the three ledgers ---
    def test_twelve_fail_energy(self):
        self.assertEqual(summary()["n_failing_energy"], 12)

    def test_six_fail_mass(self):
        self.assertEqual(summary()["n_failing_mass"], 6)

    def test_two_fail_salt(self):
        self.assertEqual(summary()["n_failing_salt"], 2)

    def test_five_conserve_all_three(self):
        self.assertEqual(summary()["n_conserving_all"], 5)

    def test_two_exceed_eei(self):
        self.assertEqual(summary()["n_exceeding_eei"], 2)

    # --- the headline numbers ---
    def test_worst_energy_leaker_is_cnrm_esm2(self):
        s = summary()
        self.assertEqual(s["worst_energy_model"], "CNRM-ESM2-1")
        self.assertAlmostEqual(s["worst_drift_wm2"], 1.485, places=2)
        self.assertAlmostEqual(s["worst_ratio_to_eei"], 1.93, places=2)

    def test_worst_overall_is_bcc_esm1(self):
        s = summary()
        self.assertEqual(s["worst_overall_model"], "BCC-ESM1")
        self.assertEqual(s["worst_overall_ledgers_failed"], 3)

    def test_worst_mass_leaker_is_access_esm1_5(self):
        s = summary()
        self.assertEqual(s["worst_mass_model"], "ACCESS-ESM1-5")
        self.assertAlmostEqual(s["worst_mass_mm_per_yr"], -1.032, places=2)

    def test_worst_salt_leaker_is_bcc_esm1(self):
        s = summary()
        self.assertEqual(s["worst_salt_model"], "BCC-ESM1")
        self.assertAlmostEqual(s["worst_salt_g_per_kg_per_yr"], -4.12e-5, places=7)

    # --- the coupling conclusion ---
    def test_leak_lives_in_the_atmosphere(self):
        s = summary()
        self.assertAlmostEqual(s["median_abs_nettoa_wm2"], 0.241, places=2)
        self.assertAlmostEqual(s["median_abs_ocean_wm2"], 0.051, places=2)
        self.assertGreater(s["median_abs_nettoa_wm2"], 3 * s["median_abs_ocean_wm2"])

    def test_cnrm_ocean_is_clean_but_atmosphere_leaks(self):
        row = next(r for r in verdict_table() if r["model"] == "CNRM-ESM2-1")
        self.assertLess(abs(row["ocean_drift_wm2"]), 0.1)
        self.assertAlmostEqual(row["non_ocean_leak_wm2"], 1.399, places=2)

    # --- trust ranking tiers (by ledgers failed) ---
    def test_trust_ranking_tiers(self):
        t = trust_ranking()
        self.assertEqual(len(t["broken"]), 5)
        self.assertEqual(len(t["leaking"]), 9)
        self.assertEqual(len(t["clean"]), 5)
        self.assertIn("BCC-ESM1", t["broken"])  # fails all three ledgers


if __name__ == "__main__":
    unittest.main()
