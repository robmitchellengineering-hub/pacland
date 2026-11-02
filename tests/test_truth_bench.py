"""The truth bench: a statistic checked against a spectrum whose answer is arithmetic."""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("tb", ROOT / "scripts" / "truth_bench.py")


def _module():
    mod = importlib.util.module_from_spec(SPEC)
    SPEC.loader.exec_module(mod)
    return mod


class TestTruthBench(unittest.TestCase):

    def test_the_box_spectrum_is_exact_and_countable(self):
        modes = _module().box_modes((4.0, 4.0, 2.5), 500.0)
        self.assertGreater(len(modes), 100)
        # every mode is a real eigenfrequency: positive and inside the band
        self.assertGreater(min(modes), 0.0)
        self.assertLessEqual(max(modes), 500.0 + 1e-9)
        self.assertEqual(modes, sorted(modes))

    def test_a_poisson_spectrum_reads_near_the_poisson_value(self):
        # exponential gaps -> Poisson; the statistic should land near 0.386, not 0.531
        import random
        rng = random.Random(11)
        levels, x = [], 0.0
        for _ in range(20000):
            x += rng.expovariate(1.0)
            levels.append(x)
        r = _module().ratio_statistic(levels)
        self.assertAlmostEqual(r, 0.386, delta=0.02)

    def test_a_rigid_spectrum_reads_high(self):
        r = _module().ratio_statistic([float(i) for i in range(1, 5001)])
        self.assertGreater(r, 0.6)

    def test_degradation_removes_the_requested_fraction(self):
        modes = _module().box_modes((4.0, 4.0, 2.5), 500.0)
        kept = _module().degrade(modes, 0.5, 0.0)
        self.assertLess(len(kept), 0.6 * len(modes))
        self.assertGreater(len(kept), 0.4 * len(modes))

    def test_the_statistic_needs_enough_levels(self):
        self.assertNotEqual(_module().ratio_statistic([1.0, 2.0]), _module().ratio_statistic([1.0, 2.0]))


if __name__ == "__main__":
    unittest.main()
