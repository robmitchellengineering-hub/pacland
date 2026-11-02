"""Three rooms, one ceiling height: the spread is the instrument, not the building."""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("he", ROOT / "scripts" / "height_error.py")


def _module():
    mod = importlib.util.module_from_spec(SPEC)
    SPEC.loader.exec_module(mod)
    return mod


class TestHeightError(unittest.TestCase):

    def test_the_three_measured_ceilings(self):
        s = _module().summarise([2.65, 2.47, 2.62])
        self.assertAlmostEqual(s["mean_m"], 2.58, places=2)
        self.assertAlmostEqual(s["spread_m"], 0.18, places=2)
        self.assertAlmostEqual(s["half_spread_m"], 0.09, places=2)
        self.assertTrue(s["usable"])

    def test_identical_measurements_have_no_error(self):
        s = _module().summarise([2.5, 2.5, 2.5])
        self.assertEqual(s["spread_m"], 0.0)
        self.assertTrue(s["usable"])

    def test_a_wild_spread_is_not_usable(self):
        # 1.8 m and 3.4 m cannot both be the same ceiling
        s = _module().summarise([1.8, 3.4])
        self.assertFalse(s["usable"])

    def test_one_value_cannot_give_an_error(self):
        s = _module().summarise([2.5])
        self.assertEqual(s["stdev_m"], 0.0)
        self.assertEqual(s["spread_m"], 0.0)


if __name__ == "__main__":
    unittest.main()
