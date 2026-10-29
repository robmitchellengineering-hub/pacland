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


class TestVacuumSolver(unittest.TestCase):
    """A root finder is proven by construct-and-recover, not by not crashing."""

    def test_it_recovers_a_constructed_vacuum(self):
        r = P.validation_by_construction()
        self.assertLess(r["construction_residual"], 1e-9)
        self.assertTrue(r["converged"])
        self.assertLess(r["recovery_error"], 1e-4)

    def test_generic_integer_fluxes_are_not_flat(self):
        # the ISD condition is not automatic: a small integer flux is generically not F-flat anywhere
        import numpy as np
        F = np.zeros(8); H = np.zeros(8); F[0] = 1.0; H[1] = 1.0
        f = P.f_terms(F, H, [1j, 1j, 1j, 1j])
        self.assertGreater(float(np.linalg.norm(f)), 1e-6)


class TestStationarySolver(unittest.TestCase):
    """DV = 0, validated by inheritance: a point with DW = 0 is automatically stationary for V.

    The first version of this test failed, and both reasons were the test's, not the solver's:
      - it started at random and demanded *the* constructed point, when the potential has several
        stationary points — so it was measuring a basin of attraction;
      - the finite-difference step of 1e-6 was too noisy for Newton; 1e-4 converges cleanly.
    """

    def test_it_recovers_the_known_stationary_point_from_nearby(self):
        r = P.validation_stationary(offset=0.05)
        self.assertTrue(r["pass"], r)
        self.assertLess(r["residual"], 1e-6)

    def test_it_recovers_it_from_further_away_too(self):
        r = P.validation_stationary(offset=0.3)
        self.assertTrue(r["pass"], r)

    def test_the_constructed_point_really_is_stationary(self):
        import numpy as np
        tau_star = [complex(0.3, 1.1), complex(-0.2, 0.9), complex(0.1, 1.4), complex(0.4, 0.8)]
        sol = P.flux_flat_at(tau_star)
        F, H = sol[:8], sol[8:]
        z = np.concatenate([[t.real, t.imag] for t in tau_star])
        self.assertLess(float(np.linalg.norm(P.gradient(F, H, z, step=1e-4))), 1e-7)

    def test_and_it_is_a_minimum_despite_negative_v(self):
        # DW = 0 gives V = -3 e^K |W|^2 < 0: an AdS vacuum, which is stable. The masses are positive.
        import numpy as np
        tau_star = [complex(0.3, 1.1), complex(-0.2, 0.9), complex(0.1, 1.4), complex(0.4, 0.8)]
        sol = P.flux_flat_at(tau_star)
        F, H = sol[:8], sol[8:]
        h = P.real_hessian(F, H, *tau_star)
        self.assertTrue(all(x > 0 for x in np.linalg.eigvalsh(h)))
