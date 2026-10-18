"""Mutation tests — prove the deficit guards fail on seeded faults (required-to-fail).

Valiant Verification rule: *a check that has never failed proves nothing.* Each
test here re-introduces a historical bug and asserts the correct computation
DIVERGES from the buggy one, so the guard that pins the correct value goes red on
the bug. A mutation the guards do NOT catch is a surviving mutant = a hole in the
suite.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import unittest
from math import log10

from pacland.certificate import hoeffding_radius
from pacland.deficit import deficit_report
from pacland.observables import STANDARD_OBSERVABLES


class TestMutationsAreKilled(unittest.TestCase):
    def test_mutation_measured_as_validation_is_killed(self):
        # BUG (v1): count every measured observable as a validation point, dropping
        # the `validated` requirement. Correct m is 0; the bug returns 7.
        buggy_m = sum(o.measured and o.computable for o in STANDARD_OBSERVABLES)
        correct_m = deficit_report(STANDARD_OBSERVABLES).n_validation
        self.assertEqual(correct_m, 0)
        self.assertNotEqual(buggy_m, correct_m)  # guard asserting 0 would go red

    def test_mutation_43pct_for_m19_is_killed(self):
        # BUG (v1): quote 43% for m=19 (it is the m=10 value).
        buggy = 0.4295
        correct = hoeffding_radius(19, 0.025)
        self.assertAlmostEqual(correct, 0.3116, places=4)
        self.assertNotAlmostEqual(buggy, correct, places=3)

    def test_mutation_four_orders_is_killed(self):
        # BUG (v1): "four orders of magnitude" for 18k vs 19 (it is ~3 orders, ~10^3).
        buggy = 4
        correct = round(log10(18444 / 19))  # 18444/19 ≈ 971 -> ~3
        self.assertEqual(correct, 3)
        self.assertNotEqual(buggy, correct)


if __name__ == "__main__":
    unittest.main()
