"""The graded challenge sequence must not pass vacuously — no catalog match is NOT_APPLICABLE, and
formal-verification requires a real theorem declaration."""
import unittest
from unittest import mock

from pacland import challenges as ch


class TestKnownResults(unittest.TestCase):
    def test_no_catalog_match_is_not_applicable_not_pass(self):
        # a bare hypothesis that names no catalog claim must be NOT_APPLICABLE, not PASS
        class _Sextant:
            CATALOG = {}

        with mock.patch.object(ch, "_import_sextant", return_value=(_Sextant(), None)):
            results = ch.run_sequence(ch.Candidate("bare", "some new hypothesis"))
        kr = next(r for r in results if r.name == "known-results")
        self.assertEqual(kr.verdict, "NOT_APPLICABLE")

    def test_named_forced_claim_is_failed(self):
        class _Sextant:
            CATALOG = {"chsh": {"verdict": "FORCED", "claim": "the quantum bound is 2√2"}}

        with mock.patch.object(ch, "_import_sextant", return_value=(_Sextant(), None)):
            results = ch.run_sequence(ch.Candidate("chsh", "chsh is wrong"))
        kr = next(r for r in results if r.name == "known-results")
        self.assertEqual(kr.verdict, "FAIL")


class TestLeanCheck(unittest.TestCase):
    def test_no_target_is_not_applicable(self):
        v, _ = ch._lean_check("")
        self.assertEqual(v, "NOT_APPLICABLE")

    def test_undeclared_theorem_is_inconclusive_not_pass(self):
        v, ev = ch._lean_check("DefinitelyNotARealTheoremName")
        self.assertEqual(v, "INCONCLUSIVE")
        self.assertIn("not declared", ev)


if __name__ == "__main__":
    unittest.main()
