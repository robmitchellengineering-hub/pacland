"""Lattice recovery: the algebra recovers a room the fit could not."""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("lr", ROOT / "scripts" / "lattice_recovery.py")


def _module():
    mod = importlib.util.module_from_spec(SPEC)
    SPEC.loader.exec_module(mod)
    return mod


class TestLatticeRecovery(unittest.TestCase):

    def test_the_lattice_contains_the_modes_it_should(self):
        m = _module()
        A = (m.C_AIR / (2 * 6.05)) ** 2
        C = (m.C_AIR / (2 * 2.58)) ** 2
        lat = m.lattice((A, A, C))
        # the (1,0,0) mode squared is A; the (0,0,1) mode squared is C
        self.assertTrue(any(abs(v - A) < 1e-6 for v in lat))
        self.assertTrue(any(abs(v - C) < 1e-6 for v in lat))

    def test_clean_recovery_is_exact(self):
        m = _module()
        exact = m.modes(m.TRUTH)
        coeffs, _ = m.recover(exact)
        dims = m.to_dims(coeffs)
        err = max(abs(g - t) / t for g, t in zip(dims, sorted(m.TRUTH)))
        self.assertLess(err, 0.02)

    def test_a_measured_ceiling_recovers_the_room_under_damage(self):
        """The goal: under 2% with half the modes missing and 1 Hz of jitter, using the measured ceiling as a prior."""
        import numpy as np
        m = _module()
        exact = m.modes(m.TRUTH)
        rng = np.random.default_rng(5)
        keep = rng.random(len(exact)) >= 0.5
        noisy = np.sort(exact[keep] + rng.normal(0, 1.0, keep.sum()))
        noisy = noisy[noisy > 0]
        tol = max(0.75, 0.015 * float(np.median(noisy)))
        coeffs, score = m.recover_with_height(noisy, m.CEILING_M, tol)
        dims = m.to_dims(coeffs)
        err = max(abs(g - t) / t for g, t in zip(dims, sorted(m.TRUTH)))
        self.assertLess(err, 0.02, f"error {err:.3%} on {dims}")

    def test_the_prior_is_taken_seriously_and_not_whisked_away(self):
        # a ceiling of 4 m is a wrong prior, and the recovery must move with it rather than ignore it
        import numpy as np
        m = _module()
        exact = m.modes(m.TRUTH)
        coeffs, _ = m.recover_with_height(exact, 4.0, 1.5)
        dims = m.to_dims(coeffs)
        heights = [d for d in dims if abs(d - m.CEILING_M) < 0.05]
        self.assertEqual(heights, [], "a 4 m prior must not return a 2.58 m room")

    def test_dims_from_coefficients_round_trip(self):
        m = _module()
        dims = (6.05, 6.05, 2.58)
        coeffs = tuple((m.C_AIR / (2 * d)) ** 2 for d in dims)
        back = m.to_dims(coeffs)
        for got, want in zip(back, sorted(dims)):
            self.assertAlmostEqual(got, want, places=6)

    def test_the_lattice_is_sorted_and_positive(self):
        m = _module()
        lat = m.lattice((100.0, 200.0, 400.0))
        self.assertEqual(list(lat), sorted(lat))
        self.assertGreater(len(lat), 0)
        self.assertTrue((lat > 0).all())


if __name__ == "__main__":
    unittest.main()
