import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import unittest

from pacland.viability import (
    clip_polygon,
    elimination_compression,
    polygon_area,
    viable_polytope,
)


class TestPolygonArea(unittest.TestCase):
    def test_unit_square(self):
        sq = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
        self.assertAlmostEqual(polygon_area(sq), 1.0)

    def test_degenerate(self):
        self.assertEqual(polygon_area([(0.0, 0.0), (1.0, 1.0)]), 0.0)


class TestClipPolygon(unittest.TestCase):
    def test_halfplane_halves_square(self):
        sq = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
        clipped = clip_polygon(sq, 1.0, 0.0, 0.5)  # x <= 0.5
        self.assertAlmostEqual(polygon_area(clipped), 0.5)

    def test_clip_to_empty(self):
        sq = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
        clipped = clip_polygon(sq, 1.0, 0.0, -1.0)  # x <= -1: nothing
        self.assertEqual(clipped, [])


class TestViablePolytope(unittest.TestCase):
    def test_single_constraint(self):
        box = (0.0, 1.0, 0.0, 1.0)
        hp = [(1.0, 0.0, 0.5, "left half")]
        v = viable_polytope(hp, box)
        self.assertAlmostEqual(v["area_fraction"], 0.5)
        self.assertEqual(v["active_constraints"], ["left half"])

    def test_redundant_constraint_not_active(self):
        box = (0.0, 1.0, 0.0, 1.0)
        hp = [(1.0, 0.0, 2.0, "x <= 2 (never binds)")]
        v = viable_polytope(hp, box)
        self.assertEqual(v["area_fraction"], 1.0)
        self.assertEqual(v["active_constraints"], [])


class TestEliminationCompression(unittest.TestCase):
    def test_two_90pct(self):
        c = elimination_compression([0.9, 0.9])
        self.assertAlmostEqual(c["survivor"], 0.01)
        self.assertAlmostEqual(c["equivalent_90pct_constraints"], 2.0)

    def test_none(self):
        c = elimination_compression([])
        self.assertEqual(c["survivor"], 1.0)


if __name__ == "__main__":
    unittest.main()
