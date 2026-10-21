"""Climate deficit port — the honest two-tier count (playbook item #1).

Guards the headline numbers so the report cannot drift: historical m = 4,
projection m = 0 (vacuous), historical radius ~0.679 at delta_e = 0.025.
"""
import unittest
from math import inf

from pacland.climate.deficit import climate_deficit_report
from pacland.climate.observables import HISTORICAL_OBSERVABLES, PROJECTION_OBSERVABLES


class TestClimateDeficit(unittest.TestCase):
    def test_historical_validation_count_is_four(self):
        hist, _ = climate_deficit_report()
        self.assertEqual(hist.n_observables, len(HISTORICAL_OBSERVABLES))
        self.assertEqual(hist.n_validation, 4)
        self.assertEqual(hist.n_measured, hist.n_observables)

    def test_projection_is_vacuous(self):
        _, proj = climate_deficit_report()
        self.assertTrue(proj.vacuous)
        self.assertEqual(proj.n_validation, 0)
        self.assertEqual(proj.n_prediction_zone, len(PROJECTION_OBSERVABLES))
        self.assertEqual(proj.radius, inf)

    def test_historical_radius_about_68_percent(self):
        hist, _ = climate_deficit_report(delta_e=0.025)
        self.assertAlmostEqual(hist.radius, 0.679, places=3)


if __name__ == "__main__":
    unittest.main()
