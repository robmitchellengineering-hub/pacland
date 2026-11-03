"""The independent tadpole count must agree with the closed form everywhere it is cheap to check.

This is the PASS-2 guard for the exactness claims: `tadpole_distribution.verify()` compares the closed form
with a numpy enumeration that shares its block algebra, so agreement there is necessary but not sufficient.
The script under test reaches the same distribution through nested loops over the definition, sharing no
code path with either. If the two ever disagree, the closed form is wrong and every claim built on it
narrows.
"""
import importlib.util
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from pacland.exactness import tadpole_distribution as T  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "tadpole_independent_count", ROOT / "scripts" / "tadpole_independent_count.py")
_ind = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_ind)


class TestIndependentAgreement(unittest.TestCase):
    def test_the_window_holds_every_primitive_pair(self):
        # 3^(2*b3) pairs, minus the all-zero one
        for b3 in (2, 4):
            counts, orbits = _ind.distribution(b3)
            self.assertEqual(orbits, 3 ** (2 * b3) - 1, f"b3={b3}")
            self.assertEqual(orbits, sum(counts.values()), f"b3={b3}")

    def test_the_independent_count_matches_the_closed_form(self):
        for b3 in (2, 4, 6):
            counts, _ = _ind.distribution(b3)
            closed = dict(T.counts(b3))
            self.assertEqual(closed, counts,
                             f"b3={b3}: independent and closed form disagree")

    def test_the_range_is_the_tadpole_bound(self):
        # max |N| = b3 — the theorem this distribution is built on
        for b3 in (2, 4):
            counts, _ = _ind.distribution(b3)
            self.assertEqual(max(counts), b3, f"b3={b3} maximum")
            self.assertEqual(min(counts), -b3, f"b3={b3} minimum")


if __name__ == "__main__":
    unittest.main()
