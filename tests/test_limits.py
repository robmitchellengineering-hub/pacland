import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import unittest

from pacland.limits import Boundary, LimitType, boundary_map, certify


class TestLimits(unittest.TestCase):
    def test_map_has_four_boundaries(self):
        self.assertEqual(len(boundary_map()), 4)

    def test_certify_search_is_intractable(self):
        b = certify("search the flux landscape over W0")
        self.assertIsNotNone(b)
        self.assertEqual(b.limit, LimitType.INTRACTABLE)

    def test_certify_selection_is_underdetermined(self):
        b = certify("Why this vacuum")
        self.assertIsNotNone(b)
        self.assertEqual(b.limit, LimitType.UNDERDETERMINED)

    def test_certify_unknown_returns_none(self):
        self.assertIsNone(certify("an unrelated question"))


if __name__ == "__main__":
    unittest.main()
