"""Drug deficit port — the honest two-tier count (playbook item #2)."""
import unittest
from math import inf

from pacland.drugs.deficit import drug_deficit_report
from pacland.drugs.observables import PROSPECTIVE_OBSERVABLES, RETROSPECTIVE_OBSERVABLES


class TestDrugsDeficit(unittest.TestCase):
    def test_retrospective_validation_count_is_four(self):
        ret, _ = drug_deficit_report()
        self.assertEqual(ret.n_observables, len(RETROSPECTIVE_OBSERVABLES))
        self.assertEqual(ret.n_validation, 4)
        self.assertEqual(ret.n_measured, ret.n_observables)

    def test_prospective_is_vacuous(self):
        _, pro = drug_deficit_report()
        self.assertTrue(pro.vacuous)
        self.assertEqual(pro.n_validation, 0)
        self.assertEqual(pro.n_prediction_zone, len(PROSPECTIVE_OBSERVABLES))
        self.assertEqual(pro.radius, inf)

    def test_retrospective_radius_about_68_percent(self):
        ret, _ = drug_deficit_report(delta_e=0.025)
        self.assertAlmostEqual(ret.radius, 0.679, places=3)


if __name__ == "__main__":
    unittest.main()
