"""The floor's cost: the sensitivity that says whether the assumption is worth measuring."""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("ef", ROOT / "scripts" / "edna_floor.py")


def _module():
    mod = importlib.util.module_from_spec(SPEC)
    SPEC.loader.exec_module(mod)
    return mod


class TestFloorCost(unittest.TestCase):

    def test_the_sweep_spans_a_wide_range(self):
        m = _module()
        self.assertGreaterEqual(max(m.RATES) / min(m.RATES), 1000)

    def test_more_contamination_means_a_higher_limit(self):
        # the floor is a step function, so at the cleanest end two rates can share a floor and the limit wobbles by 0.1;
        # the test allows that and still fails on a real inversion
        from pacland.edna import limit as L
        m = _module()
        lims = [L.detection_limit_reads(c, 10) for c in m.RATES]
        for a, b in zip(lims, lims[1:]):
            self.assertGreaterEqual(b, a - 0.25, f"limit fell from {a} to {b}")

    def test_more_contamination_means_fewer_resolved_species(self):
        from pacland.edna import limit as L
        m = _module()
        counts = [L.distinguishable_species(1e6, 40.0, c) for c in m.RATES]
        self.assertEqual(counts, sorted(counts, reverse=True))

    def test_the_floor_is_consequential_on_this_range(self):
        # the script's own verdict, as a test: it should not silently become harmless
        from pacland.edna import limit as L
        m = _module()
        ratio = L.detection_limit_reads(m.RATES[-1], 10) / L.detection_limit_reads(m.RATES[0], 10)
        self.assertGreater(ratio, 1.5)


if __name__ == "__main__":
    unittest.main()
