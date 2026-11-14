"""SU(2) lattice gauge Monte-Carlo: quaternion sanity + the area-law signature at both couplings."""
import unittest

import numpy as np

from pacland.lattice_ym_su2 import qmul, qconj, measure_string_tension


class TestSU2LatticeYM(unittest.TestCase):
    def test_quaternion_identity(self):
        one = np.array([1.0, 0.0, 0.0, 0.0])
        v = np.array([0.3, 0.4, 0.5, -0.2])
        np.testing.assert_allclose(qmul(one, v), v, atol=1e-12)
        np.testing.assert_allclose(qmul(v, qconj(v)), np.array([np.sum(v**2), 0, 0, 0]), atol=1e-12)

    def test_string_tension_positive_at_strong_coupling(self):
        chi = measure_string_tension(1.0, d=4, N=6, n_sweeps=3, seed=0)
        self.assertGreater(chi, 0.0)

    def test_string_tension_positive_at_weak_coupling(self):
        # SU(2) confines at weak coupling too — the area law persists (the confinement conjecture)
        chi = measure_string_tension(2.5, d=4, N=6, n_sweeps=3, seed=0)
        self.assertGreater(chi, 0.0)


if __name__ == "__main__":
    unittest.main()
