"""Guard tests — positive cases plus seeded-fault mutations (required-to-fail).

Each guard must BOTH pass on correct input AND go red on the fault it exists to
catch. A guard with no failing case proves nothing (Valiant Verification rule).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import unittest

from pacland import guards


class TestHodgeNumbers(unittest.TestCase):
    def test_passes_on_quintic(self):
        self.assertTrue(guards.guard_hodge_numbers(1, 101)[0])

    def test_fails_on_wrong_hodge(self):
        # seeded fault: a solver returning plausible-but-wrong numbers
        self.assertFalse(guards.guard_hodge_numbers(1, 100)[0])


class TestMirrorSymmetry(unittest.TestCase):
    def test_passes_on_quintic_mirror_pair(self):
        # quintic (1,101,chi=-200) <-> mirror (101,1,chi=+200)
        self.assertTrue(guards.guard_mirror_symmetry(1, 101, -200, 101, 1, 200)[0])

    def test_fails_if_mirror_does_not_swap(self):
        # seeded fault: a mirror computation returning the SAME Hodge numbers
        self.assertFalse(guards.guard_mirror_symmetry(1, 101, -200, 1, 101, -200)[0])

    def test_fails_if_chi_does_not_flip(self):
        # seeded fault: correct swap but wrong Euler sign
        self.assertFalse(guards.guard_mirror_symmetry(1, 101, -200, 101, 1, -200)[0])


class TestTadpole(unittest.TestCase):
    def test_passes_within_bound(self):
        self.assertTrue(guards.guard_tadpole((1, 2, 2), 10)[0])

    def test_fails_over_bound(self):
        self.assertFalse(guards.guard_tadpole((1, 2, 3), 10)[0])


class TestIntegerFlux(unittest.TestCase):
    def test_passes_on_integers(self):
        self.assertTrue(guards.guard_integer_flux((1, -2, 3))[0])

    def test_fails_on_float_contamination(self):
        self.assertFalse(guards.guard_integer_flux((1, 2.5, 3))[0])


class TestSl2zRedundancy(unittest.TestCase):
    def test_passes_on_distinct(self):
        self.assertTrue(guards.guard_no_sl2z_redundancy([(1, 2), (2, 1)])[0])

    def test_fails_on_sign_flip_duplicate(self):
        self.assertFalse(guards.guard_no_sl2z_redundancy([(1, 2), (-1, -2)])[0])

    def test_fails_on_exact_duplicate(self):
        self.assertFalse(guards.guard_no_sl2z_redundancy([(1, 2), (1, 2)])[0])


class TestRicciFlat(unittest.TestCase):
    def test_passes_on_small_residual(self):
        self.assertTrue(guards.guard_ricci_flat(1e-4, tol=1e-2)[0])

    def test_fails_on_fubini_study_residual(self):
        # seeded fault: the Fubini-Study metric (~0.4) is not Ricci-flat
        self.assertFalse(guards.guard_ricci_flat(0.4, tol=1e-2)[0])


if __name__ == "__main__":
    unittest.main()
