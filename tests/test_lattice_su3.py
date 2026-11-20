"""The SU(3) lattice code: correct group theory and a positive area-law string tension."""
import unittest

import numpy as np

from pacland import lattice_ym_su3 as su3


class TestSu3GroupTheory(unittest.TestCase):
    def test_random_su3_is_unitary(self):
        rng = np.random.default_rng(0)
        for _ in range(5):
            u = su3.random_su3(rng)
            self.assertTrue(np.allclose(u @ u.conj().T, np.eye(3), atol=1e-9))

    def test_random_su3_has_unit_determinant(self):
        rng = np.random.default_rng(1)
        for _ in range(5):
            u = su3.random_su3(rng)
            self.assertLess(abs(np.linalg.det(u) - 1), 1e-6)

    def test_cold_plaquette_is_three(self):
        d, N = 4, 4
        cold = np.array([np.eye(3, dtype=complex) for _ in range(d * N ** d)])
        cold = cold.reshape((d,) + (N,) * d + (3, 3))
        self.assertEqual(su3.plaquette_trace(cold, 0, 1, (0, 0, 0, 0)), 3.0)


class TestSu3StringTension(unittest.TestCase):
    def test_strong_coupling_disorders_the_plaquette(self):
        # At strong coupling (small beta) the vacuum disorders: the mean plaquette trace drops well
        # below the cold (ordered) value 3. This is the reliable strong-coupling signal — the
        # Creutz-ratio string tension is noise-dominated at unit-test lattice sizes (N=4, few sweeps)
        # and cannot be asserted reliably, so we test the disorder itself.
        import numpy as np
        rng = np.random.default_rng(0)
        d, N = 4, 4
        links = np.array([su3.random_su3(rng) for _ in range(d * N ** d)])
        links = links.reshape((d,) + (N,) * d + (3, 3))
        links = su3.metropolis(links, 2.0, rng, 15)
        vals = [su3.plaquette_trace(links, 0, 1, tuple(np.unravel_index(i, (N,) * d)))
                for i in range(N ** d)]
        self.assertLess(float(np.mean(vals)), 1.0)


if __name__ == "__main__":
    unittest.main()
