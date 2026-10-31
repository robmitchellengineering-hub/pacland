"""Chamber analysis: the fundamental, the two LUF estimates, and the Weyl check."""
import math
import unittest

from pacland.spectral import em_modes as E

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
import chamber as C  # noqa: E402


class TestLUF(unittest.TestCase):
    def test_fundamental_is_c_over_twice_the_longest_side(self):
        self.assertAlmostEqual(C.fundamental(3.0, 2.5, 2.2), E.C_LIGHT / (2 * 3.0), places=3)

    def test_the_rule_of_thumb_is_three_times_the_fundamental(self):
        r = C.analyse(3.0, 2.5, 2.2, 1e9, 200.0)
        self.assertAlmostEqual(r["luf_rule_hz"], 3.0 * r["fundamental_hz"], places=3)

    def test_luf_rises_with_q(self):
        # a higher-Q chamber needs more modes to overlap, so its usable frequency is HIGHER
        lo = C.analyse(3.0, 2.5, 2.2, 1e9, 100.0)["luf_density_hz"]
        hi = C.analyse(3.0, 2.5, 2.2, 1e9, 400.0)["luf_density_hz"]
        self.assertLess(lo, hi)

    def test_luf_is_above_the_rule_of_thumb_for_these_chambers(self):
        # the measured result this module exists to publish: the 3x rule is OPTIMISTIC
        r = C.analyse(3.0, 2.5, 2.2, 1e9, 200.0)
        self.assertGreater(r["luf_density_hz"], r["luf_rule_hz"])


class TestModeCount(unittest.TestCase):
    def test_weyl_agrees_with_exact_enumeration(self):
        r = C.analyse(3.0, 2.5, 2.2, 1e9, 200.0)
        self.assertLess(abs(r["weyl_error"]), 0.01, r)

    def test_the_field_is_diffuse_at_the_top_of_the_band(self):
        r = C.analyse(3.0, 2.5, 2.2, 1e9, 200.0)
        self.assertGreater(r["modes_in_one_modal_width_at_f_max"], 1)


if __name__ == "__main__":
    unittest.main()
