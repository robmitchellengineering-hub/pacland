import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.oracle.exact_t6 import (  # noqa: E402
    T6Background,
    exact_t6_oracle,
    gauge_coupling,
    kahler_metric,
    kahler_potential,
    period_vector,
    superpotential,
    symplectic_form,
    tadpole,
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


if __name__ == "__main__":
    unittest.main()
