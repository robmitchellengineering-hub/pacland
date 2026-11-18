"""The SU(3) glueball: the operator runs and the mass is a real number (may be noise at small N)."""
import unittest

import numpy as np

from pacland import glueball_su3 as g3
from pacland import lattice_ym_su3 as su3


class TestGlueballSu3(unittest.TestCase):
    def test_operator_on_cold_config(self):
        # cold links: every spatial plaquette trace is 3, and there are (d-1)(d-2)/2 = 3 planes
        # per site, N^3 spatial sites => the operator is 3 * 3 * N^3
        d, N = 4, 4
        cold = np.zeros((d,) + (N,) * d + (3, 3), dtype=complex)
        for i in range(d):
            for j in range(N ** d):
                cold[i][np.unravel_index(j, (N,) * d)] = np.eye(3)
        planes = (d - 1) * (d - 2) // 2
        self.assertAlmostEqual(g3.glueball_op_su3(cold, 0), 3.0 * planes * N ** 3)

    def test_mass_is_a_finite_float(self):
        m = g3.glueball_mass_su3(2.5, N=4, n_sweeps=6, n_meas=6, seed=0)
        self.assertTrue(np.isfinite(m))


if __name__ == "__main__":
    unittest.main()
