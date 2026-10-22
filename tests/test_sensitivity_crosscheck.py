"""Three-axis trust cross-check: conservation × sensitivity × forcing."""
import unittest

from pacland.climate.sensitivity_crosscheck import crosscheck, summary, forcing_tier


class TestSensitivityCrosscheck(unittest.TestCase):
    def test_two_models_survive_all_three_axes(self):
        s = summary()
        self.assertEqual(s["n_survives_all"], 2)
        self.assertEqual(sorted(s["survives_all_axes"]), ["GISS-E2-1-G", "GISS-E2-1-G-CC"])

    def test_e3sm_is_clean_but_hot(self):
        row = next(r for r in crosscheck() if r["model"] == "E3SM-1-1")
        self.assertEqual(row["ledgers_failed"], 0)
        self.assertEqual(row["sensitivity"], "hot")
        self.assertEqual(row["n_axes_failed"], 1)
        self.assertIn("sensitivity", row["axes_failed"])
        self.assertGreater(row["ecs_K"], 5.0)

    def test_cnrm_fails_all_three_axes(self):
        row = next(r for r in crosscheck() if r["model"] == "CNRM-ESM2-1")
        self.assertGreaterEqual(row["ledgers_failed"], 2)
        self.assertEqual(row["sensitivity"], "hot")
        self.assertEqual(row["forcing"], "low")
        self.assertEqual(row["n_axes_failed"], 3)

    def test_ec_earth_veg_is_clean_but_high_sensitivity(self):
        row = next(r for r in crosscheck() if r["model"] == "EC-Earth3-Veg")
        self.assertEqual(row["ledgers_failed"], 0)
        self.assertEqual(row["sensitivity"], "high")
        self.assertEqual(row["n_axes_failed"], 1)

    def test_mpi_lr_forces_too_strongly(self):
        row = next(r for r in crosscheck() if r["model"] == "MPI-ESM1-2-LR")
        self.assertEqual(row["forcing"], "high")
        self.assertEqual(row["n_axes_failed"], 2)
        self.assertIn("forcing", row["axes_failed"])

    def test_access_esm15_forces_too_weakly(self):
        row = next(r for r in crosscheck() if r["model"] == "ACCESS-ESM1-5")
        self.assertEqual(row["forcing"], "low")
        self.assertEqual(row["n_axes_failed"], 2)

    def test_forcing_tier_boundaries(self):
        d = {"forcing_range_Wm2": [3.3, 4.1]}
        self.assertEqual(forcing_tier(3.3, d), "reasonable")
        self.assertEqual(forcing_tier(4.1, d), "reasonable")
        self.assertEqual(forcing_tier(3.29, d), "low")
        self.assertEqual(forcing_tier(4.11, d), "high")


if __name__ == "__main__":
    unittest.main()
