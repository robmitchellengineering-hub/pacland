import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import unittest
from math import inf

from pacland.certificate import hoeffding_radius
from pacland.deficit import DeficitObservable, deficit_report
from pacland.observables import STANDARD_OBSERVABLES, TOPOLOGY_OBSERVABLES

# Canonical ten-observable set (docs/observable-measure.md §3), classified for
# the deficit report. Source of truth: pacland.observables.STANDARD_OBSERVABLES.
TODAY = STANDARD_OBSERVABLES


class TestDeficit(unittest.TestCase):
    def test_today_is_vacuous(self):
        r = deficit_report(TODAY)
        self.assertEqual(r.n_observables, 10)
        self.assertEqual(r.n_measured, 10)
        self.assertEqual(r.n_computable, 7)
        self.assertEqual(r.n_validation, 0)
        self.assertEqual(r.n_unverifiable, 3)
        self.assertTrue(r.vacuous)
        self.assertEqual(r.radius, inf)

    def test_measured_is_not_validation(self):
        # The v1 conflation: treat every measured parameter as a validation point.
        # Measured-but-not-validated observables must NOT count toward m.
        r = deficit_report(TODAY)
        self.assertLess(r.n_validation, r.n_measured)
        self.assertNotEqual(r.n_validation, r.n_measured)

    def test_one_validated_point_gives_finite_radius(self):
        obs = [DeficitObservable("alpha_s_MZ", True, True, True)]
        r = deficit_report(obs)
        self.assertEqual(r.n_validation, 1)
        self.assertFalse(r.vacuous)
        self.assertAlmostEqual(r.radius, hoeffding_radius(1, 0.025))

    def test_prediction_zone_not_counted(self):
        # computable AND NOT measured: falsifiable later, contributes nothing now.
        obs = [DeficitObservable("future_observable", False, True, True)]
        r = deficit_report(obs)
        self.assertEqual(r.n_prediction_zone, 1)
        self.assertEqual(r.n_validation, 0)

    def test_topology_sector_is_first_validated_oracle(self):
        # CYTools reproduces the quintic's h11=1, h21=101 exactly, so topology is
        # the first sector with a calibrated error model: m=2, bounded (not vacuous).
        r = deficit_report(TOPOLOGY_OBSERVABLES)
        self.assertEqual(r.n_observables, 2)
        self.assertEqual(r.n_validation, 2)
        self.assertFalse(r.vacuous)
        self.assertAlmostEqual(r.radius, hoeffding_radius(2, 0.025))

    def test_pinned_radii(self):
        # Guard the numbers: m=19 -> ~31%, m=10 -> ~43%.
        self.assertAlmostEqual(hoeffding_radius(19, 0.025), 0.3116, places=4)
        self.assertAlmostEqual(hoeffding_radius(10, 0.025), 0.4295, places=4)


if __name__ == "__main__":
    unittest.main()
