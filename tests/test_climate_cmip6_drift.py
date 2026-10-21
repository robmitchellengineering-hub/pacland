"""CMIP6 conservation-drift guard — known-answer tests (Irving et al. 2021 data)."""
import unittest

from pacland.climate.cmip6_drift import drift_wm2, load, summary


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


if __name__ == "__main__":
    unittest.main()
