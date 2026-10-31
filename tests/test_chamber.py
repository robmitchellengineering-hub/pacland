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


class TestClosedFormLUF(unittest.TestCase):
    """LUF = (Q c^3 / (8 pi V))^(1/3) — a scaling law, not a fit."""

    def test_closed_form_matches_the_bisection(self):
        import math
        for volume in (5.0, 16.5, 60.0):
            a = volume ** (1 / 3)
            for q in (100.0, 200.0, 400.0):
                r = C.analyse(a, a, a, 3e9, q)
                cf = C.luf_closed_form(volume, q)
                self.assertLess(abs(cf - r["luf_density_hz"]) / r["luf_density_hz"], 1e-6)

    def test_quadrupling_q_scales_luf_by_the_cube_root_of_four(self):
        x = C.luf_closed_form(16.5, 400.0) / C.luf_closed_form(16.5, 100.0)
        self.assertAlmostEqual(x, 4 ** (1 / 3), places=6)

    def test_eight_times_the_volume_halves_the_luf(self):
        x = C.luf_closed_form(132.0, 200.0) / C.luf_closed_form(16.5, 200.0)
        self.assertAlmostEqual(x, 0.5, places=6)


class TestModeCount(unittest.TestCase):
    def test_weyl_agrees_with_exact_enumeration(self):
        r = C.analyse(3.0, 2.5, 2.2, 1e9, 200.0)
        self.assertLess(abs(r["weyl_error"]), 0.01, r)

    def test_the_field_is_diffuse_at_the_top_of_the_band(self):
        r = C.analyse(3.0, 2.5, 2.2, 1e9, 200.0)
        self.assertGreater(r["modes_in_one_modal_width_at_f_max"], 1)


if __name__ == "__main__":
    unittest.main()
