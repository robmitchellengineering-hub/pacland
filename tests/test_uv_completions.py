"""Tests for the UV-completion catalog (Machine 3)."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.uv_completions import CATALOG, deficit


class TestUVCompletions(unittest.TestCase):
    def test_catalog_nonempty(self):
        self.assertGreaterEqual(len(CATALOG), 10)

    def test_collapse_counts(self):
        expected = {
            "Standard Model": 0,
            "Minimal SU(5)": 5,
            "Minimal SO(10)": 12,
            "Minimal E6": 12,
            "Minimal Pati-Salam": 12,
            "Minimal trinification SU(3)^3": 12,
            "Flipped SU(5)": 2,
            "Realistic multi-Higgs SO(10)/E6/PS": 2,
            "MSSM": 1,
            "SUSY SU(5)": 6,
            "SUSY minimal SO(10)": 13,
            "Warped RS / composite / Froggatt-Nielsen / texture zeros": 0,
        }
        for c in CATALOG:
            with self.subTest(completion=c.name):
                self.assertEqual(c.collapse_count(), expected[c.name])

    def test_numerically_correct_maximum_is_two(self):
        self.assertEqual(max(c.numerically_correct() for c in CATALOG), 2)

    def test_deficit_names_gauge_unification(self):
        self.assertIn("gauge-coupling unification", deficit())


if __name__ == "__main__":
    unittest.main()
