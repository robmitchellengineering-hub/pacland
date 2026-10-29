"""Mitchell's uniqueness theorem at scale: confirmed against the full algebra, and scoped to one pair."""
import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("uniq", ROOT / "scripts" / "validate_uniqueness_at_scale.py")
uniq = importlib.util.module_from_spec(spec)
spec.loader.exec_module(uniq)


class TestOneFluxPair(unittest.TestCase):
    def test_exactly_one_invariant_for_every_b3(self):
        for m in (1, 2, 3):
            self.assertEqual(uniq.invariant_bilinear_forms(m, 1)["invariants"], 1, m)

    def test_the_algebra_is_the_full_symplectic_one(self):
        # dim sp(2m) = m(2m+1)
        for m in (1, 2, 3):
            self.assertEqual(uniq.invariant_bilinear_forms(m, 1)["algebra_dim"], m * (2 * m + 1))


class TestTwoFluxPairs(unittest.TestCase):
    def test_a_second_sector_brings_three_more_invariants(self):
        for m in (1, 2, 3):
            self.assertEqual(uniq.invariant_bilinear_forms(m, 2)["invariants"], 4, m)

    def test_which_is_the_scope_limit_the_doctrine_must_state(self):
        one = uniq.invariant_bilinear_forms(2, 1)["invariants"]
        two = uniq.invariant_bilinear_forms(2, 2)["invariants"]
        self.assertGreater(two, one)


if __name__ == "__main__":
    unittest.main()
