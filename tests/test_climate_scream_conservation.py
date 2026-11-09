"""SCREAM conservation — the p̂_e (oracle-vs-truth) term behind STRATA.

Known answers, all recomputed from the repo's own CMIP6 drift data
(data/climate/cmip6_drift.json) and SCREAM's source (check_energy.F90):

- E3SM-1-0 (SCREAM's parent lineage): net-TOA drift ~-0.0226 W/m2 (clean),
  ocean-mass drift ~-0.4861 mm/yr (LEAKS mass).
- E3SM-1-1: net-TOA ~-0.0677 W/m2, mass ~+0.0802 mm/yr — passes all three
  ledgers (energy + mass + salt).
- SCREAM's physics enforces energy: check_energy.F90 checks column energy to
  1e-14 relative error and water to 1e-10, and applies a global energy FIXER.
"""
import unittest

from pacland.climate.scream_conservation import (
    ENERGY_REL_TOL,
    ENERGY_TOL_WM2,
    MASS_TOL_MM_PER_YR,
    WATER_REL_TOL,
    parent_drift,
    verdict,
)


class TestParentLineage(unittest.TestCase):
    def test_both_e3sm_parents_are_clean_on_energy(self):
        pd = parent_drift()
        for m in ("E3SM-1-0", "E3SM-1-1"):
            self.assertLess(abs(pd[m]["netTOA_wm2"]), ENERGY_TOL_WM2, m)

    def test_e3sm_1_0_energy_value(self):
        self.assertAlmostEqual(parent_drift()["E3SM-1-0"]["netTOA_wm2"], -0.0226, places=4)

    def test_e3sm_1_1_energy_value(self):
        self.assertAlmostEqual(parent_drift()["E3SM-1-1"]["netTOA_wm2"], -0.0677, places=4)

    def test_e3sm_1_0_leaks_mass(self):
        m = parent_drift()["E3SM-1-0"]["mass_mm_per_yr"]
        self.assertAlmostEqual(m, -0.4861, places=4)
        self.assertGreater(abs(m), MASS_TOL_MM_PER_YR)

    def test_e3sm_1_1_does_not_leak_mass(self):
        m = parent_drift()["E3SM-1-1"]["mass_mm_per_yr"]
        self.assertLess(abs(m), MASS_TOL_MM_PER_YR)


class TestTheFixer(unittest.TestCase):
    def test_energy_and_water_check_tolerances(self):
        self.assertEqual(ENERGY_REL_TOL, 1e-14)
        self.assertEqual(WATER_REL_TOL, 1e-10)

    def test_verdict_says_energy_is_enforced(self):
        v = verdict()
        self.assertTrue(v["energy_enforced_by_fixer"])

    def test_km_scale_drift_is_not_measurable_from_published_data(self):
        # the STRATA-published data (17-day forced, no radiation, ~33 TB tape)
        # cannot re-measure the km-scale equilibrium drift
        self.assertFalse(verdict()["km_scale_drift_measurable_from_published"])


class TestTheVerdict(unittest.TestCase):
    def test_energy_is_clean(self):
        self.assertTrue(verdict()["parent_energy_clean"])

    def test_mass_leak_names_e3sm_1_0_only(self):
        v = verdict()
        self.assertIn("E3SM-1-0", v["parent_mass_leak_mm_per_yr"])
        self.assertNotIn("E3SM-1-1", v["parent_mass_leak_mm_per_yr"])

    def test_verdict_text_is_honest_about_the_unknown(self):
        v = verdict()["verdict"]
        self.assertIn("does not leak energy", v)
        # the km-scale drift and fixer magnitude are UNKNOWN, not claimed clean
        self.assertIn("UNKNOWN", v)


if __name__ == "__main__":
    unittest.main()
