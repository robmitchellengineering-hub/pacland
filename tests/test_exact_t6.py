import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.oracle.exact_t6 import (  # noqa: E402
    T6Background,
    exact_t6_oracle,
    gauge_coupling,
    geodesic_distance,
    kahler_metric,
    kahler_potential,
    kk_mass,
    period_vector,
    superpotential,
    symplectic_form,
    tadpole,
    tower_mass,
    winding_mass,
    zero_error_model,
)


class TestIntersectionForm(unittest.TestCase):
    def test_unimodular(self):
        self.assertAlmostEqual(np.linalg.det(symplectic_form()), 1.0, places=12)

    def test_antisymmetric(self):
        S = symplectic_form()
        np.testing.assert_allclose(S, -S.T, atol=1e-12)


class TestKahlerPotential(unittest.TestCase):
    def test_identity(self):
        t1, t2, t3 = 1.3 + 2.1j, 0.9 + 1.7j, 1.1 + 3.3j
        pi = period_vector(t1, t2, t3)
        lhs = 1j * (pi.conj() @ symplectic_form() @ pi)
        self.assertAlmostEqual(float(np.real(lhs)), 8 * t1.imag * t2.imag * t3.imag, places=12)

    def test_closed_form(self):
        t1, t2, t3 = 1.3 + 2.1j, 0.9 + 1.7j, 1.1 + 3.3j
        self.assertAlmostEqual(
            kahler_potential(t1, t2, t3),
            -np.log(8 * t1.imag * t2.imag * t3.imag),
            places=12,
        )


class TestMetric(unittest.TestCase):
    def test_diagonal(self):
        t1, t2, t3 = 1.3 + 2.1j, 0.9 + 1.7j, 1.1 + 3.3j
        g = kahler_metric(t1, t2, t3)
        expect = np.diag([1 / (4 * x.imag ** 2) for x in (t1, t2, t3)])
        np.testing.assert_allclose(g, expect, atol=1e-12)


class TestTadpole(unittest.TestCase):
    def test_antisymmetric_and_integer(self):
        rng = np.random.default_rng(0)
        F = tuple(int(x) for x in rng.integers(-3, 4, 8))
        H = tuple(int(x) for x in rng.integers(-3, 4, 8))
        self.assertEqual(tadpole(F, F), 0)
        self.assertEqual(tadpole(F, H), -tadpole(H, F))
        self.assertIsInstance(tadpole(F, H), int)


class TestSuperpotential(unittest.TestCase):
    def test_dot_product(self):
        rng = np.random.default_rng(1)
        F = tuple(int(x) for x in rng.integers(-3, 4, 8))
        H = tuple(int(x) for x in rng.integers(-3, 4, 8))
        tau0 = 0.4 + 2.0j
        t1, t2, t3 = 1.3 + 2.1j, 0.9 + 1.7j, 1.1 + 3.3j
        direct = (np.asarray(F, float) - tau0 * np.asarray(H, float)) @ period_vector(t1, t2, t3)
        self.assertAlmostEqual(superpotential(F, H, tau0, t1, t2, t3), direct, places=12)


class TestOracle(unittest.TestCase):
    def test_exact_observables(self):
        bg = T6Background((1, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 1))
        obs = exact_t6_oracle(bg)
        self.assertEqual(set(obs), {"log_W0", "log_gs", "tadpole", "kahler_potential"})
        self.assertAlmostEqual(obs["log_gs"], np.log(gauge_coupling(bg.tau0)), places=12)

    def test_zero_error_model(self):
        em = zero_error_model()
        self.assertTrue(em.validated)
        self.assertEqual((em.bias, em.scale, em.beta), (0.0, 0.0, 0.0))

    def test_flux_length_guarded(self):
        with self.assertRaises(ValueError):
            T6Background((1, 2, 3), (1, 2, 3))


class TestDistanceConjecture(unittest.TestCase):
    def test_tower_mass_exponential(self):
        v0, v = 1.0, 100.0
        self.assertAlmostEqual(kk_mass(v), v ** -0.5, places=12)
        self.assertAlmostEqual(winding_mass(v), v ** 0.5, places=12)
        self.assertAlmostEqual(
            tower_mass(v),
            tower_mass(v0) * np.exp(-geodesic_distance(v, v0)),
            places=12,
        )


class TestExactSymbolic(unittest.TestCase):
    """Exact (sympy) versions of the core identities — zero tolerance, not 1e-12."""

    @classmethod
    def _sympy(cls):
        try:
            import sympy as sp
        except ImportError:
            raise unittest.SkipTest("sympy not installed")
        return sp

    def test_symplectic_and_period_identity(self):
        sp = self._sympy()
        a1, b1, a2, b2, a3, b3 = sp.symbols("a1 b1 a2 b2 a3 b3", real=True, positive=True)
        tau1, tau2, tau3 = a1 + sp.I * b1, a2 + sp.I * b2, a3 + sp.I * b3
        sigma = sp.Matrix([[0, 1], [-1, 0]])
        Sigma = sp.kronecker_product(sp.kronecker_product(sigma, sigma), sigma)
        self.assertEqual(sp.simplify(Sigma.det() - 1), 0)
        p = lambda t: sp.Matrix([1, t])
        Pi = sp.kronecker_product(sp.kronecker_product(p(tau1), p(tau2)), p(tau3))
        Pi_dag = Pi.applyfunc(sp.conjugate).T
        lhs = sp.expand((sp.I * (Pi_dag * Sigma * Pi))[0])
        rhs = sp.expand(8 * b1 * b2 * b3)
        self.assertEqual(sp.simplify(lhs - rhs), 0)

    def test_tadpole_antisymmetry_symbolic(self):
        sp = self._sympy()
        sigma = sp.Matrix([[0, 1], [-1, 0]])
        Sigma = sp.kronecker_product(sp.kronecker_product(sigma, sigma), sigma)
        F = sp.Matrix(sp.symbols("F0:8"))
        H = sp.Matrix(sp.symbols("H0:8"))
        self.assertEqual(sp.simplify((F.T * Sigma * H)[0] + (H.T * Sigma * F)[0]), 0)


if __name__ == "__main__":
    unittest.main()
