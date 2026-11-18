"""The mass-gap falsifiers converge with lattice size and are wired into the router."""
import unittest
from unittest import mock

from pacland import mass_gap_falsifiers as mg
from pacland import runner


class TestConvergence(unittest.TestCase):
    def test_close_values_converge(self):
        self.assertTrue(mg._converged(1.0, 1.1))

    def test_far_values_do_not_converge(self):
        self.assertFalse(mg._converged(1.0, 2.0))

    def test_zero_does_not_divide_by_zero(self):
        self.assertTrue(mg._converged(0.0, 0.0))


class TestFalsifierRouting(unittest.TestCase):
    def test_the_three_falsifiers_are_registered(self):
        for key in ("d5-mass-gap", "bulk-transition", "universality"):
            self.assertIn(key, runner.FALSIFIERS)

    def test_d5_reports_non_convergence_honestly(self):
        # a signal that jumps wildly across N must be flagged as a demonstration, not a measurement
        with mock.patch("pacland.lattice_ym_su2.measure_string_tension",
                        side_effect=[1.0, 1.0, 1.0, 0.1, 0.1, 0.1]):
            survived, evidence = mg.verify_d5_mass_gap(betas=(2.0, 2.4, 2.8), Ns=(4, 6))
        self.assertFalse(survived)
        self.assertIn("does NOT converge", evidence)


if __name__ == "__main__":
    unittest.main()
