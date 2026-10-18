import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import unittest

from pacland.limits import Boundary, LimitType, boundary_map, certify


class TestLimits(unittest.TestCase):
    def test_map_has_eight_boundaries(self):
        self.assertEqual(len(boundary_map()), 8)

    def test_all_four_walls_are_covered(self):
        types = {b.limit for b in boundary_map()}
        self.assertEqual(
            types,
            {LimitType.INTRACTABLE, LimitType.UNMEASURABLE,
             LimitType.UNDERDETERMINED, LimitType.UNDECIDABLE},
        )

    def test_certify_search_is_intractable(self):
        b = certify("flux landscape over W0")
        self.assertIsNotNone(b)
        self.assertEqual(b.limit, LimitType.INTRACTABLE)

    def test_certify_selection_is_underdetermined(self):
        b = certify("Why this vacuum")
        self.assertIsNotNone(b)
        self.assertEqual(b.limit, LimitType.UNDERDETERMINED)

    def test_certify_vacuum_decidability_is_undecidable(self):
        b = certify("decide whether a flux configuration admits")
        self.assertIsNotNone(b)
        self.assertEqual(b.limit, LimitType.UNDECIDABLE)

    def test_certify_unknown_returns_none(self):
        self.assertIsNone(certify("an unrelated question"))


if __name__ == "__main__":
    unittest.main()
