"""The RG curvature bound: finite critical exponents + a bounded flow trajectory (A1 + A3)."""
import unittest

from pacland import rg_curvature as rc


class TestRgCurvature(unittest.TestCase):
    def test_critical_exponents_are_finite(self):
        ce = rc.critical_exponents(4.0)
        self.assertTrue(ce["finite"])
        self.assertAlmostEqual(ce["lam_star"], 0.25, places=3)  # the Einstein-Hilbert fixed point

    def test_stability_matrix_is_the_jacobian(self):
        lam, g = 0.25, 0.02
        jac = rc.stability_matrix(lam, g)
        self.assertEqual(len(jac), 2)
        self.assertEqual(len(jac[0]), 2)

    def test_flow_trajectory_stays_finite(self):
        path = rc.flow_trajectory(4.0, t_end=5.0, n_steps=500)
        self.assertTrue(all(abs(l) < float("inf") for l, g in path))

    def test_curvature_is_uniform(self):
        self.assertTrue(rc.check_curvature_uniform(4.0)["uniform"])


if __name__ == "__main__":
    unittest.main()
