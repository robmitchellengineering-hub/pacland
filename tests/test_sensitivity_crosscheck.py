"""Two-axis trust cross-check: conservation × sensitivity."""
import unittest

from pacland.climate.sensitivity_crosscheck import crosscheck, summary


class TestSensitivityCrosscheck(unittest.TestCase):
    def test_two_models_survive_both_axes(self):
        s = summary()
        self.assertEqual(s["n_survives_both"], 2)
        self.assertEqual(sorted(s["survives_both_axes"]), ["GISS-E2-1-G", "GISS-E2-1-G-CC"])

    def test_e3sm_is_clean_but_hot(self):
        row = next(r for r in crosscheck() if r["model"] == "E3SM-1-1")
        self.assertEqual(row["verdict"], "clean but hot sensitivity")
        self.assertGreater(row["ecs_K"], 5.0)

    def test_cnrm_is_leaky_and_hot(self):
        row = next(r for r in crosscheck() if r["model"] == "CNRM-ESM2-1")
        self.assertEqual(row["verdict"], "leaky AND hot sensitivity")
        self.assertGreaterEqual(row["ledgers_failed"], 2)

    def test_ec_earth_veg_is_clean_but_high(self):
        row = next(r for r in crosscheck() if r["model"] == "EC-Earth3-Veg")
        self.assertEqual(row["verdict"], "clean but high sensitivity")
        self.assertEqual(row["ledgers_failed"], 0)


if __name__ == "__main__":
    unittest.main()
