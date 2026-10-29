"""The scalar potential: two exact identities, one symmetry, and a finite Hessian."""
import unittest

import numpy as np

from pacland.oracle import potential_t6 as P


class TestValidation(unittest.TestCase):
    def test_the_no_scale_identity_holds_exactly(self):
        tau = (1j, 1j, 2j)
        g = P.kahler_metric(1j, *tau)[1:, 1:]
        kg = np.array(P.kahler_gradients(1j, *tau)[1:])
        val = float(np.real(kg.conj() @ np.linalg.inv(g) @ kg))
        self.assertAlmostEqual(val, 3.0, places=9)

    def test_a_constant_superpotential_cancels(self):
        r = P.validate()
        names = {c["check"]: c for c in r["checks"]}
        self.assertTrue(names["constant W gives V = 0 on the Kaehler sector"]["pass"])

    def test_the_shift_symmetry_holds(self):
        r = P.validate()
        names = {c["check"]: c for c in r["checks"]}
        self.assertTrue(names["V is invariant under tau0 -> tau0+1 with F -> F+H"]["pass"])

    def test_everything_passes(self):
        self.assertTrue(P.validate()["all_pass"])


class TestHessian(unittest.TestCase):
    def test_the_hessian_is_symmetric_and_finite(self):
        F = np.zeros(8); H = np.zeros(8); F[0] = 1.0; H[2] = 1.0
        h = P.real_hessian(F, H, 1j, 1j, 1j, 1j)
        self.assertTrue(np.all(np.isfinite(h)))
        self.assertTrue(np.allclose(h, h.T))

    def test_the_spectrum_has_eight_real_values(self):
        F = np.zeros(8); H = np.zeros(8); F[1] = 1.0; H[3] = -1.0
        m = P.mass_spectrum(F, H)
        self.assertEqual(len(m), 8)
        self.assertEqual(m, sorted(m))


if __name__ == "__main__":
    unittest.main()
