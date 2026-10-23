"""Conservation repair — guards the drift-correction result against drift.

Known answers (data/climate/cmip6_drift.json, Irving et al. 2021):
- 19 models, 12 leak energy (net TOA beyond 0.1 W/m2).
- The leak is localized to the atmosphere-ocean coupling (salt conserved).
- Drift-correction makes every model conserve by construction.
- Post-fix: the strict gate reduces to sensitivity+forcing -> 15 models, ~3.08 K.
"""
import unittest

from pacland.climate.drift_correction import (
    leak,
    post_fix_prediction,
    repair,
    repair_report,
)


class TestRepairReport(unittest.TestCase):
    def test_19_models(self):
        self.assertEqual(repair_report()["n_models"], 19)

    def test_12_leak_energy(self):
        n_energy = sum(1 for m in repair_report()["models"] if m["energy_leaks"])
        self.assertEqual(n_energy, 12)

    def test_leak_localized_to_coupling(self):
        # more models leak at the coupling (energy/mass) than at the ocean (salt)
        rp = repair_report()
        self.assertGreater(rp["n_coupling_leak"], rp["n_models"] - rp["n_coupling_leak"])

    def test_all_correctable(self):
        self.assertTrue(repair_report()["all_correctable"])


class TestRepair(unittest.TestCase):
    def test_repair_conserves_by_construction(self):
        self.assertTrue(repair("CNRM-ESM2-1")["conserves_after_fix"])

    def test_repair_is_the_negated_leak(self):
        lk = leak("CNRM-ESM2-1")
        rp = repair("CNRM-ESM2-1")
        self.assertAlmostEqual(rp["correct_energy_by_Wm2"], -lk["energy_Wm2"], places=4)

    def test_repair_names_what_it_does_not_fix(self):
        self.assertIn("spatial", repair("CNRM-ESM2-1")["what_it_does_not_fix"])


class TestPostFixPrediction(unittest.TestCase):
    def test_post_fix_ecs_is_sens_forc(self):
        p = post_fix_prediction()
        self.assertAlmostEqual(p["after_fix_ECS_K"], 3.08, places=2)
        self.assertEqual(p["after_fix_models"], 15)

    def test_before_fix_is_giss(self):
        self.assertAlmostEqual(post_fix_prediction()["before_fix_strict_ECS_K"], 2.71, places=2)


if __name__ == "__main__":
    unittest.main()
