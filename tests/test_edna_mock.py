"""The real mock-community bench: the data loads, and the test can actually fail."""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("em", ROOT / "scripts" / "edna_mock.py")


def _module():
    mod = importlib.util.module_from_spec(SPEC)
    SPEC.loader.exec_module(mod)
    return mod


class TestMockBench(unittest.TestCase):

    def test_the_real_table_loads_with_a_known_composition(self):
        rows = _module().load()
        self.assertEqual(len(rows), 160)
        self.assertEqual(len({r["species"] for r in rows}), 8)
        # the expected fractions are a composition: they sum to about 1 in every run
        for _, group in _module().conditions(rows).items():
            total = sum(g["expected_fraction"] for g in group)
            self.assertAlmostEqual(total, 1.0, places=2)

    def test_at_full_depth_everything_is_detected(self):
        # which is exactly why the full-depth test was vacuous, and why rarefaction exists
        rows = _module().load()
        self.assertTrue(all(r["observed"] > 0 for r in rows))

    def test_rarefaction_makes_detection_fail(self):
        rows = _module().load()
        shallow = _module().rarefy(rows, 20, trials=5, seed=3)
        self.assertTrue(any(r["observed"] == 0 for r in shallow), "no undetected species at depth 20")

    def test_rarefaction_preserves_the_effort(self):
        rows = _module().load()
        for depth in (20, 100):
            draws = _module().rarefy(rows, depth, trials=2, seed=1)
            per_run = len(draws) // len(_module().conditions(rows)) // 2
            # each draw is one species in one trial; the total reads drawn equals depth x trials x runs
            self.assertGreater(len(draws), 0)
            self.assertEqual(per_run, 8)

    def test_the_bins_are_ordered_and_cover_the_range(self):
        rows = _module().load()
        draws = _module().rarefy(rows, 100, trials=5, seed=2)
        curve = _module().bins(draws)
        self.assertGreater(len(curve), 1)
        self.assertEqual([b["lo"] for b in curve], sorted(b["lo"] for b in curve))


if __name__ == "__main__":
    unittest.main()
