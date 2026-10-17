import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import math
import unittest

from pacland.certificate import finite_d_certificate, hoeffding_radius
from pacland.measure import Measure, Observable
from pacland.oracle import (
    Oracle,
    ToricBackground,
    exact_toric_oracle,
    zero_error_model,
)


class TestExactToric(unittest.TestCase):
    def test_closed_form(self):
        bg = ToricBackground("toy", (1, 0, 0))
        out = exact_toric_oracle(bg)
        self.assertAlmostEqual(out["gauge_coupling_log"], -math.log(2.0), places=12)

    def test_zero_error_model(self):
        em = zero_error_model()
        self.assertEqual(em.bias, 0.0)
        self.assertEqual(em.scale, 0.0)
        self.assertTrue(em.validated)

    def test_end_to_end_certificate_loop(self):
        # Full loop on the exact background: candidate == oracle (perfect
        # agreement), so p_g_exact == 0; the only remaining uncertainty is the
        # oracle-validation term, which is still > 0 for finite m.
        bg = ToricBackground("toy", (1, 0, 0))
        h = exact_toric_oracle(bg)
        obs = Observable("gauge_coupling_log", target_log=None, computable=True)
        measure = Measure.uniform((obs,))
        p_g_exact = measure.exact_disagreement(h, h, threshold=0.01)
        self.assertEqual(p_g_exact, 0.0)
        cert = finite_d_certificate(p_g_exact, p_hat_e=0.0, m=10, delta_e=0.05)
        self.assertAlmostEqual(cert.bound, hoeffding_radius(10, 0.05), places=12)
        self.assertGreater(cert.bound, 0.0)


class TestOracleProtocol(unittest.TestCase):
    def test_exact_oracle_satisfies_protocol(self):
        self.assertIsInstance(exact_toric_oracle, Oracle)


class TestAdapters(unittest.TestCase):
    def test_missing_package_raises_actionable_error(self):
        from pacland.oracle.adapters import require_package

        with self.assertRaises(ImportError) as ctx:
            require_package(
                "definitely_not_a_real_pkg_xyz",
                "definitely-not-a-real-pkg-xyz",
                "https://example.com",
            )
        self.assertIn("pip install", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
