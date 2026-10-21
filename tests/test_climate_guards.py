"""Mutation tests for the climate guard-suite (playbook item #1).

Each test proves a guard passes on a conserving/valid case AND goes red on the
seeded fault it exists to catch — the Valiant "a check that never runs reads as
a check that passed" rule (KNOWN-HAZARDS H17).
"""
import unittest

from pacland.climate.guards import (
    guard_carbon_budget,
    guard_energy_budget,
    guard_nonnegative_specific_humidity,
    guard_water_budget,
)


class TestClimateGuards(unittest.TestCase):
    def test_energy_budget_passes_when_closed(self):
        ok, _ = guard_energy_budget(net_toa_flux=0.71, d_energy_dt=0.71)
        self.assertTrue(ok)

    def test_energy_budget_fires_on_drift(self):
        ok, msg = guard_energy_budget(net_toa_flux=0.71, d_energy_dt=1.5)
        self.assertFalse(ok)
        self.assertIn("residual", msg)

    def test_water_budget_passes_when_closed(self):
        ok, _ = guard_water_budget(precip=2.7, evap=2.4, runoff=0.3, d_column_water=0.0)
        self.assertTrue(ok)

    def test_water_budget_fires_on_leak(self):
        ok, _ = guard_water_budget(precip=2.7, evap=2.4, runoff=0.8, d_column_water=0.0)
        self.assertFalse(ok)

    def test_carbon_budget_passes_when_closed(self):
        ok, _ = guard_carbon_budget(emissions=11.5, d_atm=5.2, ocean_uptake=2.9, land_uptake=3.4)
        self.assertTrue(ok)

    def test_carbon_budget_fires_on_missing_sink(self):
        ok, _ = guard_carbon_budget(emissions=11.5, d_atm=5.2, ocean_uptake=2.0, land_uptake=3.4)
        self.assertFalse(ok)

    def test_humidity_passes_when_nonnegative(self):
        ok, _ = guard_nonnegative_specific_humidity([0.01, 0.02, 0.0])
        self.assertTrue(ok)

    def test_humidity_fires_on_negative(self):
        ok, msg = guard_nonnegative_specific_humidity([0.01, -0.001, 0.02])
        self.assertFalse(ok)
        self.assertIn("negative specific humidity", msg)


if __name__ == "__main__":
    unittest.main()
