"""The vector field model must satisfy the two properties it was never checked against."""
import sys
import unittest

sys.path.insert(0, "scripts")
sys.path.insert(0, "src")

import polarisation_validation as V  # noqa: E402


class TestBoundaryConditions(unittest.TestCase):
    def test_no_tangential_field_survives_on_any_wall(self):
        for kind, idx in (("TE", (1, 1, 1)), ("TE", (2, 1, 3)), ("TM", (1, 1, 1)), ("TM", (2, 3, 2))):
            self.assertLess(V.tangential_residual(idx, kind), 1e-9, (kind, idx))


class TestPolarisationRotation(unittest.TestCase):
    def test_coupling_follows_a_cosine(self):
        rows, peak = V.coupling_vs_angle((1, 1, 1), "TE", (0.37 * V.A, 0.41 * V.B, 0.29 * V.D))
        import math
        e = __import__("pacland.spectral.em_modes", fromlist=["mode_field"]).mode_field(
            (1, 1, 1), "TE", 0.37 * V.A, 0.41 * V.B, 0.29 * V.D, V.A, V.B, V.D)
        phi = math.atan2(e[1], e[0])
        worst = max(abs(v - peak * abs(math.cos(th - phi))) for th, v in rows)
        self.assertLess(worst / peak, 1e-9, worst / peak)


if __name__ == "__main__":
    unittest.main()
